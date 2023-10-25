import logging

from spaceone.inventory.libs.connector import AWSConnector
from spaceone.inventory.libs.connector import *

_LOGGER = logging.getLogger(__name__)


class JobConnector(AWSConnector):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.set_connect(kwargs.get('secret_data'))

    def get_regions(self):
        _session = get_session(self.secret_data, DEFAULT_REGION)
        ec2_client = _session.client('ec2', verify=BOTO3_HTTPS_VERIFIED)

        return list(map(lambda region_info: region_info.get('RegionName'),
                        ec2_client.describe_regions().get('Regions')))