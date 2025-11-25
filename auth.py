from models import User, hash_password

def authenticate(email, password):
    user = User.get_by_email(email)
    if not user:
        return None

    user_id, name, email, phone, hashed_password, user_type = user
    if hash_password(password) == hashed_password:
        return {
            "id": user_id,
            "name": name,
            "email": email,
            "type": user_type
        }
    return None
