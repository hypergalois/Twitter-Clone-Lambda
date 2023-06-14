import sys
import logging
import pymysql
import json
# import argon2
# from argon2 import PasswordHasher

rds_host = "amarillo.ci81pvlxi225.us-east-1.rds.amazonaws.com"

usernameDB = "admin"
passwordDB = "password"
dbname = "calculadora"

def lambda_handler(event, context):
    user = event["queryStringParameters"]["user"]
    password = event["queryStringParameters"]["password"]
    print(user)
    print(password)

    # ahora tenemos que hashear esa contraseña que hemos recibido
    # ph = PasswordHasher()
    # hashed_password = ph.hash(password)
    # print(hashed_password)

    # aqui sera no insertar sino comprobar que existe y que esta bien era solo para probar si esta bien redirige
    # si no esta bien alert(passwrod no esta bien, user no existe/ email no existe lo que sea)
    # primero comprueba user/email y despues password no al reves
    try:
        conn = pymysql.connect(rds_host, user=usernameDB, passwd=passwordDB, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            # ahora aqui tenemos que select id user que sea igual todo lo que nos ha dado
            cur.execute("select id_user from usuarios where username='" + user + "' and password='" + password + "'")
            # cur.execute("insert into usuarios (username, password) values('" + user + "','" + password + "')")
            conn.commit()
            result = cur.fetchone()
            
            # ahora lo que falta es ahi ver si es contraseña o username lo que falla
            # si existe un user con ese username entonces lo que falla es la contraseña y si no esa cuenta no existe
            if result is None:
                cur.execute("select * from usuarios where username = '" + user + "'")
                result2 = cur.fetchone()
                if result2 is None:
                    print("hola")
                    # entonces el user no existe
                    cur.close()
                    conn.close()
                    return {
                        'statusCode': 202,
                        'headers': { 'Access-Control-Allow-Origin' : '*'},
                        'body' : json.dumps( { 'res': "fail", 'user_id': None, 'wrong': 'user'} )
                    }
                else:
                    print("contra")
                    # entonces la contraseña esta mal
                    cur.close()
                    conn.close()
                    return {
                        'statusCode': 202,
                        'headers': { 'Access-Control-Allow-Origin' : '*'},
                        'body' : json.dumps( { 'res': "fail", 'user_id': None, 'wrong': 'password'} )
                    }
                
            cur.close()
    except pymysql.MySQLError as e:
        print(e)
    conn.close()
    print(result)
    print()
    # id_user = result["id_user"]
    
    # aqui ya podemos mandarselo al user de vuelta
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*'},
        'body' : json.dumps( { 'res': "ok", 'user_id': result[0]} )
    }
