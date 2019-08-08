from flask import Flask, render_template, request, redirect,jsonify
import requests
import bash_in_python as wf_runner
import json

app = Flask(__name__)

@app.route('/', methods=['GET'])
def homepage():
    return("CWL Flask Service")

@app.route('/run-wf',methods = ['POST'])
def run_wf():
    result = {}
    #Read in Posted Data and confirm its a jsonld
    #Convert to schema.org if required
    if request.data == b'':
        return(jsonify({'error':"Please POST JSON, with workflow, job, and path to directory"}))

    try:
        given = json.loads(request.data.decode('utf-8'))
    except:
        return(jsonify({'error':"Please POST JSON, with workflow, job, and path to directory"}))
    inputs = [None,given['workflow'],given['job'],given['path']]
    return(jsonify(wf_runner.workflow(inputs)))


if __name__ == "__main__":
    app.run()
