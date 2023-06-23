import json

import sys, os, base64, datetime, hashlib, hmac 

bucket = "twitter-clone-utad"
bucketUrl = "https://twitter-clone-utad.s3.us-east-1.amazonaws.com/"
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
    
    aws_access_key_id="ASIAYRRDPMR6GEZ3MIFQ"
    aws_secret_access_key="MRigOiU7LPB6fNpAEtZq2tg8QcLjWaVV5SxP+BuZ"
    aws_session_token="FwoGZXIvYXdzEKz//////////wEaDP5Mhc8KBugqNN5uUiK+AQFaaPMvrddHbVSsBkP5JCG9PwEqiythyQ80fbtOLtkXZQcVBRQStd+dkPOD3F85pfpi3zfZOvd/xHeseWGaRoAEvbuqPRoo0dfcGEqGX3/11iraVj6sd9kb9l+AHEmbZlAgaLWf+4RrxuIjRt0UpylRXJgaSbRys3bPyDcWevw1p1cwvCO4jQcUFve7gkUujoP0CFtVwXGAUKBUN8I0qE0+rWn3wsG4iWkFZlb90Rj/yM73t2EIrFbmNuGOHSgojczXpAYyLRpaAThmUEdslc59o55BxqWFnvRV05T5oCOD3bJ+t/V2Mr1+wDmMys6gdTIyrw=="
    
    stringToSign= b""
    
    
    # He borrado el redirect   
    policy = """{"expiration": "2023-12-30T12:00:00.000Z",
    "conditions": [
    {"bucket": \"""" + bucket +"""\"},
    ["starts-with", "$key", ""],
    {"acl": "public-read"},
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
