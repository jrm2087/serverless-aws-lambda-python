import json


def lambda_handler(event, context):
    order = {'id': 12345678, 'itemName': 'Lenovo Yoga', 'quantity': 200}
    return {
        'statusCode': 201,
        'headers': {},
        'body': json.dumps(order)
    }
