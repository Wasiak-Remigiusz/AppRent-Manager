from datetime import date, datetime

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
from sqlalchemy import asc, desc

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
from utils import date_utils

apartment_manager = Blueprint("apartment_manager", __name__,template_folder='../templates')


@apartment_manager.route('/apartment-manager/<string:apartment_name>/', defaults={'tab_name':'rental-agreement-tab '} ,methods=['GET','POST'])
@apartment_manager.route('/apartment-manager/<string:apartment_name>/<string:tab_name>', methods=['GET', 'POST'])
def manager(apartment_name, tab_name):


    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    # tab_name = tab_name
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                    ApartmentModel.userId==user_model.userId).first()
    
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()

    get_all_apartment_agreements = RentalAgreementModel.query.filter(RentalAgreementModel.userId ==user_model.userId,
                                                                RentalAgreementModel.apartmentId == current_apartment.apartmentId
                                                                ).order_by(asc(RentalAgreementModel.startDate)).all()
    
    get_apartment_rent_payments = MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.apartmentId == current_apartment.apartmentId
                                                                       ).order_by(asc(MonthlyRentPaymentModel.monthBillingPeriod)).all()
    
    get_all_apartment_bills = BillModel.query.filter(BillModel.apartmentId == current_apartment.apartmentId
                                                     ).order_by(asc(BillModel.monthBillingPeriod)).all()
    
    get_bills_settlements = BillSettlementModel.query.filter(BillSettlementModel.apartmentId ==current_apartment.apartmentId
                                                            ).order_by(BillSettlementModel.monthBillingPeriod).all()
    # print(get_apartment_rent_payments)
    # agreements = None
    
    apartment_name =apartment_name
    
    return render_template('apartment_manager.html',
                            login=login, 
                            active_menu ='apprent_manager',
                            apartment_name= current_apartment, 
                            apartments=get_all_user_apartments,
                            agreements = get_all_apartment_agreements,
                            apartment_rent_payments = get_apartment_rent_payments,
                            apartment_bills = get_all_apartment_bills,
                            bills_settlements = get_bills_settlements,
                            tab_name = tab_name)


