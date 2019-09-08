
# To install 

```
pip3 install flask
pip3 install neo4j
```

# To run 

```
#!/bin/bash
export FLASK_APP=be
export FLASK_ENV=development
flask run
```



# Info

### session

session is a dict that stores data across requests. When validation succeeds, the user’s id is stored in a new session. The data is stored in a cookie that is sent to the browser, and the browser then sends it back with subsequent requests. Flask securely signs the data so that it can’t be tampered with.
https://flask.palletsprojects.com/en/1.1.x/tutorial/views/


