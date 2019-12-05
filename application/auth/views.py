from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, ManageForm

# Luodaan login-sivu
@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)
    # mahdolliset validoinnit

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "Väärä tunnus tai salasana")


    print("Käyttäjä " + user.name + " tunnistettiin")
    login_user(user)
    return redirect(url_for("index"))    

# Luodaan logout-sivu
@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))    


# Luodaan index-sivu
@app.route("/manage", methods=["GET"])
@login_required(role=['admin'])
def manage_index():
    return render_template("manage/list.html", users = User.query.all())

# Formin route
@app.route("/manage/new/")
@login_required(role=['admin'])
def manage_form():
    return render_template("manage/add.html", form = ManageForm())

# Luodaan createn get-käsky
@app.route("/manage/", methods=["POST"])
@login_required(role=['admin'])
def manage_create():
    form = ManageForm(request.form)

    if not form.validate():
        return render_template("manage/add.html", form = form)

    t = User(form.name.data, form.username.data, form.password.data, form.role.data)

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("manage_index"))


# Luodaan editoinnin get-käsky
@app.route("/manage/edit/<user_id>/", methods=["GET"])
@login_required(role=['admin'])
def show_user(user_id):
    user = User.query.get(user_id)
    return render_template("manage/edit.html", user = user, form = ManageForm(obj=user))

# Luodaan editoinnin post-käsky
@app.route("/manage/edit/<user_id>/", methods=["POST"])
@login_required(role=['admin'])
def manage_edit(user_id):

    form = ManageForm(request.form)
    user = User.query.get(user_id)

    if not form.validate():
        return render_template("manage/edit.html", user = user, form = form, error = 0)

    if form.password.data == form.passwordCheck.data:
        save_changes(user, form)
    else:
        return render_template("manage/edit.html", user = user, form = form, error = 1)
  
    return redirect(url_for("manage_index"))



# Luodaan deletekäsky
@app.route("/manage/delete/<user_id>/", methods=["POST"])
@login_required(role=['admin'])
def manage_delete(user_id):


    t = User.query.get(user_id)
    db.session.delete(t)
    db.session().commit()
  
    return redirect(url_for("manage_index"))

# Luodaan tallennus
def save_changes(user_id, form, new=False):

    user_id.name = form.name.data
    user_id.username = form.username.data
    user_id.password = form.password.data
    user_id.role = form.role.data
    db.session().commit()