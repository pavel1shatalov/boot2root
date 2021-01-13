import os
import tarfile


d = {}
tar = tarfile.open('C:\\Users\\pavel\\shared_folder\\fun', 'r:')

for member in tar.getmembers():
    f = tar.extractfile(member)
    if not f:
        continue
    content = f.read().decode('utf-8')
    b = content.split('//file')
    s = int(b[1])
    d[s] = b[0]
for i in sorted(d.keys()):
    e = open('C:\\Users\\pavel\\shared_folder\\script.c', 'a')
    e.write(d[i])