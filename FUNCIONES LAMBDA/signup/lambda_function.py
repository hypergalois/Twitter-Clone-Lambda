import sys
import logging
import pymysql
import json

rds_host = "amarillo.ci81pvlxi225.us-east-1.rds.amazonaws.com"

usernameDB = "admin"
passwordDB = "password"
dbname = "calculadora"

def lambda_handler(event, context):
    nombre = event["queryStringParameters"]["nombre"]
    user = event["queryStringParameters"]["user"]
    email = event["queryStringParameters"]["email"]
    password = event["queryStringParameters"]["password"]
    frase = event["queryStringParameters"]["frase"]
    print(nombre)
    print(user)
    print(email)
    print(password)
    print(frase)
    id_user = 1

    # no he comprobado que el usuario ya no este en la base de datos vaya
    try:
        conn = pymysql.connect(rds_host, user=usernameDB, passwd=passwordDB, db=dbname, connect_timeout=10, port=3306)
        with conn.cursor() as cur:
            cur.execute("select * from usuarios where username = '" + user + "'")
            result = cur.fetchone()
            if result is None:
                # insert into usuarios (nombre, username, email, password, frase) values ("juanito del castillo", "vegeta777", "juan@gmail.com", "secreto", "vivo en madrid")
                cur.execute("insert into usuarios (nombre, username, email, password, frase) values ('" + nombre + "','" + user + "','" + email + "','" + password + "','" + frase + "')")
                conn.commit()
                # aqui tenemos que obtener el id
                cur.execute("select id_user from usuarios where username = '" + user + "'")
                result2 = cur.fetchone()
                print(result2)
                id_user = result2[0]
            else:
                # aqui tenemos que devolver que ese user esta pillado
                return {
                    'statusCode': 202,
                    'headers': { 'Access-Control-Allow-Origin' : '*'},
                    'body' : json.dumps( { 'res': 'fail', 'user': "", 'id_user': "", 'wrong': 'userUsed'} )
                }
            cur.close()
    except pymysql.MySQLError as e:
        print(e)
    conn.close()
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*'},
        'body' : json.dumps( { 'res': 'ok', 'user': user, 'id_user': id_user} )
    }
