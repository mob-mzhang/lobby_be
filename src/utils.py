def format_phone_number(phone: str) -> str:
    phone_str = ''.join(filter(str.isdigit, phone))
    if len(phone_str) == 10:
        return f"({phone_str[:3]}) {phone_str[3:6]}-{phone_str[6:]}"
    return phone  # Return original if not 10 digits

import uuid

def generate_unique_id():
    return str(uuid.uuid4())
