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


def get_item_translated(key, language, dynamodb=None):
    # cliente para traducir
    translate = boto3.client('translate')
    # cliente para detectar idioma de entrada
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

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
            # obtenemos el lenguaje del to-do
            result_comprehend = comprehend.detect_dominant_language(Text= result['Item']['text'])
            sourceLanguage = result_comprehend["Languages"][0]["LanguageCode"]
            # traducimos
            result_translate = translate.translate_text(
                Text=result['Item']['text'],
                SourceLanguageCode=sourceLanguage,
                TargetLanguageCode=language)
            return result_translate.get('TranslatedText')
