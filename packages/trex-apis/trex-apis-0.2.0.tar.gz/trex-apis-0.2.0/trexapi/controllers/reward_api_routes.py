'''
Created on 14 Jul 2021

@author: jacklok
'''

from flask import Blueprint, request, session, jsonify 
from flask_restful import abort
import logging
from trexlib.utils.log_util import get_tracelog
from flask_restful import Api
from trexmodel.utils.model.model_util import create_db_client
#from flask.json import jsonify
from datetime import datetime, timedelta
from trexapi.decorators.api_decorators import auth_token_required,\
    outlet_key_required
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.customer_models import Customer
from trexmodel.models.datastore.user_models import User
from trexadmin.libs.http import create_rest_message
from trexadmin.libs.http import StatusCode
from trexmodel.models.datastore.merchant_models import Outlet,\
    MerchantAcct, MerchantUser
from trexapi.forms.reward_api_forms import GiveRewardTransactionForm, RedeemRewardTransactionForm
from werkzeug.datastructures import ImmutableMultiDict
import gettext
from trexmodel.models.datastore.transaction_models import CustomerTransaction
from trexadmin.libs.app.utils.reward_transaction_helper import create_sales_transaction,\
    redeem_reward_transaction
from trexapi.utils.api_helpers import get_logged_in_api_username
from trexmodel.models.datastore.voucher_models import MerchantVoucher
from trexapi import conf

logger = logging.getLogger('api')


reward_api_bp = Blueprint('reward_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/reward')

logger = logging.getLogger('api')


@reward_api_bp.route('/<reference_code>', methods=['GET'])
@auth_token_required
def read_reward(reference_code):
    logger.debug('reference_code=%s', reference_code)
    
    if is_not_empty(reference_code):
        db_client = create_db_client(caller_info="read_reward")
        with db_client.context():
            customer   = Customer.get_by_reference_code(reference_code)
            if customer:
                
                all_reward_summary = {}
                
                for k, v in customer.reward_summary.items():
                    all_reward_summary[k] = v.get('amount')
                
                all_voucher_list = []
                    
                for k, v in customer.entitled_voucher_summary.items():
                    for redeem_info in v.get('redeem_info_list'):
                        all_voucher_list.append({
                                            'label'         : v.get('label'),
                                            'image_url'     : v.get('image_url'),
                                            'label'         : v.get('label'),
                                            'redeem_code'   : redeem_info.get('redeem_code'),
                                            'effective_date': redeem_info.get('effective_date'),
                                            'expiry_date'   : redeem_info.get('expiry_date'),
                                            })
                '''
                if all_voucher_list:        
                    all_reward_summary['vouchers'] = all_voucher_list        
                '''
                        
                return create_rest_message(
                                            entitled_reward_summary  = all_reward_summary, 
                                            status_code=StatusCode.OK
                                            )
            
        if customer is None:
            return create_rest_message('Reference code is invalid', status_code=StatusCode.BAD_REQUEST)
            
    else:
        return create_rest_message('Reference code is required', status_code=StatusCode.BAD_REQUEST)
    

