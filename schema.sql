drop table if exists channel;
create table channel (
  id integer primary key autoincrement,
  channelName text not null
);

drop table if exists collections;
create table collections(
  id integer primary key autoincrement,
  collectionName text not null,
  collectionType integer,
  collectionImageUrl text,
  collectionImageUrl2 text,
  contentList text
);

drop table if exists contents;
create table contents(
  id integer primary key autoincrement,
  contentName text not null,
  collectionType integer,
  description text not null,
  publish text not null,
  author text not null,
  length integer,
  downloadCount integer,
  relatedContentList text
);

drop table if exists chapters;
create table chapters  (
  id integer primary key autoincrement,
  ContentId integer,
  chapterName text,
  chapterStatus integer,
  chapterFileName text
);

drop table if exists incomings;
create table incomings (
  id integer primary key autoincrement,
  userId integer,
  chapterId integer,
  amount  float
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
