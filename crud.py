from model import db, User, Project, Meeting, UserMeeting


###############   User   #################

def create_user(email, username, password):
    user=User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return "success"

def get_user(email):
    return User.query.filter_by(email=email).first()

def update_user(email):
    return User.query.filter_by(email=email).first()

def delete_user(email):
    return User.query.filter_by(email=email).first()


###############   Projects   #################

def create_project(project_name,project_description):
    project=Project(project_name=project_name,project_description=project_description)
    db.session.add(project)
    db.session.commit()
    return project

def get_projects():
    projects=Project.query.all()
    return projects

def delete_a_project(project_id):
    project=Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()

def update_project(project_id,new_name,project_description):
    project=Project.query.get(project_id)
    if new_name :
        project.project_name=new_name
    if project_description:
        project.project_description=project_description
    db.session.commit()


###############   Meeting   #################

def create_meeting(title,brief_summary,detail_summary,project_id):
    meeting=Meeting(title=title,brief_summary=brief_summary,detail_summary=detail_summary,project_id=project_id)
    db.session.add(meeting)
    db.session.commit()
    return meeting

def get_meetings():
    meeting=Meeting.query.all()
    return meeting

def get_a_meeting(meeting_id):
    return Meeting.query.get(meeting_id)

def update_meeting(meeting_id,title,brief_summary,detail_summary,project_id):
    meeting=Meeting.query.get(meeting_id)
    if title :
        meeting.title=title
    if brief_summary:
        meeting.brief_summary=brief_summary
    if detail_summary:
        meeting.detail_summary=detail_summary
    if project_id:
        meeting.project_id=project_id
    # return meeting

def delete_a_meeting(meeting_id):
    meeting=Meeting.query.get(meeting_id)
    db.session.delete(meeting)
    db.session.commit()
    # return meeting

