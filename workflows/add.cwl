#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3", "/Users/justinniestroy-admin/Documents/Work/Randall Data/houlter data/add.py"]

inputs:
  x:
    type: int
    inputBinding:
      position: 1
  y:
    type: int
    inputBinding:
      position: 2

stdout: cwl.output.json

outputs:
  answer:
    type: int
