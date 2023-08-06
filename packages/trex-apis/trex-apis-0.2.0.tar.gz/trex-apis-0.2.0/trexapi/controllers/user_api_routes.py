'''
Created on 7 Jul 2021

@author: jacklok
'''

from flask import Blueprint, request
import logging
from trexlib.utils.log_util import get_tracelog
from trexmodel.utils.model.model_util import create_db_client
from datetime import datetime
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.user_models import User
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from werkzeug.datastructures import ImmutableMultiDict
from trexapi.forms.user_api_forms import UserRegistrationForm
from trexapi.conf import APPLICATION_NAME, APPLICATION_BASE_URL
from trexmail.email_helper import trigger_send_email

user_api_bp = Blueprint('user_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/users')

logger = logging.getLogger('api')


@user_api_bp.route('/register', methods=['POST'])
def user_register():
    logger.debug('user_register: ---user_register---')
    
    try:
        user_data_in_json   = request.get_json()
        logger.debug('user_register: user_data_in_json=%s', user_data_in_json)
        
        register_user_form  = UserRegistrationForm(ImmutableMultiDict(user_data_in_json))
        if register_user_form.validate():
            logger.debug('user_register:  registration input is valid')
            db_client = create_db_client(caller_info="user_register")
            
            registered_user_acct    = None
            
            with db_client.context():
                email           = register_user_form.email.data
                name            = register_user_form.name.data
                mobile_phone    = register_user_form.mobile_phone.data
                password        = register_user_form.password.data
                
                checking_registered_user_acct = User.get_by_email(email)
                if checking_registered_user_acct is None:
                    if is_not_empty(mobile_phone):
                        checking_registered_user_acct = User.get_by_mobile_phone(mobile_phone)
                        if checking_registered_user_acct is None:
                            registered_user_acct = User.create(name=name, email=email, mobile_phone=mobile_phone, password=password, create_email_vc=True, create_mobile_phone_vc=True)
                            logger.debug('new registered_user_acct=%s', registered_user_acct)
                        else:
                            return create_rest_message('Mobile Phone have been taken', status_code=StatusCode.BAD_REQUEST)
                    else:
                        registered_user_acct = User.create(name=name, email=email, mobile_phone=mobile_phone, password=password, create_email_vc=True, create_mobile_phone_vc=True)
                        logger.debug('new registered_user_acct=%s', registered_user_acct)
                        
                else:
                    return create_rest_message('Email have been taken', status_code=StatusCode.BAD_REQUEST)
                
                                
            if registered_user_acct is not None:
                
                send_email_verification_code_email(registered_user_acct)
                
                
                return create_rest_message(status_code=StatusCode.OK, 
                                           reference_code=registered_user_acct.reference_code,
                                           email_vc_expiry_datetime             = str(registered_user_acct.email_vc_expiry_datetime),
                                           mobile_phone_vc_expiry_datetime      = str(registered_user_acct.mobile_phone_vc_expiry_datetime),
                                           )
            else:
                return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
        else:
            logger.warn('user_register: user registration input is invalid')
            error_message = register_user_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
            
    except:
        logger.error('user_register: Fail to register user due to %s', get_tracelog())
        
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)


