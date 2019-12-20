from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo


#FlaskForm is written inside bracket here as it is parent class and we are inheriting it's feature
class InsertForm(FlaskForm):
    title  = StringField('Title',
                        validators=[DataRequired(), Length(min =5, max = 40)])
    description =  TextAreaField('Descriptions',
                        validators=[DataRequired()])

    submit = SubmitField('Add New Item')