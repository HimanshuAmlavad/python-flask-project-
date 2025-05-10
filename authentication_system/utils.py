import re
def not_valid_password(password):
    if len(password) < 8:
        return "Password atleast contain 8 character"
    if not re.search(r"[A-Z]",password):
        return "password should atleast contain upper case"
    if not re.search(r"[a-z]", password):
        return "password should atleast contain lower case"
    if not re.search(r"\d", password):
        return "password should atleast contain digits"
    if not re.search(r"[!@#$%^&*()_+-={}|\\:\";'<>?,./']", password):
        return "password should atleast contain symbol"
    if re.search(r"\s", password):
        return "password should not contain any space"
    return None