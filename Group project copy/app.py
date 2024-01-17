from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Sample data structures to store tenant and energy consumption information
tenants = [
    {"id": 1, "name": "Mazen Alić", "email": "john@example.com", "phone": "555-1234", "address": "123 Main St", "room_number": "101", "energy_consumption": 100},
    {"id": 2, "name": "Doruk Aydoğan, ", "email": "jane@example.com", "phone": "555-5678", "address": "456 Oak St", "room_number": "202", "energy_consumption": 150},
    {"id": 3, "name": "Odon Rooijer", "email": "bob@example.com", "phone": "555-9876", "address": "789 Pine St", "room_number": "303", "energy_consumption": 120},
    {"id": 4, "name": "Avend Ayoub", "email": "alice@example.com", "phone": "555-4321", "address": "101 Elm St", "room_number": "404", "energy_consumption": 130}
]

# Sample user data structure (for demonstration purposes)
users = []

addblocker_data = [{"device": "Computer", "status": "Disabled"}]

app.static_folder = 'static'

# Sample announcements data
announcements = [
    "Important Announcement: Classes are canceled tomorrow.",
    "Reminder: Rent is due by the end of the week."
]

# Sample complaints data
complaints = []

# Route for deleting announcements
@app.route('/delete_announcement', methods=['POST'])
def delete_announcement():
    announcement_text = request.form.get('announcement_text')

    if announcement_text in announcements:
        announcements.remove(announcement_text)
        return jsonify({'success': True, 'message': 'Announcement deleted successfully'})
    else:
        return jsonify({'success': False, 'message': 'Announcement not found'})


# Upload announcement route
@app.route('/upload_announcement', methods=['POST'])
def upload_announcement():
    if request.method == 'POST':
        announcement_text = request.form.get('announcement')
        announcements.append(announcement_text)
        return redirect(url_for('home'))


# Signup route
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple example: Check if the username is not already taken
        if any(user['username'] == username for user in users):
            return render_template('signup.html', error='Username already taken')

        # Store the user data (for demonstration purposes)
        users.append({'username': username, 'password': password})

        # Redirect to login page after successful registration
        return redirect(url_for('login'))

    return render_template('signup.html', error=None)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Simple example: Check if username and password match
        user = next((u for u in users if u['username'] == username and u['password'] == password), None)
        if user:
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')

    return render_template('login.html', error=None)

# Route for the home page
@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Handle the uploaded announcement here (save to database, etc.)
        announcement = request.form.get('announcement')
        announcements.append(announcement)

    return render_template('index.html', tenants=tenants, announcements=announcements)

# Route to display tenant information
@app.route('/tenant/<int:tenant_id>')
def tenant_info(tenant_id):
    tenant = next((t for t in tenants if t['id'] == tenant_id), None)
    if tenant:
        return render_template('tenant_info.html', tenant=tenant)
    else:
        return "Tenant not found", 404

# Route to display energy consumption information
@app.route('/energy/<int:tenant_id>')
def energy_info(tenant_id):
    tenant = next((t for t in tenants if t['id'] == tenant_id), None)
    if tenant:
        consumption = tenant['energy_consumption']
        return render_template('energy_info.html', tenant=tenant, consumption=consumption)
    else:
        return "Tenant not found", 404

# Dashboard route
@app.route('/dashboard')
def dashboard():
    return render_template('energy_overview.html', tenants=tenants)

# Network Monitoring route
@app.route('/add_blocker')
def add_blocker():
    return render_template('add_blocker.html', addblocker_data=addblocker_data)

# Route to enable the ad blocker
@app.route('/enable_add_blocker', methods=['POST'])
def enable_add_blocker():
    # Your logic to enable the ad blocker (update the status in adblocker_data)
    addblocker_data[0]['status'] = 'Enabled'  # Replace this with your actual logic
    return redirect(url_for('add_blocker'))
    
    # Redirect back to the add blocker page
    return redirect(url_for('add_blocker'))

# Complaint upload route
# Rename the route function from 'complaint' to 'submit_complaint'
@app.route('/upload_complaint', methods=['POST'])
def upload_complaint():
    if request.method == 'POST':
        complaint_text = request.form.get('complaint')
        complaints.append(complaint_text)
        # Redirect to the complaints page after successful complaint submission
        return redirect(url_for('view_complaints'))

# Rename the route function for viewing complaints to 'complaints'
# Rename the route function for viewing complaints to 'view_complaints'
@app.route('/complaints')
def view_complaints():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('complaints.html', complaints=complaints)

@app.route('/rules')
def rules():
    return render_template('rules.html')


# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Use '0.0.0.0' as the host and 5000 as the port
    app.run(host='0.0.0.0', port=5000, debug=True)
