'''
Created on 7 Jul 2021

@author: jacklok
'''

from flask import Blueprint, request, session 
from flask_restful import abort
import logging
from trexlib.utils.log_util import get_tracelog
from flask_restful import Api
from trexmodel.utils.model.model_util import create_db_client
from flask.json import jsonify
from datetime import datetime
from trexapi.decorators.api_decorators import auth_token_required,\
    outlet_key_required
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.customer_models import Customer
from trexmodel.models.datastore.user_models import User
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.merchant_models import Outlet,\
    MerchantAcct
from trexapi.forms.customer_api_forms import CustomerDetailsForm
from werkzeug.datastructures import ImmutableMultiDict
import gettext

logger = logging.getLogger('api')


customer_api_bp = Blueprint('customer_api_base_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/customers')

logger = logging.getLogger('api')

customer_api = Api(customer_api_bp)



@customer_api_bp.route('/', methods=['POST'])
@auth_token_required
@outlet_key_required
def create_customer():
    customer_data_in_json   = request.get_json()
    register_customer_form  = CustomerDetailsForm(ImmutableMultiDict(customer_data_in_json))
    
    logger.debug('create_customer: customer_data_in_json=%s', customer_data_in_json)
    
    try:
        if register_customer_form.validate():
            logger.debug('customer registration input is valid')
            db_client = create_db_client(caller_info="create_customer")
            
            is_email_used           = False
            is_mobile_phone_used    = False
            customer_is_exist       = False
            created_customer        = None
            created_user_acct       = None
            
            with db_client.context():
                merchant_acct   = MerchantAcct.fetch(session.get('acct_id'))
                outlet          = Outlet.fetch(request.headers.get('x-outlet-key'))
                
                email           = customer_data_in_json.get('email')
                mobile_phone    = customer_data_in_json.get('mobile_phone')
                
                if is_not_empty(email):
                    created_user_acct = User.get_by_email(email)
                    
                    if created_user_acct:
                        is_email_used = True
                
                if is_not_empty(mobile_phone):
                    mobile_phone = mobile_phone.replace(" ", "")
                    created_user_acct = User.get_by_mobile_phone(mobile_phone)
                    
                    if created_user_acct:
                        is_mobile_phone_used = True
                
                
                logger.debug('is_email_used=%s', is_email_used)
                logger.debug('is_mobile_phone_used=%s', is_mobile_phone_used)
                
                if merchant_acct and outlet:
                        
                    logger.debug('merchant_acct.key_in_str=%s', merchant_acct.key_in_str)
                    logger.debug('outlet.merchant_acct_key=%s', outlet.merchant_acct_key)
                    
                    if merchant_acct.key_in_str == outlet.merchant_acct_key: 
                        logger.debug('Valid granted outlet key for merchant acct')
                        birth_date              = customer_data_in_json.get('birth_date')
                        
                        if is_not_empty(birth_date):
                            birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
                        
                        logger.debug('birth_date=%s', birth_date)
                        
                        if is_email_used:
                            created_customer = Customer.get_by_email(email)
                            
                        elif is_mobile_phone_used:
                            created_customer = Customer.get_by_mobile_phone(mobile_phone)    
                        
                        if is_email_used or is_mobile_phone_used:
                            if created_customer is None:
                                logger.debug('User account have been created, but customer account is not yet created')
                                
                                created_user_acct = User.update(created_user_acct,
                                                                name                    = customer_data_in_json.get('name'), 
                                                                email                   = customer_data_in_json.get('email'), 
                                                                gender                  = customer_data_in_json.get('gender'),
                                                                birth_date              = birth_date,
                                                                mobile_phone            = customer_data_in_json.get('gender'), 
                                                                password                = customer_data_in_json.get('password'),
                                                                )
                                
                                created_customer        = Customer.create_from_user(merchant_acct, outlet, created_user_acct, customer_data_in_json.get('merchant_reference_code'))
                            
                            else:
                                customer_is_exist = True
                                logger.warn('Customer account using same email or mobile phone have been created')
                        else:
                            created_customer        = Customer.create(merchant_acct = merchant_acct, 
                                                            outlet                  = outlet, 
                                                            name                    = customer_data_in_json.get('name'), 
                                                            email                   = customer_data_in_json.get('email'), 
                                                            gender                  = customer_data_in_json.get('gender'),
                                                            birth_date              = birth_date,
                                                            mobile_phone            = mobile_phone, 
                                                            merchant_reference_code = customer_data_in_json.get('merchant_reference_code'), 
                                                            password                = customer_data_in_json.get('password'),
                                                            )
                        logger.debug('created_customer=%s', created_customer)
                    else:
                        logger.warn('Invalid granted outlet key')
                else:
                    logger.warn('Invalid granted outlet key')
                
                if customer_is_exist:
                    if is_email_used==True:
                        return create_rest_message('Email have been taken', status_code=StatusCode.BAD_REQUEST)
                    
                    elif is_mobile_phone_used==True:
                        return create_rest_message('Mobile phone have been taken', status_code=StatusCode.BAD_REQUEST)
                    
                else:
                    if created_customer:
                        return create_rest_message(status_code=StatusCode.OK, reference_code=created_customer.reference_code)
                    else:
                        return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
        else:
            logger.warn('customer registration input is invalid')
            error_message = register_customer_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
    except:
        logger.error('Fail to register customer due to %s', get_tracelog())
        
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)


        

