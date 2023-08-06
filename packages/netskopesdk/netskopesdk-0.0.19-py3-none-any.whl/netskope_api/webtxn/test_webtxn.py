import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../api", "..")))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, "../api", "..", "..", "..")))
from netskope_api.webtxn.netskope_subscriber import NetskopeSubscriber
from netskope_api.webtxn.const import Const
import pytest

def test_valid_parameters():
    params = {
        Const.NSKP_PROJECT_NUMBER : 11111111,
        Const.NSKP_CLOUD_REGION : "us-west1",
        Const.NSKP_ZONE_ID : "a",
        Const.NSKP_SUBSCRIPTION_ID : "web_txn_sdk_subscription",
        Const.NSKP_REGIONAL : False,
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params) is None

# Regional = True doesn't need Zone Id
def test_valid_parameters_2():
    params = {
        Const.NSKP_PROJECT_NUMBER : 11111111,
        Const.NSKP_CLOUD_REGION : "us-west1",
        Const.NSKP_SUBSCRIPTION_ID : "web_txn_sdk_subscription",
        Const.NSKP_REGIONAL : True,
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params) is None

def test_valid_parameters_with_subs_path():
    params = {
        Const.NSKP_SUBSCRIPTION_PATH : "projects/11111111/locations/us-west1-a/subscriptions/test-goskope-sub-streaming-0000",
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params) is None

# wrong format for subs path
@pytest.mark.xfail(raises=ValueError)
def test_invalid_parameters_with_subs_path():
    params = {
        Const.NSKP_SUBSCRIPTION_PATH : "projects/11111111/location/us-west1-a/subscription/test-goskope-sub-streaming-0000",
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params) is None

@pytest.mark.xfail(raises=ValueError)
def test_invalid_missing_project_number_parameters():
    params = {
        Const.NSKP_CLOUD_REGION : "us-west1",
        Const.NSKP_SUBSCRIPTION_ID : "web_txn_sdk_subscription",
        Const.NSKP_REGIONAL : False,
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params)

@pytest.mark.xfail(raises=ValueError)
def test_invalid_missing_sub_key_parameters():
    params = {
        Const.NSKP_PROJECT_NUMBER : 11111111,
        Const.NSKP_CLOUD_REGION : "us-west1",
        Const.NSKP_SUBSCRIPTION_ID : "web_txn_sdk_subscription",
        Const.NSKP_REGIONAL : False,
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params)

@pytest.mark.xfail(raises=ValueError)
def test_invalid_missing_zone_key_parameters():
    params = {
        Const.NSKP_PROJECT_NUMBER : 11111111,
        Const.NSKP_CLOUD_REGION : "us-west1",
        Const.NSKP_SUBSCRIPTION_ID : "web_txn_sdk_subscription",
        Const.NSKP_REGIONAL : False,
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params)

# REGIONAL Default value is false
@pytest.mark.xfail(raises=ValueError)
def test_invalid_missing_zone_key_parameters_2():
    params = {
        Const.NSKP_PROJECT_NUMBER : 11111111,
        Const.NSKP_CLOUD_REGION : "us-west1",
        Const.NSKP_SUBSCRIPTION_ID : "web_txn_sdk_subscription",
        Const.NSKP_SUBSCRIPTION_KEY : "test_sub_key"
    }
    subscriber= NetskopeSubscriber(params)
    assert subscriber.validate_params(params)
