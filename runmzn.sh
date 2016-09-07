#!/bin/bash
cd "${0%/*}"
ulimit -t 60;	# 60 seconds of CPU time
minizinc timetable.mzn data.dzn > out.txt 2>&1
