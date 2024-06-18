import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from dotenv import load_dotenv

# load .env file to environment
load_dotenv()

db = SQLAlchemy()
POSTGRES_URI = os.getenv("POSTGRES_URI")

def connect_to_db(flask_app, db_uri = POSTGRES_URI, echo = True):
    #Connect the Flask app to the database    
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(flask_app)
    print("Connected to the db!")


class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password_hash = db.Column(db.String, nullable=False)

    def __init__(self,  email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        
    def get_id(self):
        #Return the unique identifier for the user.
        return str(self.user_id)

    def check_password(self, password):
        #Check if the provided password matches the stored password hash
        return check_password_hash(self.password_hash, password)

    def __repr__(self)  :
        return f"<User username={self.username}>"


class Project(db.Model):
    __tablename__ = "projects"
    
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    project_description = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", backref="projects")

    # def __init__(self, project_name, project_description=None):
    #     self.project_name = project_name
    #     self.project_description = project_description
        
    def __repr__(self):
        return f"<Project project_id={self.project_id} project_name={self.project_name}>"
    
class Meeting(db.Model):
    __tablename__ = "meetings"
    
    meeting_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    brief_summary = db.Column(db.Text)
    detail_summary = db.Column(db.Text)

    project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))
    project = db.relationship("Project", backref="meetings")

    def __repr__(self):
        return f"<Meeting meeting_id={self.meeting_id} title={self.title}>"


# class UserProject(db.Model):
#     __tablename__ = "user_projects"
    
#     user_projects_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
#     project_id = db.Column(db.Integer, db.ForeignKey("projects.project_id"))

#     user = db.relationship("User", backref="user_projects")
#     project = db.relationship("Project", backref="user_projects")

#     def __repr__(self):
#         return f"<UserProject user_id={self.user_id} project_id={self.project_id}>"

if __name__ == "__main__":
    from app import app
    connect_to_db(app)
    with app.app_context():
        db.create_all()
        # project=Project("Other")
        # db.session.add(project)
        # db.session.commit()

