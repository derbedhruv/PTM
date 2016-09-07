# Constraint Optimization
Parent Teacher Meeting scheduling Constraint optimization

(This project was done as volunteer work for a high school, the code and live program is available for anyone to use under the [MIT license](https://opensource.org/licenses/MIT))

Using [Minizinc](http://minizinc.org/) to solve the NP-hard problem of scheduling timings for parent-teacher meetings in designated slots at a high school. Pre-processing, parsing information and generation of the minizinc code is done using python.

A sample XLSX input file is given as `classes_input.xlsx`.

To run simply run the file `gen_timetable_mzn.py`.

 * This would first generate the file data.dzn, which is a parsing of the information from a fixed excel file `classes_input.xlsx`  to a format usable by minizinc.
 * Next, the same python script calls `runmzn.sh` which is an executable within the same repo. This runs the model on minizinc (which should be installed and in $PATH)
 * Minizinc's output is redirected into `out.txt` which is then read in and parsed by the python file
 * This information is then stored into a freshly created excel `timetable.xlsx` in a usable format, which should have the timetable schedule which satisfies the given constraints.

UPDATE: Have added a simple flask-based server, where one uploads an XLSX file and the program spits out an XLSX file after processing it on server using python. A lightweight demo of the same is at [ptm.derbedhruv.webfactional.com](http://ptm.derbedhruv.webfactional.com)