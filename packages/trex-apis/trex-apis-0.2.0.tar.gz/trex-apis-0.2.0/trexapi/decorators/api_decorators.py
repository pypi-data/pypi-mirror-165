'''
Created on 1 Jul 2021

@author: jacklok
'''
from functools import wraps
from flask import request, session, abort
from trexlib.utils.string_util import is_not_empty
from trexlib.utils.crypto_util import decrypt_json
import logging
from datetime import datetime

logger = logging.getLogger('decorator')


def auth_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('x-auth-token')
            
        logger.debug('auth_token=%s', auth_token)
        
        if is_not_empty(auth_token):
            try:
                auth_details_json = decrypt_json(auth_token)
            except:
                return ("Authenticated token is not valid", 401)
            
            logger.debug('auth_details_json=%s', auth_details_json)
            
            if auth_details_json:
                expiry_datetime = auth_details_json.get('expiry_datetime')
                if is_not_empty(expiry_datetime):
                    expiry_datetime = datetime.strptime(expiry_datetime, '%d-%m-%Y %H:%M:%S')
                    logger.debug('expiry_datetime=%s', expiry_datetime)
                    
                    now             = datetime.now()
                    if now < expiry_datetime: 
                        logger.debug('auth token is still valid')
                        return f(*args, **kwargs)
                    else:
                        logger.debug('auth token is not logger valid')
                        
                        return ("Authenticated token is expired", 401)
                
        
        return ("Authenticated token is required", 401)

    return decorated_function

def outlet_key_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        outlet_key = request.headers.get('x-outlet-key')
            
        logger.debug('outlet_key=%s', outlet_key)
        
        if is_not_empty(outlet_key):
            logger.debug('Going to execute')
            return f(*args, **kwargs)
            
        
        return ("Outlet Key is required", 401)

    return decorated_function
