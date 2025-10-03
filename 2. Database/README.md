## Database Fundamentals

This guide gives beginners a practical introduction to databases. You will learn how different database types compare, write core SQL in PostgreSQL, understand ORM concepts with migration workflows, and complete hands-on homework to practice skills used at work.

### Learning Outcomes
- Understand relational vs NoSQL databases and when to choose each
- Write essential SQL queries in PostgreSQL for real use cases
- Use an ORM for basic CRUD and schema migrations
- Apply indexing, transactions, joins, and query analysis

---

## 1) Database Types

### What is a Relational Database (RDBMS)?
- Structured data organized into tables (rows and columns)
- Strong schema with data types and constraints
- ACID transactions: Atomicity, Consistency, Isolation, Durability
- SQL for querying and manipulating data
- Supports joins across tables to model relationships

#### Structure: Fixed schema with tables, rows, and columns

```mermaid
graph TD
    subgraph "Database: shop"
        subgraph "Table: users"
            U1["Row 1<br/>id: 1<br/>email: alice@example.com<br/>full_name: Alice Smith<br/>created_at: 2024-01-15"]
            U2["Row 2<br/>id: 2<br/>email: bob@example.com<br/>full_name: Bob Lee<br/>created_at: 2024-01-16"]
            U3["Row 3<br/>id: 3<br/>email: charlie@example.com<br/>full_name: Charlie Brown<br/>created_at: 2024-01-17"]
        end
        
        subgraph "Table: orders"
            O1["Row 1<br/>id: 101<br/>user_id: 1<br/>status: paid<br/>amount: $50<br/>created_at: 2024-01-20"]
            O2["Row 2<br/>id: 102<br/>user_id: 1<br/>status: shipped<br/>amount: $75<br/>created_at: 2024-01-21"]
            O3["Row 3<br/>id: 103<br/>user_id: 2<br/>status: paid<br/>amount: $25<br/>created_at: 2024-01-22"]
        end
        
        subgraph "Table: products"
            P1["Row 1<br/>id: 201<br/>name: Notebook<br/>price: $5<br/>category: Stationery"]
            P2["Row 2<br/>id: 202<br/>name: Pen<br/>price: $2<br/>category: Stationery"]
        end
    end
    
    U1 -.-> O1
    U1 -.-> O2
    U2 -.-> O3
    
    style U1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style U2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style U3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style O1 fill:#1a202c,stroke:#2d3748,color:#68d391
    style O2 fill:#1a202c,stroke:#2d3748,color:#68d391
    style O3 fill:#1a202c,stroke:#2d3748,color:#68d391
    style P1 fill:#1a202c,stroke:#2d3748,color:#fbb6ce
    style P2 fill:#1a202c,stroke:#2d3748,color:#fbb6ce
```

**Key Concepts:**
- **Schema**: Fixed structure (all users must have email, name, etc.)
- **Table**: Collection of similar records (users table, orders table)
- **Row**: Individual record (one user, one order)
- **Column**: Specific field (email, name, price)
- **Primary Key**: Unique identifier (id)
- **Foreign Key**: Link to another table (user_id in orders references users.id)


#### Popular Relational Databases

| Database | License | Strengths | Trade-offs | Typical Use |
|---|---|---|---|---|
| PostgreSQL | Open Source (PostgreSQL License) | Standards-compliant, rich features (CTEs, window functions, JSONB, extensions), strong consistency, great tooling | Slightly steeper learning curve vs MySQL, can require tuning for high write workloads | General-purpose apps, analytics, geospatial, event-driven systems |
| MySQL | Open Source (GPL) | Widely adopted, easy to start, strong read performance, large ecosystem | Historically weaker SQL features than Postgres (improved over time), transactional nuances across engines | Web apps, CMS, e-commerce |
| SQLite | Public Domain | Zero-configuration, embedded, single file, excellent for testing/development | Single writer limitation, not suitable for high-concurrency web apps | Mobile apps, desktop apps, embedded systems, testing, prototyping |
| SQL Server | Commercial | Enterprise tooling, BI integration, Windows ecosystem | License costs, platform coupling | Enterprise apps, BI-heavy stacks |
| Oracle | Commercial | Extremely mature, advanced features, mission-critical workloads | Expensive, vendor lock-in | Large enterprises, financial/telecom |

