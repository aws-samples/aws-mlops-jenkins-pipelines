"""
This sample is non-production-ready template
© 2021 Amazon Web Services, Inc. or its affiliates. All Rights Reserved.
This AWS Content is provided subject to the terms of the AWS Customer Agreement available at
http://aws.amazon.com/agreement or other written agreement between Customer and either
Amazon Web Services, Inc. or Amazon Web Services EMEA SARL or both.
"""

from datetime import timedelta
import logging
import numpy as np
import pandas as pd
import traceback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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