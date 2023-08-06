'''
Created on 20 Jul 2022

@author: jacklok
'''
#from flask.blueprints import Blueprint
import logging
from flask import abort
from flask.blueprints import Blueprint
from trexlib.utils.string_util import is_not_empty
from trexmodel.models.datastore.merchant_models import Outlet, BannerFile
from trexmodel.utils.model.model_util import create_db_client
from trexmodel.models.datastore.product_models import ProductCatalogue
from trexapi.controllers.pos_api_routes import get_product_category_structure_code_label_json
from flask_restful import abort
from flask.helpers import url_for
from trexmodel.models import merchant_helpers

outlet_api_bp = Blueprint('outlet_api_bp', __name__,
                                 template_folder='templates',
                                 static_folder='static',
                                 url_prefix='/api/v1/outlets')

logger = logging.getLogger('debug')

@outlet_api_bp.route('/details/<outlet_key>', methods=['GET'])
def read_outlet(outlet_key):
    
    outlet_details          = None
    merchant_acct           = None
    catalogue_details       = None
    outlet_setting_in_json  = {}   
    output_json             = {
                                'score': 0.0
                                } 
    
    if is_not_empty(outlet_key):
        db_client = create_db_client(caller_info="read_outlet")
        with db_client.context():
            outlet_details      = Outlet.fetch(outlet_key)
            if outlet_details:
                merchant_acct           = outlet_details.merchant_acct_entity
                catalogue_key           = outlet_details.assigned_catalogue_key
                outlet_setting_in_json  = merchant_helpers.construct_setting_by_outlet(outlet_details)
                logger.debug('assigned catalogue_key=%s', catalogue_key)
                banner_listing = []
                
                banner_file_listing =  BannerFile.list_by_merchant_acct(merchant_acct)
                logger.debug('banner_file_listing=%s', banner_file_listing)
                if banner_file_listing:
                    for banner_file in banner_file_listing:
                        banner_listing.append(banner_file.banner_file_public_url)
                    
                    outlet_setting_in_json['banners'] = banner_listing
                        
                product_catalogue   = ProductCatalogue.fetch(catalogue_key)
            
                if product_catalogue:
                    logger.debug('Found catalogue')
                    last_updated_datetime               = outlet_details.modified_datetime
                        
                    category_tree_structure_in_json     = get_product_category_structure_code_label_json(merchant_acct)
                    
                    catalogue_details =  {
                                        'key'                       : catalogue_key,    
                                        'category_list'             : category_tree_structure_in_json,
                                        'product_by_category_map'   : product_catalogue.published_menu_settings,
                                        'last_updated_datetime'     : last_updated_datetime.strftime('%d-%m-%Y %H:%M:%S')
                                    }
    
    if outlet_setting_in_json:
        output_json['settings'] = outlet_setting_in_json
        
        if catalogue_details:
            output_json['product_catalogue'] = catalogue_details
        
        
        return output_json
    else:
        abort
        
