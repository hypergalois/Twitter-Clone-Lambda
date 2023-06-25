import json
import pymysql
import os

# Configuración de la base de datos
host = os.environ['rds_host']
user = os.environ['usernameDB']
password = os.environ['passwordDB']
db_name = os.environ['dbname']

def lambda_handler(event, context):
    
    # Obtener id_user desde el evento
    user_id = event["queryStringParameters"]["user_id"]
    
    # Conectarse a la base de datos
    connection = pymysql.connect(host=host, user=user, password=password, db=db_name)
    
    try:
        # Obtener los tweets del usuario
        with connection.cursor() as cursor:
            sql = """
                SELECT message, attachment_id, created_at
                FROM mensajes
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT 20
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchall()
            
            # Construir la respuesta
            try:
                dataTweets = [
                    {'message': row[0], 'attachment_id': row[1], 'created_at': row[2].strftime('%H:%M %d/%m/%Y')}
                    for row in result
                ]
            except:
                dataTweets = [
                    {'message': row[0], 'attachment_id': row[1], 'created_at': row[2]}
                    for row in result
                ]
            
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'res': 'ok', 'tweets': dataTweets})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'res': 'fail', 'error': str(e)})
        }
    
    finally:
        connection.close()
