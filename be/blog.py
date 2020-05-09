import random 
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, send_from_directory, make_response
)
from werkzeug.exceptions import abort
# from be.auth import login_required
import be.db as bedb
import json

bp = Blueprint('blog', __name__)

# @bp.route('/')
# def index():
#     db = bedb.get_db()
#     user_id = session.get('user_id')
#     posts = db.get_posts_by_user(user_id)
#     return render_template('blog/index.html', posts=posts)

@bp.route('/upload', methods=('GET', 'POST'))
def upload():

    print(request.files)
    f = request.files.get('sampleFile')
    f.save('./uploads/'+ f.filename)

    print(f)
    tags = str(request.form)
    print("TAGS = " + tags)
    print("ARGS = " + str(request.args))
    if request.method == 'POST':
        return "upload POST"
    else:
        return "upload GET"

# TODO: Clean up this messsss! Find a better way to GET a 'static' file
@bp.route('/uploads/<fn>', methods=['GET'])
def uploads(fn):
    print('GET a file from ./static/ with filename = ' + str(fn))
    # return send_from_directory('./static/', fn, as_attachment=True)

    resp = make_response(send_from_directory('./static/', fn, as_attachment=True))
    print(resp)
    resp.headers["Access-Control-Allow-Origin"] =  "http://localhost:3666"
    resp.headers["Access-Control-Allow-Credentials"] =  "true"
    for x in resp.headers:
        print('header: ', x)
    return resp



@bp.route('/creatememe', methods=('GET', 'POST'))
def meme_create():
    f = request.files.get('sampleFile')
    if f.filename != '':
        f.save('./uploads/'+ f.filename)

    meme_file = f.filename
    meme_name = str(request.form['name'])
    meme_tags = str(request.form['tags'])
    meme_text = str(request.form['text'])

    print("TAGS = " + meme_tags)
    print("NAME = " + meme_name)
    print("FILE = " + meme_file)
    print("TEXT = " + meme_text)

    db = bedb.get_db()
    db.add_meme(meme_name, meme_tags, meme_file, meme_text)
    return redirect(request.referrer) 

@bp.route('/getmemes', methods=['GET'])
def meme_get_all():
    db = bedb.get_db()
    ms = db.get_memes()
    ret = []
    for m in ms:
        # m_dict = {'id': m.id, 'name':m['name'], 'fn':m['file'], 'tags':m['tags'].split(',')}
        # ret.append(json.dumps(m_dict))
        m_dict = {'id': m.id, 'name':m['name'], 'text': m['text'] if m['text'] else '', 'fn':m['file'], 'tags':m['tags'].split(',')}
        ret.append(json.dumps(m_dict))
    ret_str = ','.join(ret)
    #print(ret_str)
    return '['+ret_str+']'

    
def get_a_meme(meme):
    print("-----------> meme_get: ", meme)
    db = bedb.get_db()
    ms = db.get_meme(meme)
    #print(str(ms))
    ret = []
    for m in ms:
#        m_dict = {'id': m.id, 'name':m['name'], 'text':m['text'], 'fn':m['file'], 'tags':m['tags'].split(',')}
        m_dict = {'id': m.id, 'name':m['name'],  'text': m['text'] if m['text'] else '', 'fn':m['file'], 'tags':m['tags'].split(',')}
        ret.append(json.dumps(m_dict))
    ret_str = ','.join(ret)
    #print(ret_str)
    
    # return '['+ret_str+']'
    resp = make_response('['+ret_str+']')
    print(resp)
    for x in resp.headers:
        print('header: ', x)
    return resp

@bp.route('/getmeme/<meme>', methods=['GET'])
def meme_get(meme):
    return get_a_meme(meme)

@bp.route('/getmemerandom/', methods=['GET'])
def meme_get_random():
    db = bedb.get_db()
    ms = db.get_memes()
    k_random = random.randint(1,len(ms))-1
    print(k_random)
    m = ms[k_random]
    m_name = m['name']
    print(m_name)
    # return '[{"id": 66666, "name": "random", "text": "lskdkfieow", "fn": "", "tags": ["t1", "t3"]}]'

    return get_a_meme(m_name)


# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = bedb.get_db()
#             user_id = session.get('user_id')
#             print("create a post: " + str(user_id))
#             db.add_post(title, body, user_id)
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')

# def get_post(id, check_author=True):
#     db = bedb.get_db()
#     post = db.get_post(id)
#     if post is None:
#         abort(404, "Post id {0} doesn't exist.".format(id))

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# # @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)


# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))
