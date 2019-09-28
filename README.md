
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


# Standard Context in Templates
https://flask.palletsprojects.com/en/1.1.x/templating/

# Info

### session

session is a dict that stores data across requests. When validation succeeds, the user’s id is stored in a new session. The data is stored in a cookie that is sent to the browser, and the browser then sends it back with subsequent requests. Flask securely signs the data so that it can’t be tampered with.
https://flask.palletsprojects.com/en/1.1.x/tutorial/views/


### `request` in `templates`
The pattern {{ request.form['title'] or post['title'] }} is used to choose what data appears in the form. When the form hasn’t been submitted, the original post data appears, but if invalid form data was posted you want to display that so the user can fix the error, so request.form is used instead. request is another variable that’s automatically available in templates.
https://flask.palletsprojects.com/en/1.1.x/tutorial/blog/
