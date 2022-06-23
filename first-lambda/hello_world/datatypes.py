import time
import os
import random

global_random_val = random.random()


def cold_start_basics(event, context):
    local_random_val = random.random()
    print(local_random_val)
    print(global_random_val)


def simple_types(event, context):
    print(event)
    return event


def list_types(event, context):
    print(event)
    students_scores = {'jrm2087': 100, 'jdrodrig': 88}
    scores = []
    for name in event:
        scores.append(students_scores[name])
    return scores


def dict_types(event, context):
    print(event['jrm2087'])
    return event


def lambda_handler(event, context):
    print("Lambda function ARN:", context.invoked_function_arn)
    print("CloudWatch log stream name:", context.log_stream_name)
    print("CloudWatch log group name:", context.log_group_name)
    print("Lambda Request ID:", context.aws_request_id)
    print("Lambda function memory limits in MB:", context.memory_limit_in_mb)
    time.sleep(4)
    print("Lambda time remaining in MS:", context.get_remaining_time_in_millis())
    # variables de entorno
    print('restapiurl', os.getenv('restapiurl'))
    print('dbname', os.getenv('dbname'))
