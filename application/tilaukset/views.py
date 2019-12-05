from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db, login_required
from application.tilaukset.models import Tilaus
from application.tilaukset.forms import TilausForm
from application.tilaukset.forms import TilausAddForm
from application.varaosat.models import Varaosa
from application.models import Liitostaulu

# Luodaan index-sivu
@app.route("/tilaukset", methods=["GET"])
def tilaus_index():
    return render_template("tilaukset/list.html", tilaukset = Tilaus.query.all())

# Luodaan form-sivu
@app.route("/tilaukset/new/")
@login_required(role=['admin','warehouse', 'retail'])
def tilaus_form():

    # Luodaan ensin uusi tilaus placeholder-arvoilla
    tilaus = Tilaus('hcsc-tampere','draft')
    tilaus.account_id = current_user.id
    #form = TilausForm(request.form)
    db.session().add(tilaus)
    db.session().commit()

    return redirect(url_for('tilaus_edit', tilaus_id=tilaus.id))

# Luodaan create-sivu
@app.route("/tilaukset/", methods=["POST"])
@login_required(role=['admin','warehouse', 'retail'])
def tilaus_create():

    # Luodaan ensin uusi tilaus placeholder-arvoilla
    tilaus = Tilaus('hcsc-tampere','draft')
    tilaus.account_id = current_user.id
    #form = TilausForm(request.form)
    db.session().add(tilaus)
    db.session().commit()

    return redirect(url_for('tilaus_edit', tilaus_id=tilaus.id))


# Editoinnin get-käsky
@app.route("/tilaukset/edit/<tilaus_id>/", methods=["GET"])
@login_required(role=['admin','warehouse', 'retail'])
def show_tilaus(tilaus_id):
    tilaus = Tilaus.query.get(tilaus_id)
    varaosat = db.session.query(Varaosa).filter(Varaosa.id == Liitostaulu.varaosa_id).filter(tilaus.id == Liitostaulu.tilaus_id).all()

    return render_template("tilaukset/edit.html", tilaus = tilaus, form = TilausForm(obj=tilaus), varaosat = varaosat)

# Luodaan edit-sivu
@app.route("/tilaukset/edit/<tilaus_id>/", methods=["POST"])
@login_required(role=['admin','warehouse', 'retail'])
def tilaus_edit(tilaus_id):

    form = TilausForm(request.form)
    tilaus = Tilaus.query.get(tilaus_id)
    varaosat = db.session.query(Varaosa).filter(Varaosa.id == Liitostaulu.varaosa_id).filter(tilaus.id == Liitostaulu.tilaus_id).all()

    if not form.validate():
        return render_template("tilaukset/edit.html", tilaus = tilaus, form = TilausForm(obj=tilaus), varaosat = varaosat)

    save_changes(tilaus, form)
  
    return redirect(url_for("tilaus_index"))

# Luodaan tallennuskäsky
def save_changes(tilaus_id, form, new=False):

    tilaus_id.orderPlace = form.orderPlace.data
    tilaus_id.orderStatus = form.orderStatus.data

    db.session().commit()

# Luodaan delete-käsky
@app.route("/tilaus/delete/<tilaus_id>/", methods=["POST"])
@login_required(role=['admin','warehouse', 'retail'])
def tilaus_delete(tilaus_id):


    tilaus = Tilaus.query.get(tilaus_id)
    db.session.delete(tilaus)
    db.session().commit()
  
    return redirect(url_for("tilaus_index"))

# Varaosan lisäyksen get-käsky
@app.route("/tilaukset/add/<tilaus_id>/", methods=["GET"])
@login_required(role=['admin','warehouse', 'retail'])
def show_add(tilaus_id):
    tilaus = Tilaus.query.get(tilaus_id)
    return render_template("tilaukset/add.html", tilaus = tilaus, form = TilausAddForm(obj=tilaus))

# Luodaan add-käsky varaosalle
@app.route("/tilaus/add/<tilaus_id>/", methods=["POST"])
@login_required(role=['admin','warehouse', 'retail'])
def tilaus_add(tilaus_id):


    form = TilausAddForm(request.form)
    tilaus = Tilaus.query.get(tilaus_id)

    if not form.validate():
        # return render_template("varaosat/list.html", varaosat = Varaosa.query.all())
        return render_template("tilaukset/add.html", tilaus = tilaus, form = form, error = 0)

    exists = db.session.query(db.exists().where(Varaosa.partCode == form.orderPart.data)).scalar()

    if exists == True:

        varaosa = db.session.query(Varaosa).filter(Varaosa.partCode == form.orderPart.data).first()
        tilaus.varaosat.append(varaosa)
        db.session().commit()

    else:
        return render_template("tilaukset/add.html", tilaus = tilaus, form = form, error = 1)
  
    return redirect(url_for("tilaus_edit",tilaus_id=tilaus.id))

# Luodaan varaosan delete-käsky
@app.route("/tilaus/add/<tilaus_id>/delete/<varaosa_id>/", methods=["POST"])
@login_required(role=['admin','warehouse', 'retail'])
def tilaus_varaosa_delete(tilaus_id,varaosa_id):

    tilaus = Tilaus.query.get(tilaus_id)
    varaosa = Varaosa.query.get(varaosa_id)
    liitos = db.session.query(Varaosa).filter(Varaosa.id == Liitostaulu.varaosa_id).filter(tilaus.id == Liitostaulu.tilaus_id).first()

    tilaus.varaosat.remove(liitos)

    #tilaus.varaosat.remove(varaosa)
    #db.session.delete(varaosa)
    db.session().commit()
  
    return redirect(url_for("tilaus_edit",tilaus_id=tilaus.id))
