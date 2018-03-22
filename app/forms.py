from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FileField
from wtforms.validators import InputRequired,Email, Length, Regexp, Required
from flask_wtf.file import FileField, FileField, FileRequired, FileAllowed


class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])
    gender=SelectField('Gender',choices= [('F','Female'), ('M','Male')], default = 'F')
    # created_on= StringField('Start Date', validators=[InputRequired()])
    bio = TextAreaField('Short Bio', validators=[InputRequired()])
    
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'Images only!'])
    ])  
    
    location =StringField('Location', validators=[InputRequired()])
    
    email = StringField('Email',validators=[Email(), InputRequired()])

  
