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


-- 示例数据插入脚本
-- 基于 learning/2. Database/README.md 中的表结构

-- 1. 插入用户数据
INSERT INTO users (email, full_name, created_at) VALUES
('john.doe@example.com', 'John Doe', '2024-01-15 10:30:00+00'),
('jane.smith@example.com', 'Jane Smith', '2024-01-20 14:15:00+00'),
('bob.wilson@example.com', 'Bob Wilson', '2024-02-01 09:45:00+00'),
('alice.brown@example.com', 'Alice Brown', '2024-02-10 16:20:00+00'),
('charlie.davis@example.com', 'Charlie Davis', '2024-02-15 11:10:00+00'),
('diana.miller@example.com', 'Diana Miller', '2024-03-01 13:30:00+00'),
('eve.jones@example.com', 'Eve Jones', '2024-03-05 08:45:00+00'),
('frank.garcia@example.com', 'Frank Garcia', '2024-03-10 15:20:00+00'),
('grace.lee@example.com', 'Grace Lee', '2024-03-15 12:00:00+00'),
('henry.taylor@example.com', 'Henry Taylor', '2024-03-20 17:30:00+00'),
('iris.moore@example.com', 'Iris Moore', '2024-04-01 10:15:00+00'),
('jack.white@example.com', 'Jack White', '2024-04-05 14:45:00+00'),
('kate.harris@example.com', 'Kate Harris', '2024-04-10 09:30:00+00'),
('leo.martin@example.com', 'Leo Martin', '2024-04-15 16:00:00+00'),
('mary.thompson@example.com', 'Mary Thompson', '2024-04-20 11:45:00+00');

-- 2. 插入产品数据
INSERT INTO products (name, price_cents) VALUES
('MacBook Pro 16"', 249999),
('iPhone 15 Pro', 99999),
('AirPods Pro', 24999),
('iPad Air', 59999),
('Apple Watch Series 9', 39999),
('Magic Keyboard', 9999),
('Magic Mouse', 7999),
('Studio Display', 159999),
('Mac Studio', 199999),
('AirTag 4-pack', 9999),
('Lightning Cable', 1999),
('USB-C Cable', 1999),
('Wireless Charger', 3999),
('Phone Case', 2999),
('Laptop Stand', 4999),
('External SSD 1TB', 19999),
('Bluetooth Speaker', 7999),
('Noise Cancelling Headphones', 29999),
('Gaming Mouse', 5999),
('Mechanical Keyboard', 12999);

-- 3. 插入订单数据
INSERT INTO orders (user_id, status, created_at) VALUES
(1, 'paid', '2024-01-16 10:30:00+00'),
(1, 'shipped', '2024-02-01 14:20:00+00'),
(1, 'paid', '2024-03-15 09:15:00+00'),
(2, 'paid', '2024-01-25 16:45:00+00'),
(2, 'cancelled', '2024-02-05 11:30:00+00'),
(2, 'paid', '2024-03-20 13:20:00+00'),
(3, 'pending', '2024-02-15 08:30:00+00'),
(3, 'paid', '2024-03-01 15:45:00+00'),
(4, 'paid', '2024-02-20 12:15:00+00'),
(4, 'shipped', '2024-03-10 10:30:00+00'),
(5, 'paid', '2024-02-25 14:00:00+00'),
(5, 'paid', '2024-03-25 11:45:00+00'),
(6, 'paid', '2024-03-05 09:30:00+00'),
(6, 'paid', '2024-04-01 16:20:00+00'),
(7, 'paid', '2024-03-10 13:15:00+00'),
(7, 'shipped', '2024-04-05 10:45:00+00'),
(8, 'paid', '2024-03-15 12:30:00+00'),
(8, 'paid', '2024-04-10 15:00:00+00'),
(9, 'paid', '2024-03-20 11:20:00+00'),
(9, 'cancelled', '2024-04-15 14:30:00+00'),
(10, 'paid', '2024-03-25 16:45:00+00'),
(10, 'paid', '2024-04-20 09:15:00+00'),
(11, 'paid', '2024-04-05 13:30:00+00'),
(12, 'paid', '2024-04-10 10:45:00+00'),
(13, 'paid', '2024-04-15 15:20:00+00'),
(14, 'paid', '2024-04-20 12:00:00+00'),
(15, 'pending', '2024-04-25 14:30:00+00');

-- 4. 插入订单项数据
INSERT INTO order_items (order_id, product_id, quantity, price_cents_at_purchase) VALUES
-- 订单1 (用户1)
(1, 1, 1, 249999),  -- MacBook Pro
(1, 3, 1, 24999),   -- AirPods Pro

