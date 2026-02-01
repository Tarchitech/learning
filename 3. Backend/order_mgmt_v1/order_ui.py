"""
Flask Template Rendering Example (Jinja2) - Simplified Learning Version

Core Concepts:
1. Flask uses render_template() to render HTML templates
2. Jinja2 is a template engine that allows variables, loops, conditions in HTML
3. Template files are placed in templates/ directory
4. Data is passed to templates via render_template() second parameter
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from db_operations import list_users, create_user, list_products, list_orders, create_product, create_order

# Create Flask application instance
app = Flask(__name__)
# Secret key is required to sign session cookie; without it session data cannot be trusted.
# In production use a random value from env (e.g. os.environ.get('SECRET_KEY')).
app.secret_key = 'secret-key-for-session-data'


@app.context_processor
def inject_current_user():
    """
    Inject current_user into every template so we can show 'Logged in as ...' in the nav.
    Session stores user_id and user_name after login; here we expose them as current_user.
    """
    user = None
    if session.get('user_id') and session.get('user_name'):
        user = {'id': session['user_id'], 'full_name': session['user_name']}
    return dict(login_user=user)


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
# Login - Check user in DB and save to session
# ============================================================================
@app.route('/login', methods=['POST'])
def login():
    """
    Login: look up user by full_name (using list_users), save to session, show success/failure message.
    Session is server-side state keyed by a cookie; after login we store user_id and user_name
    so other routes and templates can know who is logged in without passing it in the URL.
    """
    user_name = request.form.get('user_name', '').strip()
    users = list_users().get('users', [])
    user = next((u for u in users if u['full_name'] == user_name), None) if user_name else None
    if user:
        # Store logged-in user in session; persisted in signed cookie, available on subsequent requests
        session['user_id'] = user['id']
        session['user_name'] = user['full_name']
        flash('Login successful.', 'success')
    else:
        flash('Login failed. User not found.', 'error')
    return redirect(url_for('index'))


# ============================================================================
# Logout - Clear session so user is no longer logged in
# ============================================================================
@app.route('/logout')
def logout():
    """Clear session so the user is logged out; redirect to home."""
    session.clear()
    return redirect(url_for('index'))


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
            return redirect(url_for('users_page'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('new_user'))

    
    # GET request: Display form page
    # Render new_user.html template
    return render_template('new_user.html', title='Create User')


# ============================================================================
# Route 4: Products List
# ============================================================================
@app.route('/products')
def products_page():
    """
    Products list page
    
    Workflow:
    1. Get products data from database
    2. Pass data to template
    3. Template uses Jinja2 syntax to render HTML
    """
    # Get products data from database
    result = list_products()
    products = result.get('products', [])  # List of products
    total = result.get('total', 0)    # Total number of products
    
    # Render template with data
    # In template, can use: {{ products }}, {{ total }}, {{ title }}
    return render_template(
        'products.html',
        products=products,      # Variable passed to template
        total=total,        # Variable passed to template
        title='Products List' # Variable passed to template
    )

# ============================================================================
# Route 5: Create Product
# ============================================================================
@app.route('/products/new', methods=['GET', 'POST'])
def new_product():
    """
    Create new product form
    
    Workflow:
    - GET request: Display form page
    - POST request: Handle form submission, create product
    """
    # Handle POST request (form submission)
    if request.method == 'POST':
        # Get data from form
        # request.form is a dictionary containing form fields
        name = request.form.get('name')        # Get name field value
        price = request.form.get('price')  # Get price field value

        # Create product
        try:
            result = create_product(name, int(float(price)*100))
            flash(f'Product {name} created successfully!', 'success')
            return redirect(url_for('products_page'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('new_product'))

    # GET request: Display form page
    return render_template('new_product.html', title='Create Product')


# ============================================================================
# Route 6: Orders List - Select user first, then list orders
# ============================================================================
@app.route('/orders', methods=['GET', 'POST'])
def orders_page():
    """
    Orders list page
    
    Workflow:
    1. User selects a user from dropdown
    2. Get orders data for selected user from database
    3. Pass data to template
    4. Template displays orders list
    """
    # Get users for dropdown
    users_result = list_users()
    users = users_result.get('users', [])
    
    # Handle POST request (user selection)
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        
        if user_id:
            user_id = int(user_id)
            # Get orders for selected user
            result = list_orders(user_id)
            orders = result.get('orders', [])
            total = result.get('total', 0)
            
            return render_template(
                'orders.html',
                users=users,
                orders=orders,
                total=total,
                selected_user_id=user_id,
                title='Orders List'
            )
    
    # GET request: show user selection form; pre-select the logged-in user from session if any
    # so the dropdown defaults to current user without requiring them to pick again
    selected_user_id = session.get('user_id')
    return render_template(
        'orders.html',
        users=users,
        orders=[],
        total=0,
        selected_user_id=selected_user_id,
        title='Orders List'
    )

# ============================================================================
# Route 7: Create Order - Simple order creation form
# ============================================================================
@app.route('/orders/new', methods=['GET', 'POST'])
def new_order():
    """
    Create new order form
    
    Workflow:
    - GET request: Display form with user dropdown and products table
    - POST request: Handle form submission, create order with selected items
    """
    # Get users and products for the form
    users_result = list_users()
    users = users_result.get('users', [])
    products_result = list_products()
    products = products_result.get('products', [])
    
    # Handle POST request (form submission)
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        
        if not user_id:
            flash('Please select a user', 'error')
            return redirect(url_for('new_order'))
        
        # Collect items with quantity > 0
        items = []
        for product in products:
            quantity = request.form.get(f'qty_{product["id"]}', '0')
            try:
                qty = int(quantity)
                if qty > 0:
                    items.append({
                        'product_id': product['id'],
                        'quantity': qty
                    })
            except ValueError:
                pass  # Skip invalid quantities
        
        if not items:
            flash('Please select at least one product', 'error')
            return redirect(url_for('new_order'))
        
        # Create order
        try:
            result = create_order(int(user_id), 'pending', items)
            flash(f'Order #{result["id"]} for user #{user_id} in {result["status"]} Status created successfully!', 'success')
            return redirect(url_for('orders_page'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('new_order'))
    
    # GET request: display form; pre-select logged-in user from session so Create Order
    # form opens with the current user already selected in the dropdown
    selected_user_id = session.get('user_id')
    return render_template(
        'new_order.html',
        users=users,
        products=products,
        selected_user_id=selected_user_id,
        title='Create Order'
    )





# ============================================================================
# Start Server
# ============================================================================
if __name__ == '__main__':
    # Run Flask development server
    # debug=True: Enable debug mode (auto-reload on code changes)
    # port=8022: Use port 8022 (avoid conflict with order_api.py on 8021)
    app.run(debug=True, host='0.0.0.0', port=8022)

