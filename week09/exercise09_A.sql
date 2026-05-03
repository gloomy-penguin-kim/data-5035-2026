
use database USER$DOLPHIN; 

create or replace temporary table customers (
    customer_id int, 
    name varchar, 
    state varchar(2)
);
insert into customers values (1, 'Alice', 'MO');
insert into customers values (2, 'Bob', 'IL');
insert into customers values (3, 'Carol', 'Tx');

create or replace table orders (
    order_id int, 
    customer_id int, 
    order_date TIMESTAMP, 
    amount decimal(10,2)
);
insert into orders values (101, 1, '2024-01-01', 100.00);
insert into orders values (102, 1, '2024-01-05', 50.00);
insert into orders values (103, 2, '2024-01-03', 75.00);

select * from orders; 

create or replace temporary table order_returns (
    return_id int, 
    order_id int, 
    return_date TIMESTAMP
);
insert into order_returns values (9001, 102, '2024-01-10');

-- Q! Show all puraches with the customer who made them. 
-- Assumptions: you might have purchases without a customer and do not care 
-- about customers with no purchases, based on wording 
-- select  orders.order_id, orders.cusomer_id, customer.name, customer.state, orders.order_date, orders.amount 
-- from    orders
--         left outer join customers on orders.customer_id = customers.customer_id;