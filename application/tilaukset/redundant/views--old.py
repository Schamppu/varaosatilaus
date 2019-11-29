from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tilaukset.models import Tilaus
from application.tilaukset.models import TilausVaraosa
from application.tilaukset.forms import TilausForm
from application.tilaukset.forms import TilausMainForm

# Luodaan index-sivu
@app.route("/tilaukset", methods=["GET"])
def tilaus_index():
    return render_template("tilaukset/list.html", tilaukset = Tilaus.query.all())

# Luodaan form-sivu
@app.route("/tilaukset/new/")
@login_required
def tilaus_form():
    return render_template("tilaukset/new.html", form = TilausMainForm())

# Luodaan create-sivu
@app.route("/tilaukset/", methods=["POST"])
@login_required
def tilaus_create():

    form = TilausMainForm(request.form)

    if form.validate_on_submit():
        # Create race
        tilaus = Tilaus()

        db.session.add(tilaus)

        for spare in form.osat.data:
            uusi_osa = TilausVaraosa(**spare)

            # Add to race
            tilaus.osat.append(uusi_osa)

        db.session.commit()

    return redirect(url_for("tilaus_index"))