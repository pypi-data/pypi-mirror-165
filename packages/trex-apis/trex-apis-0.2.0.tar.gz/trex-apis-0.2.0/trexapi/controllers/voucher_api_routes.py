'''
Created on 19 Jul 2021

@author: jacklok
'''

from flask import Blueprint, request, session 
import logging
from trexlib.utils.log_util import get_tracelog
from trexmodel.utils.model.model_util import create_db_client
from datetime import datetime, timedelta
from trexapi.decorators.api_decorators import auth_token_required
from trexlib.utils.string_util import is_not_empty, is_empty
from trexmodel.models.datastore.customer_models import Customer
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.merchant_models import Outlet,\
    MerchantUser
from trexapi.forms.reward_api_forms import VoucherRedeemForm
from werkzeug.datastructures import ImmutableMultiDict
import json
from trexapi.utils.api_helpers import get_logged_in_api_username
from trexmodel.models.datastore.voucher_models import MerchantVoucher
from trexmodel.models.datastore.reward_models import CustomerEntitledVoucher

from trexmodel.models.datastore.redeem_models import CustomerRedemption
from trexanalytics.bigquery_upstream_data_config import create_merchant_customer_redemption_upstream_for_merchant
from trexmodel import program_conf
from trexapi import conf

logger = logging.getLogger('api')


voucher_api_bp = Blueprint('voucher_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/vouchers')

logger = logging.getLogger('api')

@voucher_api_bp.route('/<redeem_code>', methods=['GET'])
@auth_token_required
def read_voucher(redeem_code):
    if is_not_empty(redeem_code):
        voucher_details = None
        db_client = create_db_client(caller_info="read_reward")
        with db_client.context():
            customer_voucher    = CustomerEntitledVoucher.get_by_redeem_code(redeem_code)
            if customer_voucher:
                merchant_voucher    = MerchantVoucher.fetch(customer_voucher.entitled_voucher_key)
                voucher_conf        = merchant_voucher.configuration
                if merchant_voucher.configuration:
                    if isinstance(merchant_voucher.configuration, str):
                        voucher_conf = json.loads(merchant_voucher.configuration)
                else:
                    voucher_conf = {}
                voucher_details = {
                                    'label'                 : merchant_voucher.label,
                                    'desc'                  : merchant_voucher.desc,
                                    'terms_and_conditions'  : merchant_voucher.terms_and_conditions,
                                    'configuration'         : voucher_conf,
                                    'image_url'             : merchant_voucher.image_public_url,
                                    'effective_date'        : customer_voucher.effective_date.strftime('%d-%m-%Y'),
                                    'expiry_date'           : customer_voucher.expiry_date.strftime('%d-%m-%Y'),
                                    'redeem_code'           : redeem_code,
                                    'is_redeemed'           : customer_voucher.is_used,
                                    }
                
        
        if voucher_details is None:
            return create_rest_message('Invalid voucher redeem code', status_code=StatusCode.BAD_REQUEST)
        else:
            return create_rest_message(voucher_details=voucher_details, status_code=StatusCode.OK)
    else:
        return create_rest_message('Voucher redeem code is required', status_code=StatusCode.BAD_REQUEST) 
    
