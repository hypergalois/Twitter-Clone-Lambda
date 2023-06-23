import json
import pymysql
import os

# Configuración de la base de datos
host = os.environ['rds_host']
user = os.environ['usernameDB']
password = os.environ['passwordDB']
db_name = os.environ['dbname']

def lambda_handler(event, context):
    
    # Obtener detalles del tweet desde el evento
    user_id = event["queryStringParameters"]["user_id"]
    message = event["queryStringParameters"]["message"]
    
    # Conectarse a la base de datos
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    
    try:
        # Insertar el mensaje
        with connection.cursor() as cursor:
            sql = "INSERT INTO mensajes (user_id, message) VALUES (%s, %s)"
            cursor.execute(sql, (user_id, message))
        connection.commit()
        
        return {
            'statusCode': 200,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body': json.dumps({'res': 'ok'})
        }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body': json.dumps({'res': 'fail'})
        }
    
    finally:
        connection.close()

