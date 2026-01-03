"""
Flask Template Rendering Example (Jinja2) - Simplified Learning Version

Core Concepts:
1. Flask uses render_template() to render HTML templates
2. Jinja2 is a template engine that allows variables, loops, conditions in HTML
3. Template files are placed in templates/ directory
4. Data is passed to templates via render_template() second parameter
"""

from flask import Flask, render_template, request, redirect, url_for, flash
from db_operations import list_users, create_user, list_products

# Create Flask application instance
app = Flask(__name__)
app.secret_key = 'secret-key-for-flash-messages'  # Required for flash messages


# ============================================================================
# Route 1: Home Page - Demonstrates basic variable passing
# ============================================================================
@app.route('/')
def index():
    """
    Home page route
    
    Notes:
    - render_template() looks for templates/index.html file
    - Second parameter title='Home' is passed to template, accessible as {{ title }}
    """
    return render_template('index.html', title='Home')


# ============================================================================
# Route 2: Users List - Demonstrates loops and conditionals
# ============================================================================
@app.route('/users')
def users_page():
    """
    Users list page
    
    Workflow:
    1. Get user data from database
    2. Pass data to template
    3. Template uses Jinja2 syntax to render HTML
    """
    # Get user data from database
    result = list_users()
    users = result.get('users', [])  # List of users
    total = result.get('total', 0)    # Total number of users
    
    # Render template with data
    # In template, can use: {{ users }}, {{ total }}, {{ title }}
    return render_template(
        'users.html',
        users=users,      # Variable passed to template
        total=total,        # Variable passed to template
        title='Users List' # Variable passed to template
    )

# ============================================================================
# Route 3: Create User Form - Demonstrates form handling
# ============================================================================
@app.route('/users/new', methods=['GET', 'POST'])
def new_user():
    """
    Create new user form
    
    Notes:
    - GET request: Display form page
    - POST request: Handle form submission, create user
    
    request.method checks request type:
    - 'GET': User visits page to see form
    - 'POST': User submits form
    """
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get data from form
        # request.form is a dictionary containing form fields
        email = request.form.get('email')        # Get email field value
        full_name = request.form.get('full_name')  # Get full_name field value
        
        # Create user
        try:
            result = create_user(email, full_name)
            # flash() displays temporary messages (success/error notifications)
            flash(f'User {full_name} created successfully!', 'success')
            # redirect() redirects to users list page
            return redirect(url_for('users_page'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            # On error, redirect back to form page
            return redirect(url_for('new_user'))
    
    # GET request: Display form page
    # Render new_user.html template
    return render_template('new_user.html', title='Create User')


# ============================================================================
# Start Server
# ============================================================================
if __name__ == '__main__':
    # Run Flask development server
    # debug=True: Enable debug mode (auto-reload on code changes)
    # port=8022: Use port 8022 (avoid conflict with order_api.py on 8021)
    app.run(debug=True, host='0.0.0.0', port=8022)

