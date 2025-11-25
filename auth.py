from models import User

def authenticate(email, password):
    user = User.get_by_email(email)
    if not user:
        return None
    if User.verify_password(user[4], password):
        return user
    return None
