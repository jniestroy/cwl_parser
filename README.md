# cwl_parser

Repo contains wf parser, wf upload to minio, and workflow runner

3 Endpoints in main file

run-wf:
  takes in cwl file name to be pulled from minio and job file
  both cwl workflow and job file must be posted to minio before you can run the workflow
  example: 
    test = {"workflow":"clean_data.cwl","job":"fig.yaml"}
    req = requests.post("http://localhost:5002/run-wf",json = test)
    
post-wf:
  posts cwl workflow and accompnanying commandLineTools to minio, workflow must be first file posted
  example:
     url = 'http://localhost:5002/post-wf'
     files = {'test_workflow.cwl': open('/Users/justinniestroy-admin/Documents/Work/cwl_parser/workflows/test_workflow.cwl',        'rb'),
     'add.cwl':open('/Users/justinniestroy-admin/Documents/Work/cwl_parser/workflows/add.cwl', 'rb'),
     'multiply.cwl':open('/Users/justinniestroy-admin/Documents/Work/cwl_parser/workflows/multiply.cwl', 'rb')
        }

      r = requests.post(url, files=files)
post-job:
  same as above but with job files 
  example:
    url = 'http://localhost:5002/post-job'
    files = {'test.yaml': open('/Users/justinniestroy-admin/Documents/Work/cwl_parser/workflows/test_job.yaml', 'rb')}
    r = requests.post(url, files=files)
