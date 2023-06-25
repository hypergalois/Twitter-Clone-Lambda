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
    attachment_id = event["queryStringParameters"]["attachment_id"]
    
    # Conectarse a la base de datos
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    
    try:
        # Obtener los datos de la URL y tipo del adjunto
        with connection.cursor() as cursor:
            sql = """
                SELECT url, type
                FROM adjuntos
                WHERE attachment_id = %s
            """
            cursor.execute(sql, (attachment_id,))
            result = cursor.fetchone()
            
            # Verificar si se encontró un resultado
            if result is None:
                return {
                    'statusCode': 404,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'res': 'fail', 'error': 'Attachment not found'})
                }
            
            # Construir la respuesta
            attachment_data = {
                'url': result[0],
                'type': result[1]
            }
            
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'res': 'ok', 'attachment': attachment_data})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'res': 'fail', 'error': str(e)})
        }
    
    finally:
        connection.close()
