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
    project.project_name=new_name
    project.project_description=project_description
    db.session.commit()


###############   Meeting   #################

def create_meeting(title,brief_summary,detail_summary,project_id):
    meeting=Meeting(title=title,brief_summary=brief_summary,detail_summary=detail_summary,project_id=project_id)
    db.session.add(meeting)
    db.session.commit()
    return meeting

def get_meeting():
    
    pass

def update_meeting():
    pass

def delete_meeting():
    pass
