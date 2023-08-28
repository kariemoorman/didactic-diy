<h2 align='center'>RESTful API in Flask</h2>
<h4 align='center'>Database Interactions via HTTP(s).</h4>

---

## Table of Contents
- <b>[Basic Flask App](#basic-flask-app)</b>
- <b>[Add SSL Certification](#add-ssl-certification)</b>
- <b>[Add API Key Authentication](#add-api-key-authentication)</b>
---

## Basic Flask App

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

#### Execute HTTP requests to add, modify, and/or delete database entries: 
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

PUT changes to the first to update both the task title and completion status: 
```bash
curl -X PUT \ 
  -H "Content-Type: application/json" \
  -d '{"title": "Buy fruit", "done": true}' \
  http://127.0.0.1:5000/tasks/1
```

PATCH the second task to update the completion status:
```bash
curl -X PATCH \
  -H "Content-Type: application/json" \
  -d '{"done": true}' \ 
  http://127.0.0.1:5000/tasks/2
```

DELETE the first task entry:
```bash
curl -X DELETE http://127.0.0.1:5000/tasks/1
```


--- 

## Add SSL Certification

#### Create credentials:
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
#### Execute HTTP requests to add, modify, and/or delete database entries: 
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

#### Execute HTTP requests to add, modify, and/or delete database entries: 
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

<p align='center'><b>License: <a href='https://choosealicense.com/licenses/gpl-3.0/'>GNU General 
Public License v3.0</a></b></p>


