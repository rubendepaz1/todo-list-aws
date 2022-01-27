import json
import decimalencoder
import translate


def getTranslate(event, context):
    # create a response
    item = translate.get_item_translated(event['pathParameters']['id']['language'])
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
