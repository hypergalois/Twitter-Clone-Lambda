import sys
import logging
import pymysql
import json

rds_host = "amarillo.ci81pvlxi225.us-east-1.rds.amazonaws.com"

usernameDB = "admin"
passwordDB = "password"
dbname = "calculadora"

def lambda_handler(event, context):
    user = event["queryStringParameters"]["user"]
    frase = event["queryStringParameters"]["frase"]
    print(user)
    print(frase)
    parecidas = 0

    # aqui comprobamos que existe el usuario y si existe comparamos las frases a ver si son like y si lo son same frase = 1
    #  y devolvemos ok o fail
    try:
        conn = pymysql.connect(rds_host, user=usernameDB, passwd=passwordDB, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            cur.execute("select * from usuarios where username='" + user + "'")
            resultado = cur.fetchone()
            if resultado != None:
                # SELECT IF(500<1000, "YES", "NO");
                # podemos hacer la comparacion directamente en sql o como voy a hacer yo obtener el valor y hacerlo en python
                cur.execute("select frase from usuarios where username='" + user + "'")
                resultado = cur.fetchone()
                fraseReal = resultado[0]
                # comparamos
                if frase != fraseReal:
                    # entonces nada
                    return {
                        'statusCode': 202,
                        'headers': { 'Access-Control-Allow-Origin' : '*'},
                        'body' : json.dumps( { 'res': "fail", 'error': 'frase'} )
                    }
            else:
                # devolvemos fallo no existe el user
                # hay que mirar que codigo poner que no se todavia
                return {
                    'statusCode': 202,
                    'headers': { 'Access-Control-Allow-Origin' : '*'},
                    'body' : json.dumps( { 'res': "fail", 'error': 'user'} )
                }
            cur.close()
    except pymysql.MySQLError as e:
        print(e)
    conn.close()
    
    # aqui ya podemos mandarselo al user de vuelta
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*'},
        'body' : json.dumps( { 'res': "ok", 'user': user} )
    }
