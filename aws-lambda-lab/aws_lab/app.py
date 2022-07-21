import os
import json
import csv
import logging
import boto3

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
    name, extension = os.path.splitext(str(file_key))
    logger.info(f'name -> {name}')
    logger.info(f'extension -> {extension}')

    if str(file_key).find('/') >= 0:
        logger.error(str(file_key).find('/'))
        logger.error('No es la ruta raiz')
        return

    # obtemos contenido archivo json
    file_content = obj['Body'].read().decode('utf-8')
    data_json = json.loads(file_content)

    # generamos archivo para escribir
    data_file = open('/tmp/data.csv', 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(data_file)

    count = 0
    for data in data_json:
        if count == 0:
            header = data.keys()
            csv_writer.writerow(header)
            count += 1
        csv_writer.writerow(data.values())
    data_file.close()

    # Leemos el archivo y lo ponemos en la ruta del bucket
    with open('/tmp/data.csv', 'r', encoding='utf-8') as data_csv:
        s3.put_object(Bucket=bucket_name, Body=data_csv.read(), Key=f'data/{name}.csv')

    return