# TAB - Rental Agreement
@apartment_manager.route('/new-rental-agreement/<string:apartment_name>', methods=['GET','POST'])
def new_rental_agreement(apartment_name):



    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                                ApartmentModel.userId==user_model.userId).first()
    
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    
    countries_list = CountryModel.query.all()
    currencies_list = CurrencyModel.query.all()

    # data_start_model = RentalAgreementModel.query.filter(RentalAgreementModel.userId==user_model.userId,
    #                                              RentalAgreementModel.apartmentId ==current_apartment.apartmentId
    #                                              ).with_entities(RentalAgreementModel.startDate).all()
    
    # data_start_list = [  data  for data in data_start_model]
    # print(min(data_start_list))

    

    agreement= {}
    

    if request.method=='GET':
        return render_template('new_rental_agreement.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               countries_list= countries_list,
                               currencies_list= currencies_list,
                               agreement = agreement,
                               apartment = current_apartment,
                               apartments = get_all_user_apartments)
    else:
        
        agreement = {}
        message = None

        agreement_name = request.form.get('agreement_name', '')
        tenant_first_name = request.form.get('tenant_first_name', '')
        tenant_last_name = request.form.get('tenant_last_name', '')
        tenant_phone_number = request.form.get('tenant_phone_number', '')
        tenant_email  = request.form.get('tenant_email', '')
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        currency_id = int(request.form.get('currencyId', 4)) # Polish Zloty id for default value
        payment_due_date = request.form.get('payment_due_date', '')
        deposit_amount = request.form.get('deposit_amount', '')
        monthly_rent_payment = request.form.get('monthly_rent_payment', '')
        bills_settlement = request.form.get('bills_settlement')
        monthly_bills_amount = request.form.get('monthly_bills_amount', '')
        additional_information = request.form.get('additional_information', '')

        is_renatl_agreement_name_unique = (RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId).count() ==0)


        # Checking the form
        match is_renatl_agreement_name_unique:
            case False:
                message = 'The agreement name must be unique.'
                flash(message)

        match  agreement_name:
            case '':
                message = 'The agreement name cannot be left empty.'
                flash(message)

        match  tenant_first_name:
            case '':
                message = "Tenant's first name cannot be left empty."
                flash(message)

        match  start_date:
            case '':
                message = "Start date name cannot be left empty."
                flash(message)


        match  end_date:
            case '':
                message = "End date name cannot be left empty."
                flash(message)

        match  payment_due_date:
            case '':
                message = "The monthly payment due date cannot be left empty."
                flash(message)

        match  deposit_amount: 
            case '':
                message = "The deposit amount cannot be left empty."
                flash(message)

        match  monthly_rent_payment:
            case '':
                message = "Monthly rent payment cannot be left empty."
                flash(message)

        match (bills_settlement, monthly_bills_amount):
            case ('yes', ''):
                message = "Monthly bills amount cannot be left empty if there is a bills settlement."
                flash(message)
                

        if start_date:
            start_date = date.fromisoformat(start_date)

        if end_date:
            end_date =date.fromisoformat(end_date)

        if not start_date == '' and  not end_date == '':
            if start_date >= end_date:
                message = "The start date must be earlier than the end date."
                flash(message)
            else:
                # Overlapping
                overlapping_agreements = RentalAgreementModel.query.filter(RentalAgreementModel.apartmentId  == current_apartment.apartmentId,
                                                                           RentalAgreementModel.userId==user_model.userId,
                                                                           RentalAgreementModel.startDate <= end_date,
                                                                           RentalAgreementModel.endDate >= start_date).all()
                # print('Overlapping: ', overlapping_agreements)
                if overlapping_agreements:
                    message = "The new rental period overlaps with an existing rental agreement."
                    flash(message)


        match bills_settlement:
            case 'yes':
                bills_settlement = True
            case 'no': 
                bills_settlement = False
                monthly_bills_amount = None

        # START ---- Check
        # request_form_data ={}
        # for key in request.form:
        #     request_form_data[key] = request.form.get(key,'')

        # for key, value in request_form_data.items():
        #     print(key, value)
        # END ---- Check

        if not message:

            # TenantModel
            tenant = TenantModel(tenantFirstName = tenant_first_name,
                                tenantLastName = tenant_last_name,
                                tenantTelephone = tenant_phone_number, 
                                tenantEmail = tenant_email)
            db.session.add(tenant)
            db.session.commit()

            # RentalAgreementModel
            new_rental_agreement = RentalAgreementModel(agreementName  = agreement_name,
                                                    userId =  user_model.userId,
                                                    apartmentId =  current_apartment.apartmentId,
                                                    tenantId = tenant.tenantId,
                                                    startDate = start_date ,
                                                    endDate = end_date ,
                                                    currencyId = currency_id ,
                                                    paymentDueDate = payment_due_date,
                                                    depositAmount = deposit_amount,
                                                    monthlyRentPayment = monthly_rent_payment,
                                                    isBillsSettlement = bills_settlement,
                                                    monthlyBillsAmount  = monthly_bills_amount,
                                                    aditionalInformation  = additional_information)
            db.session.add(new_rental_agreement)
            db.session.commit()


            # MonthlyRentPaymentModel
            months_dict = date_utils.get_months_between_dates(start_date, end_date, payment_due_date)

            for month, due_date in months_dict.items():
                month = date.fromisoformat(month)
                due_date = date.fromisoformat(due_date)

                match bills_settlement:
                    case True:
                        amount_payment = float(monthly_rent_payment) + float(monthly_bills_amount)
                    case _: 
                        amount_payment = float(monthly_rent_payment)
                        monthly_bills_amount = None
                

                new_month_rent_payment = MonthlyRentPaymentModel(apartmentId = new_rental_agreement.apartmentId,
                                                                agreementId = new_rental_agreement.agreementId,
                                                                monthBillingPeriod = month,
                                                                paymentDueDate = due_date,
                                                                amountPayment = amount_payment,
                                                                monthlyRentPayment = monthly_rent_payment,
                                                                monthlyBillsAmount  = monthly_bills_amount,
                                                                isBillsSettlement = bills_settlement,
                                                                isPaid = False,
                                                                monthlyRentPaymentDesc = '')
                db.session.add(new_month_rent_payment)
            db.session.commit()


            # BillSettlementModel
            if bills_settlement:

                get_all_new_month_rent_payment = MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.agreementId == new_rental_agreement.agreementId).all()
                
                for i in get_all_new_month_rent_payment:
                    # print(i.monthBillingPeriod)
                    monthly_bill_with_settlement = BillModel.query.filter(BillModel.apartmentId == current_apartment.apartmentId,
                                                                          BillModel.monthBillingPeriod == i.monthBillingPeriod,
                                                                          BillModel.isSettlement == True).all()
                    
                    # print('monthly_bill_with_settlement :',monthly_bill_with_settlement)

                    
                    if isinstance(monthly_bill_with_settlement, list):
                        total_bills_sett_amount = 0
                        for bill in monthly_bill_with_settlement:
                            # print('bill: ', bill.billName)
                            # print('bill.amountBill: ', bill.amountBill)
                            total_bills_sett_amount +=  bill.amountBill
                        # print('total_bills_sett_amount: ', total_bills_sett_amount)
                        # print('i.monthlyBillsAmount: ', i.monthlyBillsAmount)
                         

                        if total_bills_sett_amount == i.monthlyBillsAmount:
                            to_be_refunded_by_landlord = 0
                            to_be_refunded_by_tenant = 0
                        elif total_bills_sett_amount < i.monthlyBillsAmount:
                            to_be_refunded_by_landlord = i.monthlyBillsAmount - total_bills_sett_amount
                            to_be_refunded_by_tenant = None
                        elif total_bills_sett_amount >i.monthlyBillsAmount:
                            to_be_refunded_by_landlord = None
                            to_be_refunded_by_tenant = total_bills_sett_amount - i.monthlyBillsAmount

                        new_monthly_bill_sett = BillSettlementModel(apartmentId = current_apartment.apartmentId,
                                                                        agreementId = new_rental_agreement.agreementId,
                                                                        rentPaymentId = i.rentPaymentId,
                                                                        monthBillingPeriod = i.monthBillingPeriod,
                                                                        toBeRefundedByLandlord = to_be_refunded_by_landlord,
                                                                        toBeRefundedByTenant = to_be_refunded_by_tenant,
                                                                        isPaid = False,
                                                                        billSettlementDesc  = '')
                        db.session.add(new_monthly_bill_sett)
                        db.session.commit()


                    else:
                        # if monthly_bill_with_settlement:
                        bill_sett_amount = 0
                        # print('monthly_bill_settlement' , monthly_bill_with_settlement.billName)
                        bill_sett_amount = monthly_bill_with_settlement.amountBill
                        # print('bill_sett_amount :',bill_sett_amount)
                        # print('i.monthlyBillsAmount :',i.monthlyBillsAmount)

                        if bill_sett_amount == i.monthlyBillsAmount:
                            to_be_refunded_by_landlord = 0
                            to_be_refunded_by_tenant = 0
                        elif bill_sett_amount > i.monthlyBillsAmount:
                            to_be_refunded_by_landlord = i.monthlyBillsAmount - bill_sett_amount
                            to_be_refunded_by_tenant = None
                        elif bill_sett_amount <i.monthlyBillsAmount:
                            to_be_refunded_by_landlord = None
                            to_be_refunded_by_tenant = i.monthlyBillsAmount - bill_sett_amount

                        new_monthly_bill_sett = BillSettlementModel(apartmentId = current_apartment.apartmentId,
                                                                    agreementId = new_rental_agreement.agreementId,
                                                                    rentPaymentId = i.rentPaymentId,
                                                                    monthBillingPeriod = i.monthBillingPeriod,
                                                                    toBeRefundedByLandlord = to_be_refunded_by_landlord,
                                                                    toBeRefundedByTenant = to_be_refunded_by_tenant,
                                                                    isPaid = False,
                                                                    billSettlementDesc = '')
                        db.session.add(new_monthly_bill_sett)
                        db.session.commit()

                    # print('-----------------')

        


            current_apartment = current_apartment.apartmentName

            tab_name = 'rental-agreement-tab'
            flash('New rental agreement created.')
            return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
        
        else:
            
            agreement ={
                    'agreement_name' : agreement_name,
                    'tenant_first_name'  : tenant_first_name,
                    'tenant_last_name'  : tenant_last_name,
                    'tenant_phone_number'  : tenant_phone_number,
                    'tenant_email'   : tenant_email,
                    'start_date'  : start_date,
                    'end_date'  : end_date,
                    'currency_id'  : currency_id,
                    'payment_due_date'  : payment_due_date,
                    'deposit_amount'  : deposit_amount,
                    'monthly_rent_payment' : monthly_rent_payment,
                    'bills_settlement'   : bills_settlement,
                    'monthly_bills_amount'   : monthly_bills_amount,
                    'additional_information'   : additional_information ,
            }

            # print(agreement)

            return render_template('new_rental_agreement.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               countries_list= countries_list,
                               currencies_list= currencies_list,
                               agreement = agreement,
                               apartment = current_apartment,
                               apartments = get_all_user_apartments)


