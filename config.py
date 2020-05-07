import random
import string

def generate_key(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

SECRET_KEY = generate_key(12)
SEND_FILE_MAX_AGE_DEFAULT = 0