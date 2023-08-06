import os
import sys
import concurrent.futures
import logging
import gzip
from concurrent.futures._base import TimeoutError
from google.pubsub_v1 import PubsubMessage
from google.cloud.pubsublite.cloudpubsub import SubscriberClient
from google.cloud.pubsublite.types import (
    CloudRegion,
    CloudZone,
    FlowControlSettings,
    MessageMetadata,
    SubscriptionPath,
)

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../api", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../api", "..", "..", "..")))
from netskope_api.webtxn.const import Const

_logger = logging.getLogger()

THREAD_COUNT = None


def callback_decompress_data(message: PubsubMessage):
    _logger.info("Received txn log message {} ".format(message))
    decompressed_msg = gzip.decompress(message.data)
    _logger.info("Decompressed txn log message {} ".format(decompressed_msg))
    message.ack()


def callback(message: PubsubMessage):
    _logger.info("Received txn log message {} ".format(message))
    message.ack()


def make_default_thread_pool_executor(thread_count=THREAD_COUNT):
    return concurrent.futures.ThreadPoolExecutor(max_workers=thread_count)


class NetskopeSubscriberClient:
    def __init__(self, params):
        """

        :param params:
        """

        configs = {
            "subscription_path": params.get(Const.NSKP_SUBSCRIPTION_PATH),
            "subscription_key": params.get(Const.NSKP_SUBSCRIPTION_KEY),
            "cloud_region": params.get(Const.NSKP_CLOUD_REGION),
            "zone_id": params.get(Const.NSKP_ZONE_ID),
            "project_number": params.get(Const.NSKP_PROJECT_NUMBER),
            "subscription_id": params.get(Const.NSKP_SUBSCRIPTION_ID),
            "timeout": params.get(Const.NSKP_TIMEOUT),
            "thread_count": params.get(Const.NSKP_THREAD_COUNT, Const.NSKP_MIN_THREAD_COUNT),
            "messages_outstanding": params.get(Const.NSKP_OUTSTANDING_MESSAGES, Const.NSKP_MIN_OUT_MESSAGES),
            "bytes_outstanding": params.get(Const.NSKP_OUTSTANDING_BYTES, Const.NSKP_MIN_OUT_BYTES),
            "regional": params.get(Const.NSKP_REGIONAL, Const.NSKP_DEFAULT_REGIONAL),
            "decompress_data": params.get(Const.NKSP_DECOMPRESS_DATA, Const.NKSP_DEFAULT_DECOMPRESS_DATA)
        }
        self.configs = configs
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.configs.get("subscription_key")

    def get_subscription_path(self):
        subscription_path = self.configs.get("subscription_path")
        if subscription_path:
            return subscription_path
        else:
            cloud_region = self.configs.get("cloud_region")
            zone_id = self.configs.get("zone_id")
            project_number = self.configs.get("project_number")
            subscription_id = self.configs.get("subscription_id")
            regional = self.configs.get("regional")
            location = None
            if regional:
                location = CloudRegion(cloud_region)
            else:
                location = CloudZone(CloudRegion(cloud_region), zone_id)
            subscription_path = SubscriptionPath(project_number, location, subscription_id)
            return subscription_path

    def stream(self):
        global streaming_pull_future

        per_partition_flow_control_settings = FlowControlSettings(
            # Must be >0.
            messages_outstanding=self.configs.get("messages_outstanding"),
            # Must be greater than the allowed size of the largest message.
            bytes_outstanding=self.configs.get("bytes_outstanding"),
        )
        thread_count = self.configs.get('thread_count')
        subscription_path = self.get_subscription_path()
        executor = make_default_thread_pool_executor(thread_count=thread_count)
        decompress_data = self.configs.get("decompress_data")
        if decompress_data:
            with SubscriberClient(executor=executor) as subscriber_client:

                streaming_pull_future = subscriber_client.subscribe(
                    subscription_path,
                    callback=callback_decompress_data,
                    per_partition_flow_control_settings=per_partition_flow_control_settings,
                )

                _logger.info(
                    "Listening for messages on the pub sub lite subscription {}".format(str(subscription_path)))
                try:
                    timeout = self.configs.get("timeout")
                    if timeout:
                        streaming_pull_future.result(timeout=self.configs.get("timeout"))
                    else:
                        streaming_pull_future.result()
                except TimeoutError or KeyboardInterrupt:
                    streaming_pull_future.cancel()
                    assert streaming_pull_future.done()
        else:
            with SubscriberClient(executor=executor) as subscriber_client:

                streaming_pull_future = subscriber_client.subscribe(
                    subscription_path,
                    callback=callback,
                    per_partition_flow_control_settings=per_partition_flow_control_settings,
                )

                _logger.info(
                    "Listening for messages on the pub sub lite subscription {}".format(str(subscription_path)))
                try:
                    timeout = self.configs.get("timeout")
                    if timeout:
                        streaming_pull_future.result(timeout=self.configs.get("timeout"))
                    else:
                        streaming_pull_future.result()
                except TimeoutError or KeyboardInterrupt:
                    streaming_pull_future.cancel()
                    assert streaming_pull_future.done()
