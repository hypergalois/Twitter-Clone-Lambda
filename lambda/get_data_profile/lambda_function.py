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
        # Obtener los datos del perfil del usuario
        with connection.cursor() as cursor:
            sql = """
                SELECT username, avatar, biography, name, created_at
                FROM usuarios
                WHERE user_id = %s
            """
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            
            # Verificar si se encontró un resultado
            if result is None:
                return {
                    'statusCode': 404,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'res': 'fail', 'error': 'User not found'})
                }
            
            # Construir la respuesta
            try:
                profile_data = {
                    'username': result[0],
                    'avatar': result[1],
                    'biography': result[2],
                    'name': result[3],
                    'created_at': result[4].strftime('%H:%M %d/%m/%Y')
                }
            except:
                profile_data = {
                    'username': result[0],
                    'avatar': result[1],
                    'biography': result[2],
                    'name': result[3],
                    'created_at': result[4]
                }
            
            return {
                'statusCode': 200,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'res': 'ok', 'profile': profile_data})
            }
    
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'res': 'fail', 'error': str(e)})
        }
    
    finally:
        connection.close()
