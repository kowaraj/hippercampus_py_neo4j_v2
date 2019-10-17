import click
from flask import current_app, g
from flask.cli import with_appcontext
from neo4j import GraphDatabase

def create_uniqueness_constraint(tx, label, property):
    query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE"
    query = query.format(label=label, property=property)
    tx.run(query)

class DB(object): 
    def __init__(self):
        self.driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "1234"))
        with self.driver.session() as session:
            session.write_transaction(create_uniqueness_constraint, "User", "username")
            session.write_transaction(create_uniqueness_constraint, "Post", "id")

    def get_driver(self):
        return self.driver
        
    def get_user(self, username):

        def __tx_get_user(tx, username):
            return tx.run("MATCH (u:User) WHERE u.username = $name RETURN u", name = username).single()

        session = self.get_driver().session()
        u = session.read_transaction(__tx_get_user, username)
        return u

    def get_user_by_id(self, id):

        def __tx_get_user_by_id(tx, id):
            return tx.run("MATCH (n) WHERE ID(n) = $id RETURN n", id = id).single()

        session = self.get_driver().session()
        u = session.read_transaction(__tx_get_user_by_id, id)
        return u

    def add_user(self, username, password_hash):

        def __tx_add_user(tx, username, password_hash):
            return tx.run("CREATE (u:User {username:$username, password:$password}) RETURN u.username", username=username, password=password_hash)

        # print("add_user: " + username)
        session = self.get_driver().session()
        u = session.write_transaction(__tx_add_user, username, password_hash)
        # print("add_user: result " + str(u))
    
    def get_post(self, id):
        def __tx_get_post(tx, id):
            return tx.run("MATCH (p:Post) WHERE ID(p) = $id RETURN p", id = id).single()
        print("get_post: " + str(id))
        session = self.get_driver().session()
        u = session.read_transaction(__tx_get_post, id)
        print("get_post: result " + str(u))

    def get_posts(self):
        def __tx_get_posts(tx):
            return tx.run("MATCH (p:Post) RETURN p").value()

        print("get_posts: ALL")
        session = self.get_driver().session()
        ps = session.read_transaction(__tx_get_posts)
        print("get_posts: ps = " + str(ps))
        psx = [{'id': p.id, 'author_id':p['author_id'], 'title': p['title'], 'body':p['body'], 'created':p['created']} for p in ps]
        print("get_posts: psx = " + str(psx))
        return psx

    def get_posts_by_user(self, id):
        def __tx_get_posts_by_user(tx, author_id):
            return tx.run("MATCH (p:Post) WHERE p.author_id = $id RETURN p", id = id).value()

        print("get_posts_by_user: " + str(id))
        session = self.get_driver().session()
        ps = session.read_transaction(__tx_get_posts_by_user, id)
        print("get_posts_by_user: ps = " + str(ps))
        psx = [{'id': p.id, 'author_id':p['author_id'], 'title': p['title'], 'body':p['body'], 'created':p['created']} for p in ps]
        print("get_posts: psx = " + str(psx))
        return psx

    def add_post(self, title, body, user_id):
        def __tx_add_post(tx, t, b, user_id):
            return tx.run("CREATE (p:Post {title:$title, body:$body, author_id:$author_id, created:$ts}) RETURN p", title=title, body=body, author_id=user_id, ts=666)
        print("add_post: " + title)
        session = self.get_driver().session()
        u = session.write_transaction(__tx_add_post, title, body, user_id)
        print("add_post: result " + str(u))

    def add_meme(self, name, tags, file):

        def __tx_add_meme(tx, name, tags, file):
            return tx.run("CREATE (n:Meme {name:$name, tags:$tags, file:$file} ) RETURN n.name", name=name, tags=tags, file=file)

        print("add_meme: " + name)
        session = self.get_driver().session()
        u = session.write_transaction(__tx_add_meme, name, tags, file)
        print("add_meme: result " + str(u))

    def get_user(self, username):

        def __tx_get_user(tx, username):
            print("tx_get_user: "+ username)
            return tx.run("MATCH (u:User) WHERE u.username = $name RETURN u", name = username).single()

        print("get_user: " + username)
        session = self.get_driver().session()
        u = session.read_transaction(__tx_get_user, username)
        print("get_user: return [" + str(u) + "]")
        return u
        
    def get_memes(self, props=None):
        session = self.get_driver().session()
        ret = session.run("MATCH (m:Meme) RETURN m").value()
        print('RET === ' + str(ret))
        return ret

    def get_meme(self, meme):
        session = self.get_driver().session()
        print('-> requested meme: meme = ' + meme)
        ret = session.run("MATCH (m:Meme) WHERE m.name = $name RETURN m", name=meme).value()
        print('-> requested meme: returns = ' + str(ret))
        return ret


# Let's call the driver a 'db'
def get_db():
    print("get_db: ")

    if 'db' not in g:        
        print("---------------> connecting to DB:")
        g.db = DB()
        print("---------------> connecting to DB: done")

    print("get_db: done")
    return g.db

def close_db(e=None):
    print("---> close_db: !")
    db = g.pop('driver', None)

    if db is not None:
        print("Closing DB here. TODO: disconnect?")
    else:
        print("db is None. Nothing else to be done.")

    print("---> close_db: done")

def init_driver():
    d = get_db()

@click.command('init-db')
@with_appcontext
def init_db_command():
    print("---> init_db_command: !")
    """Clear the existing data and create new tables."""
    init_driver()
    click.echo('Initialized the database.')
    print("---> init_db_command: done")



def init_app(app):
    print("-----> init_app: !")
    #app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    print("-----> init_app: done")





    