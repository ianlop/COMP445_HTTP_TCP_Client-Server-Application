import os

path = 'Working'
max_character_name = 12
dir_content = os.listdir(path)
content = ''
for item in dir_content:
    if os.path.isdir(os.path.join(path, item)):
        content += 'DIR: %s\r\n'%(item)
    elif os.path.isfile(os.path.join(path, item)):
        split_text = item.split('.')
        split_text[0] = split_text[0].ljust(max_character_name)
        content += 'FILE: %s TYPE: %s\r\n'%(split_text[0], split_text[1])
print(content)

name = 'foo3'
filePath = ''
path = 'Working'
for root, dirs, files in os.walk(path):
    if name in files:
        filePath = os.path.join(root, name)

file = open(filePath, 'r')
with file:
    contents = file.read()
    print(contents)

