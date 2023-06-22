import sys
import logging
import pymysql
import json
import bcrypt
import os

rds_host = os.environ.get('RDS_HOST')
usernameDB = os.environ.get('DB_USER')
passwordDB = os.environ.get('DB_PASS')
dbname = os.environ.get('DB_NAME')

def lambda_handler(event, context):
    body = json.loads(event['body'])

    nombre = body['nombre']
    user = body['user']
    email = body['email']
    password = body['password']
    frase = body['frase']

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = pymysql.connect(rds_host, user=usernameDB, passwd=passwordDB, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            # Miramos si existe user
            cur.execute('SELECT * FROM usuarios WHERE username = %s', user)
            if cur.fetchone() is None:
                # Insertamos nuevo usuario
                cur.execute('INSERT INTO usuarios (nombre, username, email, password, recovery_phrase) VALUES (%s, %s, %s, %s, %s)', (nombre, user, email, hashed_password, frase))
                conn.commit()

                # Obtenemos id del usuario
                cur.execute('SELECT id_user FROM usuarios WHERE username = %s', user)
                id_user = cur.fetchone()[0]
            else:
                # En este caso el usuario ya existe
                return {
                    'statusCode' : 400,
                    'headers' : { 'Access-Control-Allow-Origin' : '*'},
                    'body' : json.dumps({'message': 'Username already exists'})
                }
    except pymysql.MySQLError as e:
        logging.error('Error: %s', str(e))
        return {
            'statusCode' : 500,
            'headers' : { 'Access-Control-Allow-Origin' : '*'},
            'body' : json.dumps({'message': 'Internal server error'})
        }
    

    return {
        'statusCode' : 200,
        'headers' : { 'Access-Control-Allow-Origin' : '*'},
        'body' : json.dumps({'message': 'Registration successful', 'user': user, 'id_user': id_user})
    }