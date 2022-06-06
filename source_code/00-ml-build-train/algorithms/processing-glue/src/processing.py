"""
/*
 * Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this
 * software and associated documentation files (the "Software"), to deal in the Software
 * without restriction, including without limitation the rights to use, copy, modify,
 * merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
 * INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
 * PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 * OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
"""

from awsglue.utils import getResolvedOptions
import boto3
from datetime import timedelta
import io
import json
import logging
import numpy as np
import os
import pandas as pd
import sys
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

glue_client = boto3.client('glue')
s3 = boto3.resource("s3")
s3_client = boto3.client('s3')

def clean_data(df):
    try:
        num_timeseries = df.shape[1]
        data_kw = df.resample("2H").sum() / 8
        timeseries = []
        for i in range(num_timeseries):
            timeseries.append(np.trim_zeros(data_kw.iloc[:, i], trim="f"))

        freq = "2H"

        # we predict for 7 days
        prediction_length = 7 * 12

        context_length = 7 * 12

        start_dataset = pd.Timestamp("2014-01-01 00:00:00", freq=freq)
        end_training = pd.Timestamp("2014-09-01 00:00:00", freq=freq)

        training_data = [
            {
                "start": str(start_dataset),
                "target": ts[
                          start_dataset: end_training - timedelta(days=1)
                          ].tolist(),  # We use -1, because pandas indexing includes the upper bound
            }
            for ts in timeseries
        ]

        logger.info(len(training_data))

        num_test_windows = 4

        test_data = [
            {
                "start": str(start_dataset),
                "target": ts[start_dataset: end_training + timedelta(days=k * prediction_length)].tolist(),
            }
            for k in range(1, num_test_windows + 1)
            for ts in timeseries
        ]
        logger.info(len(test_data))

        return training_data, test_data
    except Exception as e:
        stacktrace = traceback.format_exc()
        logger.error("{}".format(stacktrace))

        raise e

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

def split_s3_path(s3_path):
    path_parts = s3_path.replace("s3://","").split("/")
    bucket = path_parts.pop(0)
    key = "/".join(path_parts)
    return bucket, key

if __name__ == '__main__':
    args = getResolvedOptions(sys.argv, ["input", "output"])

    input_path = args["input"]
    output_path = args["output"]

    s3_input_bucket_name, s3_bucket_input_prefix = split_s3_path(input_path)
    s3_output_bucket_name, s3_bucket_output_prefix = split_s3_path(output_path)

    # s3_input_bucket_name, s3_bucket_input_prefix = split_s3_path("s3://isengard-bpistone-mlops-jenkins-project-sandbox/input/data")
    # s3_output_bucket_name, s3_bucket_output_prefix = split_s3_path("s3://isengard-bpistone-mlops-jenkins-project-sandbox/output/data")

    file_name, df = extract_data(s3_input_bucket_name, s3_bucket_input_prefix)

    training_data, test_data = clean_data(df)

    load_data(training_data, s3_output_bucket_name, s3_bucket_output_prefix + "/train", "train.json")
    load_data(test_data, s3_output_bucket_name, s3_bucket_output_prefix + "/test", "test.json")