#### RDBMS Pros and Cons
- Pros: strong consistency, powerful joins, mature tooling, robust transactions
- Cons: rigid schema changes can require migrations; horizontal scaling can be non-trivial

--------

### What is NoSQL?
“NoSQL” refers to non-relational databases optimized for specific access patterns. They often trade some relational features for scalability, flexibility, or speed.

```mermaid
flowchart LR
  A[NoSQL] --> B[Document]
  A --> C[Key-Value]
  A --> D[Wide-Column]
  A --> E[Graph]
  A --> F[Search]
```

| Type | Examples | Strengths | Trade-offs | Typical Use |
|---|---|---|---|---|
| Document | MongoDB, Couchbase | Flexible schema, nested JSON, easy iteration | Weaker joins, cross-document transactions limited (improving) | Content, catalogs, event logs |
| Key-Value | Redis, DynamoDB, Memcached | Simple and fast, in-memory options, low latency | Limited query patterns | Caching, sessions, rate limiting |
| Wide-Column | Cassandra, HBase | Massive write throughput, horizontal scalability | Modeling complexity, eventual consistency | Time-series, logs, IoT |
| Graph | Neo4j, JanusGraph | Relationship-heavy queries, traversals | Specialized indexing and ops | Social networks, fraud, recommendations |
| Search | Elasticsearch, OpenSearch | Full-text search, relevance ranking | Not a system of record | Search, log analytics |





##### Document Database (MongoDB)

**Structure**: Flexible schema with collections and documents

```mermaid
graph TD
    subgraph "Database: shop"
        subgraph "Collection: users"
            D1["Document 1<br/>{ id: ObjectId(1)<br/>email: 'alice@example.com'<br/>name: 'Alice Smith'<br/>addresses: [<br/>  {city: 'NYC', country: 'US'},<br/>  {city: 'LA', country: 'US'}<br/>]<br/>createdAt: ISODate('2024-01-15') }"]
            D2["Document 2<br/>{ id: ObjectId(2)<br/>email: 'bob@example.com'<br/>name: 'Bob Lee'<br/>profile: {<br/>  age: 25,<br/>  preferences: ['blue', 'coffee']<br/>}<br/>lastLogin: ISODate('2024-01-16') }"]
            D3["Document 3<br/>{ id: ObjectId(3)<br/>email: 'charlie@example.com'<br/>name: 'Charlie Brown'<br/>orders: [<br/>  {productId: ObjectId(201), qty: 2},<br/>  {productId: ObjectId(202), qty: 1}<br/>]<br/>isActive: true }"]
        end
        
        subgraph "Collection: products"
            P1["Document 1<br/>{ id: ObjectId(201)<br/>name: 'Notebook'<br/>price: 5.00<br/>tags: ['paper', 'writing']<br/>inStock: true }"]
            P2["Document 2<br/>{ id: ObjectId(202)<br/>name: 'Pen'<br/>price: 2.00<br/>colors: ['red', 'blue', 'black']<br/>inStock: false }"]
        end
    end
    
    style D1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style D2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style D3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style P1 fill:#1a202c,stroke:#2d3748,color:#68d391
    style P2 fill:#1a202c,stroke:#2d3748,color:#fbb6ce
```

**Key Concepts:**
- **Schema**: Flexible (documents can have different fields)
- **Collection**: Group of documents (like a table)
- **Document**: Individual record (like a row, but can be nested)
- **Field**: Key-value pair (like a cell, but can contain objects/arrays)
- **ObjectId**: Unique identifier (like primary key)
- **Embedded Document**: Nested object (addresses, profile)
- **Array**: List of values or objects (preferences, orders)

### Comparison Table

| Aspect | Relational | MongoDB |
|--------|------------|---------|
| **Structure** | Tables with fixed columns | Collections with flexible documents |
| **Schema** | Must be defined upfront | Can evolve over time |
| **Relationships** | Foreign keys + JOIN | Embedded documents or references |
| **Data Types** | Strict column types | Flexible field types |
| **Query Language** | SQL | MongoDB Query Language (MQL) |
| **Transactions** | Strong ACID | Single-document ACID |
| **Scaling** | Vertical (harder horizontal) | Horizontal sharding |

