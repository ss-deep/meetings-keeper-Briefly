from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,FileField, SelectField
from wtforms.validators import DataRequired,Email,EqualTo,InputRequired
from wtforms import ValidationError
from model import User


class LoginForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def validate_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    project_selection=SelectField("Select Project")
    submit = SubmitField("Upload File")

    def get_project_list(self,projects):
        self.project_selection.choices=[(project.project_id, project.project_name) for project in projects]


