# Order Management System - Sequence Diagrams

## Sequence Diagram: Create Order

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as Order Service
    participant UserRepo as User Repository
    participant ProductRepo as Product Repository
    participant OrderRepo as Order Repository
    participant DB as Database

    Client->>API: POST /orders (order_data)
    API->>Service: create_order(order_data)
    
    Service->>UserRepo: get(user_id)
    UserRepo->>DB: SELECT FROM users WHERE id=?
    DB-->>UserRepo: user data
    UserRepo-->>Service: User object
    
    Service->>ProductRepo: get(product_id)
    ProductRepo->>DB: SELECT FROM products WHERE id=?
    DB-->>ProductRepo: product data
    ProductRepo-->>Service: Product object
    
    Service->>OrderRepo: create_with_items(order_data, items_data)
    OrderRepo->>DB: BEGIN TRANSACTION
    OrderRepo->>DB: INSERT INTO orders
    OrderRepo->>DB: INSERT INTO order_items
    OrderRepo->>DB: COMMIT
    DB-->>OrderRepo: order with items
    OrderRepo->>DB: SELECT order + items + user + products WHERE id=?
    DB-->>OrderRepo: Order with relationships
    OrderRepo-->>Service: Order (with items, user, products)
    Service->>Service: Transform to OrderResponse<br/>(with product_name, user_name, order_id)
    Service-->>API: OrderResponse
    API-->>Client: 201 Created (JSON with order_id,<br/>user_name, items with product_name and id)
```

## Sequence Diagram: List Orders with Filters

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as Order Service
    participant OrderRepo as Order Repository
    participant DB as Database

    Client->>API: GET /orders?status=paid&user_id=1&product_id=1
    API->>Service: get_orders(status, user_id, product_id, ...)
    
    Service->>OrderRepo: get_all_with_filters(status, user_id, product_id, ...)
    
    OrderRepo->>DB: SELECT orders WHERE status=? AND user_id=?<br/>JOIN order_items WHERE product_id=?<br/>WITH eager load (items.product, user)
    DB-->>OrderRepo: orders list with relationships
    
    OrderRepo->>DB: SELECT SUM(quantity * price_cents_at_purchase),<br/>SUM(quantity) FROM order_items<br/>JOIN orders WHERE ... AND product_id=?
    DB-->>OrderRepo: totals (amount, quantity)
    
    OrderRepo-->>Service: orders + totals
    Service->>Service: Transform orders to response<br/>(filter items by product_id if specified,<br/>add product_name, user_name, order_id)
    Service-->>API: OrderListResponse (with aggregations)
    API-->>Client: 200 OK (JSON with orders array,<br/>total_amount_cents, total_quantity,<br/>limit, offset)
```

## Sequence Diagram: Update Order Status

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as Order Service
    participant OrderRepo as Order Repository
    participant DB as Database

    Client->>API: PATCH /orders/1 {status: "paid"}
    API->>Service: update_order_status(order_id, order_update)
    
    Service->>OrderRepo: update_status(order_id, status)
    OrderRepo->>DB: UPDATE orders SET status=?, updated_at=? WHERE id=?
    DB-->>OrderRepo: updated order
    
    OrderRepo->>DB: SELECT order WHERE id=?
    DB-->>OrderRepo: order with updated_at
    OrderRepo-->>Service: Order (with updated_at)
    Service->>Service: Transform to OrderStatusUpdateResponse
    Service-->>API: OrderStatusUpdateResponse
    API-->>Client: 200 OK (JSON with order_id, user_id,<br/>status, created_at, updated_at)
```

## Sequence Diagram: Get Product by ID

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as Product Service
    participant ProductRepo as Product Repository
    participant DB as Database

    Client->>API: GET /products/1
    API->>Service: get_product(product_id)
    
    Service->>ProductRepo: get(product_id)
    ProductRepo->>DB: SELECT FROM products WHERE id=?
    DB-->>ProductRepo: product data
    ProductRepo-->>Service: Product object
    Service->>Service: Transform to ProductResponse
    Service-->>API: ProductResponse
    API-->>Client: 200 OK (JSON with id, name, price_cents)
```

## Sequence Diagram: Get User by ID

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as User Service
    participant UserRepo as User Repository
    participant DB as Database

    Client->>API: GET /users/1
    API->>Service: get_user(user_id)
    
    Service->>UserRepo: get(user_id)
    UserRepo->>DB: SELECT FROM users WHERE id=?
    DB-->>UserRepo: user data
    UserRepo-->>Service: User object
    Service->>Service: Transform to UserResponse
    Service-->>API: UserResponse
    API-->>Client: 200 OK (JSON with id, email, full_name, created_at)
