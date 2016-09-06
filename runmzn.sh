#!/bin/sh
cd "${0%/*}"
minizinc timetable.mzn data.dzn > out.txt