@reward_api_bp.route('/<reference_code>/give', methods=['POST'])
@auth_token_required
@outlet_key_required
def give_reward(reference_code):
    
    logger.debug('reference_code=%s', reference_code)
    
    if is_not_empty(reference_code):
    
        transaction_data_in_json   = request.get_json()
        
        logger.debug('transaction_data_in_json=%s', transaction_data_in_json)
        
        reward_transaction_form = GiveRewardTransactionForm(ImmutableMultiDict(transaction_data_in_json))
        
        if reward_transaction_form.validate():
            logger.debug('reward transaction data is valid')
            
            sales_amount        = float(reward_transaction_form.sales_amount.data)
            tax_amount          = reward_transaction_form.tax_amount.data
            invoice_id          = reward_transaction_form.invoice_id.data
            remarks             = reward_transaction_form.remarks.data
            invoice_details     = transaction_data_in_json.get('invoice_details')
            transact_datetime   = None
            
            if tax_amount is None:
                tax_amount = .0
            else:
                tax_amount = float(tax_amount)
             
            logger.debug('sales_amount=%s', sales_amount)
            logger.debug('tax_amount=%s', tax_amount)
            logger.debug('invoice_id=%s', invoice_id)
            logger.debug('remarks=%s', remarks)
            logger.debug('invoice_details=%s', invoice_details)
            
            db_client = create_db_client(caller_info="givea_reward")
            
            if is_not_empty(invoice_id):
                with db_client.context():
                    check_transaction_by_invoice_id = CustomerTransaction.get_by_invoice_id(invoice_id)
            
            if check_transaction_by_invoice_id:
                return create_rest_message("The invoice id have been taken", status_code=StatusCode.BAD_REQUEST)
            else:
                transact_datetime_in_gmt    = reward_transaction_form.transact_datetime.data
                merchant_username           = get_logged_in_api_username()
                
                if merchant_username:
                    try:
                        with db_client.context():
                            customer = Customer.get_by_reference_code(reference_code)
                            if customer:
                                merchant_acct   = customer.registered_merchant_acct
                                transact_outlet = Outlet.fetch(request.headers.get('x-outlet-key'))
                                
                            if transact_datetime_in_gmt:
                                transact_datetime    =  transact_datetime_in_gmt - timedelta(hours=merchant_acct.gmt_hour)
                                
                                now                  = datetime.utcnow()
                                if transact_datetime > now:
                                    return create_rest_message(gettext('Transact datetime cannot be future'), status_code=StatusCode.BAD_REQUEST)
                            
                            
                            
                            transact_merchant_user = MerchantUser.get_by_username(merchant_username)
                            
                            logger.debug('going to call give_reward_transaction')
                            
                            customer_transaction = create_sales_transaction(customer, 
                                                                            transact_outlet     = transact_outlet, 
                                                                            sales_amount        = sales_amount,
                                                                            tax_amount          = tax_amount,
                                                                            invoice_id          = invoice_id,
                                                                            remarks             = remarks,
                                                                            transact_by         = transact_merchant_user,
                                                                            transact_datetime   = transact_datetime,
                                                                            invoice_details     = invoice_details,
                                                                        )
                            
                        if customer_transaction:
                            
                            customer_entitled_voucher_list = []
                            with db_client.context():
                                
                                for k, v in customer_transaction.entitled_voucher_summary.items():
                                    
                                    voucher_details = MerchantVoucher.fetch(v.get('voucher_key'))
                                    
                                    customer_entitled_voucher_list.append({
                                                                            'label'             : voucher_details.label,
                                                                            'image_url'         : voucher_details.image_public_url,
                                                                            'amount'            : v.get('amount'),
                                                                            'effective_date'    : v.get('effective_date'),
                                                                            'expiry_date'       : v.get('expiry_date'), 
                                                                        })
                            
                            transaction_details =  {
                                                    "transaction_id"            : customer_transaction.transaction_id,
                                                    'entitled_reward_summary'   : customer_transaction.entitled_reward_summary,
                                                    'entitled_voucher_summary'  : customer_entitled_voucher_list,
                                                    }
                                
                        return (transaction_details, StatusCode.OK)
                    except:
                        logger.error('Failed to proceed transaction due to %s', get_tracelog())
                        return create_rest_message('Failed to proceed transaction', status_code=StatusCode.BAD_REQUEST)
                                
                else:
                    return create_rest_message('Missing transact user account', status_code=StatusCode.BAD_REQUEST)
        else:
            logger.warn('reward transaction data input is invalid')
            error_message = reward_transaction_form.create_rest_return_error_message()
            
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
    else:
        return create_rest_message('Reference code is required', status_code=StatusCode.BAD_REQUEST)
    
