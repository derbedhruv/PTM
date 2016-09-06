#!/bin/bash
cd "${0%/*}"
minizinc timetable.mzn data.dzn > out.txt 2>&1
