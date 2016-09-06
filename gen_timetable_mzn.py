'''
 Take inputs from user/file about the classes and teachers

'''

# READ IN INPUTS FROM MZN OUTPUT FILE
f = open('out.txt')

# the first two lines contain numClasses and numSlots
[numClasses, numSlots] = map(int, f.readline().strip().split())

# Next line is the list of classes
classes = f.readline().strip().split()		# list of string

# Then we read each class's assignments in order
teachers = []	# will be a list of lists, containing each class's teacher assignments

for cl in range(numClasses):
	teachers.append(f.readline().strip().split())

# GENERATE EXCEL FILE REPRESENTATION OF THE SAME
from openpyxl import Workbook

wb = Workbook()
filename = 'timetable.xlsx'

ws = wb.active
ws.title = "PTM_assignments"

# start appending line by line
ws.append(classes)		# names of classes
for j in range(numSlots):
	ws.append([ teachers[i][j] for i in range(numClasses) ])

wb.save(filename = filename)