drop table if exists books;
create table books(
  id integer primary key autoincrement,
  fileName text not null,
  description text not null,
  publish text not null,
  author text not null,
  length integer
);
drop table if exists users;
create table users (
  id integer primary key autoincrement,
  userName text not null,
  password text not null,
  nickName text not null,
  phoneNumber text not null,
  email text not null,
  birthDay text not null
);

drop table if exists recomandBooks;
create table recomandBooks (
  id integer primary key autoincrement,
  bookId integer    
);
