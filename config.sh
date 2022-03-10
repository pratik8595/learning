#!/bin/bash

 a=$(cat asginput.txt | grep existing_asg | awk '{print $NF}') 
 b=$(cat asginput.txt | grep replace_by | awk '{print $NF}')
 sed  -i "s/$a/$b/g" updateASG.py
