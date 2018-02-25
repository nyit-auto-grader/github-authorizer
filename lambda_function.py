from getpass import getpass
import requests
import boto3
import json
import os


def build_response(isBase64Encoded=False, statusCode=200, headers=None, **kwargs):
    return dict(isBase64Encoded=isBase64Encoded, statusCode=statusCode, headers=headers or dict(), body=json.dumps(kwargs))


def create_token(name: str='default'):
    response = boto3.client('sts').assume_role(RoleArn=os.environ.get('ROLE'), RoleSessionName=name)
    credentials = response['Credentials']
    credentials['Expiration'] = credentials['Expiration'].strftime('%Y-%M-%d %H:%M:%S')
    return {'Credentials': credentials}


def github_login(username: str, password: str) -> bool:
    response = requests.get('https://api.github.com/user', auth=(username, password))
    return response.status_code == 200


# def lambda_handler(event, context):
#     if event['httpMethod'] == 'POST':
#         body = json.loads(event['body'])
#         missing_fields = [field for field in ['username', 'password'] if field not in body]
#         if len(missing_fields) > 0:
#             return build_response(statusCode=400, message='missing required fields', fields=missing_fields)
#
#         if github_login(body['username'], body['password']):
#             payload = create_token()
#             return build_response(**payload)
#         else:
#             return build_response(statusCode=401, message='invalid username or password')
#
#     else:
#         return build_response(statusCode=400, message='unsupported method')


def lambda_handler(event, context):
    if github_login(event['username'], event['password']):
        return create_token()
    else:
        return dict(message="unauthorized")


if __name__ == '__main__':
    username = input('enter your github username: ')
    password = getpass('enter your github password: ')

    if github_login(username, password):
        token = create_token()
