CREATE TABLE judges (
    id CHAR(36) PRIMARY KEY,
    judge_number INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    department VARCHAR(100),
    hour_available VARCHAR(50)
);

CREATE TABLE abstracts (
    id CHAR(36) PRIMARY KEY,
    poster_number INT,
    title TEXT,
    abstract TEXT,
    advisor_first_name VARCHAR(100),
    advisor_last_name VARCHAR(100),
    program VARCHAR(100)
);