#### When to choose what?
- Choose RDBMS when you need strong consistency, complex joins, and transactions.
- Choose NoSQL when you need flexible schemas, extreme scale, or specialized query patterns.
- Many production systems combine both: Postgres for core data, Redis for caching, Elasticsearch for search.

---

## 2) SQL with PostgreSQL

### PostgreSQL: brief history and why popular now
- Originated at UC Berkeley (POSTGRES project), first release in 1980s; evolved into PostgreSQL (SQL support) in the mid-1990s
- Open-source, community-driven; highly standards-compliant
- Extensible: custom types, functions, indexes, procedural languages, extensions (e.g., PostGIS)
- Modern features: CTEs, window functions, JSON/JSONB, full-text search, logical replication
- Broad managed service support (AWS RDS/Aurora, GCP, Azure), vibrant tooling, robust performance

### Sample schema for examples
```sql
-- Tables
CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  full_name TEXT NOT NULL,
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE products (
  id BIGSERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  price_cents INTEGER NOT NULL CHECK (price_cents >= 0)
);

CREATE TABLE orders (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id),
  status TEXT NOT NULL CHECK (status IN ('pending','paid','shipped','cancelled')),
  created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE order_items (
  id BIGSERIAL PRIMARY KEY,
  order_id BIGINT NOT NULL REFERENCES orders(id),
  product_id BIGINT NOT NULL REFERENCES products(id),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  price_cents_at_purchase INTEGER NOT NULL
);

-- Helpful indexes
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
```

### Core SQL queries

#### SELECT, INSERT, UPDATE, DELETE
```sql
SELECT * FROM users LIMIT 10;

INSERT INTO users (email, full_name) VALUES ('jane@example.com', 'Jane Doe');

UPDATE orders SET status = 'shipped' WHERE id = 123 AND status = 'paid';

DELETE FROM order_items WHERE id = 999;
```

#### UPSERT (INSERT ... ON CONFLICT)
```sql
INSERT INTO products (id, name, price_cents)
VALUES (1, 'Notebook', 599)
ON CONFLICT (id)
DO UPDATE SET name = EXCLUDED.name, price_cents = EXCLUDED.price_cents;
```

#### Transactions
```sql
BEGIN;
  UPDATE products SET price_cents = price_cents - 100 WHERE id = 1;
  UPDATE products SET price_cents = price_cents + 100 WHERE id = 2;
COMMIT;
-- ROLLBACK; -- to abort
```

#### SELECT, WHERE, ORDER BY, LIMIT/OFFSET
```sql
-- Get newest paid orders for a user
SELECT id, status, created_at
FROM orders
WHERE user_id = 42 AND status = 'paid'
ORDER BY created_at DESC
LIMIT 10 OFFSET 0;
```

#### COUNT, GROUP BY, HAVING
```sql
-- Count paid orders per user, only users with 5+ paid orders
SELECT user_id, COUNT(*) AS paid_orders
FROM orders
WHERE status = 'paid'
GROUP BY user_id
HAVING COUNT(*) >= 5
ORDER BY paid_orders DESC;
```

#### INNER JOIN, LEFT JOIN, RIGHT JOIN, FULL JOIN

##### Visual Join Diagrams

**INNER JOIN** - Returns only matching records from both tables
```mermaid
graph TD
    subgraph "Table A (Users)"
        A1["id: 1<br/>name: Alice"]
        A2["id: 2<br/>name: Bob"]
        A3["id: 3<br/>name: Charlie"]
    end
    
    subgraph "Table B (Orders)"
        B1["id: 101<br/>user_id: 1<br/>amount: $50"]
        B2["id: 102<br/>user_id: 2<br/>amount: $75"]
        B3["id: 103<br/>user_id: 4<br/>amount: $100"]
    end
    
    subgraph "INNER JOIN Result"
        R1["Alice | $50"]
        R2["Bob | $75"]
    end
    
    A1 --> R1
    A2 --> R2
    B1 --> R1
    B2 --> R2
    
    style A1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style R1 fill:#1a202c,stroke:#2d3748,color:#68d391
    style R2 fill:#1a202c,stroke:#2d3748,color:#68d391
```

