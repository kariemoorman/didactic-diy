#!/usr/bin/python3
from datetime import datetime 
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_sslify import SSLify
from flask_jwt_extended import JWTManager
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import logging
from logging.handlers import RotatingFileHandler

from utils import setup_jwt, create_access_token

##---------------------FLASK APP--------------------##
##---Create Flask App---##
app = Flask(__name__)

##------------------------SSL-----------------------##
##---Enforce HTTPS on all requests---##
# sslify = SSLify(app) 

##---------------------DATABASE---------------------##
##---Create Sample Database (in-memory database)---## 
tasks = [] 
##---Change database to SQLAlchemy---##
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # Replace with your database URL
# db = SQLAlchemy(app)

##---------------JSON WEB TOKEN (JWT)---------------##
##---Set the JWT secret key---## 
# jwt = setup_jwt(app)

# Simulated user data (replace with your authentication logic)
# users = {'example_user': {'password': 'password'}}

##---Custom handler for expired tokens---##
# @jwt.expired_token_loader
# def expired_token_callback():
#     return jsonify({'message': 'Token has expired'}), 401
##---Authenticate user and assign JWT---##
# @app.route('/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get('username')
#     password = data.get('password')
#     if not username or not password:
#         return jsonify({'message': 'Username and password are required'}), 400
#     if users.get(username) and users[username]['password'] == password:
#         access_token = create_access_token(app, username)
#         return jsonify({'access_token': access_token}), 200
#     else:
#         return jsonify({'message': 'Invalid credentials'}), 401

##------------------RATE LIMITING-------------------##
##---Set up Redis connection for rate limit storage (replace password)---##
redis_client = redis.StrictRedis(host='127.0.0.1', port=6379, db=0) #, password='your_password')
##---Add rate limiting to the app, define default limits, set redis storage endpoint---##
limiter = Limiter(app=app,key_func=get_remote_address,default_limits=["200 per day", "50 per hour", "5 per minute", "1 per second"],storage_uri="redis://127.0.0.1:6379/0")
##---Create Rate Limit Exception log function---##
def rate_limit_exceeded():
    ip_address = get_remote_address()
    app.logger.warning(f'Rate limit exceeded: {ip_address}')
    return jsonify({'message': 'Rate limit exceeded', 'status_code': 429}), 429
##---Add Rate Limit Exception logging---##
limiter.request_filter(rate_limit_exceeded)

##------------------ACTIVITY LOGS-------------------##
##---Add logging---##
logging.basicConfig(level=logging.DEBUG) 
##---Configuration to write logs to a file---##
log_file = './logs/restful_api.log' ## Specify the path and filename for the log file
handler = RotatingFileHandler(log_file, maxBytes=1024*1024, backupCount=10)  ## Create a rotating file handler
handler.setLevel(logging.DEBUG)  ## Set the logging level for the handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')  ## Specify the log message format
handler.setFormatter(formatter)  ## Apply the formatter to the handler  
app.logger.addHandler(handler)  ## Add the handler to the Flask logger

##---------------------API KEYS---------------------##
##---Add API keys---##
# valid_api_keys = ['your_api_key_1', 'your_api_key_2']
##---Create API key requirement---##
# def require_api_key():
#     api_key = request.headers.get('API-Key')
#     if api_key and api_key in valid_api_keys:
#         return True
#     else:
#         return False
##---Define API key check before processing HTTP requests---##
# @app.before_request
# def check_api_key():
#     if not require_api_key():
#         return jsonify({'message': 'Unauthorized'}), 401

##----------------HTTP REQUEST LOGIC----------------##
##------------------GET--------------------##
@app.route('/tasks', methods=['GET']) ## Define an API endpoint for GET request
##@jwt_required() ## Require JWT
@limiter.limit("2 per minute",override_defaults = True) ## Set unique rate limit (optional)
##---Get all tasks using GET---##
def get_tasks():
    try:
        # current_user = get_jwt_identity()
        # Info log for GET event
        app.logger.info({'event': 'get_tasks', 'message': f'Accessing /tasks route - Method: {request.method}'}) #, 'user': current_user
        return jsonify({'tasks': tasks})
    except Exception as e:
        # Error log for exceptions
        app.logger.error({'event': 'get_tasks', 'message': f'Error retrieving tasks: {str(e)}'})
        return jsonify({'error': 'Error retrieving tasks'}), 500
    
##------------------POST-------------------##    
@app.route('/tasks', methods=['POST']) ## Define an API endpoint for POST request
# @jwt_required() ## Require JWT
@limiter.limit("2 per minute",override_defaults = True) ## Set unique rate limit (optional)
##---Create a new task using POST---##
def create_task():
    try:
        # current_user = get_jwt_identity()
        current_datetime = datetime.now() 
        data = request.get_json()
        # Info log for POST event
        app.logger.info({'event': 'create_task', 'message': f'Creating task: {data.get("title")}'}) #, 'user': current_user
        # Warning log for missing 'title'
        if 'title' not in data:
            app.logger.warning({'event': 'create_task', 'message': 'Task creation without title'})
        # Error log if 'title' is missing
        if 'title' not in data:
            app.logger.error({'event': 'create_task', 'message': 'Task creation failed due to missing title'})
            return jsonify({'error': 'Task creation failed due to missing title'}), 400    
        task = {'id': len(tasks) + 1, 'title': data['title'], 'done': False, 'datetime': current_datetime}
        tasks.append(task)
        # Task completion log
        app.logger.info({'event': 'create_task', 'message': f'Task created successfully: {task}'})   
        return jsonify({'message': 'Task created successfully', 'task': task}), 201
    except Exception as e:
        # Error log for exceptions
        app.logger.error({'event': 'create_task', 'message': f'Error creating task: {str(e)}'})
        return jsonify({'error': 'Error creating task'}), 500

