import time
import logging
import json
import concurrent.futures

from spaceone.core.service import *
from spaceone.inventory.conf.cloud_service_conf import *

_LOGGER = logging.getLogger(__name__)


@authentication_handler
class JobService(BaseService):

    def __init__(self, metadata):
        super().__init__(metadata)

    @check_required(["secret_data", "options"])
    def get_tasks(self, params):
        services = CLOUD_SERVICE_GROUP_MAP.keys()
        _manager = self.locator.get_manager('EC2ConnectorManager')
        regions = _manager.get_regions(**params)
        mappings = []
        for service in services:
            if service in ['CloudFront', 'IAM', 'CloudTrail', 'Route53', 'S3']:
                mappings.append({'task_options': {'region_name': DEFAULT_REGION, 'service': service}})
            else:
                for region in regions:
                    mappings.append({'task_options': {'region_name': region, 'service': service}})
        return {'tasks': mappings}
