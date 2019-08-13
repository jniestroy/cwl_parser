#!/usr/bin/env cwl-runner
cwlVersion: v1.0
class: Workflow
inputs:
  num1: int
  num2: int
outputs:
  final_answer:
    type: File
    outputSource: multiply/answer
    schema:type: ImageObject
    schema:author:
      schema:type: Person
      schema:name: Justin Niestroy
      schema:memberOf: UVa
      schema:identifier: https://orcid.org/0000-0002-1103-3882
      schema:email: jcn4rh@virgnia.edu

steps:
  add:
    run: add.cwl
    in:
      y: num2
      x: num1
    out:
    - answer
  multiply:
    run: multiply.cwl
    in:
      y: num2
      x: add/answer
    out:
    - answer
$namespaces:
  schema: http://schema.org/

$schemas:
- http://edamontology.org/EDAM_1.16.owl
- http://schema.org/docs/schema_org_rdfa.html
