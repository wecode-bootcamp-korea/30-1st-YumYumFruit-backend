import re

def validate_email(email):
    regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex_email,email)   

def validate_password(password):
    regex_password = '^[A-Za-z0-9]{8,16}$'
    return re.match(regex_password, password)