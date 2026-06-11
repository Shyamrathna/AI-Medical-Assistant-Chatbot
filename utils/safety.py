def check_emergency(user_input):
    keywords = ["chest pain", "breathing problem", "severe bleeding"]

    for word in keywords:
        if word in user_input.lower():
            return True

    return False