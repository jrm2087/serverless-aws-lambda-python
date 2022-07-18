import boto3
import json
import logging
import pandas as pd

s3 = boto3.client('s3')
logger = logging.getLogger('lab-aws-lambda')
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info(f'event -> {event}')
    logger.info(f'context -> {context}')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    file_key = event['Records'][0]['s3']['object']['key']
    logger.info(f'Reading {file_key} from {bucket_name}')
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    file_content = obj['Body'].read().decode('utf-8')
    data_json = json.loads(file_content)

    # convertimos json a csv y movemos a data
    name = str(file_key).split('.')
    df = pd.DataFrame.from_dict(data_json)
    s3.put_object(Bucket=bucket_name, Body=df.to_csv(index=False, header=True), Key=f'data/{name[0]}.csv')

    return None
