from Lab_Journal import app, db
from Lab_Journal.models import Nota, Nota_Form
from flask import render_template, request, redirect
import datetime

@app.route('/')
def index():
    note = Nota.query.all()
    return render_template('list.html', note = note)

@app.route('/nota/<id_nota>')
def nota(id_nota):
    n = Nota.query.filter(Nota.id == id_nota).first()
    return render_template('nota.html', nota = n)

@app.route('/new', methods=['GET', 'POST'])
def new():
    nota_form = Nota_Form()
    if nota_form.validate_on_submit():
        n = Nota(nota_form.titolo.data, datetime.date.today(), nota_form.testo.data)
        db.session.add(n)
        db.session.commit()
        return redirect('/nota/'+ str(n.id))
    else:
        return render_template('new.html', nota_form = nota_form, errors = nota_form.errors)

@app.route('/modify/<id_nota>', methods=['GET', 'POST'])
def modify(id_nota):
    nota_form = Nota_Form()
    n = Nota.query.filter(Nota.id == id_nota).first()

    if nota_form.validate_on_submit():
        n.titolo = nota_form.titolo.data
        n.testo = nota_form.testo.data
        db.session.commit()
        return redirect('/nota/'+str(n.id))
    else:
        nota_form.testo.data = n.testo
        return render_template('modify.html', nota_form=nota_form, errors=nota_form.errors, titolo=n.titolo)
