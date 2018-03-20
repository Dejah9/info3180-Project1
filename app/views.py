"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import LoginForm
from models import UserProfile


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route('/secure-page/')
@login_required
def secure_page():
    return render_template('secure_page.html')

@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')


@app.route("/login", methods=["GET", "POST"])
def login():
    #if user is already logged in,redirect them to your secure page
    if current_user.is_authenticated:
        return redirect(url_for('secure_page'))
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        
        # change this to actually validate the entire form submission
        # and not just one field
        username= form.username.data
        password= form.password.data
        
        user= UserProfile.query.filter_by(username=username,password=password).first()
        
        if user is not None:
            # Get the username and password values from the form.

            # using your model, query database for a user based on the username
            # and password submitted
            # store the result of that query to a `user` variable so it can be
            # passed to the login_user() method.

            # get user id, load into session
            login_user(user)
            flash('Logged in successfully.','success')
            

            # remember to flash a message to the user
            return redirect(url_for("secure_page"))  # they should be redirected to a secure-page route instead
        else:
            flash('Username or Password is incorrect.','danger')
    flash_errors(form)    
    return render_template("login.html", form=form)
    

@app.route('/logout')
@login_required 
def logout():
    logout_user()
    flash('You were logged out', 'success')
    return redirect(url_for('home'))



# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))
    

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