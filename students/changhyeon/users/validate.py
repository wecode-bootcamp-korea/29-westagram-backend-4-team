import re
from django.core.exceptions import ValidationError 

def validate_email(email):
  email_pattern = re.match('^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)
  if email_pattern == None:
    raise ValidationError(
      message = ('INVALID VALUE'),
      code    = 'invalid'
    )   

def validate_password(password):
  password_pattern = re.match("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}" , password)
  if password_pattern == None:
    raise ValidationError(
      message = ('INVALID VLAUE'),
      code    = 'invalid'
    )

