import jwt
import datetime

SECRET_KEY = 'secret'

user_id = 134

payload = {
    'user_id': user_id,
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)
}

token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

print(token)