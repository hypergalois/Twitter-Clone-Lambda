import jwt
import datetime

SECRET_KEY = 'secret'

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxMzQsImV4cCI6MTY4ODM5MDI4NX0.vSeZoyBQaIHE-C6jv6C821YLj3XlLci5_q85Ssywv74'

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms='HS256')
    print('Valid token')
    print(payload.keys())
    print(payload['exp'])
    print(payload['user_id'])
except jwt.InvalidTokenError:
    print('Invalid token')
except jwt.ExpiredSignatureError:
    print('Expired token')

datetime.datetime.utcnow()