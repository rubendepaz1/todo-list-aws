import os
import boto3
import functools
from botocore.exceptions import ClientError


def get_table(dynamodb=None):
    if not dynamodb:
        URL = os.environ['ENDPOINT_OVERRIDE']
        if URL:
            print('URL dynamoDB:'+URL)
            boto3.client = functools.partial(boto3.client, endpoint_url=URL)
            boto3.resource = functools.partial(boto3.resource,
                                               endpoint_url=URL)
        dynamodb = boto3.resource("dynamodb")
    # fetch todo from the database
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])
    return table


def ingles(key, dynamodb=None):

    sourceLanguage = 'es'
    targetLanguage = 'en'

    # cliente para traducir
    translate = boto3.client('translate')

    table = get_table(dynamodb)
    try:
        result = table.get_item(
            Key={
                'id': key
            }
        )

    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print('Result getItem:'+str(result))
        if 'Item' in result:
            result_translate = translate.translate_text(
                Text=result['Item']['Text'],
                SourceLanguageCode=sourceLanguage,
                TargetLanguageCode=targetLanguage)
            return result_translate.get('TranslatedText')