@apartment_manager.route('/edit-rental-agreement/<string:apartment_name>/<string:agreement_name>', methods=['GET','POST'])
def edit_rental_agreement(apartment_name,agreement_name):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                                ApartmentModel.userId==user_model.userId).first()

    current_agreement= RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId).first()
    
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    
    countries_list = CountryModel.query.all()
    currencies_list = CurrencyModel.query.all()



    if request.method == 'GET':
        
        agreement ={
                    'agreement_name' : current_agreement.agreementName,
                    'tenant_first_name': current_agreement.tenant.tenantFirstName,
                    'tenant_last_name': current_agreement.tenant.tenantLastName,
                    'tenant_phone_number': current_agreement.tenant.tenantTelephone,
                    'tenant_email': current_agreement.tenant.tenantEmail,
                    'start_date': current_agreement.startDate,
                    'end_date': current_agreement.endDate,
                    'currency_id': current_agreement.currency.currencyId,
                    'payment_due_date': current_agreement.paymentDueDate,
                    'deposit_amount': current_agreement.depositAmount,
                    'monthly_rent_payment': current_agreement.monthlyRentPayment,
                    'bills_settlement': current_agreement.isBillsSettlement,
                    'monthly_bills_amount': current_agreement.monthlyBillsAmount,
                    'additional_information': current_agreement.aditionalInformation,
            }
        

        # Store the original agreement name in the session
        session['original_agreement_name'] = current_agreement.agreementName

        return render_template('edit_rental_agreement.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               countries_list= countries_list,
                               currencies_list= currencies_list,
                               agreement = agreement,
                               apartment = current_apartment,
                               apartments = get_all_user_apartments)
    else:

        # Check if the agreement name has changed
        original_agreement_name = session.get('original_agreement_name')
        agreement_name = request.form.get('agreement_name', '')
        # print('original_agreement_name', original_agreement_name)
        # print('agreement_name', agreement_name)

        if original_agreement_name != agreement_name:
            flash("The agreement name cannot be changed.")
            return  redirect(url_for('apartment_manager.manager',apartment_name = current_apartment.apartmentName))

        agreement = {}
        message = None

        
        tenant_first_name = request.form.get('tenant_first_name', '')
        tenant_last_name = request.form.get('tenant_last_name', '')
        tenant_phone_number = request.form.get('tenant_phone_number', '')
        tenant_email  = request.form.get('tenant_email', '')
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        currency_id = int(request.form.get('currencyId', 4)) # Polish Zloty id for default value
        payment_due_date = request.form.get('payment_due_date', '')
        deposit_amount = request.form.get('deposit_amount', '')
        # monthly_rent_payment = request.form.get('monthly_rent_payment', '')
        # bills_settlement = request.form.get('bills_settlement')
        # monthly_bills_amount = request.form.get('monthly_bills_amount', '')
        additional_information = request.form.get('additional_information', '')

        is_renatl_agreement_name_unique = (RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId
                                                                ).filter(RentalAgreementModel.agreementId != current_agreement.agreementId).count() ==0)


        # Checking the form
        match is_renatl_agreement_name_unique:
            case False:
                message = 'The agreement name must be unique.'
                flash(message)

        match  agreement_name:
            case '':
                message = 'The agreement name cannot be left empty.'
                flash(message)

        match  tenant_first_name:
            case '':
                message = "Tenant's first name cannot be left empty."
                flash(message)

        # match  start_date:
        #     case '':
        #         message = "Start date name cannot be left empty."
        #         flash(message)


        # match  end_date:
        #     case '':
        #         message = "End date name cannot be left empty."
        #         flash(message)


        match  payment_due_date:
            case '':
                message = "The monthly payment due date cannot be left empty."
                flash(message)

        match  deposit_amount: 
            case '':
                message = "The deposit amount cannot be left empty."
                flash(message)

                
        # match  monthly_rent_payment:
        #     case '':
        #         message = "Monthly rent payment cannot be left empty."
        #         flash(message)

        # match (bills_settlement, monthly_bills_amount):
        #     case ('yes', ''):
        #         message = "Monthly bills amount cannot be left empty if there is a bills settlement."
        #         flash(message)
                

        # if start_date:
        #     start_date = date.fromisoformat(start_date)

        # if end_date:
        #     end_date =date.fromisoformat(end_date)

        # if not start_date == '' and  not end_date == '':
        #     if start_date >= end_date:
        #         message = "The start date must be earlier than the end date."
        #         flash(message)
        #     else:
        #         # Overlapping
        #         overlapping_agreements = RentalAgreementModel.query.filter(RentalAgreementModel.apartmentId  == current_apartment.apartmentId,
        #                                                                    RentalAgreementModel.userId==user_model.userId,
        #                                                                    RentalAgreementModel.startDate <= end_date,
        #                                                                    RentalAgreementModel.endDate >= start_date).filter(RentalAgreementModel.agreementId != current_agreement.agreementId).all()
        #         # print('Overlapping: ', overlapping_agreements)
        #         if overlapping_agreements:
        #             message = "The new rental period overlaps with an existing rental agreement."
        #             flash(message)


        # match bills_settlement:
        #     case 'yes':
        #         bills_settlement = True
        #     case 'no': 
        #         bills_settlement = False
        #         monthly_bills_amount = None

        # START ---- Check
        # request_form_data ={}
        # for key in request.form:
        #     request_form_data[key] = request.form.get(key,'')

        # for key, value in request_form_data.items():
        #     print(key, value)
        # END ---- Check

        if not message:
            tenant =TenantModel.query.filter(TenantModel.tenantId == current_agreement.tenantId).first()

            if not tenant:
                tenant = TenantModel()
                db.session.add()

            # Order of Update - Step 1 - TenantModel
            tenant.tenantFirstName = tenant_first_name
            tenant.tenantLastName = tenant_last_name
            tenant.tenantTelephone = tenant_phone_number
            tenant.tenantEmail = tenant_email

            # Order of Update - Step 2 - RentalAgreementModel
            current_agreement.agreementName = agreement_name
            # current_agreement.startDate = start_date
            # current_agreement.endDate = end_date
            current_agreement.currencyId = currency_id
            current_agreement.paymentDueDate = payment_due_date
            current_agreement.depositAmount = deposit_amount
            # current_agreement.monthlyRentPayment = monthly_rent_payment
            # current_agreement.isBillsSettlement = bills_settlement
            # current_agreement.monthlyBillsAmount = monthly_bills_amount
            current_agreement.aditionalInformation = additional_information

            
            # match bills_settlement:
            #         case True:
            #             amount_payment = float(monthly_rent_payment) + float(monthly_bills_amount)
            #         case _: 
            #             amount_payment = float(monthly_rent_payment)
            #             monthly_bills_amount = None


            # Order of Update - Step 2 - MonthlyRentPaymentModel
            
             
            months_dict = date_utils.get_months_between_dates(current_agreement.startDate, current_agreement.endDate, payment_due_date)

            due_date_list = []
            for month, due_date in months_dict.items():
                month = date.fromisoformat(month)
                due_date = date.fromisoformat(due_date)
                due_date_list.append(due_date)


            get_monthly_rent_payment  = MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.agreementId == current_agreement.agreementId,
                                                                         MonthlyRentPaymentModel.apartmentId == current_apartment.apartmentId).all()


            for i, due_date in zip(get_monthly_rent_payment, due_date_list):
                i.paymentDueDate = due_date
                # i.amountPayment = amount_payment
                # i.monthlyRentPayment = monthly_rent_payment
                # i.monthlyBillsAmount = monthly_bills_amount 
                # i.isBillsSettlement = bills_settlement 

            db.session.commit()


            # tenant = TenantModel(tenantFirstName = tenant_first_name,
            #                     tenantLastName = tenant_last_name,
            #                     tenantTelephone = tenant_phone_number, 
            #                     tenantEmail = tenant_email)
            # db.session.add(tenant)
            # db.session.commit()

            # new_rental_agreement = RentalAgreementModel(agreementName  = agreement_name,
            #                                         userId =  user_model.userId,
            #                                         apartmentId =  current_apartment.apartmentId,
            #                                         tenantId = tenant.tenantId,
            #                                         startDate = start_date ,
            #                                         endDate = end_date ,
            #                                         currencyId = currency_id ,
            #                                         paymentDueDate = payment_due_date,
            #                                         depositAmount = deposit_amount,
            #                                         monthlyRentPayment = monthly_rent_payment,
            #                                         isBillsSettlement = bills_settlement,
            #                                         monthlyBillsAmount  = monthly_bills_amount,
            #                                         aditionalInformation  = additional_information)
            # db.session.add(new_rental_agreement)
            # db.session.commit()

            
            current_apartment = current_apartment.apartmentName

            tab_name = 'rental-agreement-tab'
            flash('Rental agreement has been updated successfully.')
            return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
        
        else:
            
            agreement ={
                    'agreement_name' : agreement_name,
                    'tenant_first_name'  : tenant_first_name,
                    'tenant_last_name'  : tenant_last_name,
                    'tenant_phone_number'  : tenant_phone_number,
                    'tenant_email'   : tenant_email,
                    'start_date'  : start_date,
                    'end_date'  : end_date,
                    'currency_id'  : currency_id,
                    'payment_due_date'  : payment_due_date,
                    'deposit_amount'  : deposit_amount,
                    # 'monthly_rent_payment' : monthly_rent_payment,
                    # 'bills_settlement'   : bills_settlement,
                    # 'monthly_bills_amount'   : monthly_bills_amount,
                    'additional_information'   : additional_information ,
            }

            # print(agreement)

            return render_template('edit_rental_agreement.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               countries_list= countries_list,
                               currencies_list= currencies_list,
                               agreement = agreement,
                               apartment = current_apartment,
                               apartments = get_all_user_apartments)



