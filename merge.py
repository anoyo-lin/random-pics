#!/usr/bin/python
import shlex,subprocess,csv,os
from random import choice

os.environ["MAGICK_TEMPORARY_PATH"]=os.getcwd()

lst=[]
file="find ./ -regex '.*\.bak\.JPEG$' -printf '%h/%f\n'"
args=shlex.split(file)
output=subprocess.Popen(args,stdout=subprocess.PIPE)
for x in output.stdout:
	lst.append(x.rstrip('\n'))

cnt=round(len(lst)**0.5)
i=0
alist=['convert','-monitor','-limit','map','2GiB','-limit','disk','4GiB','-limit','memory','2GiB','(']
res=set()
lwidth=cnt*250
#for x in lst:
while len(lst) > 0:
	if i==0 or i%cnt !=0:
		x=lst.pop(lst.index(choice(lst)))
		alist.append(x)
	else:
		space = "%sx%s" % (lwidth,lwidth)
		alist.append('+append')
		alist.append(')')
		alist.append('-background')
		alist.append('none')
		alist.append('-resize')
		alist.append(space)
		result="result_%s.jpg" % i
		alist.append(result)
		res.add(result)
		output=subprocess.Popen(alist,stdout=subprocess.PIPE).communicate()
		alist=['convert','-monitor','-limit','map','2GiB','-limit','disk','4GiB','-limit','memory','2GiB','(']
		x=lst.pop(lst.index(choice(lst)))
		alist.append(x)
	i+=1
n=0
alist=['convert','-monitor','(']
for x in res:
	if n != 0:
		alist.append('result.jpg')
	alist.append(x)
	alist.append('-append')
	alist.append(')')
	alist.append('-background')
	alist.append('none')
	alist.append('result.jpg')
	print alist
	output=subprocess.Popen(alist,stdout=subprocess.PIPE).communicate()
	alist=['convert','-monitor','(']
	n=n+1

#ditem="find ./ -regex '.*\(jpg\|JPG\|jpeg\|JPEG\)\.bak$' -print0|xargs -0 rm -f"
#output=subprocess.Popen(ditem,shell=True,stdout=subprocess.PIPE).communicate()

ditem="rm -f result_*.jpg"
output=subprocess.Popen(ditem,shell=True,stdout=subprocess.PIPE).communicate()
