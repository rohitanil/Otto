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

CREATE TABLE poster_judge_mapping (
    id CHAR(36) PRIMARY KEY DEFAULT (UUID_TO_BIN(UUID())),
    poster_number INT,
    Judge1 DOUBLE DEFAULT 0,
    Judge2 DOUBLE DEFAULT 0,
    Judge3 DOUBLE DEFAULT 0,
    Judge4 DOUBLE DEFAULT 0,
    Judge5 DOUBLE DEFAULT 0
);

CREATE TABLE poster_score (
    judge1_id CHAR(36) NOT NULL,
    judge2_id CHAR(36) NOT NULL,
    abstract_id CHAR(36) NOT NULL,
    score1 DOUBLE NOT NULL,
    score2 DOUBLE NOT NULL,
    overall DOUBLE AS ((score1 + score2) / 2) VIRTUAL,  -- Use VIRTUAL instead of STORED
    FOREIGN KEY (judge1_id) REFERENCES judges(id),
    FOREIGN KEY (judge2_id) REFERENCES judges(id) ,
    FOREIGN KEY (abstract_id) REFERENCES abstracts(id)
)ENGINE=InnoDB;

