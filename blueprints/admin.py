import pycountry
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
from models import (
    ApartmentModel,
    BillModel,
    BillSettlementModel,
    BillTypeModel,
    CountryModel,
    CurrencyModel,
    MonthlyRentPaymentModel,
    RentalAgreementModel,
    TenantModel,
    UserModel,
    UserPass,
)

admin = Blueprint("admin", __name__,template_folder='../templates')



@admin.route('/init-app')
def init_app():

    # check if there are users defined (at least one active admin required)
    active_admins = UserModel.query.filter(UserModel.isActive==True, UserModel.isAdmin ==True).count()

    if active_admins > 0:
        flash('Aplication is already set-up.')
        return redirect(url_for('main.index'))

    # if not - create/update admin account with a new password and admin privileges, display random username    
    user_pass = UserPass()
    user_pass.get_random_user_pasword()
    
    new_admin=UserModel(firstName=user_pass.first_name,
                        lastName = user_pass.last_name, 
                        userName = user_pass.user_name, 
                        email='test.operator@gmail.com',
                        password = user_pass.hash_password(),
                        isActive = True , 
                        isAdmin = True )
    db.session.add(new_admin)
    db.session.commit()

    flash('User {} with password {} has been created.'.format(user_pass.user_name, user_pass.password))
    return(redirect(url_for('main.index')))


@admin.route('/create-country-table')
def create_country_table():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()

    if not login.is_valid or not login.is_admin:
        return redirect(url_for('auth.log_in'))
    
    countries_exists = CountryModel.query.count()
    if countries_exists:
        flash('Countries already exist in the database.')
        return redirect(url_for('main.index'))

    european_countries_alpha_2 = [
            'FR', 'DE', 'IT',  'PL', 
            'ES', 'GB'
            ]

    other_countries_alpha_2 = ['US','JP']

    selected_countries_alpha_2 = european_countries_alpha_2 + other_countries_alpha_2
    selected_countries =[pycountry.countries.get(alpha_2=alpha_2) for alpha_2 in selected_countries_alpha_2]
    selected_countries = sorted(selected_countries, key=lambda country : country.name)


    for country in selected_countries:
        new_country = CountryModel.query.filter(CountryModel.countryName == country.name).first()
        if not new_country:
            new_country = CountryModel(countryName=country.name)
            db.session.add(new_country)
        
        db.session.commit()
    
    flash("Countries have been added to the database.")
    return(redirect(url_for('main.index')))
        

@admin.route('/create-currency-table')
def create_currency_table():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()

    if not login.is_valid or not login.is_admin:
        return redirect(url_for('auth.log_in'))
    
    currencies_exists = CurrencyModel.query.count()
    if currencies_exists:
        flash('Currencies already exist in the database.')
        return redirect(url_for('main.index'))

    alpha_3_county_codes =  ['EUR', 'JPY', 'PLN', 'GBP', 'USD']
    alpha_3_county_codes = sorted(alpha_3_county_codes)

    for code in alpha_3_county_codes:
        new_code = CurrencyModel.query.filter(CurrencyModel.currencySymbol == code).first()
        if not new_code:
            new_code = CurrencyModel(currencySymbol =code)
            db.session.add(new_code)
        
        db.session.commit()

    flash("Currencies have been added to the database.")
    return(redirect(url_for('main.index')))

@admin.route('/create-bill-type-table')
def create_bill_type_table():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()

    if not login.is_valid or not login.is_admin:
        return redirect(url_for('auth.log_in'))
    
    bill_type_exists = BillTypeModel.query.count()
    if bill_type_exists:
        flash('Bill type table already exist in the database.')
        return redirect(url_for('main.index'))

    bill_type_list =  ['Administrative Rent/Fees', 'Electricity', 'Water', 'Gas', 'Internet', 
                       'Trash Collection', ' Maintenance Fees', 'Property Taxes', 'Home Insurance', 'TV/Streaming Services','Other' ]

    for bill_type in bill_type_list:
        new_bill_type = BillTypeModel.query.filter(BillTypeModel.billTypeName == bill_type).first()
        if not new_bill_type:
            new_bill_type = BillTypeModel(billTypeName = bill_type)
            db.session.add(new_bill_type)
        
        db.session.commit()

    flash("Currencies have been added to the database.")
    return(redirect(url_for('main.index')))


