from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, User, Meeting, Project, UserMeeting
from jinja2 import StrictUndefined
from forms import LoginForm, RegistrationForm, UploadFileForm
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
import email_validator
import os
from werkzeug.utils import secure_filename
from text_converter import video_to_text_converter
from crud import create_project, create_user, get_projects, get_user, delete_a_project,update_project,create_meeting, get_meetings, update_meeting, delete_a_meeting,get_a_meeting
from groq_api import summary_generator


app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined=StrictUndefined
app.app_context().push()


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "home"
login_manager.login_message = "Please log in to access this page."
@login_manager.user_loader
def load_user(user_id):
    return User.query.get((user_id))


app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'avi', 'mp3', 'wav'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

######################################################################################
###############   View function for User - Login, Logout, Register   #################

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def home():
    if current_user.is_active:
        print(f"log in : {current_user.email}")
        return render_template('base.html')
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = get_user(form.email.data)
            if user and user.check_password(form.password.data):
                login_user(user)
                return render_template('base.html')
            else:
                flash('Invalid email or password.', 'danger')
        return render_template('login.html', form=form)
    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    logout_user()
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if form.validate_on_submit():
        create_user(form.email.data, form.username.data, form.password.data)
        flash('Thanks for registering! Now you can log in!', 'success')
        return redirect(url_for('home'))
    else:
        flash('User already exists!', 'danger')
        return render_template('register.html', form=form)
    

@app.route("/base")
@login_required
def base():
    return render_template('base.html')

####################################################################
###############   View function to Upload a file   #################
###############   View function for Meetings   #####################

@app.route('/meetings')
@login_required
def meetings():
    return render_template("meetings.html",meetings=get_meetings())


@app.route('/upload', methods=['GET', 'POST'])
# @app.route('/upload')
@login_required
def upload_file():
    form = UploadFileForm(project_selection=9)
    form.get_project_list(Project.query.all())
    # to get project id (passed as arguments) after clicking Add meeting in projects.html
    project_id=request.args.get('project_id')
    if request.method == 'POST':
        if form.validate_on_submit():
            file = form.file.data # First grab the file
            if 'file' not in request.files:
                flash('No file part', 'danger')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename) #secure_filename("My cool movie.mov") converts it to 'My_cool_movie.mov'
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                title=filename.capitalize()
                # Convert uploaded file to text
                transcript = video_to_text_converter(filename)
                # Call Groq for summary
                summary=summary_generator(transcript)
                flash('File successfully uploaded', 'success')
                # Call function to insert in database  
                meeting=create_meeting(title=title , brief_summary=summary, detail_summary=transcript, project_id=form.project_selection.data)
                return render_template("summary.html",meeting=meeting, projects=get_projects())
            else:
                flash('File type not allowed', 'danger')
    return render_template('upload.html',form=form)
    

@app.route('/summary/<meeting_id>')
@login_required
def summary(meeting_id):
    meeting=Meeting.query.get(meeting_id)
    projects=get_projects()
    return render_template("summary.html",meeting=meeting,projects=projects)

@app.route('/update_summary/<meeting_id>', methods=['POST'])
def update_summary(meeting_id):
    meeting = Meeting.query.get_or_404(meeting_id)
    summary_id = request.form.get('summary_id')
    content = request.form.get('content')

    if summary_id == 'briefSummary':
        meeting.brief_summary = content
        db.session.commit()
        # flash('Summary updated successfully', 'success')
    elif summary_id == 'detailSummary':
        meeting.detail_summary = content
        db.session.commit()
        # flash('Transcript updated successfully', 'success')
    else:
        flash('Failed to update summary', 'error')

    print(f"summary_id---------{summary_id}")
    print(f"content---------{content}")

    return redirect(url_for('summary',meeting_id=meeting_id))


@app.route('/delete/<meeting_id>')
@login_required
def delete_meeting(meeting_id):
    delete_a_meeting(meeting_id)
    flash('Meeting Deleted', 'danger')
    return render_template("meetings.html", meetings=get_meetings())

@app.route('/add_project/<meeting_id>', methods=["POST"])
@login_required
def add_project_to_meeting(meeting_id):
    meeting=get_a_meeting(meeting_id)
    print(f"options--------{request.form.get('options')}")
    pass

@app.route('/change_project/<int:meeting_id>', methods=['POST'])
def change_project(meeting_id):
    project_id = request.form.get('project_id')
    meeting = Meeting.query.get_or_404(meeting_id)
    
    if project_id:
        meeting.project_id = project_id
        db.session.commit()
        flash('Project updated successfully!', 'success')
    else:
        flash('Failed to update project. Please try again.', 'danger')
    
    return redirect(url_for('summary', meeting_id=meeting_id))

################################################################
###############   View function for Projects   #################

@app.route('/projects',methods=["GET","POST"])
@login_required
def projects():
    if request.method=='POST':
        project_name=request.form.get("project-name")
        project_description=request.form.get("project_description")
        create_project(project_name,project_description)
        print(f"project name : -----------{project_name}")
    return render_template("projects.html", projects=get_projects())


@app.route('/edit_project/<project_id>',methods=["POST"])
@login_required
def edit_project(project_id):
    new_name=request.form.get("project-name")
    project_description=request.form.get("project_description")
    update_project(project_id,new_name,project_description)
    flash('Project Updated', 'success')
    return render_template("projects.html", projects=get_projects())


@app.route('/delete/<project_id>')
@login_required
def delete_project(project_id):
    delete_a_project(project_id)
    flash('Project Deleted', 'danger')
    return render_template("projects.html", projects=get_projects())

################################################################
######################   Other function   ######################


def get_files(target):
    files_list=[]
    for file in os.listdir(target):
        path = os.path.join(target, file)
        if os.path.isfile(path):
            files_list.append(file)
            # yield (
            #     file
            #     # os.path.getsize(path)
            # )
    return files_list
 




if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    connect_to_db(app)
    app.run(debug=True)