@reward_api_bp.route('/<reference_code>/redeem', methods=['POST'])
@auth_token_required
@outlet_key_required
def redeem_reward(reference_code):
    
    logger.debug('reference_code=%s', reference_code)
    
    if is_not_empty(reference_code):
    
        transaction_data_in_json   = request.get_json()
        
        logger.debug('transaction_data_in_json=%s', transaction_data_in_json)
        
        redeem_reward_transaction_form = RedeemRewardTransactionForm(ImmutableMultiDict(transaction_data_in_json))
        
        if redeem_reward_transaction_form.validate():
            logger.debug('reward transaction data is valid')
            
            reward_format           = redeem_reward_transaction_form.reward_format.data
            reward_amount           = redeem_reward_transaction_form.reward_amount.data
            invoice_id              = redeem_reward_transaction_form.invoice_id.data
            remarks                 = redeem_reward_transaction_form.remarks.data
            redeem_datetime_in_gmt  = redeem_reward_transaction_form.redeem_datetime.data
            merchant_username       = get_logged_in_api_username()
            
            if reward_amount:
                reward_amount = float(reward_amount)
            else:
                reward_amount = .0
             
            logger.debug('reward_format=%s', reward_format)
            logger.debug('reward_amount=%s', reward_amount)
            logger.debug('invoice_id=%s', invoice_id)
            logger.debug('remarks=%s', remarks)
            logger.debug('redeem_datetime_in_gmt=%s', redeem_datetime_in_gmt)
            
            db_client = create_db_client(caller_info="redeem_reward")
            with db_client.context():
                redeemed_by_outlet      = Outlet.fetch(request.headers.get('x-outlet-key'))
                merchant_acct           = redeemed_by_outlet.merchant_acct_entity
            
            if redeem_datetime_in_gmt:
                redeem_datetime    =  redeem_datetime_in_gmt - timedelta(hours=merchant_acct.gmt_hour)
                
                now                  = datetime.utcnow()
                if redeem_datetime > now:
                    return create_rest_message('Redeem datetime cannot be future', status_code=StatusCode.BAD_REQUEST)
                
                
                
            if merchant_username:
                try:
                    with db_client.context():
                        customer = Customer.get_by_reference_code(reference_code)
                        if customer:
                            merchant_acct   = customer.registered_merchant_acct
                            redeem_outlet = Outlet.fetch(request.headers.get('x-outlet-key'))
                            
                        redeem_by_merchant_user = MerchantUser.get_by_username(merchant_username)
                        
                        logger.debug('going to call redeem_reward_transaction')
                        
                        customer_redemption = redeem_reward_transaction(customer, 
                                                                        redeem_outlet       = redeem_outlet, 
                                                                        reward_format       = reward_format,
                                                                        reward_amount       = reward_amount,
                                                                        invoice_id          = invoice_id,
                                                                        remarks             = remarks,
                                                                        redeemed_by         = redeem_by_merchant_user,
                                                                        redeemed_datetime   = redeem_datetime,
                                                                        
                                                                    )
                        
                    if customer_redemption:
                        
                        transaction_details =  {
                                                "transaction_id"            : customer_redemption.transaction_id,
                                                }
                            
                    return (transaction_details, StatusCode.OK)
                
                except Exception as e:
                    logger.error('Failed to proceed transaction due to %s', get_tracelog())
                    error_message = e.message
                    
                    logger.error('Failed to proceeed transaction due to %s'. error_message)
                    
                    return create_rest_message('Failed to proceed transaction', status_code=StatusCode.BAD_REQUEST)
                            
            else:
                return create_rest_message('Missing redeem user account', status_code=StatusCode.BAD_REQUEST)
        
        else:
            error_message = redeem_reward_transaction_form.create_rest_return_error_message()
        
            return create_rest_message(error_message, status_code=StatusCode.BAD_REQUEST)
        
    else:
        return create_rest_message('Reference code is required', status_code=StatusCode.BAD_REQUEST)   
