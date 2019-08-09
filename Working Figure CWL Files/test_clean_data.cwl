#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3","/Figure WF Files/data_cleaning.py"]


inputs:
  file:
    type: File
    inputBinding:
      position: 1
outputs:
  answer:
    type: File
    outputBinding:
      glob: clean.csv
