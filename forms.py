from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileField, FileAllowed

class MembershipForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    father_name = StringField('Father Name', validators=[DataRequired(), Length(min=2, max=50)])
    cnic = StringField('CNIC', validators=[DataRequired(), Length(min=13, max=13)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    cnic_pic = FileField('Upload CNIC Front Picture', validators=[FileAllowed(['jpg', 'png'])])
    profile_pic = FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Submit')
