# example interview

Kubernetes service: GKE

Language: Python

Library: Flask, kubernetes client

## Project structured:

![Untitled](media/Untitled.png)

1. Data_processor(Rust project): include source  code and Dockerfile
2. Job_manager: provide api help us manage job in k8s, include source code and Dockerfile
3. Deployment: include config file to deploy service to k8s system

## Feature and how to test

- API create a job in k8s: http://jobs-manager-stag.itv-example.today/jobs

```bash
curl --location --request POST 'http://jobs-manager-stag.itv-example.today/jobs' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "test10"
}'
```

- API get all jobs in k8s: http://jobs-manager-stag.itv-example.today/jobs/stats

```bash
curl --location --request GET 'http://jobs-manager-stag.itv-example.today/jobs/stats'
```

- API create a  schedule job in k8s: http://jobs-manager-stag.itv-example.today/jobs/schedule

By default the schedule is: /1 * * * * (1 minute run 1 time)

```bash
curl --location --request POST 'http://jobs-manager-stag.itv-example.today/jobs/schedule' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "test6"
}'
```

- API health check of Job manager service: http://jobs-manager-stag.itv-example.today/health_check

Or you can import my postman collection I attach in repo.

example.postman_collection.json

## Response structured:

Response include: 

- List of normal jobs ("jobtype": "normal")
- List of Schedule jobs ("jobtype": "schedule")

```jsx
{
		"Normal_Job_name": {
				"jobtype": "normal",
				....
		},
		"Schedule_Job_name": [
				"Child_Schedule_Job_name": {
						"jobtype": "Schedule",
						....
				},
		]
}
```

Example:

```jsx
{
    "test10": {
        "failed": 1,
        "jobtype": "normal",
        "succeeded": 1,
        "uuid": "bdabbf8e-3256-49f9-a8a6-6ee0b6a6df59"
    },
    "test12": {
        "failed": 2,
        "jobtype": "normal",
        "succeeded": 1,
        "uuid": "582c5553-09d5-40a3-81fe-5747c9eb5627"
    },
    "test6": [
        {
            "failed": 3,
            "jobtype": "schedule",
            "name": "test6-27768142",
            "succeeded": 0,
            "uuid": "91e63c33-6069-46ee-9841-3a6a4bf98a47"
        },
        {
            "failed": 2,
            "jobtype": "schedule",
            "name": "test6-27768144",
            "succeeded": 1,
            "uuid": "01042270-ee43-4143-9e67-6e4d64fc454c"
        }
    ]
}
```

**My opinion How to monitor Jobs in real world:**

We should collect metrics data and visualize all of them in Dashboard, after that I will setup alert when Job fail or pending. Also we can collect some important information like: how much data import successful or fail. 

This architecture help us achieve that:

![Untitled](media/Untitled%201.png)

For long time endpoint like: Kubernetes Node, Service(backend, frontend) , Database. We chose pull architecture, so prometheus connect and pull metrics from them. 

For short time like jobs, it is difficult for us to determine when the job is done. That why I chose push architecture. When job complete, job push metrics to prometheus push gateway then prometheus server will connect and pull all of metrics above. 

You can set notification’s rule depending on your demand. Prometheus allow you config and customize, it is very flexible and stong.

When you have enough metrics about your system, your jobs. Grafana will help you visualize all of them in Grafana dashboard. It’s very clear and beautiful chart. 

For example:

- K8s monitor:

![Untitled](media/Untitled%202.png)

- Jobs monitor:

![Untitled](media/Untitled%203.png)

**My opinion about fault tolerance and scalability:**

Kubernetes help us easy to achieve horizontal scale by config limit, request of memory and cpu (resource quotas) of each job. The  limit, request of memory and cpu help k8s allocate resources more accurately. For example: instead of running all in one node, kubernetes will distribute the load evenly among all nodes. For services like backend, frontend, you can setup Pod horizontal auoscale.

If all nodes are overloaded , we should turn on node auto scale and config rule of node auto scale

**For fault tolerance:** 

- multiple instances for each service and multiple nodes in cluster
- Load balance from into services
- Storage & backups system
- We should have centralized log collection and tracing system to support trade off and check detail of issue
- WE should have apply an  architecture for monitor system help us know if the system is working properly.
- Apply risk management life cycle (Checklist to prepare before incident, automation some task when incident happen,  take a lesson learn from it)
- And another important thing is the system's recovery ability

## How to run 100 jobs in parallel:

In template to create kubernetes Job, we have two mode to run parallel jobs:

- completions mode: how many completions do you want in this jobs.
- parallelism: how many jobs do you want to run parallel

Ex:

"completions": 10, 
"parallelism": 10,

k8s will run this job until archive 10 completions, on that moment 10 job will run parallel

Or if you want to run **100 different jobs** in parallel, i will write a new api for you to do this. In this API, I will prepare  100 different jobs template with different images and then use python kubernetes client to create 100 different jobs in parallel

## Cluster management

I used these tools to manage the k8s cluster: 

- Rancher to access k8s
- Monitor tool: Prometheus + Grafana
- Secret management: Key vault
- Logging system: Fluent bit, Fluentd → Es ← Kibana (query log)
- Tracing: Opentelemetry → AWS XRay
- Manage k8s event: Sloop
- Load balance insight K8s cluster: Nginx ingress controller or Kong ingress gateway
- Helm chart to package and deploy service  to k8s
- CICD tools: Jenkins, ArgoCD, Gitlab
- Divide nodes into auto scale groups to serve separate tasks, and put labels on the nodes to avoid the case that some services when scaling, or fail, will affect other services