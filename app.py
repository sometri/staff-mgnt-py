from flask import Flask, render_template, request, redirect, url_for, send_file
import mysql.connector
import csv
from io import BytesIO, TextIOWrapper

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # your MySQL username
        password="",  # your MySQL password
        database="staff_mgnt_py"
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_staff', methods=['GET', 'POST'])
def add_staff():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        department = request.form['department']
        email = request.form['email']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO staffs (name, position, department, email) VALUES (%s, %s, %s, %s)",
            (name, position, department, email)
        )
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('staff_list'))
    
    return render_template('add_staff.html')

@app.route('/staff_list')
def staff_list():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM staffs")
    staffs = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('staff_list.html', staffs=staffs)

@app.route('/report')
def report():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM staffs")
    staffs = cursor.fetchall()
    cursor.close()
    connection.close()

    # Create a CSV file
    output = BytesIO()
    writer = csv.writer(TextIOWrapper(output, 'utf-8', newline=''))
    writer.writerow(['ID', 'Name', 'Position', 'Department', 'Email'])
    for staff in staffs:
        writer.writerow(staff)
    
    output.seek(0)
    
    return send_file(output, download_name='staff_report.csv', as_attachment=True, mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)
