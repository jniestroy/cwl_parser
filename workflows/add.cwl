#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: CommandLineTool
baseCommand: ["python3","/add.py"]

inputs:
  x:
    type: int
    inputBinding:
      position: 1
  y:
    type: int
    inputBinding:
      position: 2

stdout: ans.txt
outputs:
  answer:
    type: stdout
