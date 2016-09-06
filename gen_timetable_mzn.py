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

print "reading in..."

## READ INPUTS FROM XLSX FILE
wb = xlrd.open_workbook('./classes_input.xlsx')		# name is fixed
ws = wb.sheet_by_index(0)							# Sheet1 is fixed

classes = map(str, ws.row_values(0))[1:]			# list of classes, first col is label 'Subject'
numClasses = len(classes)
numSlots = ws.nrows-1		# arbitrary and emperical -> equal to number of distinct subjects

# initialize teachers_assignments, an empty list numClasses no of lists
teachers_assignments = [[] * 1 for i in range(numClasses)]
teacher_avatars = ['--']
teacher_ids = [0]

# Now we read in row by row, ignoring the first col
# Read into 2 dictionaries - 
# one will map distinct ['teacher names'] to a single ID (which will be the first id it is given)
# and another which will map teacher_id to ['teacher names'] 
# this one will map more than one ID to a name, allowing for multiple teacher avatars
t2id = {}
id2t = {}

# initialize the EMPTY category (empty slot) with ID 0  (dummy teacher avatar)
id2t[0] = '--'
t_id = 0		# initialize id to 0, this will promptly be increased to 1 at the first run of the next loop. 0 if forbidden and reserved

# loop through the teacher names for rows which have values (ws.nrows is the upper limit)
for r in range(1, ws.nrows):
	excel_row = map(str, ws.row_values(r))[1:]
	# Now iterate through excel_row and put the entries in the dictionaries
	for classID, teacher in enumerate(excel_row):
		# increment t_id and update id2t to map t_id to 'teacher'
		if (teacher != ''):
			t_id += 1
			id2t[t_id] = teacher
			teacher_avatars.append(teacher)
			# And now we append the current teacher_id into the list keeping track of it
			teachers_assignments[classID].append(t_id)
			# check if the id exists already, if so append to teacher_ids
			try:
				if (t2id[teacher]):
					# this is the case where the id exists previously
					# so append to teacher_ids the value of t2id[teacher]
					teacher_ids.append(t2id[teacher])
			except KeyError:
				# there is no key for this teacher, so create it
				t2id[teacher] = t_id
				teacher_ids.append(t_id)


## Generate the dzn file
f_dzn = open('data.dzn', 'w')
f_dzn.write('numSlots = ' + str(numSlots) + ';\n')

# TODO: write the timeslots using a for loop
time_hour = 8
time_min = 50
timeslot_interval = 10	# minutes

f_dzn.write('timeSlots = [')
for i in range(numSlots):
	if (time_min + 10 == 60):
		time_min = 0
		time_hour += 1
	else:
		time_min += 10

	f_dzn.write('"' + str(time_hour) + ":" + str(time_min) + '", ')

f_dzn.write('];\n')

# write teacher avatars
f_dzn.write('num_avatars = ' + str(t_id+1) + ';\n')
f_dzn.write('teacher_avatars = [')
for avatar in teacher_avatars:
	f_dzn.write('"' + avatar + '", ')

f_dzn.write('];\n')

# teacher_ids - very important so that there are no conflicts between the same teachers
f_dzn.write('teacher_ids = [')
for t in teacher_ids:
	f_dzn.write(str(t) + ', ')

f_dzn.write('];\n')

# TODO: How to handle coordinators, special cases?

# subjects
f_dzn.write('teachers_assignments = [')
for cl in range(numClasses):
	f_dzn.write('{')
	for x in teachers_assignments[cl]:
		f_dzn.write(str(x) + ', ')
	f_dzn.write('},')

f_dzn.write('];\n')

# classes and names
f_dzn.write('numClasses = ' + str(numClasses) + ';\n')
f_dzn.write('class_names = [')
for cl in classes:
	f_dzn.write('"' + cl + '",')

f_dzn.write('];\n')

# finally close the file and it's ready to roll
f_dzn.close()
print "generated the minizinc data.dzn file successfully!"

'''
 * RUN THE CODE AND PRODUCE OUTPUT, CLEANUP AFTERWARDS
 -----------------------------------------------------------------------------------------------
 ***********************************************************************************************
'''
# Run the bash script runmzn.sh specifically designed to run this particular model with the dzn file
# And dump the contents into a file out.txt
print "running model on minizinc..."
import subprocess
subprocess.call(['./runmzn.sh'])

print "success! Now generating the excel file..."

## READ IN INPUTS FROM MZN OUTPUT FILE
f = open('out.txt')

# Then we read each class's assignments in order
teachers = []	# will be a list of lists, containing each class's teacher assignments
f.readline()		# dummy first line

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
	ws.append([ id2t[int(teachers[i][j])] for i in range(numClasses) ])

wb.save(filename = filename)


print "Finished! Please check the file timetable.xlsx for the final output!"