@apartment_manager.route('/delete-rental-agreement/<string:agreement_name>', methods=['GET','POST'])
def delete_rental_agreement(agreement_name):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))

    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_agreement= RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId).first()

    tenant = TenantModel.query.filter(TenantModel.tenantId == current_agreement.tenantId).first()
    
    current_apartment = current_agreement.apartment.apartmentName
    # print(current_apartment)
    
    # print(current_apartment)
    if current_agreement:

        # Order of Deletion: Step 1 => BillSettlementModel 
        BillSettlementModel.query.filter(BillSettlementModel.agreementId == current_agreement.agreementId).delete()

        # Order of Deletion: Step 2 => MonthlyRentPaymentModel 
        MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.agreementId == current_agreement.agreementId).delete()

        # Order of Deletion: Step 3 => RentalAgreementModel 
        flash('Renatl agreement  {} has been removed.'.format(current_agreement.agreementName))
        db.session.delete(current_agreement)

        # Order of Deletion: Step 3 => TenantModel 
        if tenant:
            other_agreements_count = RentalAgreementModel.query.filter(RentalAgreementModel.tenantId == tenant.tenantId).count()
            
            if other_agreements_count == 0:
                db.session.delete(tenant)


        tab_name = 'rental-agreement-tab'
        db.session.commit()
        return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))

    
    return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment))



# TAB - Monthly Rent Payments
@apartment_manager.route('/edit-rental-payment/<string:agreement_name>/<int:rental_payment_Id>', methods=['GET','POST'])
def edit_rental_payment(agreement_name,rental_payment_Id):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_agreement= RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId).first()
    
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    payment = MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.rentPaymentId == rental_payment_Id,
                                                   MonthlyRentPaymentModel.agreementId == current_agreement.agreementId).first()
    
    current_apartment = current_agreement.apartment.apartmentName
    
    
    
    if request.method == 'GET':
                return render_template('edit_rental_payment.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               agreement = current_agreement,
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               payment = payment)
        # return 'get'
    else:
        paymentDate = request.form.get('paymentDate', '')
        monthlyRentPayment = request.form.get('monthlyRentPayment', '')
        monthlyBillsAmount = request.form.get('monthlyBillsAmount', '')
        isPaid = request.form.get('isPaid')
        monthlyRentPaymentDesc = request.form.get('monthlyRentPaymentDesc', '')

        message = None

        match  monthlyRentPayment:
            case '':
                message = "The monthly rent payment cannot be empty."
                flash(message)

        match  monthlyBillsAmount:
            case '':
                message = "The monthly bills amount cannot be empty."
                flash(message)
                

        if not message:

            if payment.monthlyBillsAmount != monthlyBillsAmount:
                update_bill_settlement = True
            else:
                update_bill_settlement = False


            if paymentDate:
                try: 
                    paymentDate =  date.fromisoformat(paymentDate)
                except ValueError:
                    paymentDate = None
            else:
                paymentDate = None


            if isPaid == 'yes':
                isPaid = True
            else:
                isPaid = False


            bills_settlement = payment.rental_agreement.isBillsSettlement
            match bills_settlement:
                    case True:
                        amountPayment = float(monthlyRentPayment) + float(monthlyBillsAmount)
                    case _: 
                        amountPayment = float(monthlyRentPayment)
                        monthlyBillsAmount = None

            payment.paymentDate = paymentDate
            payment.amountPayment = amountPayment
            payment.monthlyRentPayment  = monthlyRentPayment 
            payment.monthlyBillsAmount  = monthlyBillsAmount 
            payment.isPaid = isPaid
            payment.monthlyRentPaymentDesc = monthlyRentPaymentDesc

            db.session.commit()

            # BillModel and BillSettlementModel 
            # Step 01: BillModel
            if update_bill_settlement:

                monthly_bill_with_settlement = BillModel.query.filter(BillModel.apartmentId == current_agreement.apartmentId,
                                                                          BillModel.monthBillingPeriod == payment.monthBillingPeriod,
                                                                          BillModel.isSettlement == True).all()
                
                if isinstance(monthly_bill_with_settlement, list):
                        total_bills_sett_amount = 0
                        for bill in monthly_bill_with_settlement:
                            # print('bill: ', bill.billName)
                            # print('bill.amountBill: ', bill.amountBill)
                            total_bills_sett_amount +=  bill.amountBill
                        # print('total_bills_sett_amount: ', total_bills_sett_amount)
                        # print('i.monthlyBillsAmount: ', i.monthlyBillsAmount)
                         

                        if total_bills_sett_amount == payment.monthlyBillsAmount:
                            to_be_refunded_by_landlord = 0
                            to_be_refunded_by_tenant = 0
                        elif total_bills_sett_amount < payment.monthlyBillsAmount:
                            to_be_refunded_by_landlord = payment.monthlyBillsAmount - total_bills_sett_amount
                            to_be_refunded_by_tenant = None
                        elif total_bills_sett_amount >payment.monthlyBillsAmount:
                            to_be_refunded_by_landlord = None
                            to_be_refunded_by_tenant = total_bills_sett_amount - payment.monthlyBillsAmount

                        # Step 02: BillSettlementModel
                        bill_settlement = BillSettlementModel.query.filter(BillSettlementModel.rentPaymentId == payment.rentPaymentId,
                                                       BillSettlementModel.apartmentId  == current_agreement.apartmentId,
                                                   BillSettlementModel.agreementId == current_agreement.agreementId).first()

                        bill_settlement.toBeRefundedByLandlord  = to_be_refunded_by_landlord
                        bill_settlement.toBeRefundedByTenant  = to_be_refunded_by_tenant

                        
                        db.session.commit()
                




                
                
                

            tab_name = 'monthly-rent-tab'
            current_apartment = current_agreement.apartment.apartmentName

            return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
        
        else:
            return render_template('edit_rental_payment.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               agreement = current_agreement,
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               payment = payment)


