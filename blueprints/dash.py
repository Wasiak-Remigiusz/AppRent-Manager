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
    CountryModel,
    MonthlyRentPaymentModel,
    RentalAgreementModel,
    TenantModel,
    UserModel,
    UserPass,
)

dash = Blueprint("dash", __name__,template_folder='../templates')

@dash.route('/dashboard/', methods=['GET','POST'])
def dashboard():

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))

    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()

    tab_name = 'rental-agreement-tab'


    return render_template('dashboard.html',
                          active_menu ='dashboard', 
                          login=login, 
                          apartments =get_all_user_apartments, 
                          tab_name =tab_name)



@dash.route('/new-apartment/<string:user_name>', methods=['GET','POST'])
def new_apartment(user_name):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))

    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()

    countries_list = CountryModel.query.all()

    apartment= {}

    if request.method == 'GET':
        return render_template('new_apartment.html', 
                               active_menu='dashboard', 
                               user=login,login=login, 
                               countries_list = countries_list,
                               apartment=apartment,
                               apartments =get_all_user_apartments)
    else:
        message = None

        apartment['apartment_name'] = request.form.get('apartment_name', '')
        apartment['street_name'] = request.form.get('street_name', '')
        apartment['street_number'] = request.form.get('street_number', '')
        apartment['apartment_number'] = request.form.get('apartment_number', '')
        apartment['city_name'] = request.form.get('city_name', '')
        apartment['countryId'] = int(request.form.get('countryId', 5)) # Polish id for default value

        is_apartment_name_unique = (ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment['apartment_name'], 
                                                                ApartmentModel.userId==user_model.userId).count() ==0)
        apartment_name = apartment['apartment_name']
        city_name =  apartment['city_name']

        match is_apartment_name_unique:
            case False:

                message = ('The apartment name must be unique.')
                flash(message)

        match apartment_name:
            case '':
                message = ('Apartment must have a name.')
                flash(message)
        
        match city_name:
            case '':
                message = ('The apartment must have a city specified.')
                flash(message)


        if not message:
            new_apartment = ApartmentModel(apartmentName=apartment['apartment_name'],
                                    userId=user_model.userId,
                                    city=apartment['city_name'],
                                    street= apartment['street_name'],
                                    streetNumber= apartment['street_number'] ,
                                    apartmentNumber= apartment['apartment_number'],
                                    countryId = apartment['countryId'])
            db.session.add(new_apartment)
            db.session.commit()
                
            flash('Apartment {} created.'.format(apartment['apartment_name']))
            return redirect(url_for('dash.dashboard'))
            
        else:
            return render_template('new_apartment.html', active_menu='dashboard', 
                                   user=login,login=login, 
                                   countries_list = countries_list, 
                                   apartment=apartment,
                                   apartments =get_all_user_apartments)
       


@dash.route('/edit-apartment/<string:apartment>', methods=['GET','POST'])
def edit_apartment(apartment):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    countries_list = CountryModel.query.all()
    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment, 
                                                                ApartmentModel.userId==user_model.userId).first()
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    


    if request.method == 'GET':
        return render_template('edit_apartment.html',
                               login=login, 
                               active_menu='dashboard',
                               countries_list =countries_list, 
                               apartment=current_apartment,
                               apartments = get_all_user_apartments)
    
    else:
        message = None
    
        updated_apartmentName = request.form.get('apartmentName', '')
        updated_street= request.form.get('street', '')
        updated_streetNumber = request.form.get('streetNumber', '')
        updated_apartmentNumber = request.form.get('apartmentNumber', '')
        updated_city= request.form.get('city', '')
        updated_countryId = int(request.form.get('countryId', 5)) # Polish id for default value

        is_apartment_name_unique = (ApartmentModel.query.filter(ApartmentModel.apartmentName ==updated_apartmentName, 
                                                                ApartmentModel.userId==user_model.userId).filter(ApartmentModel.apartmentId != current_apartment.apartmentId).count() ==0)

        print('is_apartment_name_unique: ',is_apartment_name_unique)
    

        match is_apartment_name_unique:
            case False:
                message = ('The apartment name must be unique.')
                flash(message)

        match updated_apartmentName:
            case '':
                message = ('Apartment must have a name.')
                flash(message)
        
        match updated_city:
            case '':
                message = ('The apartment must have a city specified.')
                flash(message)

        if not message:
            current_apartment.apartmentName=updated_apartmentName
            current_apartment.userId=user_model.userId
            current_apartment.city=updated_city
            current_apartment.street=  updated_street
            current_apartment.streetNumber= updated_streetNumber 
            current_apartment.apartmentNumber= updated_apartmentNumber
            current_apartment.countryId = updated_countryId 
            db.session.commit()
                
            flash('Apartment {} has beed updated.'.format(updated_apartmentName))
            return redirect(url_for('dash.dashboard'))
        else:

            apartment ={
                'apartmentName': updated_apartmentName,
                'street': updated_street,
                'streetNumber': updated_streetNumber,
                'apartmentNumber': updated_apartmentNumber,
                'city': updated_city,
                'countryId': updated_countryId,
            }

            return render_template('edit_apartment.html',
                               active_menu='dashboard',
                               login=login, 
                               countries_list =countries_list, 
                               apartment=apartment,
                               apartments = get_all_user_apartments)
        


@dash.route('/delete-apartment/<string:apartment_name>')
def delete_apartment(apartment_name):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))

    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                                ApartmentModel.userId==user_model.userId).first()

    
    # print(current_apartment)
    if current_apartment:

        agreements = RentalAgreementModel.query.filter(RentalAgreementModel.apartmentId == current_apartment.apartmentId).all()

        for agreement in agreements:
            # Order of Deletion: Step 1 => BillSettlementModel 
            BillSettlementModel.query.filter(BillSettlementModel.agreementId == agreement.agreementId).delete()

            # Order of Deletion: Step 2 => BillModel 
            BillModel.query.filter(BillModel.agreementId == agreement.agreementId).delete()

            # Order of Deletion: Step 3 => MonthlyRentPaymentModel 
            MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.agreementId == agreement.agreementId).delete()

            # Order of Deletion: Step 4 => RentalAgreementModel 
            flash('Rental agreement  {} has been removed.'.format(agreement.agreementName))
            db.session.delete(agreement)

            # Order of Deletion: Step 3 => TenantModel 
            tenant = TenantModel.query.filter(TenantModel.tenantId == agreement.tenantId).first()
            if tenant:
                other_agreements_count = RentalAgreementModel.query.filter(RentalAgreementModel.tenantId == agreement.tenantId).count()
                
                if other_agreements_count == 0:
                    db.session.delete(tenant)



        flash('Apartment {} has been removed.'.format(current_apartment.apartmentName))
        db.session.delete(current_apartment)
        db.session.commit()
        return redirect(url_for('dash.dashboard'))

    
    return redirect(url_for('dash.dashboard', login=login))

    