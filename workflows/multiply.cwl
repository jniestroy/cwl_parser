#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3", "/Users/justinniestroy-admin/Documents/Work/Randall Data/houlter data/multiply.py"]

inputs:
  x:
    type: int
    inputBinding:
      position: 1
  y:
    type: int
    inputBinding:
      position: 2



outputs:
  answer:
    type: stdout
stdout: output_test1.txt