@apartment_manager.route('/update-rental-payment-status/<string:agreement_name>/<int:rental_payment_Id>', methods=['GET','POST'])
def update_rental_payment_status(agreement_name,rental_payment_Id):


    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_agreement= RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId).first()
    
    payment = MonthlyRentPaymentModel.query.filter(MonthlyRentPaymentModel.rentPaymentId == rental_payment_Id,
                                                   MonthlyRentPaymentModel.agreementId == current_agreement.agreementId).first()

    payment.isPaid = (payment.isPaid + 1) % 2
    db.session.commit()

    # tenant = TenantModel.query.filter(TenantModel.tenantId == current_agreement.tenantId).first()
    
    current_apartment = current_agreement.apartment.apartmentName
    
    tab_name = 'monthly-rent-tab'

    return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))

# TAB - Bills
@apartment_manager.route('/new-bill/<string:apartment_name>', methods=['GET','POST'])
def new_bill(apartment_name):
    
    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName == login.user_name).first()
    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                                ApartmentModel.userId==user_model.userId).first()
    
    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    
    bill_type_list = BillTypeModel.query.all()
    currencies_list = CurrencyModel.query.all()
    agreement= {}
    new_bill = {}
    

    if request.method=='GET':
        return render_template('new_bill.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               bill_type_list= bill_type_list,
                               agreement = agreement,
                               apartment = current_apartment,
                               apartments = get_all_user_apartments,
                               currencies_list= currencies_list,
                               bill = new_bill)
    else:
         
        
        new_bill = {}
        message = None

        # for key, value in request.form.items():
        #     print(key,value)

        bill_name = request.form.get('bill_name', '')
        bill_type_id = int(request.form.get('bill_type_id',1))
        month_billing_period = request.form.get('month_billing_period', '')
        currency_id = int(request.form.get('currency_id', 4)) # Polish Zloty id for default value
        payment_due_date = request.form.get('payment_due_date', '')
        amount_bill = request.form.get('amount_bill', '')
        is_settlement = request.form.get('is_settlement')
        media_bill_desc = request.form.get('media_bill_desc', '')



        # Checking the form


        match  month_billing_period:
            case '':
                message = "The month cannot be empty."
                flash(message)

        match  payment_due_date:
            case '':
                message = "The monthly payment due date cannot be empty."
                flash(message)

        match  amount_bill:
            case '':
                message = "The bill amount cannot be empty."
                flash(message)

                

        if month_billing_period:
            try:
                get_month_billing_period = datetime.strptime(month_billing_period + '-01', '%Y-%m-%d').date()
            except ValueError as e:
                message = f"Invalid month format: {e}"
                flash(message)


        match is_settlement:
            case 'yes':
                is_settlement = True
            case 'no': 
                is_settlement = False


        if not message:

            # BillModel
            months_dict = date_utils.get_months_between_dates(get_month_billing_period, get_month_billing_period, payment_due_date)

            for month, due_date in months_dict.items():
                month = date.fromisoformat(month)
                due_date = date.fromisoformat(due_date)

                

                new_bill = BillModel(apartmentId = current_apartment.apartmentId,
                                        currencyId = currency_id,
                                        monthBillingPeriod = get_month_billing_period,
                                        paymentDueDate = due_date,
                                        amountBill = amount_bill,
                                        billName = bill_name ,
                                        billTypeId = bill_type_id,
                                        isSettlement  = is_settlement,
                                        isPaid = False,
                                        mediaBillDesc = media_bill_desc)
            
                db.session.add(new_bill)
            db.session.commit()


            # BillModel and BillSettlementModel 
            # Step 01: BillModel
            if is_settlement:
                # print(is_settlement)
                monthly_bill_with_settlement = BillModel.query.filter(BillModel.apartmentId == current_apartment.apartmentId,
                                                                          BillModel.monthBillingPeriod == new_bill.monthBillingPeriod,
                                                                          BillModel.isSettlement == True).all()
                
                if isinstance(monthly_bill_with_settlement, list):
                        total_bills_sett_amount = 0
                        for bill in monthly_bill_with_settlement:
                            # print('bill: ', bill.billName)
                            # print('bill.amountBill: ', bill.amountBill)
                            total_bills_sett_amount +=  bill.amountBill
                        # print('total_bills_sett_amount: ', total_bills_sett_amount)
                        # print('i.monthlyBillsAmount: ', i.monthlyBillsAmount)
                         
                        
                        # Step 02: BillSettlementModel
                        get_all_bills_settlement_monthly = BillSettlementModel.query.filter(BillSettlementModel.apartmentId ==current_apartment.apartmentId,
                                                                                            BillSettlementModel.monthBillingPeriod ==new_bill.monthBillingPeriod
                                                                                            ).all()


                        if isinstance(get_all_bills_settlement_monthly, list):
                            for agreement in get_all_bills_settlement_monthly:
                                # print('bill: ', bill.billName)
                                # print('bill.amountBill: ', bill.amountBill)
                                # total_bills_sett_amount +=  bill.amountBill
                                # print('agreement: ', agreement.rental_agreement.agreementName)
                                # print('agreement: ', agreement.toBeRefundedByLandlord)
                                # print('agreement: ', agreement.toBeRefundedByTenant)
                                # print('agreement: ', agreement.toBeRefundedByTenant)
                                # print('agreement.monthly_rent_payment.monthlyBillsAmount: ', agreement.monthly_rent_payment.monthlyBillsAmount)
                                # print('--------')

                                monthlyBillsAmount  = agreement.monthly_rent_payment.monthlyBillsAmount
                                
                           
                                if total_bills_sett_amount == monthlyBillsAmount:
                                    to_be_refunded_by_landlord = 0
                                    to_be_refunded_by_tenant = 0
                                elif total_bills_sett_amount < monthlyBillsAmount:
                                    to_be_refunded_by_landlord = monthlyBillsAmount - total_bills_sett_amount
                                    to_be_refunded_by_tenant = None
                                elif total_bills_sett_amount >monthlyBillsAmount:
                                    to_be_refunded_by_landlord = None
                                    to_be_refunded_by_tenant = total_bills_sett_amount - monthlyBillsAmount

                                


                                agreement.toBeRefundedByLandlord  = to_be_refunded_by_landlord
                                agreement.toBeRefundedByTenant  = to_be_refunded_by_tenant

                                
                                db.session.commit()
                
            # else:
            #     print('is_settlement: ',is_settlement)


                # ----------

            current_apartment = current_apartment.apartmentName

            tab_name = 'bills-tab'
            flash('New bill created.')
            return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
        

        else:
            
            new_bill ={
                    'bill_name' : bill_name,
                    'bill_type_id'  : bill_type_id,
                    'month_billing_period'  : month_billing_period,
                    'currency_id'  : currency_id,
                    'payment_due_date'   : payment_due_date,
                    'amount_bill'  : amount_bill,
                    'is_settlement'  : is_settlement, 
                    'currency_id'  : currency_id,
                    'media_bill_desc': media_bill_desc
                    }



            return render_template('new_bill.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               bill_type_list= bill_type_list,
                               agreement = agreement,
                               apartment = current_apartment,
                               apartments = get_all_user_apartments,
                               currencies_list= currencies_list,
                               bill = new_bill)



