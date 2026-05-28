use oel;
go

-- 1. Drop the central fact table first to release foreign key holds
if object_id('dbo.fact_sales', 'u') is not null drop table dbo.fact_sales;
if object_id('dbo.dim_time', 'u') is not null drop table dbo.dim_time;
if object_id('dbo.dim_product', 'u') is not null drop table dbo.dim_product;
if object_id('dbo.dim_customer', 'u') is not null drop table dbo.dim_customer;
go

-- 2. Create Customer Dimension Table
create table dim_customer (
    customer_key int identity(1,1) primary key,
    customer_id int, 
    customer_name varchar(100),
    country varchar(50),
    segment varchar(50)
);

-- 3. Create Product Dimension Table
create table dim_product (
    product_key int identity(1,1) primary key,
    product_id int, 
    product_name varchar(100),
    category varchar(50),
    brand varchar(50)
);

-- 4. Create Time Dimension Table
create table dim_time (
    time_key int identity(1,1) primary key,
    full_date date,
    day_of_week varchar(15),
    month_name varchar(15),
    quarter int,
    year int
);

-- 5. Create Fact Table
create table fact_sales (
    sales_key int identity(1,1) primary key,
    customer_key int foreign key references dim_customer(customer_key),
    product_key int foreign key references dim_product(product_key),
    time_key int foreign key references dim_time(time_key),
    quantity_sold int,
    sales_amount decimal(10,2),
    cost_amount decimal(10,2)
);
go

-- 6. Insert full dataset
insert into dim_customer (customer_id, customer_name, country, segment)
values 
(1, 'Ayan', 'Pakistan', 'Premium'),
(2, 'Bilal', 'Pakistan', 'Standard'),
(3, 'Husnain', 'Pakistan', 'Standard');

insert into dim_product (product_id, product_name, category, brand)
values 
(101, 'Smartphone X', 'Electronics', 'TechBrand'),
(102, 'Leather Wallet', 'Apparel', 'StyleBrand'),
(103, 'Mechanical Keyboard', 'Electronics', 'KeyBrand'),
(104, 'Charging Cable', 'Electronics', 'TechBrand'),
(105, 'Screen Protector', 'Electronics', 'TechBrand');

insert into dim_time (full_date, day_of_week, month_name, quarter, year)
values 
('2026-05-26', 'Tuesday', 'May', 2, 2026),
('2026-05-27', 'Wednesday', 'May', 2, 2026);

insert into fact_sales (customer_key, product_key, time_key, quantity_sold, sales_amount, cost_amount)
values 
(1, 1, 1, 1, 999.00, 600.00),
(1, 4, 1, 1, 15.00, 5.00),
(1, 5, 1, 1, 10.00, 3.00),
(2, 1, 1, 1, 999.00, 600.00),
(2, 4, 1, 1, 15.00, 5.00),
(2, 2, 1, 2, 90.00, 40.00),  
(3, 1, 2, 1, 999.00, 600.00),
(3, 5, 2, 1, 10.00, 3.00),  
(3, 3, 2, 1, 120.00, 75.00);
go