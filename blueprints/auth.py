
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
from models import UserModel, UserPass

auth = Blueprint("auth", __name__,template_folder='../templates')




@auth.route('/signup', methods=['GET','POST'])
def sign_up():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()

    message = None
    user ={}

    if request.method == 'GET':
        return render_template('signup.html',user=user, login=login)
    else:
        user['first_name'] = '' if not 'first_name' in request.form else request.form['first_name'] 
        user['last_name'] = '' if not 'last_name' in request.form else request.form['last_name'] 
        user['user_name'] = '' if not 'user_name' in request.form else request.form['user_name'] 
        user['user_email'] = '' if not 'user_email' in request.form else request.form['user_email'] 
        user['password'] = '' if not 'password' in request.form else request.form['password'] 
    
        is_user_name_unique = (UserModel.query.filter(UserModel.userName ==user['user_name']).count() ==0)
        is_user_email_unique = (UserModel.query.filter(UserModel.email ==user['user_email']).count() ==0)

        if user['user_name']  == '':
            message = 'Name cannot be emtpy'
        elif user['user_email'] == '':
            message = 'email cannot be emtpy'
        elif user['password'] == '':
            message = 'Password cannot be emtpy'
        elif not is_user_name_unique:
            message = 'User with the User name {} already exists'.format(user['user_name'])
        elif not is_user_email_unique:
            message = 'User with the email {} already exists'.format(user['user_email'])

        
        
        if not message:
            user_pass = UserPass(first_name = user['first_name'],
                                 last_name = user['last_name'],
                                 user_name = user['user_name'],
                                 user_email = user['user_email'],
                                 password =  user['password'])
            
            password_hash = user_pass.hash_password()

            new_user = UserModel(firstName=user['first_name'],
                                lastName=user['last_name'],
                                userName=user['user_name'],
                                email= user['user_email'],
                                password= password_hash,
                                isActive= True,
                                isAdmin = False)
            db.session.add(new_user)
            db.session.commit()
            
            flash('Welcome {} to the AppRent!'.format(user['user_name']))
            flash('You can now log in and manage your rental apartments as the owner.')
            return redirect(url_for('dash.dashboard',login=login ))
        else:
            flash('Correct error: {}.'.format(message))
            login = ''
            return render_template('signup.html',user=user,login=login)



@auth.route('/login', methods=['GET','POST'])
def log_in():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()

    if request.method == 'GET':
        return render_template('login.html', active_menu='login', login=login)
    else:
        user_name = '' if 'user_name' not in request.form else request.form['user_name']
        password = '' if 'password' not in request.form else request.form['password']

        login = UserPass(user_name = user_name,password = password)
        login_record = login.login_user()

        if login_record != None:
            session['user'] = user_name
            flash('Logon succesfull, welcome {}.'.format(user_name))
            return redirect(url_for('main.index'))
        else:
            flash('Logon failed, try again.')
            return render_template('login.html',active_menu ='login',login=login)
        

        
@auth.route('/logout')
def log_out():
    
    if 'user' in session:
        session.pop('user', None)
        flash('You are logged out.')
    return redirect(url_for('auth.log_in'))