**LEFT JOIN** - Returns all records from left table (A) and matching records from right table (B)
```mermaid
graph TD
    subgraph "Table A (Users)"
        A1["id: 1<br/>name: Alice"]
        A2["id: 2<br/>name: Bob"]
        A3["id: 3<br/>name: Charlie"]
    end
    
    subgraph "Table B (Orders)"
        B1["id: 101<br/>user_id: 1<br/>amount: $50"]
        B2["id: 102<br/>user_id: 2<br/>amount: $75"]
        B3["id: 103<br/>user_id: 4<br/>amount: $100"]
    end
    
    subgraph "LEFT JOIN Result"
        R1["Alice | $50"]
        R2["Bob | $75"]
        R3["Charlie | NULL"]
    end
    
    A1 --> R1
    A2 --> R2
    A3 --> R3
    B1 --> R1
    B2 --> R2
    
    style A1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style R1 fill:#1a202c,stroke:#2d3748,color:#68d391
    style R2 fill:#1a202c,stroke:#2d3748,color:#68d391
    style R3 fill:#1a202c,stroke:#2d3748,color:#f56565
```

**RIGHT JOIN** - Returns all records from right table (B) and matching records from left table (A)
```mermaid
graph TD
    subgraph "Table A (Users)"
        A1["id: 1<br/>name: Alice"]
        A2["id: 2<br/>name: Bob"]
        A3["id: 3<br/>name: Charlie"]
    end
    
    subgraph "Table B (Orders)"
        B1["id: 101<br/>user_id: 1<br/>amount: $50"]
        B2["id: 102<br/>user_id: 2<br/>amount: $75"]
        B3["id: 103<br/>user_id: 4<br/>amount: $100"]
    end
    
    subgraph "RIGHT JOIN Result"
        R1["Alice | $50"]
        R2["Bob | $75"]
        R3["NULL | $100"]
    end
    
    A1 --> R1
    A2 --> R2
    B1 --> R1
    B2 --> R2
    B3 --> R3
    
    style A1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style R1 fill:#1a202c,stroke:#2d3748,color:#68d391
    style R2 fill:#1a202c,stroke:#2d3748,color:#68d391
    style R3 fill:#1a202c,stroke:#2d3748,color:#f56565
```

**FULL OUTER JOIN** - Returns all records from both tables, with NULLs for non-matching records
```mermaid
graph TD
    subgraph "Table A (Users)"
        A1["id: 1<br/>name: Alice"]
        A2["id: 2<br/>name: Bob"]
        A3["id: 3<br/>name: Charlie"]
    end
    
    subgraph "Table B (Orders)"
        B1["id: 101<br/>user_id: 1<br/>amount: $50"]
        B2["id: 102<br/>user_id: 2<br/>amount: $75"]
        B3["id: 103<br/>user_id: 4<br/>amount: $100"]
    end
    
    subgraph "FULL OUTER JOIN Result"
        R1["Alice | $50"]
        R2["Bob | $75"]
        R3["Charlie | NULL"]
        R4["NULL | $100"]
    end
    
    A1 --> R1
    A2 --> R2
    A3 --> R3
    B1 --> R1
    B2 --> R2
    B3 --> R4
    
    style A1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style A3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B1 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B2 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style B3 fill:#2d3748,stroke:#4a5568,color:#e2e8f0
    style R1 fill:#1a202c,stroke:#2d3748,color:#68d391
    style R2 fill:#1a202c,stroke:#2d3748,color:#68d391
    style R3 fill:#1a202c,stroke:#2d3748,color:#f56565
    style R4 fill:#1a202c,stroke:#2d3748,color:#f56565
```

##### Join Type Summary

| Join Type | Description | When to Use | Result Size |
|-----------|-------------|-------------|-------------|
| **INNER JOIN** | Only matching records from both tables | When you need complete data pairs | Smallest |
| **LEFT JOIN** | All records from left table + matching from right | When you want all left records, even without matches | Medium |
| **RIGHT JOIN** | All records from right table + matching from left | When you want all right records, even without matches | Medium |
| **FULL OUTER JOIN** | All records from both tables | When you need complete picture from both sides | Largest |


#### Practical SQL Examples


```sql
-- Create a covering index for frequent filter and sort
CREATE INDEX idx_orders_user_status_created_at
  ON orders(user_id, status, created_at DESC);

-- Analyze a query
EXPLAIN ANALYZE
SELECT * FROM orders
WHERE user_id = 42 AND status = 'paid'
ORDER BY created_at DESC
LIMIT 20;
```

