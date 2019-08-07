#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: Workflow

requirements:
  DockerRequirement:
    dockerPull: jniestroy/recreate-figure

inputs:
  input_data:
    type: File


outputs:
  final_figure:
    type: File
    outputSource: create_fig/figure


steps:
  cleandata:
    run: clean_data.cwl
    in:
      file: input_data
    out:
    - answer
  create_fig:
    run: make_fig.cwl
    in:
      clean: cleandata/answer
    out:
    - figure
