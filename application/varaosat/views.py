from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.varaosat.models import Varaosa
from application.varaosat.forms import VaraosaForm

# Formin route
@app.route("/varaosat/new/")
@login_required
def varaosa_form():
    return render_template("varaosat/new.html", form = VaraosaForm())

# Indexin route
@app.route("/varaosat", methods=["GET"])
def varaosa_index():
    return render_template("varaosat/list.html", varaosat = Varaosa.query.all())


# Määrittelee create käskyn
@app.route("/varaosat/", methods=["POST"])
@login_required
def varaosa_create():
    form = VaraosaForm(request.form)

    if not form.validate():
        return render_template("varaosat/new.html", form = form)

    t = Varaosa(form.partCode.data, form.partType.data, form.partBrand.data)

    t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("varaosa_index"))

# Tallennuskäsky
def save_changes(varaosa_id, form, new=False):

    varaosa_id.partCode = form.partCode.data
    varaosa_id.partType = form.partType.data
    varaosa_id.partBrand = form.partBrand.data
    varaosa_id.account_id = current_user.id

    db.session().commit()

# Editoinnin get-käsky
@app.route("/varaosat/edit/<varaosa_id>/", methods=["GET"])
@login_required
def show_varaosa(varaosa_id):
    varaosa = Varaosa.query.get(varaosa_id)
    return render_template("varaosat/edit.html", varaosa = varaosa, form = VaraosaForm(obj=varaosa))

# Tämä määrittelee editointikäskyn
@app.route("/varaosat/edit/<varaosa_id>/", methods=["POST"])
@login_required
def varaosa_edit(varaosa_id):

    form = VaraosaForm(request.form)
    varaosa = Varaosa.query.get(varaosa_id)

    if not form.validate():
        return render_template("varaosat/edit.html", varaosa = varaosa, form = form)

    save_changes(varaosa, form)
  
    return redirect(url_for("varaosa_index"))


# Tämä määrittelee poistokäskyn
@app.route("/varaosat/delete/<varaosa_id>/", methods=["POST"])
@login_required
def varaosa_delete(varaosa_id):


    t = Varaosa.query.get(varaosa_id)
    db.session.delete(t)
    db.session().commit()
    
    print("poistettu tietokannasta")
  
    return redirect(url_for("varaosa_index"))