```sql
-- Total quantity and spend per product across paid orders
SELECT p.id, p.name,
       SUM(oi.quantity) AS total_qty,
       SUM(oi.quantity * oi.price_cents_at_purchase) AS total_spend_cents
FROM order_items oi
INNER JOIN orders o ON o.id = oi.order_id AND o.status = 'paid'
INNER JOIN products p ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY total_spend_cents DESC;

-- Users and their latest order (users without orders still appear)
SELECT u.id, u.email, o.id AS last_order_id, o.created_at AS last_order_at
FROM users u
LEFT JOIN LATERAL (
  SELECT id, created_at FROM orders
  WHERE user_id = u.id
  ORDER BY created_at DESC
  LIMIT 1
) o ON TRUE;

-- Right join example: products that appeared in any order (or not)
SELECT p.id, p.name, oi.order_id
FROM order_items oi
RIGHT JOIN products p ON p.id = oi.product_id;

-- Full outer join example: union of users and order owners
SELECT u.id AS user_id, o.user_id AS order_user_id
FROM users u
FULL OUTER JOIN (
  SELECT DISTINCT user_id FROM orders
) o ON o.user_id = u.id;
```

#### Subqueries and CTEs (WITH)
```sql
-- Latest order per user using CTE
WITH ranked_orders AS (
  SELECT id, user_id, created_at,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
  FROM orders
)
SELECT *
FROM ranked_orders
WHERE rn = 1;
```

#### Window functions
```sql
-- Running total of spend across time for each user
SELECT o.user_id,
       o.created_at,
       SUM(oi.quantity * oi.price_cents_at_purchase)
         OVER (PARTITION BY o.user_id ORDER BY o.created_at
               ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_spend_cents
FROM orders o
JOIN order_items oi ON oi.order_id = o.id
WHERE o.status = 'paid';
```

---

## 2.5) MongoDB by Example (Document Database)

### When to use MongoDB
- Flexible JSON-like documents, schema evolves easily
- Great for content, catalogs, event logs, user settings, embedded/nested data

### Example database and collections
- Database: `shop`
- Collections: `users`, `products`, `orders`

### Sample documents

```json
// users
{
  "_id": { "$oid": "665a1c2f9f1a2b3c4d5e6f01" },
  "email": "jane@example.com",
  "fullName": "Jane Doe",
  "addresses": [
    { "label": "home", "city": "San Francisco", "country": "US" },
    { "label": "office", "city": "San Jose", "country": "US" }
  ],
  "createdAt": { "$date": "2024-05-20T12:00:00Z" }
}
```

```json
// products
{
  "_id": { "$oid": "665a1c2f9f1a2b3c4d5e7001" },
  "name": "Notebook",
  "priceCents": 599,
  "tags": ["stationery", "paper"],
  "inStock": true
}
```

```json
// orders (embed items in the order document)
{
  "_id": { "$oid": "665a1c2f9f1a2b3c4d5e8001" },
  "userId": { "$oid": "665a1c2f9f1a2b3c4d5e6f01" },
  "status": "paid",
  "createdAt": { "$date": "2024-06-01T09:30:00Z" },
  "items": [
    { "productId": { "$oid": "665a1c2f9f1a2b3c4d5e7001" }, "quantity": 2, "priceCentsAtPurchase": 599 },
    { "productId": { "$oid": "665a1c2f9f1a2b3c4d5e7002" }, "quantity": 1, "priceCentsAtPurchase": 1299 }
  ]
}
```

### Native MongoDB Query Language (MQL) vs Atlas SQL

#### Native MongoDB Query Language (MQL)
MQL is MongoDB's native query language, designed specifically for document databases:

**MQL Examples:**
```javascript
// Simple find with filters
db.users.find({ email: "jane@example.com" })

// Complex aggregation pipeline
db.orders.aggregate([
  { $match: { status: "paid" } },
  { $unwind: "$items" },
  { $group: {
    _id: "$items.productId",
    totalQty: { $sum: "$items.quantity" },
    revenue: { $sum: { $multiply: ["$items.quantity", "$items.priceCentsAtPurchase"] } }
  }},
  { $sort: { revenue: -1 } },
  { $limit: 10 }
])

// Array operations
db.users.find({ "addresses.city": "San Francisco" })

// Update with nested fields
db.users.updateOne(
  { email: "jane@example.com" },
  { $set: { "profile.age": 25 } }
)
```

