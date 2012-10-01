-- drop table if exists categories;
-- create table categories (
-- id integer primary key autoincrement,
-- category string not null
-- );

-- drop table if exists ingredients;
-- create table ingredients (
-- id integer primary key autoincrement,
-- ingredient string not null
-- category foreign key
-- );

drop table if exists pizzas;
create table pizzas (
id integer primary key autoincrement,
ingredients string not null
);