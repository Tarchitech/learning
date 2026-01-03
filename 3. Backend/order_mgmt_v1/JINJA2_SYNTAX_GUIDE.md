# Jinja2 Template Syntax Guide

A beginner-friendly guide to Jinja2 template syntax with practical examples for Flask web development.

## Table of Contents

1. [Introduction](#introduction)
2. [Basic Syntax](#basic-syntax)
3. [Variables and Filters](#variables-and-filters)
4. [Control Structures](#control-structures)
5. [Template Inheritance](#template-inheritance)
6. [Includes](#includes)
7. [Comments](#comments)
8. [Practical Examples](#practical-examples)
9. [Common Patterns](#common-patterns)

---

## Introduction

Jinja2 is a modern templating engine for Python. It allows you to embed Python-like expressions in HTML templates to dynamically generate content.

**Key Concepts:**
- **Templates**: HTML files with Jinja2 syntax (stored in `templates/` folder)
- **Variables**: Data passed from Flask to templates
- **Expressions**: `{{ }}` for output, `{% %}` for logic
- **Filters**: Functions that modify variables

---

## Basic Syntax

### 1. Variables (Output)

Use double curly braces `{{ }}` to output variables:

```html
<p>Hello, {{ name }}!</p>
<p>User ID: {{ user.id }}</p>
<p>Total: ${{ total }}</p>
```

**Example:**
```python
# Flask route
@app.route('/user/<name>')
def show_user(name):
    return render_template('user.html', name=name)
```

```html
<!-- templates/user.html -->
<h1>Welcome, {{ name }}!</h1>
```

**Output:**
```html
<h1>Welcome, John!</h1>
```

---

### 2. Accessing Dictionary/Object Properties

You can access nested properties using dot notation:

```html
{{ user.email }}           <!-- Access attribute -->
{{ user['email'] }}        <!-- Dictionary access (alternative) -->
{{ order.items[0].name }}  <!-- Nested access -->
```

**Example:**
```python
# Flask route
user = {"id": 1, "email": "john@example.com", "full_name": "John Doe"}
return render_template('profile.html', user=user)
```

```html
<!-- templates/profile.html -->
<p>Email: {{ user.email }}</p>
<p>Name: {{ user.full_name }}</p>
```

---

## Variables and Filters

Filters modify variables. Use the pipe `|` symbol:

### Common Filters

#### String Filters

```html
{{ name|upper }}           <!-- Convert to uppercase -->
{{ name|lower }}           <!-- Convert to lowercase -->
{{ name|title }}           <!-- Title case -->
{{ name|capitalize }}      <!-- First letter uppercase -->
{{ name|trim }}            <!-- Remove whitespace -->
{{ name|replace('old', 'new') }}  <!-- Replace text -->
```

**Example:**
```html
{{ "hello world"|upper }}     <!-- Output: HELLO WORLD -->
{{ "hello world"|title }}     <!-- Output: Hello World -->
{{ "  hello  "|trim }}        <!-- Output: hello -->
```

#### Number Filters

```html
{{ price|round(2) }}       <!-- Round to 2 decimal places -->
{{ count|int }}            <!-- Convert to integer -->
{{ amount|abs }}           <!-- Absolute value -->
```

**Example:**
```html
{{ 123.456|round(2) }}     <!-- Output: 123.46 -->
{{ "42"|int }}             <!-- Output: 42 -->
```

#### List/Array Filters

```html
{{ items|length }}         <!-- Get length -->
{{ items|first }}          <!-- First item -->
{{ items|last }}           <!-- Last item -->
{{ items|join(', ') }}     <!-- Join with separator -->
{{ items|sort }}           <!-- Sort list -->
{{ items|reverse }}        <!-- Reverse list -->
```

**Example:**
```html
{{ [1, 2, 3]|length }}              <!-- Output: 3 -->
{{ ['a', 'b', 'c']|join(' - ') }}  <!-- Output: a - b - c -->
```

#### Date/Time Filters

```html
{{ date|dateformat('%Y-%m-%d') }}  <!-- Format date -->
{{ datetime|time }}                 <!-- Extract time -->
```

#### Default Values

```html
{{ name|default('Anonymous') }}    <!-- Use default if empty -->
{{ value|default('N/A', true) }}   <!-- Use default if None/empty -->
```

**Example:**
```html
{{ user.name|default('Guest') }}    <!-- Shows 'Guest' if name is empty -->
```

#### Chaining Filters

You can chain multiple filters:

```html
{{ name|upper|trim|default('N/A') }}
```

**Example:**
```html
{{ "  hello world  "|trim|upper }}  <!-- Output: HELLO WORLD -->
```

---

## Control Structures

### 1. If/Else Statements

Use `{% if %}`, `{% elif %}`, `{% else %}`, `{% endif %}`:

```html
{% if condition %}
    <p>Condition is true</p>
{% elif other_condition %}
    <p>Other condition is true</p>
{% else %}
    <p>No condition is true</p>
{% endif %}
```

**Example:**
```html
{% if user.is_admin %}
    <button>Admin Panel</button>
{% else %}
    <button>User Dashboard</button>
{% endif %}
```

**Complex Conditions:**
```html
{% if user and user.is_active %}
    <p>Active user</p>
{% endif %}

{% if count > 0 and count < 100 %}
    <p>Count is between 0 and 100</p>
{% endif %}

{% if not user.is_banned %}
    <p>User is not banned</p>
{% endif %}
```

### 2. For Loops

Use `{% for %}`, `{% endfor %}` to iterate over lists:

```html
{% for item in items %}
    <p>{{ item }}</p>
{% endfor %}
```

**Example:**
```html
<ul>
    {% for user in users %}
        <li>{{ user.full_name }} - {{ user.email }}</li>
    {% endfor %}
</ul>
```

**Loop Variables:**

Jinja2 provides special loop variables:

```html
{% for item in items %}
    <p>
        Item {{ loop.index }}: {{ item }}
        (First: {{ loop.first }}, Last: {{ loop.last }})
    </p>
{% endfor %}
```

**Available Loop Variables:**
- `loop.index` - Current iteration (1-indexed)
- `loop.index0` - Current iteration (0-indexed)
- `loop.first` - True if first iteration
- `loop.last` - True if last iteration
- `loop.length` - Length of the sequence
- `loop.previtem` - Previous item (if exists)
- `loop.nextitem` - Next item (if exists)

**Example:**
```html
<table>
    <tr>
        <th>#</th>
        <th>Name</th>
        <th>Email</th>
    </tr>
    {% for user in users %}
    <tr>
        <td>{{ loop.index }}</td>
        <td>{{ user.full_name }}</td>
        <td>{{ user.email }}</td>
    </tr>
    {% endfor %}
</table>
```

**Empty Loops:**

Handle empty lists:

```html
{% for item in items %}
    <p>{{ item }}</p>
{% else %}
    <p>No items found.</p>
{% endfor %}
```

**Nested Loops:**

```html
{% for order in orders %}
    <h3>Order {{ order.id }}</h3>
    <ul>
        {% for item in order.items %}
            <li>{{ item.product.name }} x {{ item.quantity }}</li>
        {% endfor %}
    </ul>
{% endfor %}
```

### 3. Range Loops

Generate numbers:

```html
{% for i in range(1, 11) %}
    <p>Number {{ i }}</p>
{% endfor %}
```

---

## Template Inheritance

Template inheritance allows you to create a base template and extend it.

### Base Template (`base.html`)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Default Title{% endblock %}</title>
    <style>
        {% block styles %}{% endblock %}
    </style>
</head>
<body>
    <header>
        <h1>{% block header %}My Website{% endblock %}</h1>
    </header>
    
    <main>
        {% block content %}
        <!-- Child template content goes here -->
        {% endblock %}
    </main>
    
    <footer>
        {% block footer %}
        <p>&copy; 2024 My Website</p>
        {% endblock %}
    </footer>
</body>
</html>
```

### Child Template (`users.html`)

```html
{% extends "base.html" %}

{% block title %}Users - My Website{% endblock %}

{% block header %}User Management{% endblock %}

{% block content %}
<h2>All Users</h2>
<ul>
    {% for user in users %}
        <li>{{ user.full_name }}</li>
    {% endfor %}
</ul>
{% endblock %}
```

**Key Points:**
- `{% extends "base.html" %}` must be the first line
- `{% block name %}` defines replaceable sections
- `{{ super() }}` includes parent block content

**Using `super()`:**

```html
{% block styles %}
    {{ super() }}  <!-- Include parent styles -->
    <style>
        .custom { color: blue; }
    </style>
{% endblock %}
```

---

## Includes

Include other templates for reusable components:

```html
{% include 'header.html' %}

<main>
    <p>Main content</p>
</main>

{% include 'footer.html' %}
```

**Example: Navigation Component**

```html
<!-- templates/components/nav.html -->
<nav>
    <a href="/">Home</a>
    <a href="/users">Users</a>
    <a href="/products">Products</a>
</nav>
```

```html
<!-- templates/base.html -->
<body>
    {% include 'components/nav.html' %}
    {% block content %}{% endblock %}
</body>
```

**Passing Variables to Includes:**

```html
{% include 'user_card.html' with user=current_user %}
```

---

## Comments

Jinja2 comments are not included in the output:

```html
{# This is a comment #}
{# 
   Multi-line
   comment
#}

<!-- HTML comments ARE visible in source -->
```

---

## Practical Examples

### Example 1: User List Page

**Flask Route:**
```python
@app.route('/users')
def show_users():
    result = list_users()
    return render_template('users.html', 
                         users=result['users'], 
                         total=result['total'])
```

**Template (`templates/users.html`):**
```html
{% extends "base.html" %}

{% block title %}Users{% endblock %}

{% block content %}
<h1>All Users ({{ total }} total)</h1>

{% if users %}
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Created</th>
            </tr>
        </thead>
        <tbody>
            {% for user in users %}
            <tr>
                <td>{{ user.id }}</td>
                <td>{{ user.full_name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.created_at|dateformat('%Y-%m-%d') if user.created_at else 'N/A' }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% else %}
    <p>No users found.</p>
{% endif %}
{% endblock %}
```

### Example 2: Product List with Formatting

**Template:**
```html
<h2>Products</h2>
<div class="products">
    {% for product in products %}
    <div class="product-card">
        <h3>{{ product.name }}</h3>
        <p class="price">${{ (product.price_cents / 100)|round(2) }}</p>
        <p>ID: {{ product.id }}</p>
    </div>
    {% else %}
    <p>No products available.</p>
    {% endfor %}
</div>
```

### Example 3: Order Details

**Template:**
```html
{% extends "base.html" %}

{% block title %}Order #{{ order.id }}{% endblock %}

{% block content %}
<h1>Order #{{ order.id }}</h1>

<div class="order-info">
    <p><strong>User:</strong> {{ order.user.full_name }}</p>
    <p><strong>Status:</strong> 
        <span class="status-{{ order.status|lower }}">
            {{ order.status|upper }}
        </span>
    </p>
    <p><strong>Created:</strong> {{ order.created_at }}</p>
</div>

<h2>Order Items</h2>
<table>
    <thead>
        <tr>
            <th>Product</th>
            <th>Quantity</th>
            <th>Price (at purchase)</th>
            <th>Subtotal</th>
        </tr>
    </thead>
    <tbody>
        {% for item in order.order_items %}
        <tr>
            <td>{{ item.product.name }}</td>
            <td>{{ item.quantity }}</td>
            <td>${{ (item.price_cents_at_purchase / 100)|round(2) }}</td>
            <td>${{ ((item.price_cents_at_purchase * item.quantity) / 100)|round(2) }}</td>
        </tr>
        {% endfor %}
    </tbody>
    <tfoot>
        <tr>
            <td colspan="3"><strong>Total:</strong></td>
            <td><strong>${{ (order.total_amount_cents / 100)|round(2) }}</strong></td>
        </tr>
    </tfoot>
</table>
{% endblock %}
```

### Example 4: Conditional Styling

```html
<div class="user-card {% if user.is_premium %}premium{% endif %}">
    <h3>{{ user.full_name }}</h3>
    {% if user.is_premium %}
        <span class="badge">Premium Member</span>
    {% endif %}
</div>
```

### Example 5: Pagination

```html
<div class="pagination">
    {% if page > 1 %}
        <a href="?page={{ page - 1 }}">Previous</a>
    {% endif %}
    
    <span>Page {{ page }} of {{ total_pages }}</span>
    
    {% if page < total_pages %}
        <a href="?page={{ page + 1 }}">Next</a>
    {% endif %}
</div>
```

---

## Common Patterns

### Pattern 1: Format Currency

```html
<!-- Convert cents to dollars -->
${{ (price_cents / 100)|round(2) }}

<!-- Or create a custom filter in Flask -->
```

### Pattern 2: Check if List is Empty

```html
{% if items %}
    <!-- Show items -->
{% else %}
    <p>No items to display.</p>
{% endif %}
```

### Pattern 3: Conditional Classes

```html
<div class="item {% if item.is_active %}active{% else %}inactive{% endif %}">
    {{ item.name }}
</div>
```

### Pattern 4: Loop with Index

```html
<ol>
    {% for item in items %}
        <li>{{ loop.index }}. {{ item.name }}</li>
    {% endfor %}
</ol>
```

### Pattern 5: Alternating Row Colors

```html
<table>
    {% for user in users %}
    <tr class="{% if loop.index % 2 == 0 %}even{% else %}odd{% endif %}">
        <td>{{ user.name }}</td>
    </tr>
    {% endfor %}
</table>
```

---

## Quick Reference

| Syntax | Purpose | Example |
|--------|---------|---------|
| `{{ var }}` | Output variable | `{{ name }}` |
| `{% if %}` | Conditional | `{% if user %}{{ user.name }}{% endif %}` |
| `{% for %}` | Loop | `{% for item in items %}{% endfor %}` |
| `{% extends %}` | Inherit template | `{% extends "base.html" %}` |
| `{% block %}` | Define block | `{% block content %}{% endblock %}` |
| `{% include %}` | Include template | `{% include 'header.html' %}` |
| `{{ \|filter }}` | Apply filter | `{{ name\|upper }}` |
| `{# #}` | Comment | `{# This is a comment #}` |

---

## Tips and Best Practices

1. **Always escape user input** - Jinja2 auto-escapes by default, but be careful with `|safe` filter
2. **Use template inheritance** - Create a base template for consistent layout
3. **Keep logic minimal** - Complex logic should be in Flask, not templates
4. **Use includes** - Reuse common components (headers, footers, forms)
5. **Test with empty data** - Always handle empty lists/None values
6. **Use meaningful block names** - Makes templates easier to maintain

---

## Next Steps

- Practice creating templates for your order management system
- Learn about custom Jinja2 filters in Flask
- Explore Jinja2 macros for reusable template functions
- Study Flask-WTF for form handling with templates

---

**Resources:**
- [Jinja2 Official Documentation](https://jinja.palletsprojects.com/)
- [Flask Template Documentation](https://flask.palletsprojects.com/en/latest/templating/)

