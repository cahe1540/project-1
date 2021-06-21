# pass in a dict in json format and filter out the password
def remove_passwords(json_dict: dict):

    filtered = {}

    for field in json_dict:
        if field != "password":
            filtered[field] = json_dict[field]

    return filtered
