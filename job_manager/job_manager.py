import os
import base64
from copy import deepcopy
from kubernetes import client
from tempfile import NamedTemporaryFile

from template.normal_job_template import JOB_TEMPLATE
from template.schedule_job_template import CRONJOB_TEMPLATE

HOST_URL = os.environ["HOST_URL"]
CACERT = os.environ["CACERT"]
TOKEN = os.environ["TOKEN"]
MANAGED_BY_LABEL = "JobManager"

class JobManager:
    def __init__(self):
        configuration = client.Configuration()
        with NamedTemporaryFile(delete=False) as cert:
            cert.write(base64.b64decode(CACERT))
            configuration.ssl_ca_cert = cert.name
        configuration.host = HOST_URL
        configuration.verify_ssl = True
        configuration.debug = False
        configuration.api_key = {"authorization": "Bearer " + TOKEN}
        client.Configuration.set_default(configuration)
        self.client = client.BatchV1Api()

    def create_job(self, name, image):
        payload = deepcopy(JOB_TEMPLATE)
        payload["metadata"]["name"] = name
        payload["metadata"]["labels"]["managedBy"] = MANAGED_BY_LABEL
        payload["metadata"]["labels"]["jobManagedID"] = name
        payload["spec"]["template"]["spec"]["containers"][0]["name"] = name
        payload["spec"]["template"]["spec"]["containers"][0]["image"] = image

        rv = self.client.create_namespaced_job(
            namespace="default",
            body=payload,
        )
        return rv

    def get_all_job(self, name=None, offset=0, limit=None):
        reponse = self.client.list_namespaced_job(namespace="default")
        map = {}
        for job in reponse.items:
            succeeded = 0
            if hasattr(job.status, "succeeded"): 
                succeeded = job.status.succeeded or 0

            failed = 0
            if hasattr(job.status, "failed"): 
                failed = job.status.failed or 0
            
            if not "jobManagedID" in job.metadata.labels:
                continue
            
            if job.metadata.labels["jobType"] == "normal":
                map[job.metadata.labels["jobManagedID"]] = {
                    "uuid": job.metadata.uid,
                    "jobtype": "normal",
                    "succeeded": succeeded, 
                    "failed": failed
                    }
                continue
    
            if job.metadata.labels["jobManagedID"] not in map:
                map[job.metadata.labels["jobManagedID"]] = [
                    {
                        "name": job.metadata.name,
                        "jobtype": "schedule",
                        "uuid": job.metadata.uid,
                        "succeeded": succeeded, 
                        "failed": failed
                    }
                ]
            else:
                map[job.metadata.labels["jobManagedID"]].append(
                    {
                        "name": job.metadata.name,
                        "jobtype": "schedule",
                        "uuid": job.metadata.uid,
                        "succeeded": succeeded, 
                        "failed": failed
                    }
                )
        return map

    def create_cronjob(self, name, image):
        payload = deepcopy(CRONJOB_TEMPLATE)
        payload["metadata"]["name"] = name
        payload["metadata"]["labels"]["managedBy"] = MANAGED_BY_LABEL
        payload["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["name"] = name
        payload["spec"]["jobTemplate"]["spec"]["template"]["spec"]["containers"][0]["image"] = image
        payload["spec"]["jobTemplate"]["spec"]["template"]["metadata"]["labels"]["jobManagedID"] = name

        rv = self.client.create_namespaced_cron_job(
            namespace="default",
            body=payload,
        )
        return rv