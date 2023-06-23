import json
import pymysql
import os

# Configuración de la base de datos
host = os.environ['rds_host']
user = os.environ['usernameDB']
password = os.environ['passwordDB']
db_name = os.environ['dbname']

def lambda_handler(event, context):
    
    # Obtener detalles del tweet y el archivo adjunto desde el evento
    user_id = event["queryStringParameters"]["user_id"]
    message = event["queryStringParameters"]["message"]
    file_name = event["queryStringParameters"]["file_name"]
    file_type = event["queryStringParameters"]["file_type"]
    
    # Conectarse a la base de datos
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    
    try:
        # Insertar el archivo adjunto si se proporciona
        attachment_id = None
        if file_name and file_type:
            with connection.cursor() as cursor:
                sql = "INSERT INTO adjuntos (url, type) VALUES (%s, %s)"
                cursor.execute(sql, (file_name, file_type))
                attachment_id = cursor.lastrowid
            connection.commit()
        
        # Insertar el mensaje
        with connection.cursor() as cursor:
            sql = "INSERT INTO mensajes (user_id, message, attachment_id) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user_id, message, attachment_id))
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
