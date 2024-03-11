def validate_email(email):
    return '@' in email and email.endswith('.com')


def validate_password(password):
    return len(password) >= 8

def validate_data_includes_email_password(data):
    pass