#### Why Atlas SQL Was Introduced

**Problem**: MQL has a steep learning curve for developers familiar with SQL

| Aspect | **MQL (Native)** | **Atlas SQL** |
|--------|------------------|---------------|
| **Learning Curve** | ⚠️ Steep - specialized syntax | ✅ Gentle - familiar SQL |
| **Developer Adoption** | ❌ Requires MongoDB training | ✅ Leverages existing SQL skills |
| **Business Intelligence** | ❌ Limited BI tool integration | ✅ Direct BI tool compatibility |
| **Analytics** | ❌ Complex aggregation syntax | ✅ Standard SQL aggregations |
| **Cross-Database** | ❌ MongoDB-specific | ✅ SQL knowledge transfers |
| **Performance** | ✅ Optimized for MongoDB | ⚠️ Translation overhead |
| **Features** | ✅ Full MongoDB capabilities | ⚠️ SQL subset only |

**Atlas SQL Benefits:**
- ✅ **Faster adoption** for SQL developers
- ✅ **BI tool integration** (Tableau, Power BI, Looker)
- ✅ **Analytics accessibility** for business users
- ✅ **Reduced training costs** for teams
- ✅ **Migration bridge** from relational databases

**MQL Still Advantageous For:**
- ✅ **Complex document operations** (array manipulations, embedded updates)
- ✅ **Maximum performance** (no translation layer)
- ✅ **Advanced MongoDB features** (geospatial, text search, aggregation stages)
- ✅ **CRUD operations** (INSERT/UPDATE/DELETE via drivers)

**Bottom Line**: Atlas SQL serves as a **"familiar gateway"** to MongoDB for SQL developers, while MQL remains the **power user option** for MongoDB-specific features.

### MongoDB SQL: Basic queries

```sql
-- Simple key equality (users by email)
SELECT _id, email, fullName
FROM shop.users
WHERE email = 'jane@example.com';

-- Nested field equality (object inside document)
SELECT _id, email
FROM shop.users AS u
WHERE u.profile.locale = 'en-US';

-- Array contains value (tags contains 'vip')
SELECT u._id, u.email
FROM shop.users AS u
WHERE EXISTS (
  SELECT 1 FROM UNNEST(u.tags) AS tag WHERE tag = 'vip'
);

-- Wildcard search (LIKE with %)
SELECT _id, email
FROM shop.users
WHERE email LIKE '%@example.com';

-- Regex search (case-insensitive)
SELECT _id, email
FROM shop.users
WHERE REGEXP_LIKE(email, '^j.*@example\\.com$', 'i');

-- Range filter (dates)
SELECT _id, userId, createdAt
FROM shop.orders
WHERE createdAt BETWEEN DATE('2024-06-01') AND DATE('2024-06-30');

-- IN list
SELECT _id, name, priceCents
FROM shop.products
WHERE name IN ('Notebook', 'Pencil', 'Eraser');

-- Missing or NULL field
SELECT _id, email, nickname
FROM shop.users
WHERE nickname IS NULL; -- missing or explicitly null

-- Projection and sort
SELECT _id, email, createdAt
FROM shop.users
ORDER BY createdAt DESC
LIMIT 20;

-- Pagination (offset-based)
SELECT _id, email
FROM shop.users
ORDER BY _id
LIMIT 20 OFFSET 40; -- page 3 when pageSize=20
```

### Read queries with MongoDB SQL (Atlas SQL)

Note: Atlas SQL focuses on read (SELECT) queries. Use drivers/Compass for inserts/updates/deletes.

```sql
-- 1) All paid orders in the last 30 days
SELECT o._id        AS order_id,
       o.userId     AS user_id,
       o.createdAt  AS created_at
FROM shop.orders AS o
WHERE o.status = 'paid'
  AND o.createdAt >= DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
ORDER BY o.createdAt DESC;

-- 2) Orders containing a specific productId
SELECT DISTINCT o._id AS order_id
FROM shop.orders AS o
CROSS JOIN UNNEST(o.items) AS item
WHERE item.productId = OBJECTID('665a1c2f9f1a2b3c4d5e7001');

-- 3) Users in a given city (array of embedded addresses)
SELECT DISTINCT u._id, u.email
FROM shop.users AS u
CROSS JOIN UNNEST(u.addresses) AS addr
WHERE addr.city = 'San Francisco';
```

