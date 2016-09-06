# Constraint Optimization
Parent Teacher Meeting scheduling Constraint optimization

Using Minizinc(R) to solve the NP-hard problem of scheduling timings for parent-teacher meetings in designated slots at a high school. Pre-processing, parsing information and generation of the minizinc code is done using python.

To run simply run the file `gen_timetable_mzn.py`.

 * This would first generate the file data.dzn, which is a parsing of the information from a fixed excel file `classes_input.xlsx`  to a format usable by minizinc.
 * Next, the same python script calls `runmzn.sh` which is an executable within the same repo. This runs the model on minizinc (which should be installed and in $PATH)
 * Minizinc spits its output into out.txt which is then read in and parsed by the python file
 * This information is then stored into a freshly created excel `timetable.xlsx` in a usable format, which should have the timetable schedule which satisfies the given constraints.