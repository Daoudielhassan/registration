from flask import Flask, request, jsonify
import psycopg2

# Initialize Flask app
app = Flask(__name__)

# Connect to PostgreSQL database
def connect_db():
    connection = psycopg2.connect(
        host="localhost",
        database="registration_db",
        user="your_username",  # Replace with your PostgreSQL username
        password="your_password"  # Replace with your PostgreSQL password
    )
    return connection

# Endpoint to handle registration
@app.route('/register', methods=['POST'])
def register():
    # Get the form data from the request
    data = request.get_json()
    
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    
    if not first_name or not last_name or not email or not phone_number:
        return jsonify({"error": "Please fill all fields"}), 400
    
    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    try:
        # Insert the new user into the database
        cur.execute("""
            INSERT INTO users (first_name, last_name, email, phone_number)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, email, phone_number))
        
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201

    except psycopg2.IntegrityError:
        conn.rollback()  # Rollback if there's an error
        return jsonify({"error": "Email already exists"}), 400

    finally:
        cur.close()
        conn.close()

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