@voucher_api_bp.route('/<reference_code>/redeem', methods=['post'])
@auth_token_required
def redeem_voucher(reference_code):
    
    redeem_voucher_data_in_json   = request.get_json()
    
    redeem_voucher_form = VoucherRedeemForm(ImmutableMultiDict(redeem_voucher_data_in_json))
    if is_empty(reference_code):
        return create_rest_message('Customer reference code is required', status_code=StatusCode.BAD_REQUEST)
    else:
        if redeem_voucher_form.validate():
        
            __redeem_code_list    = redeem_voucher_data_in_json.get('redeem_code')
            invoice_id          = redeem_voucher_form.invoice_id.data
            remarks             = redeem_voucher_form.remarks.data
            redeemed_datetime   = redeem_voucher_form.redeem_datetime.data
            merchant_acct       = None
            
            logger.debug('redeem_code_list=%s', __redeem_code_list)
            logger.debug('redeemed_datetime=%s', redeemed_datetime)
            
            
            if __redeem_code_list:
                #redeem_code_list = redeem_code_list.split(',')
                redeem_code_list = []
                for c in __redeem_code_list:
                    redeem_code_list.append(c.strip())
                
                db_client = create_db_client(caller_info="redeem_voucher")
                with db_client.context():
                    redeemed_by_outlet      = Outlet.fetch(request.headers.get('x-outlet-key'))
                    merchant_acct           = redeemed_by_outlet.merchant_acct_entity
                
                redeem_datetime_in_gmt      = redeem_voucher_form.redeem_datetime.data
                merchant_username           = get_logged_in_api_username()
                
                
                if redeem_datetime_in_gmt:
                    redeem_datetime    =  redeem_datetime_in_gmt - timedelta(hours=merchant_acct.gmt_hour)
                    
                    now                  = datetime.utcnow()
                    if redeem_datetime > now:
                        return create_rest_message('Redeem datetime cannot be future', status_code=StatusCode.BAD_REQUEST)
                
                
                
                already_redeemed_list                               = []
                to_redeem_voucher_keys_list                         = []
                customer                                            = None
                found_not_belog_cusotmer_voucher_redeem_code_list   = []
                found_not_valid_redeem_code_list                    = []
                
                with db_client.context():
                    merchant_username       = get_logged_in_api_username()
                    redeemed_by             = MerchantUser.get_by_username(merchant_username)
                    customer                = Customer.get_by_reference_code(reference_code)
                    customer_key            = customer.key_in_str
                    
                    for redeem_code in redeem_code_list:
                        customer_voucher    = CustomerEntitledVoucher.get_by_redeem_code(redeem_code)
                        if customer_voucher:
                            if customer_voucher.entitled_customer_key == customer_key:
                                if customer_voucher.is_redeemed:
                                    already_redeemed_list.append(redeem_code)
                                else:
                                    to_redeem_voucher_keys_list.append(customer_voucher.key_in_str)
                            else:
                                found_not_belog_cusotmer_voucher_redeem_code_list.append(redeem_code)
                        else:
                            found_not_valid_redeem_code_list.append(redeem_code)
                
                if found_not_valid_redeem_code_list:
                    return create_rest_message("Voucher ({redeem_codes_list}) is not valid".format(redeem_codes_list=",".join(found_not_valid_redeem_code_list)), 
                                               status_code=StatusCode.BAD_REQUEST)            
                elif found_not_belog_cusotmer_voucher_redeem_code_list:
                    return create_rest_message("Voucher ({redeem_codes_list}) is not belong to customer".format(redeem_codes_list=",".join(found_not_belog_cusotmer_voucher_redeem_code_list)), 
                                               status_code=StatusCode.BAD_REQUEST)
                                    
                elif already_redeemed_list:
                    return create_rest_message("Voucher ({redeem_codes_list}) have been redeemed before,  thus it is not allow to redeem again".format(redeem_codes_list=",".join(already_redeemed_list)), 
                                               status_code=StatusCode.BAD_REQUEST)
                else:
                    if to_redeem_voucher_keys_list:
                        with db_client.context():
                            if to_redeem_voucher_keys_list:
                                
                                customer_redemption = CustomerRedemption.create(customer, program_conf.REWARD_FORMAT_VOUCHER , 1, redeemed_by_outlet, 
                                          redeemed_voucher_keys_list    = to_redeem_voucher_keys_list, 
                                          redeemed_by                   = redeemed_by, 
                                          redeemed_datetime             = redeemed_datetime,
                                          invoice_id                    = invoice_id,
                                          remarks                       = remarks,
                                          )
                                
                                logger.debug('customer_redemption=%s', customer_redemption)
                                
                
                            if customer_redemption:
                                create_merchant_customer_redemption_upstream_for_merchant(customer_redemption, streamed_datetime=redeemed_datetime)
                        
                        if customer_redemption:        
                            return create_rest_message(transaction_id = customer_redemption.transaction_id, status_code=StatusCode.OK)
                        else:
                            return create_rest_message("Failed to redeem voucher", status_code=StatusCode.BAD_REQUEST)
                    else:
                        return create_rest_message('Voucher redeem code is required', status_code=StatusCode.BAD_REQUEST)
        
        else:
            logger.warn('redeem voucher data input is invalid')
            error_message = redeem_voucher_form.create_rest_return_error_message()
                
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
             
    
    