"""
This sample is non-production-ready template
© 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
http://aws.amazon.com/agreement or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

import boto3
import json
import logging
import os
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3_client = boto3.client('s3')

def load_data(data, s3_bucket_name, s3_bucket_prefix, file_name):
    try:

        logger.info("Loading data into s3://{}/{}".format(s3_bucket_prefix, os.path.join(s3_bucket_prefix, file_name)))

        curr_dir = "/tmp"

        path = os.path.join(curr_dir, file_name)

        with open(path, "wb") as fp:
            for d in data:
                fp.write(json.dumps(d).encode("utf-8"))
                fp.write("\n".encode("utf-8"))

        fp.close()

        s3_client.upload_file(path, s3_bucket_name, os.path.join(s3_bucket_prefix, file_name))

        os.remove(path)
    except Exception as e:
        stacktrace = traceback.format_exc()
        logger.error("{}".format(stacktrace))

        raise e