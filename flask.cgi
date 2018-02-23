#!/usr/bin/env python3

import os, re, sys
from wsgiref.handlers import CGIHandler

sys.path.append('scripts')
from webpages import app

# Flask doesn't merge slashes - https://github.com/pallets/flask/issues/1323
# So crude-workaround
for variable in 'REDIRECT_SCRIPT_URI REQUEST_URI SCRIPT_URI PATH_INFO SCRIPT_URL REDIRECT_URL REDIRECT_SCRIPT_URL'.split():
    if '//' in os.environ.get(variable, ''):
        os.environ[variable] = re.sub(r'(^|[^:])/+', r'\1/', os.environ[variable])

# Breaks flask when not set
if 'PATH_INFO' not in os.environ:
    os.environ['PATH_INFO'] = ''

app.secret_key = open('.flask_key').read().strip()
try:
    CGIHandler().run(app)
except Exception:
    # catch any exceptions that escape Flask and print useful information
    print('Content-Type: text/plain\n', flush=True)
    etype, evalue, etraceback = sys.exc_info()
    print("\n".join(traceback.format_exception_only(etype, evalue)), flush=True)
    traceback.print_exc(file=sys.stdout)