@apartment_manager.route('/update-bill-payment-status/<string:apartment_name>/<int:bill_id>', methods=['GET','POST'])
def update_bill_payment_status(apartment_name,bill_id):


    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                    ApartmentModel.userId==user_model.userId).first()
    
    bill = BillModel.query.filter(BillModel.billId == bill_id,
                                                   BillModel.apartmentId == current_apartment.apartmentId).first()

    bill.isPaid = (bill.isPaid + 1) % 2
    db.session.commit()

    # tenant = TenantModel.query.filter(TenantModel.tenantId == current_agreement.tenantId).first()
    
    current_apartment = current_apartment.apartmentName
    
    tab_name = 'bills-tab'

    return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))



@apartment_manager.route('/edit-bill-payment/<string:apartment_name>/<int:bill_id>', methods=['GET','POST'])
def edit_bill_payment(apartment_name,bill_id):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                    ApartmentModel.userId==user_model.userId).first()
    
    bill = BillModel.query.filter(BillModel.billId == bill_id,
                                                   BillModel.apartmentId == current_apartment.apartmentId).first()
    
    current_apartment = current_apartment.apartmentName

    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    

    current_apartment = current_apartment
    
    bill_type_list = BillTypeModel.query.all()
    currencies_list = CurrencyModel.query.all()
    monthBillingPeriod  = bill.monthBillingPeriod  
    paymentDueDate  = bill.paymentDueDate
    monthBillingPeriod = datetime.strftime(monthBillingPeriod, '%Y-%m') 
    paymentDueDate  = datetime.strftime(paymentDueDate, '%d') 

    if request.method == 'GET':
                return render_template('edit_bill.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               currencies_list = currencies_list,
                               bill_type_list = bill_type_list,
                               bill = bill,
                               monthBillingPeriod = monthBillingPeriod,
                               paymentDueDate = paymentDueDate)
        # return 'get'
    else:
        message = None


        billName = request.form.get('billName', '')
        billTypeId = int(request.form.get('billTypeId',1))
        monthBillingPeriod = request.form.get('monthBillingPeriod', '')
        currencyId = int(request.form.get('currencyId', 4)) # Polish Zloty id for default value
        paymentDueDate = request.form.get('paymentDueDate', '')
        amountBill = request.form.get('amountBill', '')
        paymentDate  = request.form.get('paymentDate', '')
        isPaid  = request.form.get('isPaid')
        # isSettlement  = request.form.get('isSettlement')
        mediaBillDesc = request.form.get('mediaBillDesc', '')

        match  amountBill:
            case '':
                message = "The bill amount cannot be empty."
                flash(message)

        match  paymentDueDate:
            case '':
                message = "The monthly payment due date cannot be left empty."
                flash(message)

        if monthBillingPeriod:
            try:
                get_month_billing_period = datetime.strptime(monthBillingPeriod + '-01', '%Y-%m-%d').date()
            except ValueError as e:
                message = f"Invalid month format: {e}"
                flash(message)

        if not message:
            if paymentDate:
                try: 
                    paymentDate =  date.fromisoformat(paymentDate)
                except ValueError:
                    paymentDate = None
            else:
                paymentDate = None


            if isPaid == 'yes':
                isPaid = True
            else:
                isPaid = False


            # if isSettlement == 'yes':
            #     isSettlement = True
            # else:
            #     isSettlement = False

            # BillModel
            months_dict = date_utils.get_months_between_dates(get_month_billing_period, get_month_billing_period, paymentDueDate)

            for month, due_date in months_dict.items():
                month = date.fromisoformat(month)
                due_date = date.fromisoformat(due_date)

                bill.billName= billName
                bill.billTypeId= billTypeId
                bill.monthBillingPeriod= get_month_billing_period
                bill.currencyId= currencyId
                bill.paymentDueDate= due_date
                bill.amountBill= amountBill
                bill.paymentDate= paymentDate
                # bill.isSettlement= isSettlement
                bill.isPaid= isPaid 
                bill.mediaBillDesc= mediaBillDesc


            db.session.commit()

            tab_name = 'bills-tab'

            return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
        else:
            return render_template('edit_bill.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               currencies_list = currencies_list,
                               bill_type_list = bill_type_list,
                               bill = bill,
                               monthBillingPeriod = monthBillingPeriod,
                               paymentDueDate = paymentDueDate)


