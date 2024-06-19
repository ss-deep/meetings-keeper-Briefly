import os
from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from dotenv import load_dotenv
import bcrypt

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

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        # Hash the password, then decode it (is used to convert from binary to string) and store it in password_hash
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        # Check if the provided password matches the stored password_hash
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))      
      
    def get_id(self):
        return str(self.user_id)

    def __repr__(self)  :
        return f"<User username={self.username}>"


class Project(db.Model):
    __tablename__ = "projects"
    
    project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, nullable=False)
    project_description = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    user = db.relationship("User", backref="projects")

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


if __name__ == "__main__":
    from app import app
    connect_to_db(app)
    with app.app_context():
        db.drop_all()
        db.create_all()

