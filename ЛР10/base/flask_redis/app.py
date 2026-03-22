import time
import redis
from flask import Flask, make_response
import socket
import os

DB_HOST = os.getenv('REDIS_HOST', 'redis')
MY_ENV = os.getenv('ENV', 'unknown')

app = Flask(__name__)
cache = redis.Redis(host=DB_HOST, port=6379)

def get_hit_count():
	retries = 5
	while True:
		try: 
			return cache.incr('hits')
		except redis.exceptions.ConnectionError as exc:
			if retries == 0:
				raise exc
			retries -= 1
			time.sleep(0.5)
@app.route('/')
def hello():
	count = get_hit_count()
	return 'Hello World VERSION 5! I have been seen {} times. My name is: {}. My env {}\n'.format(count, socket.gethostname(), MY_ENV)

def incr_hit_count()-> int:
	return cache.incr('hits')

@app.route('/metrics')
def metrics():
	metrics = f'''
# HELP view_count Flask-Redis-App visit counter
# TYPE view_count counter
view_count{{service="Flask-Redis-App"}} {get_hit_count()}
''' # sic double quotes in label
	response = make_response(metrics, 200)
	response.mimetype = "text/plain"
	return response

@app.route('/')
def hello_old():
	incr_hit_count()
	count = get_hit_count()
	return 'Hello World! I have been seen {} times. My name is: {}\n'.format(count, socket.gethostname())


###old
#import time

#import redis
#from flask import Flask

#app = Flask(__name__)
#cache = redis.Redis(host='redis', port=6379)

#def get_hit_count():
#	return cache.incr('hits')

#@app.route('/')
#def hello():
#	count = get_hit_count()
#	return 'Hello World! I have been seen {} times.\n'.format(count)
