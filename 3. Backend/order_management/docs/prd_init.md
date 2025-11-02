
1. project goal
Create a order management system to provide searching, creating, updating functionality.

2. detailed requirements:
provide a set of backend APIs to provide the following functions:
- able to list all the orders
- able to list all the orders based on status, e.g. paid, shipped, cancelled
- able to list the orders based on certain user
- able to list the orders based on date
- able to list the orders based on product or product id
- able to add a new order (please consider what are the required fields)
- able to add a product
- able to update an order status
- able to update user info, e.g. email or full name
- able to update product name, price

3. additional requirements:
- when the result contains quantity of the order, please also return total quantity of the result
- when the result contains amount of the order, please also return total amount of the result
- please generate postman collection as well for all the APIs
- please use python as programming language
- use ORM to define the database entity and CRUD operation
- define env or file for database config
- follow industry coding standard and considering security best practice. 
- include folder structure in the md file following best practice
- easy to extend the feature and clear code structure. 
- include unit test.
- generate swagger api doc and make sure the all endpoints are working

4. database infomation and relationship:

- host: ep-jolly-feather-adyuujqy-pooler.c-2.us-east-1.aws.neon.tech
- port: 5432
- database: neondb
- username: <username>
- password: <password>


```sql
CREATE SCHEMA tony;

CREATE TABLE tony.users (
	id bigserial NOT NULL,
	email text NOT NULL,
	full_name text NOT NULL,
	created_at timestamptz DEFAULT now() NULL,
	CONSTRAINT users_email_key UNIQUE (email),
	CONSTRAINT users_pkey PRIMARY KEY (id)
);

CREATE TABLE tony.orders (
	id bigserial NOT NULL,
	user_id int8 NOT NULL,
	status text NOT NULL,
	created_at timestamptz DEFAULT now() NULL,
	CONSTRAINT orders_pkey PRIMARY KEY (id),
	CONSTRAINT orders_status_check CHECK ((status = ANY (ARRAY['pending'::text, 'paid'::text, 'shipped'::text, 'cancelled'::text]))),
	CONSTRAINT orders_user_id_fkey FOREIGN KEY (user_id) REFERENCES tony.users(id)
);
CREATE INDEX idx_orders_user_id ON tony.orders USING btree (user_id);


CREATE TABLE tony.products (
	id bigserial NOT NULL,
	"name" text NOT NULL,
	price_cents int4 NOT NULL,
	CONSTRAINT products_pkey PRIMARY KEY (id),
	CONSTRAINT products_price_cents_check CHECK ((price_cents >= 0))
);

CREATE TABLE tony.order_items (
	id bigserial NOT NULL,
	order_id int8 NOT NULL,
	product_id int8 NOT NULL,
	quantity int4 NOT NULL,
	price_cents_at_purchase int4 NOT NULL,
	CONSTRAINT order_items_pkey PRIMARY KEY (id),
	CONSTRAINT order_items_quantity_check CHECK ((quantity > 0))
);
CREATE INDEX idx_order_items_order_id ON tony.order_items USING btree (order_id);

```