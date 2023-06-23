import boto3
import datetime

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    
    # Datos de tu bucket y archivo
    bucket = 'twitter-clone-mais'
    file_key = 'your-file-key'
    
    # Crear una URL firmada
    url = s3_client.generate_presigned_url('put_object',
                                            Params={'Bucket': bucket, 'Key': file_key},
                                            ExpiresIn=3600,
                                            HttpMethod='PUT')
                                            
    # Devuelve la URL firmada
    return {
        'statusCode': 200,
        'body': {
            'signed_url': url,
            'x_amz_date': datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        }
    }
