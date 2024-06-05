from flask import Flask, render_template, request, flash, session, redirect, url_for
from model import connect_to_db, db, User, Meeting, Project, UserMeeting
from jinja2 import StrictUndefined
from forms import LoginForm, RegistrationForm, UploadFileForm
from flask_login import login_user, login_required, logout_user, LoginManager, current_user
import email_validator
import os
from werkzeug.utils import secure_filename
from text_converter import video_to_text_converter
from crud import create_project, create_user, get_projects, get_user, delete_a_project,update_project

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


###############   View function for User - Login, Logout, Register   #################

@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def home():
    if current_user.is_active:
        print(f"log in : {current_user.email}")
        return redirect(url_for('base'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = get_user(form.email.data)
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('base'))
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


###############   View function to Upload a file   #################

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    form = UploadFileForm()
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
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File successfully uploaded', 'success')
                return redirect(url_for('summary',filename=filename))
            else:
                flash('File type not allowed', 'danger')
    return render_template('upload.html',form=form)


###############   View function for Meetings   #################

@app.route('/meetings')
@login_required
def meetings():
    files = get_files(app.config['UPLOAD_FOLDER'])
    for file in files:
        print(f"files : {file}")
    return render_template("meetings.html",files=get_files(app.config['UPLOAD_FOLDER']))


@app.route('/summary/<filename>')
@login_required
def summary(filename):
    video_to_text_converter(filename)
    return render_template("summary.html",filename=filename)


###############   View function for Projects   #################

@app.route('/projects',methods=["GET","POST"])
@login_required
def projects():
    if request.method=='POST':
        project_name=request.form.get("project-name")
        create_project(project_name)
        print(f"project name : -----------{project_name}")
    return render_template("projects.html", projects=get_projects())


@app.route('/edit/<project_id>',methods=["POST"])
@login_required
def edit_project(project_id):
    new_name=request.form.get("project-name")
    update_project(project_id,new_name)
    flash('Project Updated', 'success')
    return render_template("projects.html", projects=get_projects())


@app.route('/delete/<project_id>')
@login_required
def delete_project(project_id):
    delete_a_project(project_id)
    flash('Project Deleted', 'danger')
    return render_template("projects.html", projects=get_projects())




def get_files(target):
    for file in os.listdir(target):
        path = os.path.join(target, file)
        if os.path.isfile(path):
            yield (
                file
                # os.path.getsize(path)
            )
 

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    connect_to_db(app)
    app.run(debug=True)