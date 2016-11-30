from Lab_Journal import app, db
from Lab_Journal.models import Nota, Categoria, Nota_Form, Delete_Form, Search_Form
from flask import render_template, request, redirect
import datetime
import code


@app.route('/')
def index():
    note = Nota.query.order_by(Nota.data.desc()).order_by(Nota.id.desc()).all()
    return render_template('list.html', note = note)

@app.route('/nota/<id_nota>')
def nota(id_nota):
    n = Nota.query.filter(Nota.id == id_nota).first()
    return render_template('nota.html', nota = n, tags=[t.tag for t in n.categorie.order_by(Categoria.tag)])

@app.route('/new', methods=['GET', 'POST'])
def new():
    nota_form = Nota_Form()
    #la prossima funzione setta dinamicamente le possibili scelte del campo tags (che e' un campo "SelectMultipleField")
    #in base ai valori presenti nel database
    nota_form.tags.choices = [(c.tag, c.tag) for c in Categoria.query.order_by(Categoria.tag).all()]
    if nota_form.validate_on_submit():
        #categorie_db sono le categorie gia presenti nel database, categorie_ricevute le categorie ricevute sulla form
        #categorie_nuove sono le categorie ricevute non presenti nel database (nuove appunto!)
        categorie_db = [c.tag for c in Categoria.query.all()]
        categorie_ricevute = nota_form.tags.data
        categorie_nuove = set(categorie_ricevute)-set(categorie_db)
        #inserimento delle categorie nuove nel db
        for c in categorie_nuove:
            new = Categoria(c)
            db.session.add(new)
            db.session.commit()
        #creazione della nuova nota, con relativo append delle sue categorie
        n = Nota(nota_form.titolo.data, datetime.date.today(), nota_form.testo.data)
        for c in categorie_ricevute:
            categoria = Categoria.query.filter(Categoria.tag == c).first()
            n.categorie.append(categoria)
        #aggiornamento del db
        db.session.add(n)
        db.session.commit()
        return redirect('/nota/'+ str(n.id))
    else:
        return render_template('edit_note.html', nota_form = nota_form, errors = nota_form.errors)

@app.route('/modify/<id_nota>', methods=['GET', 'POST'])
def modify(id_nota):
    n = Nota.query.filter(Nota.id == id_nota).first()
    nota_form = Nota_Form(prefix = 'nota_')
    nota_form.tags.choices = [(c.tag, c.tag) for c in Categoria.query.order_by(Categoria.tag).all()]
    delete_form = Delete_Form(prefix = 'delete_')

    print nota_form.tags.default

    if delete_form.validate_on_submit():
        db.session.delete(n)
        db.session.commit()
        return redirect('/')

    if nota_form.validate_on_submit():
        categorie_db = [c.tag for c in Categoria.query.all()]
        categorie_ricevute = nota_form.tags.data
        categorie_nuove = set(categorie_ricevute)-set(categorie_db)
        for c in categorie_nuove:
            new = Categoria(c)
            db.session.add(new)
            db.session.commit()

        n.titolo = nota_form.titolo.data
        n.testo = nota_form.testo.data
        #svuoto le categorie per aggiornarle
        print n.categorie.all()
        n.categorie = []
        for c in categorie_ricevute:
            categoria = Categoria.query.filter(Categoria.tag == c).first()
            n.categorie.append(categoria)

        db.session.commit()
        return redirect('/nota/'+str(n.id))
    else:
        #le prossime due righe prendono dal database le informazioni gia presenti riguardo la nota che si sta modificando
        nota_form.tags.data = [t.tag for t in n.categorie.all()]
        nota_form.testo.data = n.testo
        nota_form.titolo.data = n.titolo

        delete_form.id.data = id_nota
        return render_template('edit_note.html', nota_form = nota_form, errors = nota_form.errors, modify=True, delete_form = delete_form)

@app.route('/search', methods=['GET', 'POST'])
def search():
    search_form=Search_Form()
    search_form.tags.choices = [(c.tag, c.tag) for c in Categoria.query.order_by(Categoria.tag).all()]

    if search_form.validate_on_submit():
        categorie_ricevute = search_form.tags.data
        #questa query recupera le note che contengono tra le proprie categorie almeno una categoria presente tra le categorie_ricevute
        #la query puo essere interpretata cosi: "SELEZIONA le note per le quali ESISTE una join di nota e categoria DOVE la categoria e' presente categorie_ricevute"
        note = Nota.query.filter(Nota.categorie.any(Categoria.tag.in_(categorie_ricevute))).order_by(Nota.data.desc()).order_by(Nota.id.desc()).all()
        print Nota.query.filter(Nota.categorie.any(Categoria.tag.in_(categorie_ricevute)))
        print "_"
        print Nota.query.filter(Nota.categorie.any(Categoria.tag.in_(categorie_ricevute))).order_by(Nota.data.desc()).order_by(Nota.id.desc())
        return render_template('list.html', note=note)
    return render_template('search.html', search_form=search_form)
