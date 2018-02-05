#!/usr/bin/python3 -u

import cgi, cgitb, os, re, sys, zipfile

MAX_BYTES_UPLOADED_LIMIT = 2048000
MAX_UPLOADS_PER_EXERCISE = 1500

print("Content-Type: text/plain\n\n")

cgitb.enable()
parameters = cgi.FieldStorage()

for p in ['zid', 'exercise', 'zip']:
	if p not in parameters:
		print('no value passed for', p)
		sys.exit(0)

m = re.match(r'^z?(\d{7})$', parameters['zid'].value)
if not m:
	print('bad zid')
	sys.exit(0)
zid = m.group(1)

exercise = parameters['exercise'].value
if not re.match(r'^\w+$', exercise):
	print('bad exercise')
	sys.exit(0)

work_dir = '../../work'
exercise_dir = os.path.join(work_dir, exercise)
if not os.path.exists(exercise_dir):
	print('unknown exercise')
	sys.exit(0)

upload_base_dir = os.path.join(exercise_dir, 'autotest_results')
if os.path.exists(upload_base_dir) and len(os.listdir(upload_base_dir)) > MAX_UPLOADS_PER_EXERCISE:
	print('too many autotests already uploaded for exercise')
	sys.exit(0)
	
upload_dir = os.path.join(upload_base_dir, zid)
os.makedirs(upload_dir, mode=0o770, exist_ok=True)
	
z = parameters['zip']
zf = zipfile.ZipFile(z.file)
names = zf.namelist()
bytes = 0
for filename in zf.namelist():
	if not re.match(r'^[\.\-\w+]+$', filename):
		print('bad character in pathname')
		continue
	zi = zf.getinfo(filename)
	bytes += zi.file_size
	if bytes >MAX_BYTES_UPLOADED_LIMIT:
		print('limit of', MAX_BYTES_UPLOADED_LIMIT, 'exceeded')
		break
	print(zf.extract(filename, path=upload_dir), 'uploaded to', upload_dir)
