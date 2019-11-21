from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.tasks.models import Task
from application.tasks.forms import TaskForm
from application.tasks.forms import EditForm

@app.route("/tasks/new/")
@login_required
def tasks_form():
    return render_template("tasks/new.html", form = TaskForm())

@app.route("/tasks", methods=["GET"])
def tasks_index():
    return render_template("tasks/list.html", tasks = Task.query.all())
  
@app.route("/tasks/<task_id>/", methods=["POST"])
@login_required
def tasks_set_done(task_id):

    t = Task.query.get(task_id)
    t.done = True
    db.session().commit()


    print("taskin tilaa muokattu!")
  
    return redirect(url_for("tasks_index"))

@app.route("/tasks/", methods=["POST"])
@login_required
def tasks_create():
    form = TaskForm(request.form)

    if not form.validate():
        return render_template("tasks/new.html", form = form)

    t = Task(form.name.data)
    t.done = form.done.data
    t.account_id = current_user.id

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("tasks_index"))

def save_changes(task_id, form, new=False):
    """
    Save the changes to the database
    """

    task_id.name = form.name.data
    task_id.done = form.done.data
    task_id.account_id = current_user.id
    '''
    if new:
        # Add the new album to the database
        db_session.add(t)
    '''
    # commit the data to the database
    db.session().commit()

#Tämä määrittelee editointikäskyn
@app.route("/tasks/edit/<task_id>/", methods=["POST"])
@login_required
def tasks_edit(task_id):

    t = Task.query.get(task_id)

    form = EditForm(request.form)
    if request.method == 'POST' and form.validate():
        # save edits
        save_changes(t, form)
        print('Varaosatilausta muokattu onnistuneesti!')
        return redirect(url_for("tasks_index"))
    return render_template('tasks/edit.html', form=form, task=t)
    
    print("muokattu tietokannan riviä")

#Tämä määrittelee poistokäskyn
@app.route("/tasks/delete/<task_id>/", methods=["POST"])
@login_required
def tasks_delete(task_id):


    t = Task.query.get(task_id)
    db.session.delete(t)
    db.session().commit()
    
    print("poistettu tietokannasta")
  
    return redirect(url_for("tasks_index"))

#Tän voi poistaa !!!
'''
@app.route('/tasks/<int:id>', methods=['GET', 'POST'])
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