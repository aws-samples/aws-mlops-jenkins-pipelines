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
from libs.ETL import extract, load, transform
from libs.utils import utils
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

s3 = boto3.resource("s3")
s3_client = boto3.client('s3')

if __name__ == '__main__':
    args = getResolvedOptions(sys.argv, ["input", "output"])

    input_path = args["input"]
    output_path = args["output"]

    s3_input_bucket_name, s3_bucket_input_prefix = utils.split_s3_path(input_path)
    s3_output_bucket_name, s3_bucket_output_prefix = utils.split_s3_path(output_path)

    # s3_input_bucket_name, s3_bucket_input_prefix = utils.split_s3_path("s3://isengard-bpistone-mlops-jenkins-project-sandbox/input/data")
    # s3_output_bucket_name, s3_bucket_output_prefix = utils.split_s3_path("s3://isengard-bpistone-mlops-jenkins-project-sandbox/output/data")

    file_name, df = extract.extract_data(s3_input_bucket_name, s3_bucket_input_prefix)

    training_data, test_data = transform.clean_data(df)

    load.load_data(training_data, s3_output_bucket_name, s3_bucket_output_prefix + "/train", "train.json")
    load.load_data(test_data, s3_output_bucket_name, s3_bucket_output_prefix + "/test", "test.json")
