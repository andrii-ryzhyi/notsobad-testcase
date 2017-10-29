#!/usr/bin/python

import psycopg2
import yaml

ERR_INDEX = 2
error_records = []

def read_log(log):
	for line in log:
		line = line.strip()
		words = line.split()
		if error_found(words):
			trace_id = get_id(words)
			print("Error!!!!!!!!!!!!!!!!!!!: " + trace_id)
			handle_exception(trace_id)

def error_found(words):
	return True if words[ERR_INDEX] == "ERROR" else False

def get_id(line):
	token = line[ERR_INDEX+1].split(",")
	trace_id = token[1]
	return trace_id

def handle_exception(failed_id):	
	error_records.append(failed_id)	
	customer = ''
	user = ''
	file = open("/home/geny/git/notsobad-testcase/server.log", "r")
	for line in file:
	 	line = line.strip()
	 	words = line.split()
		curr_id = get_id(words)
		if curr_id == failed_id:
			if words[ERR_INDEX] == "INFO":
				user = words[-1]
				customer = get_customer(user)
			target.write('{0:20} {1:38} {2:25} {3:10} {4:12} {5:5} {6:40} {7}\n'.format(curr_id, user, customer, words[0], words[1], words[2], words[7], ' '.join(words[9:])))
	target.write('-------------------\n')
	file.close()

def get_customer(user):
	query = " ".join((
				"select c.name from customers c",
				"join users u",
				"on c.id = u.customer_id",
				"where u.name = '{}';".format(user)
					))
	cursor.execute(query)
	row = cursor.fetchone()
	customer = row[0]
	return customer

with open("config.yaml", 'r') as stream:
    try:
        connection = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

db = connection.get('postgresql').get('database')
hostname = connection.get('postgresql').get('host')
username = connection.get('postgresql').get('user')
passwd = connection.get('postgresql').get('password')
port_id = connection.get('postgresql').get('port')


target = open("/home/geny/git/notsobad-testcase/output.log", 'w')
target.write('{0:20} {1:38} {2:25} {3:10} {4:12} {5:5} {6:40} {7}\n'.format('Error_record', 'User', 'Customer', 'Date', 'Time', 'Type', 'Service', 'Status'))

conn = psycopg2.connect(host=hostname, database=db, user=username, password=passwd, port=port_id)
cursor = conn.cursor()

with open("/home/geny/git/notsobad-testcase/server.log", "r") as log:
	read_log(log)

target.close()
conn.close()

#cursor.execute('SELECT version()')
#version = cursor.fetchone()
#print(version)

