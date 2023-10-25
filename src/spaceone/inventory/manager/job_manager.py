import logging

from spaceone.inventory.connector.job_connector import JobConnector
from spaceone.inventory.libs.manager import AWSManager

_LOGGER = logging.getLogger(__name__)


class JobManager(AWSManager):
    connector_name = "JobConnector"

    def get_regions(self,params):
        job_conn: JobConnector = self.locator.get_connector(self.connector_name, **params)
        return job_conn.get_regions()