@admin.route('/admin-panel')
def admin_panel():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    

    # for key, value in login.__dict__.items():
    #     print(key, ': ', value)
    # print('----')
    # print(vars(login))

    if not login.is_valid or not login.is_admin:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    
    users = UserModel.query.all()
    return render_template('admin_panel.html', 
                           active_menu ='admin', 
                           users = users, 
                           login=login,
                           apartments  = get_all_user_apartments )


@admin.route('/new-user', methods=['GET','POST'] )
def new_user():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()  

    # if 'user' not in session:
    #     return redirect(url_for('auth.log_in'))
    # login = session['user']

    message = None
    user ={}

    if request.method == 'GET':
        return render_template('new_user.html', active_menu='admin', user=user,login=login, apartments=get_all_user_apartments)
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
            message = 'Email cannot be emtpy'
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
            
            flash('User {} created.'.format(user['user_name']))
            return redirect(url_for('admin.admin_panel'))
        else:
            flash('Correct error: {}.'.format(message))
            return render_template('new_user.html',user=user, active_menu ='admin',login=login, apartments=get_all_user_apartments)
        



@admin.route('/edit-user/<user_name>',methods=['GET','POST'])
def edit_user(user_name):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId).all()  
        

    # if 'user' not in session:
    #     return redirect(url_for('auth.log_in'))
    # login = session['user']


    user_model = UserModel.query.filter(UserModel.userName == user_name).first()

    user = UserPass(first_name= user_model.firstName,
                    last_name= user_model.lastName,
                    user_name=user_model.userName,
                    user_email=user_model.email)
    message_error = None


    if user_name == login.user_name:
        flash('You cannot edit yourself.')
        return redirect(url_for('admin.admin_panel'))


    if user ==None:
        flash('No such user.')
        return redirect(url_for('admin.admin_panel'))
    
    if request.method == 'GET':
        return render_template('edit_user.html', active_menu='admin', user=user,login=login, apartments=get_all_user_apartments)
    else:
        new_first_name = request.form.get('first_name', '')
        new_last_name = request.form.get('last_name', '')
        new_email = request.form.get('user_email', '')
        new_password = request.form.get('password', '')

        if new_email != user_model.email:
            is_user_email_unique = (UserModel.query.filter(UserModel.email ==new_email ).count() ==0)
        else:
            is_user_email_unique = True


        if new_first_name  == '':
            message_error = 'First name cannot be emtpy.'
            flash(message_error)
        

        if new_last_name== '':
            message_error = 'Last name cannot be emtpy.'
            flash(message_error)
    
        if new_email== '':
            message_error = 'Email cannot be emtpy'
            flash(message_error)
     

        if not is_user_email_unique:
            message_error = 'User with the email {} already exists'.format(new_email)
            flash(message_error)
          

        if not message_error:

            updated_fields = []

            if user.first_name != new_first_name:
                user_model.firstName = new_first_name
                updated_fields.append('first name')

            if user.last_name != new_last_name:
                user_model.lastName = new_last_name
                updated_fields.append('last name')

            if user.user_email != new_email:
                user_model.email = new_email
                updated_fields.append('email')

            if new_password != '':
                print()
                user.password = new_password
                user_model.password = user.hash_password()
                updated_fields.append('password')




            if len(updated_fields) ==0:
                flash('User has not been updated.')
                return redirect(url_for('admin.admin_panel', login=login))
            
            elif len(updated_fields) == 1:
                updated_fields[0] = updated_fields[0] + '.' 
                updated_fields = ', '.join(updated_fields)
            elif len(updated_fields) >= 2:
                updated_fields[-1] = "and " + updated_fields[-1] + "."
                updated_fields = ', '.join(updated_fields)


            db.session.commit()

            flash('User {} has been updated.'.format(user.user_name))
            flash('Updated fields: {}'.format(updated_fields))
            return redirect(url_for('admin.admin_panel', login=login))
        else:
            return render_template('edit_user.html', active_menu='admin', user=user,login=login, apartments=get_all_user_apartments)



