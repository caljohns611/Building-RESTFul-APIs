# task 1

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
ma = Marshmallow(app)

class MemberSchema(ma.Schema):
    name = fields.String(required=True)
    age = fields.String(required=True)

    class Meta:
        fields = ("name", "age")

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)

def get_db_connection():
    
    db_name = "gym_db"
    user = "root"
    password = "password"
    host = "127.0.0.1"

    try:
        conn = mysql.connector.connect(
            database=db_name,
            user=user,
            password=password,
            host=host
        )

        print("Connected to MSQL databse successfully")
        return conn
    
    except Error as e:
        print(f"Error: {e}")
        return None

@app.route('/')
def home():
    return 'Welcome to Gym Membership'

# task 2

@app.route("/members", methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Members"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members", methods=["POST"])
def add_member():
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
        
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        new_member = (member_data['name'], member_data['age'])

        query = "INSERT INTO Memebers (name, age) VALUES(%s, %s)"

        cursor.execute(query, new_member)
        conn.commit()

        return jsonify({"message": "New customer added successfully"}), 201
    except Error as e:
        print(f"Erro: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
        
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['name'], member_data['age'], id)

        query = 'UPDATE Members SET name = %s, age = %s WHERE id = %s'

        cursor.execute(query, updated_member)
        conn.commit()


        return jsonify({"message": "New customer added successfully"}), 201
    except Error as e:
        print(f"Erro: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/members/<int:id>", methods=["DELETE"])
def delete_member(id):
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        member_remove = (id)

        cursor.excute("SELECT * FROM Memebrs WHERE id = %s", member_remove)
        member = cursor.fetchone()
        if not member:
            return jsonify({"error": "Memeber not found"}), 404
        
        query = "DELETE FROM Members WHERE id = %s"
        cursor.excute(query, member_remove)
        conn.commit()

        return jsonify({"message": "Member removed successfully"}), 200
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"})
    
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# task 3

@app.route("/wrkout_sessions", methods=["GET"])
def get_members():
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM Workout_sessions"

        cursor.execute(query)

        members = cursor.fetchall()

        return members_schema.jsonify(members)
    
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()



@app.route("/workout_sessions/<int:id>", methods=["PUT"])
def update_member(id):
    try:
        member_data = member_schema.load(request.json)
    except ValidationError as e:
        print(f"Error: {e}")
        return jsonify(e.messages), 400
        
    try:
        conn = get_db_connection()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500
        cursor = conn.cursor()

        updated_member = (member_data['date'], member_data['member_id'], member_data['duration_minutes'], member_data['calories_burned'], id)

        query = 'UPDATE Workout_sessions SET date = %s, member_id = %s, duration_minutes = %s, calories_burned = %s WHERE id = %s'

        cursor.execute(query, updated_member)
        conn.commit()


        return jsonify({"message": "New customer added successfully"}), 201
    except Error as e:
        print(f"Erro: {e}")
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()




if __name__=='__main':
    app.run(debug=True)
