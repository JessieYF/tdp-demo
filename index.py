import json
from flask import Flask, request, jsonify
import requests
import argparse
import googleapiclient.discovery

app = Flask(__name__)

def get_client():
  """Builds a client to the container API."""
  client = googleapiclient.discovery.build('container', 'v1')
  return client

def list_clusters(client):
  result = client.projects().locations().clusters().list(
    parent='projects/techops-infradel/locations/europe-west1-c').execute()
  return jsonify(result)

def create_cluster(client, cluster_name):
  # response = requests.post("https://container.googleapis.com/v1beta1/projects/techops-infradel/locations/europe-west1-c/clusters", data={'cluster': {'name': cluster_name}})
  # return jsonify(response)
  cluster_data = {
    'cluster': {
      'name': cluster_name,
      'initialNodeCount': 1,
    }
  }
  result = client.projects().locations().clusters().create(
    parent='projects/techops-infradel/locations/europe-west1-c',
    body=cluster_data).execute()
  print(result)
  return jsonify(result)

@app.route("/")
def index():
  return "Hello World!"

@app.route("/clusters", methods=['POST', 'GET'])
def clusters():
  client = get_client()
  error = None
  if request.method == 'POST':
    # return request.data
    return create_cluster(client, request.data.decode("utf-8"))
  else:
    return list_clusters(client)