@admin.route('/delete-user/<user_name>')
def delete_user(user_name):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin:
        return redirect(url_for('auth.log_in'))

    user = UserModel.query.filter(UserModel.userName== user_name, UserModel.userName !=login.user_name).first()
    if user:
        try:
            apartments = ApartmentModel.query.filter(ApartmentModel.userId == user.userId).all()

            # Loop through each apartment to delete related data
            for apartment in apartments:
                agreements = RentalAgreementModel.query.filter(RentalAgreementModel.apartmentId == apartment.apartmentId).all()

                for agreement in agreements:
                    # Order of Deletion: Step 1 => BillSettlementModel 
                    BillSettlementModel.query.filter(BillSettlementModel.agreementId == agreement.agreementId).delete()
                    db.session.commit()

                    # Order of Deletion: Step 2 => BillModel 
                    BillModel.query.filter(BillModel.agreementId == agreement.agreementId).delete()
                    db.session.commit()

                    # Order of Deletion: Step 3 => MonthlyRentPaymentModel 
                    MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.agreementId == agreement.agreementId).delete()
                    db.session.commit()

                    # Order of Deletion: Step 4 => RentalAgreementModel 
                    flash('Rental agreement  {} has been removed.'.format(agreement.agreementName))
                    db.session.delete(agreement)
                    db.session.commit()

                    # Order of Deletion: Step 5 => TenantModel 
                    tenant = TenantModel.query.filter(TenantModel.tenantId == agreement.tenantId).first()
                    if tenant:
                        other_agreements_count = RentalAgreementModel.query.filter(RentalAgreementModel.tenantId == agreement.tenantId).count()
                        
                        if other_agreements_count == 0:
                            db.session.delete(tenant)
                            db.session.commit()

                # Delete the apartment
                db.session.delete(apartment)
                db.session.commit()



        
            flash('User {} has been removed.'.format(user_name))
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('admin.admin_panel'))
        
        except Exception as e:
            # Rollback the session in case of any error
            db.session.rollback()
            flash('An error occurred while deleting the user: {}'. format(str(e)))
            return redirect(url_for('admin.admin_panel', login=login))


    flash('You cannot delete yourself.')
    return redirect(url_for('admin.admin_panel', login=login))



@admin.route('/user/<int:userId>/apartments')
def get_user_apartments(userId):
    
    user = UserModel.query.filter(UserModel.userId==userId).first()
    aprartment = user.apartment.all()

    ret = ''

    for a in aprartment:
        ret+=str(a)+'<br>'


    return  'Apartments List of {}:<br><br>{}'.format(user.lastName,ret)



@admin.route('/user-status-change/<action>/<user_name>')
def user_status_chenge(action,user_name):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid or not login.is_admin: 
        return redirect(url_for('auth.log_in'))

    # if 'user' not in session:
    #     return redirect(url_for('auth.log_in'))
    # login = session['user']

    if action == 'active':
        user = UserModel.query.filter(UserModel.userName== user_name, UserModel.userName !=login.user_name).first()
        if user:
            user.isActive = (user.isActive + 1) % 2
            db.session.commit()

    elif action == 'admin':
        user = UserModel.query.filter(UserModel.userName== user_name, UserModel.userName !=login.user_name).first()
        if user:
            user.isAdmin  = (user.isAdmin  + 1) % 2
            db.session.commit()

    return redirect(url_for('admin.admin_panel'))





# @admin.route('/users')
# def get():
   
#     users = UserModel.query.all()
    
#     ret = ''
#     for u in users:
#         ret += str(u)+'<br>'

#     return 'Hello<br>{}'.format(ret)



