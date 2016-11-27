from Lab_Journal import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired, Length
import re

# >>> DATABASE DECLARATION <<<

class Nota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titolo = db.Column(db.String(64), nullable = False)
    data = db.Column(db.Date, nullable = False)
    testo = db.Column(db.Text)
    categorie = db.relationship('Categoria', secondary='tags', lazy='dynamic', backref=db.backref('note', lazy='dynamic'))

    def __init__(self, titolo, data, testo):
        self.titolo = titolo
        self.data = data
        self.testo = testo

    def __repr__(self):
        return '<Nota id={}>'.format(self.id)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(64), nullable=False)

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return '<Categoria id={}>'.format(self.id)

# Relazione molti a molti, definita come tabella e non come modello

tags = db.Table('tags',
    db.Column('tag_id', db.Integer, db.ForeignKey('categoria.id')),
    db.Column('nota_id', db.Integer, db.ForeignKey('nota.id'))
)

# >>> FORMS DECLARATION <<<

#la classe seguente eredita da SelectMultipleField e ne modifica il validatore.
#SelectMultipleField infatti non accetterebbe valori diversi da quelli inizialmente presenti nel suo
#array choices, cosa che per questa applicazione risulta necessaria per permettere l'inserimento di
#nuovi tag non ancora presenti nel database
class TagsSelectMultipleField(SelectMultipleField):
    def pre_validate(self, form):
        checker = re.compile("^[0-9a-zA-Z_-]{1,64}$")
        for d in self.data:
            if (d,d) not in self.choices:
                if not checker.match(d):
                    raise ValueError(self.gettext('Invalid new tag.'))


class Nota_Form(FlaskForm):
    titolo = StringField('titolo', validators=[DataRequired(), Length(max=64)])
    testo = TextAreaField('testo')
    tags = TagsSelectMultipleField('tags')
