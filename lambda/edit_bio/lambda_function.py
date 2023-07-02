import json
import pymysql
import os

# Configuración de la base de datos
host = os.environ['rds_host']
user = os.environ['usernameDB']
password = os.environ['passwordDB']
db_name = os.environ['dbname']

def lambda_handler(event, context):
    
    # Obtener attachment_id desde el evento
    user_id = event["queryStringParameters"]["user_id"]
    # Solo tenemos que cambiar la url en usuarios, nada de attachments
    bio = event["queryStringParameters"]["bio"]
    
    # Conectarse a la base de datos
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    
    try:
        # Obtener los datos de la URL y tipo del adjunto
        with connection.cursor() as cursor:
            sql = """
                UPDATE usuarios SET (bio, updated_at) VALUES (%s, NOW()) WHERE user_id = %s
            """
            cursor.execute(sql, (bio, user_id))
            connection.commit()
            
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'res': 'ok'})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'res': 'fail', 'error': str(e)})
        }
    
    finally:
        connection.close()