#!/usr/bin/env python
from scanner import app

print "testing"

app.debug = True
app.run(host='0.0.0.0')
