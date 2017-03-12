drop table if exists articles;
create table articles (
    id integer primary key autoincrement,
    url text not null,
    title text not null, 
    author text not null,
    content text not null,
    thumbnail text not null
);
