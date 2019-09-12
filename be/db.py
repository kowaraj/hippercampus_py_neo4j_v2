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
            print("tx_get_user: "+ username)
            return tx.run("MATCH (u:User) WHERE u.username = $name RETURN u", name = username).single()


        print("get_user: " + username)
        session = self.get_driver().session()
        u = session.read_transaction(__tx_get_user, username)
        print("get_user: return [" + str(u) + "]")
        return u

    def add_user(self, username, password_hash):

        def __tx_add_user(tx, username, password_hash):
            return tx.run("CREATE (u:User {username:$username, password:$password}) RETURN u.username", username=username, password=password_hash)

        print("add_user: " + username)
        session = self.get_driver().session()
        u = session.write_transaction(__tx_add_user, username, password_hash)
        print("add_user: result " + str(u))
    
    def get_posts(self):
        return []





# Let's call the driver a 'db'
def get_db():
    if 'db' not in g:
        print("Connecting to a DB...")
        g.db = DB()

    return g.db

def close_db(e=None):
    db = g.pop('driver', None)

    if db is not None:
        print("Closing DB here. TODO: disconnect?")
    else:
        print("db is None. Nothing else to be done.")

def init_driver():
    d = get_db()

    # with current_app.open_resource('schema.sql') as f:
    #     db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_driver()
    click.echo('Initialized the database.')



def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


def get_user_by_id(user_id):
    return {'id': 20, 'username': 'fakeusername'}


    