@user_api_bp.route('/auth', methods=['POST'])
def auth_user():
    
    user_data_in_json   = request.get_json()
    email               = user_data_in_json.get('email')
    password            = user_data_in_json.get('password')
    
    if is_not_empty(email) and is_not_empty(password):
        db_client = create_db_client(caller_info="auth_user")
        user_acct = None
        with db_client.context():
            user_acct = User.get_by_email(email)
        
        if user_acct:
            logger.debug('auth_user: found user account by email=%s', email)    
            logger.debug('auth_user: found user account by password=%s', password)
            if user_acct.is_valid_password(password):
                return create_rest_message(status_code=StatusCode.OK, 
                                           reference_code                       = user_acct.reference_code, 
                                           name                                 = user_acct.name, 
                                           is_email_verified                    = user_acct.is_email_verified, 
                                           is_mobile_phone_verified             = user_acct.is_mobile_phone_verified,
                                           email_vc_expiry_datetime             = str(user_acct.email_vc_expiry_datetime),
                                           mobile_phone_vc_expiry_datetime      = str(user_acct.mobile_phone_vc_expiry_datetime),
                                           )
            
            else:
                logger.warn('auth_user: user password is invalid')
                return create_rest_message('User email or password is not match', status_code=StatusCode.BAD_REQUEST)
            
        else:
            return create_rest_message('User email or password is not match', status_code=StatusCode.BAD_REQUEST)
            
    else:
        logger.warn('auth_user: user verify input is invalid')
        return create_rest_message('Missing email or password', status_code=StatusCode.BAD_REQUEST)
    
@user_api_bp.route('/verify-email', methods=['POST'])
def verify_email_account():
    
    user_data_in_json   = request.get_json()
    email               = user_data_in_json.get('email')
    verification_code   = user_data_in_json.get('verification_code')
    
    if is_not_empty(email) and is_not_empty(verification_code):
        db_client = create_db_client(caller_info="verify_email_account")
        user_acct = None
        
        logger.debug('verify_email_account: going to find user account by email=%s', email)
        
        with db_client.context():
            user_acct = User.get_by_email(email)
        
        if user_acct:
            logger.debug('verify_email_account: found user account by email=%s', email)    
            if user_acct.email_vc==verification_code:
                is_within_seconds = (user_acct.email_vc_expiry_datetime - datetime.now()).seconds
                if is_within_seconds>0:
                    with db_client.context():
                        user_acct.mark_email_verified()
                    return create_rest_message(status_code=StatusCode.OK)
                else:
                    return create_rest_message("Verification Code is expired already", status_code=StatusCode.BAD_REQUEST)
            
            else:
                logger.warn('verify_email_account: verification code is invalid')
                return create_rest_message("Invalid verification code", status_code=StatusCode.BAD_REQUEST)
            
        else:
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        logger.warn('verify_email_account: user verify input is invalid')
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)    
    
@user_api_bp.route('/verify-email', methods=['POST'])
def verify_mobile_phone_account():
    
    user_data_in_json   = request.get_json()
    mobile_phone        = user_data_in_json.get('mobile_phone')
    verification_code   = user_data_in_json.get('verification_code')
    
    if is_not_empty(mobile_phone) and is_not_empty(verification_code):
        db_client = create_db_client(caller_info="verify_mobile_phone_account")
        user_acct = None
        with db_client.context():
            user_acct = User.get_by_mobile_phone(mobile_phone)
        
        if user_acct:
            logger.debug('verify_mobile_phone_account: found user account by mobile_phone=%s', mobile_phone)    
            if user_acct.mobile_phone_vc==verification_code:
                is_within_seconds = (user_acct.mobile_phone_vc_expiry_datetime - datetime.now()).seconds
                if is_within_seconds>0:
                    with db_client.context():
                        user_acct.mark_email_verified()
                    return create_rest_message(status_code=StatusCode.OK)
                else:
                    return create_rest_message("Verification Code is expired already", status_code=StatusCode.BAD_REQUEST)
            
            else:
                logger.warn('verify_mobile_phone_account: verification code is invalid')
                return create_rest_message("Invalid verification code", status_code=StatusCode.BAD_REQUEST)
            
        else:
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        logger.warn('verify_mobile_phone_account: user verify input is invalid')
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)        
    
