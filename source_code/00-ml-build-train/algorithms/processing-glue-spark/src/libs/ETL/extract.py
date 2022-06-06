"""
This sample is non-production-ready template
© 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
http://aws.amazon.com/agreement or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import boto3
import io
import logging
import pandas as pd
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.resource("s3")
s3_client = boto3.client('s3')

def extract_data(s3_bucket_name, s3_bucket_prefix):
    files = list_objects(s3_bucket_name, s3_bucket_prefix)
    logger.info("{}".format(files))

    return_value = {}

    for file in files:
        csv_obj = s3_client.get_object(Bucket=s3_bucket_name, Key=file)

        body = csv_obj['Body']

        logger.info("Reading CSV file from: {}".format(file))

        df = pd.read_csv(
            io.BytesIO(body.read()),
            sep=";",
            error_bad_lines=False,
            index_col=0,
            parse_dates=True,
            decimal=","
        )

        return_value[file] = df

    df = return_value[list(return_value.keys())[0]]

    return "processed.csv", df

def list_objects(s3_bucket_name, s3_bucket_prefix):
    try:
        bucket = s3.Bucket(s3_bucket_name)

        objects = []

        for obj in bucket.objects.filter(Prefix="{}/".format(s3_bucket_prefix)):
            if obj.key.split("/")[-1] != "":
                objects.append(obj.key)

        logger.info("Bucket: {}".format(s3_bucket_name))
        logger.info("Prefix: {}".format(s3_bucket_prefix))
        logger.info("Objects number: {}".format(len(objects)))

        return objects
    except Exception as e:
        stacktrace = traceback.format_exc()
        logger.error("{}".format(stacktrace))