##------------------PUT--------------------##
@app.route('/tasks/<int:task_id>', methods=['PUT']) ## Define an API endpoint for PUT request
# @jwt_required() ## Require JWT
##---Update a task using PUT---##
def update_task(task_id):
    try:
        current_datetime = datetime.now()
        # current_user = get_jwt_identity()
        data = request.get_json()
        # Info log for PUT event
        app.logger.info({'event': 'update_task', 'message': f'Updating Task: {task_id}'}) #, 'user': current_user
        old_task = None
        updated_task = None
        # Update task data
        for task in tasks:
            if task['id'] == task_id:
                old_task = task.copy()
                task['title'] = data.get('title', task['title'])
                task['done'] = data.get('done', task['done'])
                task['update_datetime'] = current_datetime
                updated_task = task
                break
        if old_task:
            # Log old task data
            app.logger.info({'event': 'update_task', 'message': f'Task {task_id}', 'old_task': old_task})
        if updated_task:
            # Task update completion log
            app.logger.info({'event': 'update_task', 'message': f'Task {task_id} updated successfully: {updated_task}'})
            return jsonify({'message': f'Task updated successfully', 'task': updated_task})
        else:
            # Task not found error log
            app.logger.error({'event': 'update_task', 'message': f'Task {task_id} not found'})
            return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        # Error log for exceptions
        app.logger.error({'event': 'update_task', 'message': f'Error updating task: {str(e)}'})
        return jsonify({'error': 'Error updating task'}), 500

##------------------PATCH-------------------##
@app.route('/tasks/<int:task_id>', methods=['PATCH']) ## Define an API endpoint for PATCH request
# @jwt_required() ## Require JWT
##---Update a task using PATCH---##
def update_task_patch(task_id):
    try:
        # current_user = get_jwt_identity()
        current_datetime = datetime.now()
        data = request.get_json()
        # Info log for PATCH event
        app.logger.info({'event': 'update_task_patch', 'message': f'Updating task (PATCH): {task_id}'}) #, 'user': current_user
        old_task = None
        updated_task = None
        # Update task data
        for task in tasks:
            old_task = task.copy()
            if task['id'] == task_id:
                if 'title' in data:
                    task['title'] = data['title']
                if 'done' in data:
                    task['done'] = data['done']
                task['update_datetime'] = current_datetime    
                updated_task = task
                break
        if old_task:
            # Log old task data
            app.logger.info({'event': 'update_task_patch', 'message': f'Task {task_id}', 'old_task': old_task})
        if updated_task:
            # Task update completion log
            app.logger.info({'event': 'update_task_patch', 'message': f'Task {task_id} updated successfully: {updated_task}'})
            return jsonify({'message': 'Task updated successfully', 'task': updated_task})
        else:
            # Task not found error log
            app.logger.error({'event': 'update_task_patch', 'message': f'Task {task_id} not found'})
            return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        # Error log for exceptions
        app.logger.error({'event': 'update_task_patch', 'message': f'Error updating task (PATCH): {str(e)}'})
        return jsonify({'error': 'Error updating task'}), 500

##------------------DELETE-------------------##
@app.route('/tasks/<int:task_id>', methods=['DELETE']) ## Define an API endpoint for DELETE request
# @jwt_required() ## Require JWT
@limiter.limit("1 per minute",override_defaults = True) ## Set unique rate limit (optional)
##---Delete a task using DELETE---##
def delete_task(task_id):
    # current_user = get_jwt_identity()
    # Info log for PATCH event
    app.logger.info({'event': 'delete_task', 'message': f'Deleting Task: {task_id}'}) #, 'user': current_user
    try: 
        global tasks
        old_tasks = tasks.copy()
        tasks = [task for task in tasks if task['id'] != task_id]
        if old_tasks != tasks:
            app.logger.info({'event': 'delete_task', 'message': f'Task {task_id} deleted successfully', 'old_tasks': old_tasks, 'remaining_tasks': tasks})
            return jsonify({'message': 'Task deleted successfully'}), 200
        else:
            app.logger.error({'event': 'delete_task', 'message': f'Task {task_id} not found'})
            return jsonify({'message': 'Task not found'}), 404
    except Exception as e:
        app.logger.error({'event': 'delete_task', 'message': f'An error occurred: {str(e)}'})
        return jsonify({'message': 'An error occurred'}), 500

##---Log app starttime---##
app.logger.info({'event': 'app_start', 'message': 'Flask app started'})

##---Render HTML---##
@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    app.run(debug=True)
#    app.run(ssl_context=('./credentials/cert.pem', './credentials/key.pem'), debug=True)