@user_api_bp.route('/<reference_code>', methods=['GET'])
def read_user_acct(reference_code):
    
    if is_not_empty(reference_code):
        db_client = create_db_client(caller_info="read_user_acct")
        user_acct = None
        with db_client.context():
            user_acct = User.get_by_reference_code(reference_code)
        
        if user_acct:
            logger.debug('verify_user: found user account by reference_code=%s', reference_code)    
            is_email_verified           = user_acct.is_email_verified
            is_mobile_phone_verified    = user_acct.is_email_verified
            
            email_vc_expiry_datetime             = None
            mobile_phone_vc_expiry_datetime      = None
            
            if is_email_verified == False:
                #vg_generated_datetime = user_acct.vg_generated_datetime.strftime(user_acct.vg_generated_datetime, '%d/%m/%Y, %H:%M:%S')
                email_vc_expiry_datetime = str(user_acct.email_vc_expiry_datetime)
                
            if is_mobile_phone_verified == False:
                #vg_generated_datetime = user_acct.vg_generated_datetime.strftime(user_acct.vg_generated_datetime, '%d/%m/%Y, %H:%M:%S')
                mobile_phone_vc_expiry_datetime = str(user_acct.mobile_phone_vc_expiry_datetime)    
                
            return create_rest_message(status_code=StatusCode.OK, 
                                       reference_code                       = user_acct.reference_code, 
                                       name                                 = user_acct.name, 
                                       email                                = user_acct.email, 
                                       is_email_verified                    = is_email_verified,
                                       is_mobile_phone_verified             = is_mobile_phone_verified,
                                       email_vc_expiry_datetime             = email_vc_expiry_datetime,
                                       mobile_phone_vc_expiry_datetime      = mobile_phone_vc_expiry_datetime,
                                       )
        else:
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        logger.warn('verify_user: user verify input is invalid')
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)    
    
@user_api_bp.route('/reset-email-vc', methods=['PUT'])
def reset_email_verification_code():
    email = request.args.get('email') or request.form.get('email') or request.json.get('email')
    
    logger.debug('reset_email_verification_code: going to reset email verification code by email=%s', email)
    
    if is_not_empty(email):
        db_client = create_db_client(caller_info="reset_email_verification_code")
        user_acct = None
        
        
        
        with db_client.context():
            user_acct = User.get_by_email(email)
        
        if user_acct:
            logger.debug('reset_email_verification_code: found user account by email=%s', email)    
            is_email_verified           = user_acct.is_email_verified
            
            logger.debug('reset_email_verification_code: is_email_verified=%s', is_email_verified)
            
            email_vc_expiry_datetime = None
            
            with db_client.context():
                user_acct.reset_email_vc()
            email_vc_expiry_datetime = user_acct.email_vc_expiry_datetime
                
                #send_email_verification_code_email(user_acct)
            
            logger.debug('reset_email_verification_code: email_vc_expiry_datetime=%s', email_vc_expiry_datetime)
            logger.debug('reset_email_verification_code: verification code=%s', user_acct.email_vc)
                
            return create_rest_message(status_code=StatusCode.OK, 
                                       email_vc_expiry_datetime          = str(email_vc_expiry_datetime),
                                       
                                       )
        else:
            return create_rest_message('Cannot find user by email %s' % email, status_code=StatusCode.BAD_REQUEST)
            
    else:
        logger.warn('reset_email_verification_code: reference code is invalid')
        return create_rest_message(status_code=StatusCode.BAD_REQUEST) 
    
@user_api_bp.route('/reset-mobile-phone-vc', methods=['PUT'])
def reset_mobile_phone_verification_code():
    mobile_phone = request.args.get('mobile_phone') or request.form.get('mobile_phone') or request.json.get('mobile_phone')
    if is_not_empty(mobile_phone):
        db_client = create_db_client(caller_info="reset_verification_code")
        user_acct = None
        with db_client.context():
            user_acct = User.get_by_mobile_phone(mobile_phone)
        
        if user_acct:
            logger.debug('reset_mobile_phone_verification_code: found user account by mobile_phone=%s', mobile_phone)    
            is_mobile_phone_verified           = user_acct.is_mobile_phone_verified
            mobile_phone_vc_expiry_datetime = None
            
            with db_client.context():
                user_acct.reset_mobile_phone_vc()
                
            logger.debug('reset_mobile_phone_verification_code: mobile_phone_vc_expiry_datetime=%s', mobile_phone_vc_expiry_datetime)
            logger.debug('reset_mobile_phone_verification_code: verification code=%s', user_acct.mobile_phone_vc)   
            return create_rest_message(status_code=StatusCode.OK, 
                                       mobile_phone_vc_expiry_datetime   = str(mobile_phone_vc_expiry_datetime),
                                       
                                       )
        else:
            return create_rest_message(status_code=StatusCode.BAD_REQUEST)
            
    else:
        logger.warn('reset_mobile_phone_verification_code: mobile phone is invalid')
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)  
    
