import sys
import logging
import pymysql
import json
import bcrypt
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()

rds_host = os.environ.get('RDS_HOST')
usernameDB = os.environ.get('DB_USER')
passwordDB = os.environ.get('DB_PASS')
dbname = os.environ.get('DB_NAME')
dbport = int(os.environ.get('DB_PORT'))

print(rds_host)
print(passwordDB)

nombre = 'prueba'
user = 'user'
email = 'email@email.com'
password = 'password'
frase = 'frase'

hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

print(hashed_password)

conn = pymysql.connect(host=rds_host, user=usernameDB, passwd=passwordDB, db=dbname, connect_timeout=10, port=dbport)

with conn.cursor() as cur:
    # Miramos si existe user
    cur.execute('SELECT * FROM usuarios WHERE username = %s', user)
    if cur.fetchone() is None:
        # Insertamos nuevo usuario
        cur.execute('INSERT INTO usuarios (name, username, email, password, recovery_phrase) VALUES (%s, %s, %s, %s, %s)', (nombre, user, email, hashed_password, frase))
        conn.commit()
    else:
        print('Error')
