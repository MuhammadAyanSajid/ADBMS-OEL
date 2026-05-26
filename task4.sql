create database oel;
go
use oel;
go
-- 1. Customers Table
create table customers (
    customer_id int identity(1,1) primary key,
    name varchar(100),
    country varchar(50),
    created_at date
);

-- 2. Orders Table
create table orders (
    order_id int identity(1,1) primary key,
    customer_id int, 
    order_date date,
    total_amount decimal(10, 2)
);

-- 3. Order Items Table
create table order_items (
    item_id int identity(1,1) primary key,
    order_id int, 
    product_id int,
    quantity int,
    price decimal(10, 2)
);

-- 1. Populate Customers (10,000 rows)
with 
  L0 as (select 1 as c union all select 1),
  L1 as (select 1 as c from L0 as A cross join L0 as B),
  L2 as (select 1 as c from L1 as A cross join L1 as B),
  L3 as (select 1 as c from L2 as A cross join L2 as B),
  L4 as (select 1 as c from L3 as A cross join L3 as B),
  L5 as (select 1 as c from L4 as A cross join L4 as B),
  Nums as (select top 10000 row_number() over (order by (select null)) as n from L5)
insert into customers (name, country, created_at)
select 
    'Customer_' + cast(n as varchar(10)),
    case when n % 3 = 0 then 'USA' when n % 3 = 1 then 'UK' else 'Canada' end,
    dateadd(day, - (n % 365), cast(getdate() as date))
from Nums;

-- 2. Populate Orders (50,000 rows linked to customers 1 to 10,000)
with 
  L0 as (select 1 as c union all select 1),
  L1 as (select 1 as c from L0 as A cross join L0 as B),
  L2 as (select 1 as c from L1 as A cross join L1 as B),
  L3 as (select 1 as c from L2 as A cross join L2 as B),
  L4 as (select 1 as c from L3 as A cross join L3 as B),
  L5 as (select 1 as c from L4 as A cross join L4 as B),
  Nums as (select top 50000 row_number() over (order by (select null)) as n from L5)
insert into orders (customer_id, order_date, total_amount)
select 
    (abs(checksum(newid())) % 10000) + 1,
    dateadd(day, - (abs(checksum(newid())) % 365), cast(getdate() as date)),
    cast((abs(checksum(newid())) % 50000) / 100.0 as decimal(10,2))
from Nums;

-- 3. Populate Order Items (150,000 rows linked to orders 1 to 50,000)
with 
  L0 as (select 1 as c union all select 1),
  L1 as (select 1 as c from L0 as A cross join L0 as B),
  L2 as (select 1 as c from L1 as A cross join L1 as B),
  L3 as (select 1 as c from L2 as A cross join L2 as B),
  L4 as (select 1 as c from L3 as A cross join L3 as B),
  L5 as (select 1 as c from L4 as A cross join L4 as B),
  Nums as (select top 150000 row_number() over (order by (select null)) as n from L5)
insert into order_items (order_id, product_id, quantity, price)
select 
    (abs(checksum(newid())) % 50000) + 1,
    (abs(checksum(newid())) % 1000) + 1,
    (abs(checksum(newid())) % 10) + 1,
    cast((abs(checksum(newid())) % 10000) / 100.0 as decimal(10,2))
from Nums;

-- Unoptimized Query
    set statistics time on;
    set statistics io on;
    go

    select 
        c.name,
        c.country,
        (select sum(o.total_amount) from orders o where o.customer_id = c.customer_id) as total_spent,
        (select avg(oi.price) from order_items oi where oi.order_id in (select o.order_id from orders o where o.customer_id = c.customer_id)) as avg_item_price
    from customers c
    where c.country = 'USA' 
      and (select sum(o.total_amount) from orders o where o.customer_id = c.customer_id) > 1000;
    go

    set statistics time off;
    set statistics io off;


-- Optimized Query with Indexes
create index idx_customers_country on customers(country);
create index idx_orders_customer_id on orders(customer_id);
create index idx_order_items_order_id on order_items(order_id);

set statistics time on;
set statistics io on;
go

select 
    c.name,
    c.country,
    sum(o.total_amount) as total_spent,
    avg(oi.price) as avg_item_price
from customers c
inner join orders o on c.customer_id = o.customer_id
inner join order_items oi on o.order_id = oi.order_id
where c.country = 'USA'
group by c.customer_id, c.name, c.country
having sum(o.total_amount) > 1000;
go

set statistics time off;
set statistics io off;