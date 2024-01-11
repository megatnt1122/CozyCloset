#!/usr/bin/python3
import sqlite3

def application(environ, start_response):

	output = "<p> LOG</p>"

	db = sqlite3.connect('test.db')
	db.row_factory = sqlite3.Row
	cursor = db.cursor()
	cursor.execute('''SELECT id, message,date FROM table''')
	for row in cursor:
		print('{0} : {1}, {2}'.format(row['id'], row['message'], row['date']))
	db.close()

	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return output

