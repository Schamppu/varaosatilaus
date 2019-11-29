from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
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
@login_required
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
@login_required
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
@login_required
def show_tilaus(tilaus_id):
    tilaus = Tilaus.query.get(tilaus_id)
    # varaosat = TilausVaraosa.query.filter(TilausVaraosa.parent_id==tilaus.id).all()
    varaosat = db.session.query(Varaosa).filter(Varaosa.id == Liitostaulu.varaosa_id).filter(tilaus.id == Liitostaulu.tilaus_id).all()
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('varaosan palauttama arvo: ',varaosat,'<--- onko tää oikein?')

    return render_template("tilaukset/edit.html", tilaus = tilaus, form = TilausForm(obj=tilaus), varaosat = varaosat)

# Luodaan edit-sivu
@app.route("/tilaukset/edit/<tilaus_id>/", methods=["POST"])
@login_required
def tilaus_edit(tilaus_id):

    form = TilausForm(request.form)
    tilaus = Tilaus.query.get(tilaus_id)
    # varaosat = TilausVaraosa.query.filter(TilausVaraosa.parent_id==tilaus.id).all()
    varaosat = db.session.query(Varaosa).filter(Varaosa.id == Liitostaulu.varaosa_id).filter(tilaus.id == Liitostaulu.tilaus_id).all()
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('varaosan palauttama arvo: ',varaosat,'<--- onko tää oikein?')

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
@login_required
def tilaus_delete(tilaus_id):


    tilaus = Tilaus.query.get(tilaus_id)
    db.session.delete(tilaus)
    db.session().commit()
  
    return redirect(url_for("tilaus_index"))

# Varaosan lisäyksen get-käsky
@app.route("/tilaukset/add/<tilaus_id>/", methods=["GET"])
@login_required
def show_add(tilaus_id):
    tilaus = Tilaus.query.get(tilaus_id)
    return render_template("tilaukset/add.html", tilaus = tilaus, form = TilausAddForm(obj=tilaus))

# Luodaan add-käsky varaosalle
@app.route("/tilaus/add/<tilaus_id>/", methods=["POST"])
@login_required
def tilaus_add(tilaus_id):


    form = TilausAddForm(request.form)
    tilaus = Tilaus.query.get(tilaus_id)

    if not form.validate():
        # return render_template("varaosat/list.html", varaosat = Varaosa.query.all())
        return render_template("tilaukset/add.html", tilaus = tilaus, form = form, error = 0)

    exists = db.session.query(db.exists().where(Varaosa.partCode == form.orderPart.data)).scalar()

    if exists == True:

        varaosa = db.session.query(Varaosa).filter(Varaosa.partCode == form.orderPart.data).first()

        #varaosa = Varaosa.query.get(form.orderPart.data)
        print('AAAAAA')
        print('AAAAAA')
        print('AAAAAA')
        print('AAAAAA')
        print('AAAAAA')
        print('AAAAAA')
        print('AAAAAA')
        print('AAAAAA')
        print('varaosan palauttama arvo: ',varaosa,'<--- onko tää oikein?')
        #varaosa = db.session.query((Varaosa.id).where(Varaosa.partCode == form.orderPart.data))
        tilaus.varaosat.append(varaosa)
        db.session().commit()

    else:
        return render_template("tilaukset/add.html", tilaus = tilaus, form = form, error = 1)
  
    return redirect(url_for("tilaus_edit",tilaus_id=tilaus.id))

# Luodaan varaosan delete-käsky
@app.route("/tilaus/add/<tilaus_id>/delete/<varaosa_id>/", methods=["POST"])
@login_required
def tilaus_varaosa_delete(tilaus_id,varaosa_id):

    tilaus = Tilaus.query.get(tilaus_id)
    varaosa = Varaosa.query.get(varaosa_id)
    #varaosa = TilausVaraosa.query.get(varaosa_id)
    #varaosa = db.session.query(Liitostaulu).filter(varaosa_id == Liitostaulu.varaosa_id,tilaus_id == Liitostaulu.tilaus_id)
    #varaosa = db.session.query(Varaosa).filter(varaosa_id == Liitostaulu.varaosa_id,tilaus_id == Liitostaulu.tilaus_id)       print('AAAAAA')

    liitos = db.session.query(Varaosa).filter(Varaosa.id == Liitostaulu.varaosa_id).filter(tilaus.id == Liitostaulu.tilaus_id).first()

    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('AAAAAA')
    print('varaosa: ',varaosa.id)
    print('tilaus: ',tilaus.id)
    print('arvo mitä etitään: ',liitos,'<--- onko tää oikein?')

    tilaus.varaosat.remove(liitos)

    #tilaus.varaosat.remove(varaosa)
    #db.session.delete(varaosa)
    db.session().commit()
  
    return redirect(url_for("tilaus_edit",tilaus_id=tilaus.id))