### Aggregations with MongoDB SQL

```sql
-- Total revenue per product over paid orders (top 10)
SELECT item.productId                                AS product_id,
       SUM(item.quantity)                            AS total_qty,
       SUM(item.quantity * item.priceCentsAtPurchase) AS total_revenue_cents
FROM shop.orders AS o
CROSS JOIN UNNEST(o.items) AS item
WHERE o.status = 'paid'
GROUP BY item.productId
ORDER BY total_revenue_cents DESC
LIMIT 10;

-- Latest order per user using a window function
SELECT user_id, order_id, created_at
FROM (
  SELECT o.userId  AS user_id,
         o._id     AS order_id,
         o.createdAt AS created_at,
         ROW_NUMBER() OVER (
           PARTITION BY o.userId
           ORDER BY o.createdAt DESC
         ) AS rn
  FROM shop.orders AS o
) t
WHERE rn = 1;
```

### Join-like lookup with MongoDB SQL

```sql
-- Enrich paid orders with user email
SELECT o._id AS order_id,
       u.email,
       o.createdAt AS created_at,
       o.status
FROM shop.orders AS o
JOIN shop.users  AS u
  ON u._id = o.userId
WHERE o.status = 'paid';
```

### Indexing for performance

```javascript
// Index orders by user and time
db.orders.createIndex({ userId: 1, createdAt: -1 })

// Index for frequent status filter
db.orders.createIndex({ status: 1 })

// Multikey index on array field
db.users.createIndex({ "addresses.city": 1 })
```

### Notes on modeling
- Prefer embedding when the child data is loaded with the parent (e.g., order items)
- Prefer referencing when data is shared across many parents (e.g., product referenced by many orders)
- MongoDB supports multi-document transactions, but embedding often avoids needing them


## 3) ORM (Object-Relational Mapping)

### What is an ORM?
An ORM maps database tables to programming language classes/objects and SQL operations to method calls. It provides an abstraction to write database code in your primary language while generating SQL under the hood.

#### Pros
- Developer productivity and readability
- Safer parameterization (prevents SQL injection)
- Schema migration tooling integrated with code
- Portability across supported databases

#### Cons
- Performance overhead vs hand-tuned SQL for complex queries
- Leaky abstractions for advanced SQL constructs
- Risk of N+1 queries without careful usage

### Basic usage examples

#### Python (SQLAlchemy)
```python
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)

engine = create_engine('postgresql+psycopg2://user:pass@localhost:5432/app')
SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

with SessionLocal() as session:
    jane = User(email='jane@example.com', full_name='Jane Doe')
    session.add(jane)
    session.commit()

    users = session.query(User).filter(User.email.like('%@example.com')).all()
```

#### Node.js (Prisma)
```bash
npx prisma init --datasource-provider postgresql
```

```prisma
// schema.prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int     @id @default(autoincrement())
  email     String  @unique
  fullName  String
  createdAt DateTime @default(now())
}
```

```bash
npx prisma migrate dev --name init
```

```typescript
import { PrismaClient } from '@prisma/client'
const prisma = new PrismaClient()

async function main() {
  await prisma.user.create({ data: { email: 'jane@example.com', fullName: 'Jane Doe' } })
  const users = await prisma.user.findMany({ where: { email: { endsWith: '@example.com' } } })
  console.log(users)
}

main().finally(() => prisma.$disconnect())
```

### Database Migrations: Simple Examples

#### What are Migrations?
**Migrations** are scripts that change your database schema step-by-step. Think of them as **version control for your database structure**.

#### Python: SQLAlchemy + Alembic

**Step 1: Initialize migration system**
```bash
# Install Alembic
pip install alembic

# Create migration folder
alembic init alembic
```

**Step 2: Configure connection**
```python
# alembic/env.py (edit this file)
from sqlalchemy import create_engine
from myapp.models import Base  # Your SQLAlchemy models

engine = create_engine('postgresql://user:pass@localhost/mydb')
Base.metadata.bind = engine
```

**Step 3: Create migrations**
```bash
# Auto-generate migration from model changes
alembic revision --autogenerate -m "add users table"

# Apply migration to database
alembic upgrade head
```

