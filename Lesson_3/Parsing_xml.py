import xml.etree.ElementTree as ET
import pprint
import os

xmldir = ''
xmlfile = 'class_list.xml'

tree = ET.parse(xmlfile)
#print type(tree)

root = tree.getroot()
#print type(root)
#print root.tag

for child in root:
    print child.tag
print '\n'

class_name = root.find('./class_name') #('./class_list/student')
class_name_text = ''
for e in class_name:
    #print type(letter)
    class_name_text += e.text
print 'The name of the class is:', class_name_text

print '\nStudent List:'
student_list = root.findall('./class_list/')
for s in student_list:
    student_name = s.find('name')
    if student_name is not None:
        print student_name.text
