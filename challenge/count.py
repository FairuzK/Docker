import os
from flask import Flask
import redis

app =Flask(__name__)

redis_host = os.getenv('REDIS_HOST', 'redis')   # The hostname of the Redis container
redis_port = int(os.getenv('REDIS_PORT', 6379))     # The port on which Redis is running

r=redis.Redis(host=redis_host, port=redis_port)
# Code added to initialize the count key in Redis if it doesn't exists

@app.route('/')
def welcome():
    return "Welcome to Coderco Container Challenge"

@app.route('/count')
def count():
    count=r.incr('count')
    return f'This page has been visited {count} times.'

if __name__ == '__main__':
# This will run the Flask app on host and port 5002, which is accessible from outside the container
    app.run(host='0.0.0.0', port=5002)