**Generated migration file** (`alembic/versions/001_add_users_table.py`):
```python
"""add users table

Revision ID: 001
Revises: 
Create Date: 2024-01-20 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    # Auto-generated from your model
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('users')
```

**Step 4: Add new column to existing table**
```python
# 1. Update your model (myapp/models.py)
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False)
    phone = Column(String(20))  # NEW COLUMN!
```

```bash
# 2. Generate migration
alembic revision --autogenerate -m "add phone column to users"

# 3. Apply migration
alembic upgrade head
```

#### Node.js: Prisma

**Step 1: Define schema**
```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
}
```

**Step 2: Create initial migration**
```bash
npx prisma migrate dev --name init
```

**Step 3: Add new field**
```prisma
// Edit schema.prisma
model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  createdAt DateTime @default(now())
  phone     String?  // NEW FIELD (optional)
}
```

**Step 4: Generate and apply migration**
```bash
npx prisma migrate dev --name	add_phone_field
```

**Generated SQL file** (`prisma/migrations/20240120_add_phone_field/migration.sql`):
```sql
-- AlterTable
ALTER TABLE "User" ADD COLUMN "phone" TEXT;
```

#### Java: Flyway (already covered in ORM section)

Simple Flyway migration files:
```sql
-- V1__Create_users_table.sql
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- V2__Add_phone_column.sql  
ALTER TABLE users ADD COLUMN phone VARCHAR(20);
```

---

#### Migration Best Practices

✅ **Do's:**
- Test migrations on development first
- Use descriptive migration file name
- Review auto-generated SQL before applying
- Backup production data before major changes
- Keep migrations small and atomic

❌ **Don'ts:**
- Never edit old migration files in production
- Don't skip migration steps
- Avoid dropping columns without careful review
- Don't run migrations manually on production

---

## 4) Homework: Weather App Enhancement

### 🎯 Goal: Log User Search Activity in Weather Application

Enhance your existing weather application to **log all user search activity** to a database using an ORM. Focus on building a complete database-backed system with proper relationships and error handling.

### 📋 Core Requirements

#### **1. Database Schema Design**
Design **two related tables** that capture:
- **City information**: Name, country, coordinates (latitude/longitude)
- **Weather search activity**: When searches happened, what weather data was found
- **Proper relationship**: Use foreign keys to link weather results to cities

#### **2. ORM Implementation**
Choose **one technology stack**:
- **Python**: SQLAlchemy
- **Node.js**: Prisma
- **Other**: Any ORM you're comfortable with

**Think about**:
- How to map your database tables to ORM models
- What relationships exist between your models

#### **3. Error Handling Scenarios**
Implement robust handling for:
- **City not found**: What happens when a user searches for a non-existent city?
- **Repeat searches**: Should users get cached results or fresh API calls?
- **Database errors**: How to handle connection issues or constraint violations
- **API failures**: What if the weather service is down?

**Consider**: How do you want to communicate these errors to users?

#### **4. Application Integration**
Modify your existing weather app to:
- **Connect to database** before showing weather results
- **Log every search** with timestamp and user information
- **Display activity history** in terminal or UI
- **Handle edge cases** gracefully


### 🏆 Deliverables

1. **Database Schema**: SQL files showing your table design
2. **ORM Models**: Your chosen ORM's model definitions
3. **Enhanced Weather App**: Code that integrates database logging
4. **Activity Dashboard**: UI that displays search history and statistics
5. **User Guide**: How to run your application, screenshots are welcome in the guide.
6. **Documentation**: Brief explanation of your design decisions and any challenges faced

### 🌟 Bonus Challenges

#### **Advanced Features**
- **Display Activity History** in a UI menu
- **Most popular cities** being searched

**Think about**:
- What information is useful to display?

### 📊 Success Criteria

Your solution should demonstrate:
- **Understanding of database relationships** (foreign keys, joins)
- **ORM proficiency** (models, migrations, queries)
- **Error handling patterns** (graceful failures, fallback)
- **Frontend-backend integration** (🌟Bonus)
- **Practical problem-solving** (working with real APIs and databases)

---

### References
- PostgreSQL Docs: `https://www.postgresql.org/docs/`
- Use The Index, Luke!: `https://use-the-index-luke.com/`
- Prisma Docs: `https://www.prisma.io/docs`
- SQLAlchemy Docs: `https://docs.sqlalchemy.org/`



