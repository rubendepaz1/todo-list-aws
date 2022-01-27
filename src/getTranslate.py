import json
import decimalencoder
import todoList
import translate


def getTranslate(event, context):
    # create a response
    item = todoList.ingles(event['pathParameters']['id'])
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response