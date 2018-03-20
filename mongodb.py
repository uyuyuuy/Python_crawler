#!/usr/bin/python
# -*- coding: utf-8 -*-



import pymongo

connection = pymongo.MongoClient()
db = connection.local
tb = db.test

print(tb.find_one())

