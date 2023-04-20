import json
from ast import JoinedStr
import kubernetes
from flask import Flask, jsonify, request

from job_manager import JobManager

app = Flask(__name__)
job_manager = JobManager()

@app.route('/health_check', methods=["GET"])
def health_check():
    return jsonify({"succeeded": True}), 200

@app.route('/jobs', methods=["POST"])
def create_job():
    req = request.get_json()
    if not "name" in req:
        return jsonify({
            "succeeded": False,
            "detail": "Job 'name' is requied"
            }), 400
    if not "image" in req:
        req["image"] = "nguyentin/itv-example-data-processor:v5"

    try:
        job_manager.create_job(req["name"], req["image"])
        return jsonify({
            "succeeded": True,
            "detail": "Create normal job successful"
            }), 200
    except KeyError:
        return "request schemas error" , 400
    except kubernetes.client.exceptions.ApiException as e:
        return jsonify(json.loads(e.body)) , 400

@app.route('/jobs/stats', methods=["GET"])
def get_job():
    return jsonify(job_manager.get_all_job()), 200

@app.route('/jobs/schedule', methods=["POST"])
def schedule_job():
    req = request.get_json()
    try:
        job_manager.create_cronjob(req["name"], req["image"])
        return jsonify({
            "succeeded": True,
            "detail": "Create schedule job successful"
            }), 200
    except KeyError:
        return "request schemas error" , 400
    except kubernetes.client.exceptions.ApiException as e:
        return jsonify(json.loads(e.body)) , 400

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
