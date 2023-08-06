import sys
import os
import re

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../api", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../api", "..", "..", "..")))
from netskope_api.webtxn.netskope_subscriber_client import NetskopeSubscriberClient
from netskope_api.webtxn.const import Const


class NetskopeSubscriber:
    """Pub Sub client for netskope web transaction"""

    # Create the pub sub client
    def __init__(self, params):
        self.validate_params(params)
        self.client = NetskopeSubscriberClient(params)

    def validate_params(self, params):
        """
        Validate all the input parameters.
        :param params:
        :return:
        """
        if params.get(Const.NSKP_SUBSCRIPTION_KEY, None) is None:
            raise ValueError("Subscription key must be a valid string value")
        if params.get(Const.NSKP_SUBSCRIPTION_PATH, None) is None:
            if (params.get(Const.NSKP_CLOUD_REGION, None)) is None:
                raise ValueError("cloud region must be a valid string value")
            if (params.get(Const.NSKP_REGIONAL, Const.NSKP_DEFAULT_REGIONAL)) is False:
                # Zone Id is mandatory param if Reginal flag is not set.
                if (params.get(Const.NSKP_ZONE_ID, None)) is None:
                    raise ValueError("zone id must be a valid string value")
            if (params.get(Const.NSKP_PROJECT_NUMBER, None)) is None:
                raise ValueError("project number must be a valid string value")
            if (params.get(Const.NSKP_SUBSCRIPTION_ID, None)) is None:
                raise ValueError("subscription id must be a valid string value")
        else:
            self.validate_lite_subscription(params.get(Const.NSKP_SUBSCRIPTION_PATH))

            # check pub sub lite subscription format

    def validate_lite_subscription(self, path):
        regex = r"^projects/[^/]+/locations/[^/]+/subscriptions/[^/]+$"

        if not re.match(regex, path):
            raise ValueError("Incorrect Subscription path format. Valid format: "
                             "projects/<project-id>/locations/<region-id>-<zone-id>/subscriptions/<subscription-name>")

    def collect_events(self):
        """
        Stream events from pub sub lite.
        """
        return self.client.stream()
