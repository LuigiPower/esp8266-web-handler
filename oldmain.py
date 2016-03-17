#!/usr/bin/env python
from scanner import init_db
from scanner import init_test_data
from scanner import start_server

print "testing"

init_db()
init_test_data()
start_server()
