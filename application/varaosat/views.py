from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.varaosat.models import Varaosa
from application.varaosat.forms import VaraosaForm
from application.varaosat.forms import VaraosaEditForm

@app.route("/varaosat/new/")
@login_required
def varaosa_form():
    return render_template("varaosat/new.html", form = VaraosaForm())

@app.route("/varaosat", methods=["GET"])
def varaosa_index():
    return render_template("varaosat/list.html", varaosat = Varaosa.query.all())
  
@app.route("/varaosat/<varaosa_id>/", methods=["POST"])
@login_required
def varaosa_set_done(varaosa_id):

    t = Varaosa.query.get(varaosa_id)
    t.done = True
    db.session().commit()


    print("varaosan tilaa muokattu!")
  
    return redirect(url_for("varaosa_index"))

@app.route("/varaosat/", methods=["POST"])
@login_required
def varaosa_create():
    form = VaraosaForm(request.form)

    if not form.validate():
        return render_template("varaosat/new.html", form = form)

    t = Varaosa(form.name.data)
    t.done = form.done.data
    t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("varaosa_index"))

def save_changes(varaosa_id, form, new=False):
    """
    Save the changes to the database
    """

    varaosa_id.name = form.name.data
    varaosa_id.done = form.done.data
    varaosa_id.account_id = current_user.id
    '''
    if new:
        # Add the new album to the database
        db_session.add(t)
    '''
    # commit the data to the database
    db.session().commit()

#Tämä määrittelee editointikäskyn
@app.route("/varaosat/edit/<varaosa_id>/", methods=["POST"])
@login_required
def varaosa_edit(varaosa_id):

    t = Varaosa.query.get(varaosa_id)

    form = VaraosaEditForm(request.form)
    if request.method == 'POST' and form.validate():
        # save edits
        save_changes(t, form)
        print('Varaosatilausta muokattu onnistuneesti!')
        return redirect(url_for("varaosa_index"))
    return render_template('varaosat/edit.html', form=form, varaosa=t)
    
    print("muokattu tietokannan riviä")

#Tämä määrittelee poistokäskyn
@app.route("/varaosat/delete/<varaosa_id>/", methods=["POST"])
@login_required
def varaosa_delete(varaosa_id):


    t = Varaosa.query.get(varaosa_id)
    db.session.delete(t)
    db.session().commit()
    
    print("poistettu tietokannasta")
  
    return redirect(url_for("varaosa_index"))

#Tän voi poistaa !!!
'''
@app.route('/varaosat/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db_session.query(Album).filter(
                Album.id==id)
    album = qry.first()
 
    if album:
        form = AlbumForm(formdata=request.form, obj=album)
        if request.method == 'POST' and form.validate():
            # save edits
            save_changes(album, form)
            flash('Album updated successfully!')
            return redirect('/')
        return render_template('edit_album.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)
'''