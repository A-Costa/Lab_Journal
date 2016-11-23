from Lab_Journal import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length

# >>> DATABASE DECLARATION <<<

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(64), nullable = False)
    data = db.Column(db.Date, nullable = False)
    testo = db.Column(db.Text)

    def __init__(self, titolo, data, testo):
        self.titolo = titolo
        self.data = data
        self.testo = testo

    def __repr__(self):
        return '<Nota id={}>'.format(self.id)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64))

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return '<Categoria id={}>'.format(self.id)

# >>> FORMS DECLARATION <<<

class Nota_Form(FlaskForm):
    titolo = StringField('titolo', validators=[DataRequired(), Length(max=64)])
    testo = TextAreaField('testo')
