"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db #login_manager
from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_user, logout_user, current_user, login_required
from forms import SignUpForm
from models import UserProfile
from werkzeug.utils import secure_filename
import os


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')



@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
    
@app.route('/profile')
def profile():
    
    return render_template('profile.html')

def get_uploaded_images():
    rootdir = os.getcwd()
    print rootdir
    ls = []
    for subdir, dirs, files in os.walk(rootdir + '/app/static/uploads'):
        for file in files:
            ls.append(os.path.join(subdir, file).split('/')[-1])
    return ls
   

@app.route('/profiles')
def profiles():
    """Render the website's about page."""
    return render_template('profiles.html')
    

@app.route('/signUp',methods=['POST', 'GET'])
# @app.route('/profile/<userid>', methods=['GET'])
def signUp(userid = None):
    form = SignUpForm()
    print request.method
    print form.validate_on_submit(), form.errors.items()
    if request.method == 'POST' and form.validate_on_submit():
        print "Hola"
        first_name= form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        email = form.email.data
        location = form.location.data
        bio = form.bio.data
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        user= UserProfile(first_name= first_name, 
        
        last_name= last_name,
        gender=gender,
        email= email,
        location = location,
        bio = bio,
        photo = filename)
        print user
        db.session.add(user)
        db.session.commit()
        
        flash('File Saved', 'success')
        return redirect(url_for("profiles"))
    else:
        print form.data
    return render_template('forms.html', form = form)
    # return render_template('forms.html',form = form)
    

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
