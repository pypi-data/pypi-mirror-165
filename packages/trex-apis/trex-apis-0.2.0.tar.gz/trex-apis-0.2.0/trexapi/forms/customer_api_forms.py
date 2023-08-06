'''
Created on 12 Jul 2021

@author: jacklok
'''

from wtforms import StringField, PasswordField, validators, DateField
from trexadmin.forms.base_forms import ValidationBaseForm
from trexadmin.libs.wtforms import validators as custom_validator
from flask_babel import gettext
from datetime import date

class CustomerDetailsForm(ValidationBaseForm):
    name                = StringField(gettext('Name'), validators=[
                                        validators.InputRequired(gettext('Name is required')),
                                        validators.Length(min=3, max=300, message='Name length must be within 3 and 300 characters'),
                                        
                                        ]
                                        )
    gender              = StringField(gettext('Gender'), [
                                        validators.Optional(),
                                        validators.Length(min=1, max=1, message=gettext('Gender value is either m or f')),
                                        
                                        ]
                                        )
    
    birth_date          = DateField('Date of Birth', format='%d/%m/%Y', validators=[
                                            validators.Optional(),
                                        ])
    
    email               = StringField('Email Address', validators=[
                                        validators.Email(gettext("Please enter valid email address.")),
                                        custom_validator.RequiredIfOtherFieldEmpty(
                                                        ['mobile_phone'],
                                                        message=gettext("Either email or mobile phone is required"),
                                                        
                                                        ),
                                        ]
                                        )
    
    mobile_phone        = StringField('Mobile Phone', validators=[
                                        custom_validator.RequiredIfOtherFieldEmpty(
                                                        ['email'],
                                                        message=gettext("Either email or mobile phone is required"),
                                                        
                                                        ),
                                        
                                        ]
                                        )
    
    merchant_reference_code       = StringField('Member code', validators=[
                                        validators.Optional(),
                                        validators.Length(max=16, message=gettext("Member code length must not more than 16 characters"))
                                        ]
                                        )
    
    password                      = StringField(gettext('Password'), validators=[
                                        validators.InputRequired(gettext('Password is required')),
                                        
                                        ]
                                        )
    
    
