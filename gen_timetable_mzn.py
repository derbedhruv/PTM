'''
 TIMETABLE SCHEDULER
--------------------------------------------------------------------------
 Take inputs from user about the classes and teachers as an xlsx file
 Convert this to a dzn file for minizinc
 Run the minizinc mzn file on this
 Then take the output and convert it back into an xlsx file

'''
from openpyxl import Workbook
import xlrd

## READ INPUTS FROM XLSX FILE
wb = xlrd.open_workbook('./classes_input.xlsx')		# name is fixed
ws = wb.sheet_by_index(0)							# Sheet1 is fixed

classes = map(str, ws.row_values(0))[1:]			# list of classes, first col is label 'Subject'
numClasses = len(classes)
numSlots = numClasses + 2		# arbitrary and emperical

# initialize teachers_assignments, an empty list numClasses no of lists
teachers_assignments = [[] * 1 for i in range(numClasses)]
teacher_avatars = []

# Now we read in row by row, ignoring the first col
# Read into a dictionary - which will map teacher_id to ['teacher names'] 
# this one will map more than one ID to a name, allowing for multiple teacher avatars
id2t = {}

# initialize the EMPTY category (empty slot) with ID 0  (dummy teacher avatar)
id2t[0] = '--'
t_id = 1		# initialize id to 1, since 0 is reserved

# loop through the teacher names for rows which have values (ws.nrows is the upper limit)
for r in range(1, ws.nrows):
	teachers_list = map(str, ws.row_values(r))[1:]
	# Now iterate through teachers_list and put the entries in the dictionaries
	for classID, teacher in enumerate(teachers_list):
		# increment t_id and update id2t to map t_id to 'teacher'
		if (teacher != ''):
			t_id += 1
			id2t[t_id] = teacher
			teacher_avatars.append(teacher)
			# And now we append the current teacher_id into the list keeping track of it
			teachers_assignments[classID].append(t_id)

## Generate the dzn file
f_dzn = open('data.dzn', 'w')
f_dzn.write('numSlots = ' + str(numSlots) + '\n')

# TODO: write the timeslots using a for loop

# write teacher avatars
f_dzn.write('num_avatars = ' + str(t_id) + '\n')
f_dzn.write('teacher_avatars = {')
for avatar in teacher_avatars:
	f_dzn.write(avatar + ', ')
f_dzn.write('}\n')

# TODO: How to handle coordinators, special cases?

# subjects
f_dzn.write('numSubjects = ')

## READ IN INPUTS FROM MZN OUTPUT FILE
f = open('out.txt')

# the first two lines contain numClasses and numSlots
[numClasses, numSlots] = map(int, f.readline().strip().split())

# Next line is the list of classes
classes = f.readline().strip().split()		# list of string

# Then we read each class's assignments in order
teachers = []	# will be a list of lists, containing each class's teacher assignments

for cl in range(numClasses):
	teachers.append(f.readline().strip().split())

## GENERATE EXCEL FILE REPRESENTATION OF THE SAME
wb = Workbook()
filename = 'timetable.xlsx'

ws = wb.active
ws.title = "PTM_assignments"

# start appending line by line
ws.append(classes)		# names of classes
for j in range(numSlots):
	ws.append([ teachers[i][j] for i in range(numClasses) ])

wb.save(filename = filename)