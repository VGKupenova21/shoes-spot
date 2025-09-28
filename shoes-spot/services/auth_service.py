users = {
    "admin@abv.bg": {"password": "admin123", "role": "admin"}
}

def register_user(email, password):
    if email in users:
        return False
    users[email] = {"password": password, "role": "user"}
    print(f"[CONFIRMATION] Email {email} registered successfully!")
    return True

def authenticate_user(email, password):
    user = users.get(email)
    if user and user["password"] == password:
        return {"email": email, "role": user["role"]}
    return None