CREATE TABLE addresses (
  address_id VARCHAR(256) PRIMARY KEY,
  address VARCHAR(8192),
  zipcode INTEGER,
  state VARCHAR(256),
  country VARCHAR(256)
);

CREATE TABLE users (
  user_id VARCHAR(256) PRIMARY KEY,
  first_name VARCHAR(256),
  last_name VARCHAR(256),
  email VARCHAR(1024),
  phone_number VARCHAR(256),
  created_at TIMESTAMP,
  updated_at TIMESTAMP,
  address_id VARCHAR(256) REFERENCES addresses(address_id)
);

CREATE TABLE promos (
  promo_id VARCHAR(256) PRIMARY KEY,
  discount INTEGER,
  status VARCHAR(128)
);

CREATE TABLE products (
  product_id VARCHAR(256) PRIMARY KEY,
  name VARCHAR(1024),
  price REAL,
  inventory INTEGER
);

CREATE TABLE orders (
  order_id VARCHAR(256) PRIMARY KEY,
  user_id VARCHAR(256) REFERENCES users(user_id),
  promo_id VARCHAR(256) REFERENCES promos(promo_id),
  address_id VARCHAR(256) REFERENCES addresses(address_id),
  created_at TIMESTAMP,
  order_cost REAL,
  shipping_cost REAL,
  order_total REAL,
  tracking_id VARCHAR(256),
  shipping_service VARCHAR(128),
  estimated_delivery_at TIMESTAMP,
  delivered_at TIMESTAMP,
  status VARCHAR(128)
);

CREATE TABLE order_items (
  order_id VARCHAR(256) REFERENCES orders(order_id),
  product_id VARCHAR(256) REFERENCES products(product_id),
  quantity INTEGER,
  PRIMARY KEY(order_id, product_id)
);

CREATE TABLE events(
  event_id VARCHAR(256) PRIMARY KEY,
  session_id VARCHAR(256),
  user_id VARCHAR(256) REFERENCES users(user_id),
  page_url VARCHAR(4096),
  created_at TIMESTAMP,
  event_type VARCHAR(128),
  order_id VARCHAR(256) REFERENCES orders(order_id),
  product_id VARCHAR(256) REFERENCES products(product_id)
);

COPY addresses FROM '/data/addresses.csv' DELIMITER ',' CSV HEADER;
COPY users FROM '/data/users.csv' DELIMITER ',' CSV HEADER;
COPY promos FROM '/data/promos.csv' DELIMITER ',' CSV HEADER;
COPY products FROM '/data/products.csv' DELIMITER ',' CSV HEADER;
COPY orders FROM '/data/orders.csv' DELIMITER ',' CSV HEADER;
COPY order_items FROM '/data/order_items.csv' DELIMITER ',' CSV HEADER;
COPY events FROM '/data/events.csv' DELIMITER ',' CSV HEADER;