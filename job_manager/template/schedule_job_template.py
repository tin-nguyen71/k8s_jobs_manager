CRONJOB_TEMPLATE = {
    "apiVersion": "batch/v1",
    "kind": "CronJob",
    "metadata": {"name": None, "labels": {"managedBy": None}},
    "spec": {
        "schedule": "*/1 * * * *",
        "jobTemplate": {
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "jobManagedID": None,
                            "jobType": "schedule"
                        }
                    },
                    "spec": {
                        "containers": [
                            {
                                "name": None,
                                "image": None,
                            }
                        ],
                        "restartPolicy": "Never",
                    }
                },
                "parallelism": 1,
                "completions": 1,
                "backoffLimit": 2,
            }
        },
        "concurrencyPolicy": "Allow",
        "successfulJobsHistoryLimit": 3,
        "failedJobsHistoryLimit": 3,
    },
}