-- 订单2 (用户1)
(2, 2, 1, 99999),   -- iPhone 15 Pro
(2, 11, 2, 1999),   -- Lightning Cable

-- 订单3 (用户1)
(3, 4, 1, 59999),   -- iPad Air
(3, 6, 1, 9999),    -- Magic Keyboard

-- 订单4 (用户2)
(4, 1, 1, 249999),  -- MacBook Pro
(4, 8, 1, 159999),  -- Studio Display

-- 订单5 (用户2) - 已取消
(5, 2, 1, 99999),   -- iPhone 15 Pro

-- 订单6 (用户2)
(6, 5, 1, 39999),   -- Apple Watch
(6, 18, 1, 29999),  -- Noise Cancelling Headphones

-- 订单7 (用户3) - 待处理
(7, 3, 2, 24999),   -- AirPods Pro

-- 订单8 (用户3)
(8, 9, 1, 199999),  -- Mac Studio
(8, 16, 1, 19999),  -- External SSD

-- 订单9 (用户4)
(9, 2, 1, 99999),   -- iPhone 15 Pro
(9, 14, 1, 2999),   -- Phone Case

-- 订单10 (用户4)
(10, 4, 1, 59999),  -- iPad Air
(10, 6, 1, 9999),   -- Magic Keyboard

-- 订单11 (用户5)
(11, 1, 1, 249999), -- MacBook Pro
(11, 7, 1, 7999),   -- Magic Mouse

-- 订单12 (用户5)
(12, 5, 1, 39999),  -- Apple Watch
(12, 10, 1, 9999),  -- AirTag 4-pack

-- 订单13 (用户6)
(13, 3, 1, 24999),  -- AirPods Pro
(13, 12, 1, 1999),  -- USB-C Cable

-- 订单14 (用户6)
(14, 2, 1, 99999),  -- iPhone 15 Pro
(14, 13, 1, 3999),  -- Wireless Charger

-- 订单15 (用户7)
(15, 4, 1, 59999),  -- iPad Air
(15, 15, 1, 4999),  -- Laptop Stand

-- 订单16 (用户7)
(16, 1, 1, 249999), -- MacBook Pro
(16, 8, 1, 159999), -- Studio Display

-- 订单17 (用户8)
(17, 2, 1, 99999),  -- iPhone 15 Pro
(17, 18, 1, 29999), -- Noise Cancelling Headphones

-- 订单18 (用户8)
(18, 5, 1, 39999),  -- Apple Watch
(18, 19, 1, 5999),  -- Gaming Mouse

-- 订单19 (用户9)
(19, 3, 1, 24999),  -- AirPods Pro
(19, 20, 1, 12999), -- Mechanical Keyboard

-- 订单20 (用户9) - 已取消
(20, 1, 1, 249999), -- MacBook Pro

-- 订单21 (用户10)
(21, 4, 1, 59999),  -- iPad Air
(21, 6, 1, 9999),   -- Magic Keyboard

-- 订单22 (用户10)
(22, 2, 1, 99999),  -- iPhone 15 Pro
(22, 14, 1, 2999),  -- Phone Case

-- 订单23 (用户11)
(23, 5, 1, 39999),  -- Apple Watch
(23, 10, 1, 9999),  -- AirTag 4-pack

-- 订单24 (用户12)
(24, 1, 1, 249999), -- MacBook Pro
(24, 9, 1, 199999), -- Mac Studio

-- 订单25 (用户13)
(25, 3, 1, 24999),  -- AirPods Pro
(25, 17, 1, 7999),  -- Bluetooth Speaker

-- 订单26 (用户14)
(26, 2, 1, 99999),  -- iPhone 15 Pro
(26, 4, 1, 59999),  -- iPad Air

-- 订单27 (用户15) - 待处理
(27, 1, 1, 249999), -- MacBook Pro
(27, 8, 1, 159999); -- Studio Display

-- 验证数据
SELECT 'Users count:' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Products count:', COUNT(*) FROM products
UNION ALL
SELECT 'Orders count:', COUNT(*) FROM orders
UNION ALL
SELECT 'Order items count:', COUNT(*) FROM order_items;


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

-- Latest order per user using CTE
WITH ranked_orders AS (
  SELECT id, user_id, created_at,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at DESC) AS rn
  FROM orders
)
SELECT *
FROM ranked_orders
WHERE rn = 1;

EXPLAIN ANALYZE
SELECT user_id, COUNT(*) AS paid_orders
FROM orders
WHERE status = 'paid'
GROUP BY user_id
HAVING COUNT(*) >= 1
ORDER BY paid_orders DESC;
