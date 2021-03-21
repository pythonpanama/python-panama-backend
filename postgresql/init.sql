CREATE USER ppty WITH PASSWORD 'pass';
CREATE DATABASE ppty_dev;
GRANT ALL PRIVILEGES ON DATABASE ppty_dev TO ppty;

\connect ppty_dev ppty

\connect postgres postgres
CREATE DATABASE ppty_test;
GRANT ALL PRIVILEGES ON DATABASE ppty_test TO ppty;
