from flask import Flask, request, jsonify
import psycopg2
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/pets', methods=['GET', 'POST'])
def pets_router():
    if request.method == 'POST':
        data = request.get_json()
        post_pets(
            data['name'],
            data['owner_id'],
            data['breed'],
            data['color'] )
        return 'Created'
    elif request.method == 'GET':
        pets = get_pets()
        return jsonify(pets)
    else: 
        return 'No valid method requested'

@app.route('/pets/remove/', methods=['DELETE'] )
def delete_pet():
    id = request.args.get('id')
    send_pet_to_farm(id)
    return 'The pet was sent to the farm for good dogs.'

@app.route('/pets/update/', methods=['PUT'])
def update_pet_details_route():
    update_pet_details(
        request.form.get('name'),
        request.form.get('owner_id'),
        request.form.get('breed'),
        request.form.get('color'),
        request.form.get('pet_id')
        )
    return 'The pet with id {id_} was updated.'

@app.route('/pets/checkin/', methods=['PUT'])
def pet_checkin_route():
    id = request.get_json()['id']
    checkin_pet(id)
    return('Pet checked in')

# GET FUNCTION
def get_pets():
    conn = None
    query = "SELECT * FROM pet ORDER BY id;"
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return(rows)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# POST FUNCTION
def post_pets(name, owner_id, breed, color):
    conn = None
    query = "INSERT INTO pet (name, owner_id, breed, color) VALUES (%s, %s, %s, %s);"
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute(query, (name, owner_id, breed, color,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# DELETE FUNCTION :(
def send_pet_to_farm(pet_id):
    conn = None
    query = "DELETE FROM pet WHERE id = %s;"
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute(query, (pet_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# PUT FUNCTION FOR DETAILS
def update_pet_details(name, owner_id, breed, color, pet_id):
    conn = None
    query = "UPDATE pet SET name = %s, owner_id=%s, breed=%s, color=%s WHERE id = %s;"
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute(query, (name, owner_id, breed, color, pet_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

# PUT FUNCTION FOR CHECKIN 
def checkin_pet(pet_id):
    conn = None
    query = "UPDATE pet SET checked_in = current_date WHERE id = %s;"
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute(query, (pet_id,))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

app.route('/owner', methods=['GET', 'POST'])
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

@app.route('/count', methods=['GET'])
def count_router():
    count = get_count()
    return jsonify(count)
    
def get_count() : 
    conn = None
    query = "SELECT owner.name, count(*) FROM pet JOIN owner ON pet.owner_id = owner.id GROUP BY owner.name;"
    try:
        conn = psycopg2.connect("dbname=pet_hotel")
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        return(rows)
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


# print('name:')
# name = input()
# print('owner_id:')
# owner_id = input()
# print('breed:')
# breed = input()
# print('color:')
# color = input()
# update_pet_details('Venus', 4)
# post_pets(name, owner_id, breed, color)