@user_api_bp.route('/request-reset-password', methods=['POST'])
def request_reset_password_post():
    email = request.args.get('email') or request.form.get('email') or request.json.get('email')
    
    logger.debug('reset_password_request_post: going to reset email verification code by email=%s', email)
    
    if is_not_empty(email):
        db_client = create_db_client(caller_info="reset_email_verification_code")
        user_acct = None
        
        
        
        with db_client.context():
            user_acct = User.get_by_email(email)
        
        if user_acct:
            logger.debug('reset_password_request_post: found user account by email=%s', email)    
            is_email_verified           = user_acct.is_email_verified
            
            logger.debug('reset_email_verification_code: is_email_verified=%s', is_email_verified)
            
            if is_email_verified:
                with db_client.context():
                    user_acct.reset_password_request()
                
                send_reset_password_request_email(user_acct)
                
            return create_rest_message(status_code=StatusCode.OK
                                       
                                       )
        else:
            return create_rest_message('Cannot find user by email %s' % email, status_code=StatusCode.BAD_REQUEST)
            
    else:
        logger.warn('reset_password_post: email is invalid')
        return create_rest_message(status_code=StatusCode.BAD_REQUEST)                 


def send_email_verification_code_email(user_acct):
    message = '''
                Hi {name},
                
                
                Thanks for signing up with {application_name}!
                Your account has been created, you can login with email {email} in future. 
                
                Just one more step to get started! Please enter below code to activate your account .
                
                
                {verification_code}
                
                
                The code will be expired after 30 minutes.
                
                Cheers,
                {application_name} Team
                
                
                ***Please do not reply to this email. This is an auto-generated email.***
    
            '''.format(name=user_acct.name, email=user_acct.email, verification_code=user_acct.email_vc, application_name=APPLICATION_NAME)
    
    subject      = 'Email Verification from {application_name}'.format(application_name=APPLICATION_NAME)
    
    trigger_send_email(recipient_address = user_acct.email, subject=subject, message=message)
    '''
    send_email(sender           = DEFAULT_SENDER, 
                   to_address   = [user_acct.email], 
                   subject      = subject, 
                   body         = message,
                   app          = current_app
                   )
    '''
def send_reset_password_request_email(user_acct):
    reset_password_link = '{base_url}/user/reset-password-request/{request_reset_password_token}'.format(base_url=APPLICATION_BASE_URL, request_reset_password_token=user_acct.request_reset_password_token)
    
    message = '''
                Hi {name},
                
                
                Forgot your password? No worries.
                We received your request to reset the password for your account. 
                
                Just one more step to reset the password, please click the below link:
                
                
                {reset_password_link}
                
                
                
                Or copy and paste the URL into your web browser.
                
                Cheers,
                {application_name} Team
                
                
                ***Please do not reply to this email. This is an auto-generated email.***
    
            '''.format(name=user_acct.name, email=user_acct.email, 
                       reset_password_link=reset_password_link, 
                       application_name=APPLICATION_NAME)
    
    subject = 'Request to reset password to {application_name}'.format(application_name=APPLICATION_NAME)
            
    trigger_send_email(recipient_address = user_acct.email, subject=subject, message=message)
    '''
    send_email(sender           = DEFAULT_SENDER, 
                   to_address   = [user_acct.email], 
                   subject      = subject, 
                   body         = message,
                   app          = current_app
                   )    
    '''               