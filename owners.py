from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/owner', methods=['GET', 'POST'])
def owner_router_get_post():
    if request.method == 'POST':
        add_owner( request.args.get('name') )
        return 'POST'
    elif request.method == 'GET':
        owners = get_owners()
        return jsonify(owners)
    else: 
        return 'No valid method requested'


@app.route('/owner/delete/<id_>', methods=['DELETE'])
def owner_router_delete():
    if request.method == 'DELETE':
        delete_owner(id_)
        return 'DELETE'
    else: 
        return 'No valid method requested'


def get_owners():
    conn = None
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute("SELECT * FROM owner;")
        rows = cur.fetchall()
        return(rows)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def add_owner(name):
    conn = None
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = con.cursor()
        cur.execute("INSERT INTO owner (name) VALUES (%s);")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def delete_owner(id):
    conn = None
    query = "DELETE FROM owner WHERE id = %s;"
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute(query, (id))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
