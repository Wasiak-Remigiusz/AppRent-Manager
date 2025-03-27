from flask import (
    Blueprint,
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from db import db
from models import ApartmentModel, UserModel, UserPass

main = Blueprint("main", __name__,template_folder='../templates')



@main.route("/", methods=['GET','POST'])
def index():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()

    if login.is_valid:
        user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
        get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId).all()
    else:
        get_all_user_apartments=None

    if request.method == 'GET':
        return render_template('index.html',active_menu ='home', login=login, apartments=get_all_user_apartments)
    else:
        if not 'user' in session:
            if request.form['submit_button'] == 'sign_up':
                return redirect(url_for('auth.sign_up'))
            else:
                return redirect(url_for('auth.log_in'))
        elif 'user' in session and request.form['submit_button'] == 'sign_up':
                flash('Please log out before signing in as a new user.')
                return redirect(url_for('main.index'))
        else:
            flash('You are already logged in.')
            return redirect(url_for('main.index'))
        


@main.route("/about")
def about():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()

    if login.is_valid:
        user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
        get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId).all()
    else:
        get_all_user_apartments=None


    return render_template('about.html', active_menu ='about', login=login, apartments=get_all_user_apartments)
