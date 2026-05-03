drop temp  table if exists customers;
create temporary table customers (
    customer_id int, 
    name varchar(255), 
    state varchar(2)
);
insert into customers values (1, 'Alice', 'MO');
insert into customers values (2, 'Bob', 'IL');
insert into customers values (3, 'Carol', 'Tx');

drop temp table if exists orders; 
create temporary table orders (
    order_id int, 
    customer_id int, 
    order_date TIMESTAMP, 
    amount decimal(10,2)
);
insert into orders (order_id, customer_id, order_date, amount) values (101, 1, '2024-01-01', 100.00);
insert into orders (order_id, customer_id, order_date, amount) values (102, 1, '2024-01-05', 50.00);
insert into orders (order_id, customer_id, order_date, amount) values (103, 2, '2024-01-03', 75.00);

select * from orders; 

drop temp table if exists returns; 
create temporary table returns (
    return_id int, 
    order_id int, 
    return_date TIMESTAMP
);
insert into returns values (9001, 102, '2024-01-10');

-- Q! Show all puraches with the customer who made them. 
-- Assumptions: you might have purchases without a customer and do not care 
-- about customers with no purchases, based on wording 
select  customers.name, orders.order_id, orders.amount  
from    orders
        left outer join customers on orders.customer_id = customers.customer_id;

-- Q2 - all customera nd and orders they may have placed
select  customers.name, orders.order_id  
from    customers
        left outer join orders on customers.customer_id = orders.customer_id;

-- Q3 idefinify whether each order was returned or not 
select  orders.order_id, returns.return_id is null as is_returned 
from    orders 
        left outer join returns on returns.order_id = orders.order_id;

-- Q4 show only orders that were returned and who made them 
select  customers.name, orders.order_id, returns.return_date 
from    orders 
       join returns on returns.order_id = orders.order_id
       left outer join customers on orders.customer_id = customers.customer_id;

-- Q5 find customers who have never made a purchase  
select  customers.name 
from    customers 
       left outer join orders on customers.customer_id = orders.customer_id
       left outer join returns on returns.order_id = orders.order_id
where   orders.order_id is null and returns.return_id is null;