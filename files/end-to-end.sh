#!/bin/bash


# run the command
python overlap_v0.py input.txt new_output.txt
# compare the outputs
cmp output.txt new_output.txt && echo 'passes'
