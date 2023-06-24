import json
import pymysql
import os

# Configuración de la base de datos
host = os.environ['rds_host']
user = os.environ['usernameDB']
password = os.environ['passwordDB']
db_name = os.environ['dbname']

def lambda_handler(event, context):
    
    # Obtener user_id desde el evento
    user_id = event["queryStringParameters"]["user_id"]
    
    # Conectarse a la base de datos
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    
    try:
        # Consultar el nombre, username y avatar del usuario
        with connection.cursor() as cursor:
            sql = "SELECT name, username, avatar FROM usuarios WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            
        if result:
            # Devolver los datos del usuario
            return {
                'statusCode': 200,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body': json.dumps({
                    'res': 'ok',
                    'name': result[0],
                    'username': result[1],
                    'avatar': result[2]
                })
            }
        else:
            return {
                'statusCode': 404,
                'headers': { 'Access-Control-Allow-Origin' : '*' },
                'body': json.dumps({'res': 'fail'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': { 'Access-Control-Allow-Origin' : '*' },
            'body': json.dumps({'res': 'fail'})
        }
    
    finally:
        connection.close()