@apartment_manager.route('/duplicate-bill-payment/<string:apartment_name>/<int:bill_id>', methods=['GET','POST'])
def duplicate_bill_payment(apartment_name,bill_id):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                    ApartmentModel.userId==user_model.userId).first()
    
    
    bill = BillModel.query.filter(BillModel.billId == bill_id,
                                                   BillModel.apartmentId == current_apartment.apartmentId).first()
    

    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()
    

    current_apartment = current_apartment
    
    bill_type_list = BillTypeModel.query.all()
    currencies_list = CurrencyModel.query.all()
    monthBillingPeriod  = bill.monthBillingPeriod  
    paymentDueDate  = bill.paymentDueDate
    monthBillingPeriod = datetime.strftime(monthBillingPeriod, '%Y-%m') 
    paymentDueDate  = datetime.strftime(paymentDueDate, '%d') 

    if request.method == 'GET':
                return render_template('duplicate_bill.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               currencies_list = currencies_list,
                               bill_type_list = bill_type_list,
                               bill = bill,
                               monthBillingPeriod = monthBillingPeriod,
                               paymentDueDate = paymentDueDate)
        # return 'get'
    else:
        message = None


        billName = request.form.get('billName', '')
        billTypeId = int(request.form.get('billTypeId',1))
        monthBillingPeriod = request.form.get('monthBillingPeriod', '')
        currencyId = int(request.form.get('currencyId', 4)) # Polish Zloty id for default value
        paymentDueDate = request.form.get('paymentDueDate', '')
        amountBill = request.form.get('amountBill', '')
        isPaid  = request.form.get('isPaid')
        isSettlement  = request.form.get('isSettlement')
        mediaBillDesc = request.form.get('mediaBillDesc', '')


        match  amountBill:
            case '':
                message = "The bill amount cannot be empty."
                flash(message)

        match  paymentDueDate:
            case '':
                message = "The monthly payment due date cannot be left empty."
                flash(message)

        if monthBillingPeriod:
            try:
                get_month_billing_period = datetime.strptime(monthBillingPeriod + '-01', '%Y-%m-%d').date()
            except ValueError as e:
                message = f"Invalid month format: {e}"
                flash(message)

        if not message:

            if isPaid == 'yes':
                isPaid = True
            else:
                isPaid = False


            if isSettlement == 'yes':
                isSettlement = True
            else:
                isSettlement = False

            # BillModel
            months_dict = date_utils.get_months_between_dates(get_month_billing_period, get_month_billing_period, paymentDueDate)

            for month, due_date in months_dict.items():
                month = date.fromisoformat(month)
                due_date = date.fromisoformat(due_date)

                # bill.billName= billName
                # bill.billTypeId= billTypeId
                # bill.monthBillingPeriod= get_month_billing_period
                # bill.currencyId= currencyId
                # bill.paymentDueDate= due_date
                # bill.amountBill= amountBill
                # bill.isSettlement= isSettlement
                # bill.isPaid= isPaid 
                # bill.mediaBillDesc= mediaBillDesc

                new_bill = BillModel(apartmentId = current_apartment.apartmentId,
                                        currencyId = currencyId,
                                        monthBillingPeriod = get_month_billing_period,
                                        paymentDueDate = due_date,
                                        amountBill = amountBill,
                                        billName = billName ,
                                        billTypeId = billTypeId,
                                        isSettlement  = isSettlement,
                                        isPaid = isPaid,
                                        mediaBillDesc = mediaBillDesc)
            
                db.session.add(new_bill)


            db.session.commit()

            # BillModel and BillSettlementModel 
            # Step 01: BillModel
            if isSettlement:
                # print(isSettlement)
                monthly_bill_with_settlement = BillModel.query.filter(BillModel.apartmentId == current_apartment.apartmentId,
                                                                          BillModel.monthBillingPeriod == new_bill.monthBillingPeriod,
                                                                          BillModel.isSettlement == True).all()
                
                if isinstance(monthly_bill_with_settlement, list):
                        total_bills_sett_amount = 0
                        for bill in monthly_bill_with_settlement:
                            # print('bill: ', bill.billName)
                            # print('bill.amountBill: ', bill.amountBill)
                            total_bills_sett_amount +=  bill.amountBill
                        # print('total_bills_sett_amount: ', total_bills_sett_amount)
                        # print('i.monthlyBillsAmount: ', i.monthlyBillsAmount)
                         
                        
                        # Step 02: BillSettlementModel
                        get_all_bills_settlement_monthly = BillSettlementModel.query.filter(BillSettlementModel.apartmentId ==current_apartment.apartmentId,
                                                                                            BillSettlementModel.monthBillingPeriod ==new_bill.monthBillingPeriod
                                                                                            ).all()


                        if isinstance(get_all_bills_settlement_monthly, list):
                            for agreement in get_all_bills_settlement_monthly:
                                # print('bill: ', bill.billName)
                                # print('bill.amountBill: ', bill.amountBill)
                                # total_bills_sett_amount +=  bill.amountBill
                                # print('agreement: ', agreement.rental_agreement.agreementName)
                                # print('agreement: ', agreement.toBeRefundedByLandlord)
                                # print('agreement: ', agreement.toBeRefundedByTenant)
                                # print('agreement: ', agreement.toBeRefundedByTenant)
                                # print('agreement.monthly_rent_payment.monthlyBillsAmount: ', agreement.monthly_rent_payment.monthlyBillsAmount)
                                # print('--------')

                                monthlyBillsAmount  = agreement.monthly_rent_payment.monthlyBillsAmount
                                
                           
                                if total_bills_sett_amount == monthlyBillsAmount:
                                    to_be_refunded_by_landlord = 0
                                    to_be_refunded_by_tenant = 0
                                elif total_bills_sett_amount < monthlyBillsAmount:
                                    to_be_refunded_by_landlord = monthlyBillsAmount - total_bills_sett_amount
                                    to_be_refunded_by_tenant = None
                                elif total_bills_sett_amount >monthlyBillsAmount:
                                    to_be_refunded_by_landlord = None
                                    to_be_refunded_by_tenant = total_bills_sett_amount - monthlyBillsAmount

                                


                                agreement.toBeRefundedByLandlord  = to_be_refunded_by_landlord
                                agreement.toBeRefundedByTenant  = to_be_refunded_by_tenant

                                
                                db.session.commit()
                
            # else:
            #     print('is_settlement: ',is_settlement)


                # ----------


            current_apartment = current_apartment.apartmentName
            tab_name = 'bills-tab'

            return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
        else:

            return render_template('duplicate_bill.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               currencies_list = currencies_list,
                               bill_type_list = bill_type_list,
                               bill = bill,
                               monthBillingPeriod = monthBillingPeriod,
                               paymentDueDate = paymentDueDate)


