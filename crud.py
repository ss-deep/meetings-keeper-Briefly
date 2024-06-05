from model import db, User, Project, Meeting, UserMeeting


def create_project(project_name):
    project=Project(project_name=project_name)
    db.session.add(project)
    db.session.commit()
    return project

def create_user(email, username, password):
    user=User(email=email, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return "success"

def get_projects():
    projects=Project.query.all()
    return projects

def delete_a_project(project_id):
    project=Project.query.get(project_id)
    db.session.delete(project)
    db.session.commit()

def update_project(project_id,new_name):
    project=Project.query.get(project_id)
    project.project_name=new_name
    db.session.commit()

def get_user(email):
    return User.query.filter_by(email=email).first()