'''
Created on 14 Jul 2021

@author: jacklok
'''

from wtforms import StringField, DecimalField, validators
from trexadmin.forms.base_forms import ValidationBaseForm
from trexadmin.libs.wtforms import validators as custom_validator
from trexadmin.libs.wtforms.fields import OptionalDateTimeField, CurrencyField, JSONField

class GiveRewardTransactionForm(ValidationBaseForm):
    sales_amount                    = DecimalField('Sales Amount',[
                                                validators.InputRequired(message="Sales Amount is required"),
                                            ])
    
    tax_amount                      = DecimalField('Tax Amount',[
                                                validators.Optional()
                                            ])  
    
    invoice_id                      = StringField('Invoice No',[
                                                validators.Optional(),
                                                validators.Length(max=30, message="Invoice No length must not more than 30 characters")
                                            ])
    
    remarks                         = StringField('Remarks',[
                                                validators.Optional(),
                                                validators.Length(max=300, message="Remarks length must not more than 300 characters")
                                            ])
    
    transact_datetime               = OptionalDateTimeField('Transact Datetime', format='%d-%m-%Y %H:%M:%S') 
    
class RedeemRewardTransactionForm(ValidationBaseForm):
    reward_format                   = StringField('Reward format',[
                                                validators.InputRequired(message="Reward format is required"),
                                            ])
    
    reward_amount                   = DecimalField('Reward Amount',[
                                                validators.InputRequired(message="Reward amount is required"),
                                            ])  
    
    invoice_id                      = StringField('Invoice No',[
                                                validators.Optional(),
                                                validators.Length(max=30, message="Invoice No length must not more than 30 characters")
                                            ])
    
    remarks                         = StringField('Remarks',[
                                                validators.Optional(),
                                                validators.Length(max=300, message="Remarks length must not more than 300 characters")
                                            ])
    
    redeem_datetime                 = OptionalDateTimeField('Transact Datetime', format='%d-%m-%Y %H:%M:%S')    
     
    
    
    
class VoucherRedeemForm(ValidationBaseForm):
    redeem_code                     = StringField('Redeem Code',[
                                                validators.InputRequired(message="Redeem Code is required"),
                                            ])
    invoice_id                      = StringField('Invoice No',[
                                                validators.Optional(),
                                                validators.Length(max=30, message="Invoice No length must not more than 30 characters")
                                            ])
    
    remarks                         = StringField('Remarks',[
                                                validators.Optional(),
                                                validators.Length(max=300, message="Remarks length must not more than 300 characters")
                                            ])
    
    redeem_datetime               = OptionalDateTimeField('Redeem Datetime', format='%d-%m-%Y %H:%M:%S')      
    
    