@apartment_manager.route('/delete-bill-payment/<string:apartment_name>/<int:bill_id>', methods=['GET','POST'])
def delete_bill_payment(apartment_name, bill_id):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))

    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                    ApartmentModel.userId==user_model.userId).first()
    
    
    bill = BillModel.query.filter(BillModel.billId == bill_id,
                                                   BillModel.apartmentId == current_apartment.apartmentId).first()


    if bill:

        # Check if the bill is part of a Bill Settlement
        if bill.isSettlement:
            isSettlement = True
            monthBillingPeriod  = bill.monthBillingPeriod
            
        # Order of Deletion: Step 1 => 
        BillModel.query.filter(BillModel.billId == bill_id,
                                BillModel.apartmentId == current_apartment.apartmentId).delete()

        # Order of Deletion: Step 2 =>  
        flash('Bill has been removed.')


        # Order of Deletion: Step 3 =>  

        db.session.commit()

        # BillSettlementModel update
        # BillModel and BillSettlementModel 

        # Step 01: BillModel
        if isSettlement:
            monthly_bill_with_settlement = BillModel.query.filter(BillModel.apartmentId == current_apartment.apartmentId,
                                                                          BillModel.monthBillingPeriod == monthBillingPeriod,
                                                                          BillModel.isSettlement == True).all()
            
            if isinstance(monthly_bill_with_settlement, list):
                        total_bills_sett_amount = 0
                        for bill in monthly_bill_with_settlement:
                            # print('bill: ', bill.billName)
                            # print('bill.amountBill: ', bill.amountBill)
                            total_bills_sett_amount +=  bill.amountBill
                        print('total_bills_sett_amount: ', total_bills_sett_amount)
                        # print('i.monthlyBillsAmount: ', i.monthlyBillsAmount)
                         
                        
                        # Step 02: BillSettlementModel
                        get_all_bills_settlement_monthly = BillSettlementModel.query.filter(BillSettlementModel.apartmentId ==current_apartment.apartmentId,
                                                                                            BillSettlementModel.monthBillingPeriod ==monthBillingPeriod
                                                                                            ).all()


                        if isinstance(get_all_bills_settlement_monthly, list):
                            for agreement in get_all_bills_settlement_monthly:
                                # print('bill: ', bill.billName)
                                # print('bill.amountBill: ', bill.amountBill)
                                # total_bills_sett_amount +=  bill.amountBill
                                # print('agreement: ', agreement.rental_agreement.agreementName)
                                # print('agreement: ', agreement.toBeRefundedByLandlord)
                                # print('agreement: ', agreement.toBeRefundedByTenant)
                                # print('agreement: ', agreement.toBeRefundedByTenant)
                                # print('agreement.monthly_rent_payment.monthlyBillsAmount: ', agreement.monthly_rent_payment.monthlyBillsAmount)
                                # print('--------')

                                monthlyBillsAmount  = agreement.monthly_rent_payment.monthlyBillsAmount
                                
                           
                                if total_bills_sett_amount == monthlyBillsAmount:
                                    to_be_refunded_by_landlord = 0
                                    to_be_refunded_by_tenant = 0
                                elif total_bills_sett_amount < monthlyBillsAmount:
                                    to_be_refunded_by_landlord = monthlyBillsAmount - total_bills_sett_amount
                                    to_be_refunded_by_tenant = None
                                elif total_bills_sett_amount >monthlyBillsAmount:
                                    to_be_refunded_by_landlord = None
                                    to_be_refunded_by_tenant = total_bills_sett_amount - monthlyBillsAmount

                                


                                agreement.toBeRefundedByLandlord  = to_be_refunded_by_landlord
                                agreement.toBeRefundedByTenant  = to_be_refunded_by_tenant

                                
                                db.session.commit()




        current_apartment = current_apartment.apartmentName
        tab_name = 'bills-tab'

        return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
    

# TAB - Bills Settlement
@apartment_manager.route('/edit-bill-settlement/<string:apartment_name>/<string:agreement_name>/<int:bill_settlement_id>', methods=['GET','POST'])
def edit_bill_settlement(apartment_name,agreement_name,bill_settlement_id):

    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    
    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                    ApartmentModel.userId==user_model.userId).first()

    current_agreement= RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId).first()
    
    bill_settlement = BillSettlementModel.query.filter(BillSettlementModel.billSettlementId == bill_settlement_id,
                                                       BillSettlementModel.apartmentId  == current_agreement.apartmentId,
                                                   BillSettlementModel.agreementId == current_agreement.agreementId).first()


    get_all_user_apartments = ApartmentModel.query.filter(ApartmentModel.userId ==user_model.userId ).all()

    if request.method == 'GET':
                return render_template('edit_bill_settlement.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               bill_settlement = bill_settlement)
    else:
        message = None

        toBeRefundedByLandlord = request.form.get('toBeRefundedByLandlord', '')
        toBeRefundedByTenant = request.form.get('toBeRefundedByTenant', '')
        paymentDate  = request.form.get('paymentDate', '')
        isPaid  = request.form.get('isPaid')
        billSettlementDesc = request.form.get('billSettlementDesc', '')


        match toBeRefundedByLandlord:
            case '':
                toBeRefundedByLandlord = 0

        match toBeRefundedByTenant:
            case '':
                toBeRefundedByTenant = 0



        if float(toBeRefundedByLandlord) > 0 and  float(toBeRefundedByTenant) > 0:
            message = 'The values of "Landlord Pays" and "Tenant Pays" cannot both be greater than 0.'
            flash(message)




        if not message:
            if paymentDate:
                try: 
                    paymentDate =  date.fromisoformat(paymentDate)
                except ValueError:
                    paymentDate = None
            else:
                paymentDate = None


            if isPaid == 'yes':
                isPaid = True
            else:
                isPaid = False

            # BillSettlementModel
            bill_settlement.toBeRefundedByLandlord = toBeRefundedByLandlord
            bill_settlement.toBeRefundedByTenant = toBeRefundedByTenant
            bill_settlement.paymentDate  = paymentDate
            bill_settlement.isPaid = isPaid
            bill_settlement.billSettlementDesc  = billSettlementDesc

            db.session.commit()


            tab_name = 'bills-settlement-tab'
            current_apartment = current_apartment.apartmentName

            return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))
        else:
            return render_template('edit_bill_settlement.html', 
                               login=login, 
                               active_menu ='apprent_manager',
                               apartment = current_apartment,
                               apartments=get_all_user_apartments,
                               bill_settlement = bill_settlement)

@apartment_manager.route('/update-bill-settlement-status/<string:apartment_name>/<string:agreement_name>/<int:bill_settlement_id>', methods=['GET','POST'])
def update_bill_settlement_status(apartment_name,agreement_name,bill_settlement_id):


    login = UserPass(user_name=session.get('user'))
    login.get_user_info()
    if not login.is_valid:
        return redirect(url_for('auth.log_in'))
    
    user_model = UserModel.query.filter(UserModel.userName== login.user_name).first()

    current_apartment= ApartmentModel.query.filter(ApartmentModel.apartmentName ==apartment_name, 
                                                    ApartmentModel.userId==user_model.userId).first()
    

    current_agreement= RentalAgreementModel.query.filter(RentalAgreementModel.agreementName ==agreement_name, 
                                                                RentalAgreementModel.userId==user_model.userId).first()
    
    
    bill_settlement = BillSettlementModel.query.filter(BillSettlementModel.billSettlementId == bill_settlement_id,
                                                       BillSettlementModel.apartmentId  == current_agreement.apartmentId,
                                                   BillSettlementModel.agreementId == current_agreement.agreementId
                                                   ).first()
    
    print('bill_settlement :',bill_settlement)

    bill_settlement.isPaid = (bill_settlement.isPaid + 1) % 2
    db.session.commit()
    
    current_apartment = current_agreement.apartment.apartmentName
    
    tab_name = 'bills-settlement-tab'

    return redirect(url_for('apartment_manager.manager', apartment_name =current_apartment, tab_name=tab_name))