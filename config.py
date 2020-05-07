import os 

SECRET_KEY = os.urandom(24).encode('hex')
SEND_FILE_MAX_AGE_DEFAULT = 0