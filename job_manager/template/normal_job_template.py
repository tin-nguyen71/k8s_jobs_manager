JOB_TEMPLATE = {
    "apiVersion": "batch/v1",
    "kind": "Job",
    "metadata": {"name": None, "labels": {"managedBy": None, "jobManagedID": None, "jobType": "normal"}},
    "spec": {
        "backoffLimit": 2,
        "parallelism": 1,
        "completions": 1,
        "template": {
            "spec": {
                "restartPolicy": "Never",
                "containers": [
                    {"name": None, "image": None, "imagePullPolicy": "IfNotPresent"}
                ],
            }
        },
    },
}