```

## Sequence Diagram: Update Product

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as Product Service
    participant ProductRepo as Product Repository
    participant DB as Database

    Client->>API: PATCH /products/1 {name, price_cents}
    API->>Service: update_product(product_id, product_update)
    
    Service->>ProductRepo: get(product_id)
    ProductRepo->>DB: SELECT FROM products WHERE id=?
    DB-->>ProductRepo: product data
    ProductRepo-->>Service: Product object
    
    Service->>ProductRepo: update(product_id, update_data)
    ProductRepo->>DB: UPDATE products SET name=?, price_cents=? WHERE id=?
    DB-->>ProductRepo: updated product
    ProductRepo-->>Service: ProductResponse
    Service-->>API: ProductResponse
    API-->>Client: 200 OK (JSON)
```

## Sequence Diagram: Error Handling

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as Service Layer
    participant ExceptionHandler as Exception Handler

    Client->>API: POST /orders (invalid data)
    API->>Service: create_order(order_data)
    
    Service->>Service: Validate input
    
    alt Validation Error
        Service->>ExceptionHandler: raise ValidationError
        ExceptionHandler->>API: HTTPException(400)
        API-->>Client: 400 Bad Request<br/>{detail, code}
    else Resource Not Found
        Service->>ExceptionHandler: raise NotFoundError
        ExceptionHandler->>API: HTTPException(404)
        API-->>Client: 404 Not Found<br/>{detail, code}
    else Duplicate Resource
        Service->>ExceptionHandler: raise DuplicateError
        ExceptionHandler->>API: HTTPException(409)
        API-->>Client: 409 Conflict<br/>{detail, code}
    else Internal Error
        Service->>ExceptionHandler: raise Exception
        ExceptionHandler->>API: HTTPException(500)
        API-->>Client: 500 Internal Error<br/>{detail, code}
    end
```

## Sequence Diagram: User Update with Email Validation

```mermaid
sequenceDiagram
    participant Client
    participant API as API Endpoint
    participant Service as User Service
    participant UserRepo as User Repository
    participant DB as Database

    Client->>API: PATCH /users/1 {email, full_name}
    API->>Service: update_user(user_id, user_update)
    
    Service->>UserRepo: get(user_id)
    UserRepo->>DB: SELECT FROM users WHERE id=?
    DB-->>UserRepo: user data
    
    alt User Not Found
        UserRepo-->>Service: None
        Service-->>API: UserNotFoundError
        API-->>Client: 404 Not Found
    else User Found
        Service->>Service: Validate email format
        
        alt Invalid Email
            Service-->>API: ValidationError
            API-->>Client: 400 Bad Request
        else Valid Email
            Service->>UserRepo: email_exists(email, exclude_id)
            UserRepo->>DB: SELECT FROM users WHERE email=? AND id!=?
            DB-->>UserRepo: existing user (if any)
            
            alt Email Already Exists
                UserRepo-->>Service: True
                Service-->>API: DuplicateEmailError
                API-->>Client: 409 Conflict
            else Email Available
                Service->>UserRepo: update(user_id, update_data)
                UserRepo->>DB: UPDATE users SET email=?, full_name=? WHERE id=?
                DB-->>UserRepo: updated user
                UserRepo-->>Service: UserResponse
                Service-->>API: UserResponse
                API-->>Client: 200 OK (JSON)
            end
        end
    end
```

## Sequence Diagram: Complete Order Flow with Aggregation

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service as Order Service
    participant OrderRepo as Order Repository
    participant ProductRepo as Product Repository
    participant DB

    Note over Client,DB: Complete flow for listing orders with aggregations

    Client->>API: GET /orders?status=paid&start_date=2024-01-01&product_id=1
    
    API->>Service: get_orders(status, start_date, product_id, ...)
    
    Service->>OrderRepo: get_all_with_filters(...)
    
    rect rgb(30, 58, 100)
        Note over OrderRepo,DB: Step 1: Fetch filtered orders with relationships
        OrderRepo->>DB: SELECT orders.* FROM orders<br/>JOIN order_items ON ...<br/>WHERE status=? AND created_at>=? AND product_id=?<br/>WITH eager load (items.product, user)<br/>LIMIT ? OFFSET ?
        DB-->>OrderRepo: List of orders with items and relationships
    end
    
    rect rgb(30, 100, 58)
        Note over OrderRepo,DB: Step 2: Calculate aggregations<br/>(across ALL filtered results matching product_id)
        OrderRepo->>DB: SELECT<br/>SUM(quantity * price_cents_at_purchase) as total_amount,<br/>SUM(quantity) as total_qty<br/>FROM order_items<br/>JOIN orders ON ...<br/>WHERE status=? AND created_at>=? AND product_id=?
        DB-->>OrderRepo: Aggregation results
    end
    
    OrderRepo-->>Service: (orders, total_count, total_amount, total_quantity)
    
    Service->>Service: Transform to response format<br/>(filter items by product_id,<br/>add product_name, user_name,<br/>convert id to order_id)
    
    Service-->>API: OrderListResponse<br/>{orders, limit, offset, total_amount_cents, total_quantity}
    API-->>Client: 200 OK (JSON with orders array,<br/>each order includes user_name<br/>and items with product_name and id)
```
