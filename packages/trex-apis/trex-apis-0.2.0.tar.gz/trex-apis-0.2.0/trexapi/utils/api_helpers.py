'''
Created on 8 Jul 2021

@author: jacklok
'''
from flask import request
import logging
from trexlib.utils.crypto_util import decrypt_json

logger = logging.getLogger('helper')


def get_logged_in_api_username():
    auth_token  = request.headers.get('x-auth-token')
    username    = None
    try:
        auth_details_json = decrypt_json(auth_token)
    except:
        logger.error('Failed to decrypt authenticated token')
        
    logger.debug('auth_details_json=%s', auth_details_json)
    
    if auth_details_json:
        username = auth_details_json.get('username')
        
    return username
