<h2 align='center'>RESTful API using Flask</h2>
<h4 align='center'>Database Interactions via HTTP(s).</h4>

---

## Table of Contents
- <b>[Introduction](#introduction)</b>
- <b>[Repository Contents](#repository-contents)</b>
- <b>[Basic Flask App](#basic-flask-app)</b>
- <b>[Add SSL Certification](#add-ssl-certification)</b>
- <b>[Add API Key Authentication](#add-api-key-authentication)</b>
- <b>[Production-Readiness](#production-readiness)</b>
- <b>[Resources](#resources)</b>

---
## Introduction

A REST API (Representational State Transfer Application Programming Interface) is a widely used client-server architectural style for designing web-based networked applications. REST APIs provide a standardized and flexible way for different systems to communicate and interact with relatively low-complexity, and are most commonly used in web applications, mobile apps, and IoT devices.

The core concept of REST is transferring the state of a resource from server to client or vice versa. To do this, REST APIs utilize a uniform set of rules (e.g., HTTP methods) and conventions (e.g., security protocols) that allow different software applications to communicate with each other over the internet. In each "communication" step, REST APIs map CRUD (Create, Read, Update, Delete) operations to HTTP methods (`POST`, `GET`, `PUT/PATCH`, `DELETE`) to transfer representations of resources between client and server, often in JSON or XML format. Each resource is accessed via a specific URL endpoint (e.g., `/tasks` may represent a collection of task data). Each request is coupled with an HTTP response code to indicate the outcome of that request (e.g., 200 OK, 404 Not Found, 500 Internal Server Error), which aids in error handling scenarios and helps ensure an overall successful interaction between the client and the server. 

REST APIs play a pivotal role in enabling seamless integration and interoperability between diverse software systems while maintaining simplicity and consistency in communication.

For a more detailed overview of API protocols and HTTP requests, see my blog post: <a href='https://www.kariemoorman.com/2023/08/17/restful-api-python'>RESTful API in Flask</a>.

---

## Repository Contents

- <b>Flask App</b>: [restful_api.py](https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/restful_api.py)  
  Flask API app logic, including URL route logic, HTTP method and response logic, logging, rate-limiting, SSL certification, API keys, and JWT authentication.
- <b>JWT Creation</b>: [utils.py](https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/utils.py)  
  JSON Web Token (JWT) creation logic.
- <b>Jinja Templates</b>: [templates](https://github.com/kariemoorman/didactic-diy/tree/main/tutorials/apis/restful_api/flask/templates)  
  Presentation layer that dynamically generates HTML pages by rendering data obtained via the API.
- <b>Activity Logs</b>: [logs](https://github.com/kariemoorman/didactic-diy/tree/main/tutorials/apis/restful_api/flask/logs)  
  Example API activity logs.
- <b>Requirements</b>: [requirements.txt](https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/requirements.txt)  
  List of python packages used to build and run the Flask app.
---

## Basic Flask App
In its current state, the app is ready to run in developer-mode.

#### Run the app:
```python
python restful_api.py
```
or 
```python
export FLASK_APP=restful_api.py
flask --app restful_api run
```
or 
```python
export FLASK_APP=restful_api.py
python -m flask -app restful_api run
```

#### In the web browser: 
Navigate to the specified local host and open port: 
```
http://127.0.0.1/5000
```
<img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/images/basic_flask_api_http_url.png' alt='HTTP URL request'/>

#### In Terminal, execute HTTP requests to add, modify, and/or delete database entries: 
(see <a href='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/bash_scripts/api_http_requests.sh'>api_http_requests.sh</a>)

POST new task entries to the 'tasks' database: 
```bash
curl -X POST \           
  -H "Content-Type: application/json" \
  -d '{"title": "Buy ice cream"}' \
  http://127.0.0.1:5000/tasks

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy vegetables"}' \
  http://127.0.0.1:5000/tasks

```

<img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/images/bash_flask_api_http_post.png' alt='HTTP POST request'/>

PUT changes to the first to update both the task title and completion status: 
```bash
curl -X PUT \ 
  -H "Content-Type: application/json" \
  -d '{"title": "Buy fruit", "done": true}' \
  http://127.0.0.1:5000/tasks/1
```

<img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/images/bash_flask_api_http_put.png' alt='HTTP PUT request'/>

PATCH the second task to update the completion status:
```bash
curl -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"done": true}' \ 
  http://127.0.0.1:5000/tasks/2
```

<img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/images/bash_flask_api_http_patch.png' alt='HTTP PATCH request'/>

DELETE the first task entry:
```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1
```

<img src='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/images/bash_flask_api_http_delete.png' alt='HTTP DELETE request'/>

In its current state, the app has many privacy and security vulnerabilities. To minimize attack surface, consider adding components such as [SSL certification](#add-ssl-certification) and [API Key authentication](#add-api-key-authentication). 

--- 

## Add SSL Certification

SSL certification is a basic security protocol used to encrypt communication between the server and clients, ensuring confidentiality and data integrity. 

#### Create credentials set:
```python
mkdir credentials;

openssl req -x509 -newkey rsa:4096 -keyout ./credentials/key.pem -out ./credentials/cert.pem -days 30;
```

#### Update <a href='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/restful_api.py'>restful_api.py</a> script: 
```python
# Enforce HTTPS on all requests
sslify = SSLify(app) 

...

if __name__ == '__main__':
    app.run(ssl_context=('./credentials/cert.pem', './credentials/key.pem'), debug=True)
```

#### Run the app: 
```python
python restful_api.py
```
or 
```python
flask --app restful_api --cert=./credentials/cert.pem --key=./credentials/key.pem run
```

#### In the web browser: 
Navigate to the specified secure local host and open port: 
```
https://127.0.0.1/5000
```
#### Execute HTTPS requests to add, modify, and/or delete database entries: 
(see <a href='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/bash_scripts/api_https_requests.sh'>api_https_requests.sh</a>)

Add  ```--cacert``` flag to curl request to verify certificate, e.g.,

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy chips"}' \
  --cacert ./credentials/cert.pem \
  -k https://127.0.0.1:5000/tasks
```

---
## Add API Key Authentication

In addition to SSL certification, API key integration permits client authentication prior to request execution.

#### Update <a href='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/restful_api.py'>restful_api.py</a> script: 

```python
##---Add API keys---##
valid_api_keys = ['your_api_key_1', 'your_api_key_2']
##---Create API key requirement---##
def require_api_key():
  api_key = request.headers.get('API-Key')
  if api_key and api_key in valid_api_keys:
    return True
  else:
    return False
##---Define API key check before processing HTTP requests---##
@app.before_request
def check_api_key():
  if not require_api_key():
    return jsonify({'message': 'Unauthorized'}), 401
```

#### Execute HTTPS requests to add, modify, and/or delete database entries: 
(see <a href='https://github.com/kariemoorman/didactic-diy/blob/main/tutorials/apis/restful_api/flask/bash_scripts/api_https_requests.sh'>api_https_requests.sh</a>)

Add  ```-H "API-Key: your_api_key_here"``` to curl request to verify API keys, e.g.,

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "API-Key: your_api_key_here" \
  -d '{"title": "Buy chips"}' \
  --cacert ./credentials/cert.pem \
  -k https://127.0.0.1:5000/tasks
```

---

## Production-Readiness

While Flask provides a built-in development server, it is not secure, stable, or efficient for production use. To productionize the app, we can choose from either a local, self-hosted WSGI server or a cloud-based hosting platform. Options for self-hosting include Gunicorn (Green Unicorn), uWSGI, Nginx, and Apache. Options for cloud hosting include AWS, Google Cloud, Azure, Heroku, DigitalOcean, and PythonAnywhere.

#### Run the app using a Gunicorn server: 

```python
gunicorn restful_api:app -w 2 --certfile=./credentials/cert.pem --keyfile=./credentials/key.pem 
```

Note: Gunicorn is often used with <a href='https://docs.gunicorn.org/en/stable/deploy.html#nginx-configuration'>Nginx</a>. Gunicorn WSGI HTTP server acts as a backend server responsible for handling the actual application logic, request processing, and serving dynamic content, while Nginx is used as a frontend server to handle tasks such as serving static files, load balancing incoming requests to multiple application server instances, managing SSL/TLS certificates, and acting as a reverse proxy to pass requests to the appropriate backend server (like Gunicorn). Before deploying to production environment, first install and configure the Nginx.

---

## Resources

- Flask: https://flask.palletsprojects.com/
- Flask Limiter: https://flask-limiter.readthedocs.io
- WSGI: https://wsgi.readthedocs.io/
- Gunicorn: https://gunicorn.org/
- Nginx: https://nginx.org/en/docs/http/ngx_http_uwsgi_module.html#flask

---

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General 
Public License v3.0</a></b></p>


