# Import packages
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL connection
app.config['MYSQL_HOST'] = ''
app.config['MYSQL_USER'] = ''
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = ''

mysql = MySQL(app)

# Settings
app.config['SECRET_KEY'] = ''

# Index
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM task')
    # Get all data from DB
    data = cursor.fetchall()
    return render_template('index.html', tasks = data)  

# Add task
@app.route('/add-task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        day = request.form['day']
        state = request.form['state']
        priority = request.form['priority']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO task (name, description, day, state, priority) VALUES (%s, %s, %s, %s, %s)', (name, description, day, state, priority))
        mysql.connection.commit()
        flash('The task was created successfully')
        return redirect(url_for('index'))

# Edit task
@app.route('/edit/<id>')
def get_task(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM task WHERE id = %s', [id])
    data = cursor.fetchall()
    return render_template('edit-task.html', task = data[0])

# Update task
@app.route('/update/<id>', methods=['POST'])
def update_task(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        day = request.form['day']
        state = request.form['state']
        priority = request.form['priority']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE task
            SET name = %s,
                description = %s,
                day = %s,
                state = %s,
                priority = %s
            WHERE id = %s
        """, (name, description, day, state, priority, id))
        mysql.connection.commit()
        flash('The task was edited successfully')
        return redirect(url_for('index'))

# Delete task
@app.route('/delete/<string:id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM task WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('The task was successfully deleted')
    return redirect(url_for('index'))

# View task
@app.route('/view/<id>')
def view(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM task WHERE id = %s', [id])
    data = cursor.fetchall()
    return render_template('view-task.html', task = data[0])
    
if __name__ == '__main__':
    app.run(port = 5000, debug = True)
