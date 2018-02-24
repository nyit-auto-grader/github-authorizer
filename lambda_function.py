from getpass import getpass
import requests
import boto3
import json
import os


def build_response(**kwargs):
    return dict(isBase64Encoded=False, statusCode=200, headers=dict(), body=json.dumps(kwargs))


def create_token(name: str='default'):
    return boto3.client('sts').assume_role(RoleArn=os.environ.get('ROLE'), RoleSessionName=name)


def github_login(username: str, password: str) -> bool:
    response = requests.get('https://api.github.com/user', auth=(username, password))
    return response.status_code == 200


def lambda_handler(event, context):
    # response = sts.assume_role(RoleArn=role_arn, RoleSessionName='default')
    response = build_response(message='hello world')
    return response


if __name__ == '__main__':
    username = input('enter your github username: ')
    password = getpass('enter your github password: ')

    if github_login(username, password):
        token = create_token()