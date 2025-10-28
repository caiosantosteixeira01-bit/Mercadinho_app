from models import get_all_users
import bcrypt

current_user = {}

def login(email,password):
    conn = get_all_users()
    for u in conn:
        user_id,name,user_email,phone,user_type,is_on = u
        from db import get_connection
        c = get_connection().cursor()
        c.execute("SELECT password FROM users WHERE id=?", (user_id,))
        hashed = c.fetchone()[0]
        if user_email == email and bcrypt.checkpw(password.encode(), hashed):
            global current_user
            current_user = {
                "id":user_id,
                "name":name,
                "email":email,
                "type":user_type,
                "is_on":is_on
            }
            return True
    return False
