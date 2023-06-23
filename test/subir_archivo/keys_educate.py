import json

import sys, os, base64, datetime, hashlib, hmac 

bucket = "utadbucket1"
bucketUrl = "https://utadbucket1.s3.us-east-1.amazonaws.com/"
region = 'us-east-1'
service = 's3'

t = datetime.datetime.utcnow()
amzDate = t.strftime('%Y%m%dT%H%M%SZ')
dateStamp = t.strftime('%Y%m%d') # Date w/o time, used in credential scope
    
# Key derivation functions. See:
# http://docs.aws.amazon.com/general/latest/gr/signature-v4-examples.html#signature-v4-examples-python
def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def getSignatureKey(key, dateStamp, regionName, serviceName):
    kDate = sign(('AWS4' + key).encode('utf-8'), dateStamp)
    kRegion = sign(kDate, regionName)
    kService = sign(kRegion, serviceName)
    kSigning = sign(kService, 'aws4_request')
    return kSigning




def lambda_handler(event, context):
    # TODO implement
    #aws_access_key_id=event["queryStringParameters"]["ak"];
    #aws_secret_access_key=event["queryStringParameters"]["sk"];
    #aws_session_token=event["queryStringParameters"]["st"];
    aws_access_key_id="ASIA2E36C6W27WLQQCMV"
    aws_secret_access_key="LjT72YZWTTbHufJarKgyUOf5zKPmV8hLJrw1UIfR"
    aws_session_token="FwoGZXIvYXdzEHsaDLlIRpl8D6cvIF2wbSLAAVTFGqh+4W/ufPAHCLfhADJB7Do5lOmH2O3OAvEfJ/Hl9tZ7isjtkgIx1w3f2rZa0foM4f76WM5wKQvYDYmhup1Itf5Cu6AjeUD/upI50edd8oTlKR5aKIsY/5oQLWIvsDNU5UkXrra9YeqHEKQ1ImZeZlw9JCyTgmuF+OGazc1k3tgtAGKMF49AREBUrcrLwTtaw2XGQeeId8/lhjXQ9Y/7DUSu96KrSjJcAEET+L+k0nHFgEaGiqGuu+pUmgMkJCiardicBjItdp089qiReJHTOomzF4d83/T0y5vyjb72SdYn+GB4y49d3duiMamHNEK+MHz+"
    
    
    stringToSign= b""
    
       
    policy = """{"expiration": "2023-12-30T12:00:00.000Z",
    "conditions": [
    {"bucket": \"""" + bucket +"""\"},
    ["starts-with", "$key", ""],
    {"acl": "public-read"},
    {"success_action_redirect": \""""+ bucketUrl+"""success.html"},
        {"x-amz-credential": \""""+ aws_access_key_id+"/"+dateStamp+"/"+region+"""/s3/aws4_request"},
        {"x-amz-algorithm": "AWS4-HMAC-SHA256"},
        {"x-amz-date": \""""+amzDate+"""\" },
        {"x-amz-security-token": \"""" + aws_session_token +"""\"  }
      ]
    }"""

    
    stringToSign=base64.b64encode(bytes((policy).encode("utf-8")))

    
    signing_key = getSignatureKey(aws_secret_access_key, dateStamp, region, service)
    signature = hmac.new(signing_key, stringToSign, hashlib.sha256).hexdigest()
    
    #print(dateStamp)
    #print(signature)
    print(policy)
    return {
        'statusCode': 200,
        'headers': { 'Access-Control-Allow-Origin' : '*' },
        'body':json.dumps({ 'stringSigned' :  signature , 'stringToSign' : stringToSign.decode('utf-8') , 'xAmzCredential' : aws_access_key_id+"/"+dateStamp+"/"+region+ "/s3/aws4_request" , 'dateStamp' : dateStamp , 'amzDate' : amzDate , 'securityToken' : aws_session_token })
    }