@customer_api_bp.route('/<ref_code>', methods=['GET'])
@auth_token_required
def read_customer(ref_code):
    
    logger.debug('ref_code=%s', ref_code)
    
    if is_not_empty(ref_code):
        db_client = create_db_client(caller_info="read_customer")
        with db_client.context():
            customer = Customer.get_by_reference_code(ref_code)
        
        if customer:
        
            customer_property_list = ['name', 'email', 'mobile_phone', 'gender', 'birth_date', 'merchant_reference_code']
            
            return jsonify(customer.to_dict(dict_properties=customer_property_list, show_key=False))
            
        else:
            logger.warn('Customer with reference code (%s) is not found', ref_code)
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)


@customer_api_bp.route('/<ref_code>', methods=['PUT'])
@auth_token_required
def update_customer(ref_code):
    customer_data_in_json   = request.get_json()
    updating_customer_form  = CustomerDetailsForm(ImmutableMultiDict(customer_data_in_json))
    
    logger.debug('update_customer: customer_data_in_json=%s', customer_data_in_json)
    
    try:
        if updating_customer_form.validate():
            logger.debug('customer update input is valid')
            db_client = create_db_client(caller_info="update_customer")
            
            is_email_used                           = False
            is_mobile_phone_used                    = False
            customer_is_exist                       = False
            updating_customer                       = None
            checking_user_acct                      = None
            is_customer_email_changed               = False
            is_customer_mobile_phone_changed        = False
            is_used_email_same_user_acct            = False
            is_used_mobile_phone_same_user_acct     = False
            
            with db_client.context():
                email               = customer_data_in_json.get('email')
                mobile_phone        = customer_data_in_json.get('mobile_phone')
                
                if mobile_phone:
                    mobile_phone = mobile_phone.replace(" ", "")
                
                updating_customer   = Customer.get_by_reference_code(ref_code)
                
                if updating_customer:
                    customer_is_exist = True
                    is_customer_email_changed           = updating_customer.email!=email
                    is_customer_mobile_phone_changed    = updating_customer.mobile_phone!=mobile_phone
                
                if is_customer_email_changed:
                    if is_not_empty(email):
                        checking_user_acct = User.get_by_email(email)
                        
                        if checking_user_acct:
                            is_email_used = True
                            is_used_email_same_user_acct = checking_user_acct.key_in_str == updating_customer.registered_user_acct_key
                        
                if is_customer_mobile_phone_changed:
                    if is_not_empty(mobile_phone):
                        checking_user_acct = User.get_by_mobile_phone(mobile_phone)
                    
                        if checking_user_acct:
                            is_mobile_phone_used = True
                            is_used_mobile_phone_same_user_acct = checking_user_acct.key_in_str == updating_customer.registered_user_acct_key
                                
                logger.debug('is_customer_email_changed=%s', is_customer_email_changed)
                logger.debug('is_customer_mobile_phone_changed=%s', is_customer_mobile_phone_changed)
                logger.debug('is_email_used=%s', is_email_used)
                logger.debug('is_mobile_phone_used=%s', is_mobile_phone_used)
                logger.debug('is_used_email_same_user_acct=%s', is_used_email_same_user_acct)
                logger.debug('is_used_mobile_phone_same_user_acct=%s', is_used_mobile_phone_same_user_acct)
                
                if is_email_used==False and is_mobile_phone_used==False:
                    logger.debug('Going to update customer details') 
                    
                    birth_date              = customer_data_in_json.get('birth_date')
                        
                    if is_not_empty(birth_date):
                        birth_date = datetime.strptime(birth_date, '%d/%m/%Y')
                    
                    logger.debug('birth_date=%s', birth_date)
                    
                    Customer.update(customer=updating_customer, 
                                    name                    = customer_data_in_json.get('name'), 
                                    email                   = customer_data_in_json.get('email'), 
                                    gender                  = customer_data_in_json.get('gender'),
                                    birth_date              = birth_date,
                                    mobile_phone            = mobile_phone, 
                                    password                = customer_data_in_json.get('password'),
                                    )
                
                
                if customer_is_exist:
                    if is_email_used==True:
                        return create_rest_message('Email have been taken', status_code=StatusCode.BAD_REQUEST)
                    
                    elif is_mobile_phone_used==True:
                        return create_rest_message('Mobile phone have been taken', status_code=StatusCode.BAD_REQUEST)
                    else:
                        return create_rest_message(status_code=StatusCode.OK)
                else:
                    return create_rest_message(gettext('Customer is not exis'), status_code=StatusCode.BAD_REQUEST)
            
        else:
            logger.warn('customer registration input is invalid')
            error_message = updating_customer_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
    except:
        logger.error('Fail to register customer due to %s', get_tracelog())
        
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)
        
@customer_api_bp.route('/<ref_code>', methods=['DELETE'])
@auth_token_required 
def delete_customer(ref_code):
    if is_not_empty(ref_code):
        is_found = False
        db_client = create_db_client(caller_info="read_customer")
        with db_client.context():
            customer = Customer.get_by_reference_code(ref_code) 
            if customer:
                customer.delete()
                is_found = True
        
        if is_found:
            return create_rest_message(status_code=StatusCode.NO_CONTENT)
        else:
            return create_rest_message(gettext('Customer is not exis'), status_code=StatusCode.BAD_REQUEST)
    else:
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)        





#customer_api.add_resource(CustomerResource)    