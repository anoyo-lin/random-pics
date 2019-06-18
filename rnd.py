#!/usr/bin/python
import shlex,subprocess,csv,os
from random import choice

os.environ["MAGICK_TEMPORARY_PATH"]="/root"

ditem="rm -f result.jpg"
output=subprocess.Popen(ditem,shell=True,stdout=subprocess.PIPE).communicate()

ditem="find ./ -regex '.*\.bak\.JPEG$' -print0|xargs -0 rm -f"
output=subprocess.Popen(ditem,shell=True,stdout=subprocess.PIPE).communicate()

date="find ./ -regex '.*\.\(jpg\|JPG\|arw\|ARW\)$' -printf '%TY%Tm%Td\n'"
args=shlex.split(date)
output=subprocess.Popen(args,stdout=subprocess.PIPE)

dlst=set()
for x in output.stdout:
	dlst.add(x.rstrip('\n'))

dp="find ./ -regex '.*\.\(jpg\|JPG\|arw\|ARW\)$' -printf '%TY%Tm%Td\t%h/%f\n'"
args=shlex.split(dp)
output=subprocess.Popen(args,stdout=subprocess.PIPE).communicate()

rec=csv.DictReader(output[0].splitlines(),delimiter='\t',skipinitialspace=True,fieldnames=['date','path'])
fdict={ x:[] for x in dlst }
for x in rec:
	for y in dlst:
		if x['date'] == y:
			fdict[y].append(x['path'])
			break

lst=set()
for x in dlst:
	lst.add(choice(fdict.get(x)))

#cnt=round(len(lst)**0.5)
#i=0
#alist=['convert','-monitor','-limit','map','2GiB','-limit','disk','4GiB','-limit','memory','2GiB','(']

for x in lst:
	name="%s.bak.JPEG" % x

	cmd="convert \"%s\" -gravity center -crop `identify -format '%%[fx:min(w,h)]x%%[fx:min(w,h)]+0+0' \"%s\"` +repage -resize '250x250' \"%s\"" % (x,x,name)
	print cmd
	output=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()
	
	cmd="jhead -autorot \"%s\"" % name
	print cmd
	output=subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE).communicate()
#	if i==0 or i%cnt !=0:
#		alist.append(name)
#	else:
#		alist.append('+append')
#		alist.append(')')
#		alist.append('(')
#		alist.append(name)
#	i+=1
#alist.append('+append')
#alist.append(')')
#alist.append('-background')
#alist.append('none')
#alist.append('-append')
#alist.append('result.jpg')
#print alist
#output=subprocess.Popen(alist,stdout=subprocess.PIPE).communicate()
