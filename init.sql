CREATE TABLE judges (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
    judge_number INT,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    department VARCHAR(100),
    hour_available VARCHAR(50),
    poster_count INT NOT NULL DEFAULT 0,
    research_interests TEXT DEFAULT NULL,
    research_labels TEXT DEFAULT NULL
);

CREATE TABLE abstracts (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
    poster_number INT,
    title TEXT,
    abstract TEXT,
    advisor_first_name VARCHAR(100),
    advisor_last_name VARCHAR(100),
    program VARCHAR(100)
);