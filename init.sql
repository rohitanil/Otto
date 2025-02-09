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
    judge1 DOUBLE DEFAULT 0,
    judge1_id INT,
    judge2 DOUBLE DEFAULT 0,
    judge2_id INT,
    judge3 DOUBLE DEFAULT 0,
    judge3_id INT,
    judge4 DOUBLE DEFAULT 0,
    judge4_id INT,
    judge5 DOUBLE DEFAULT 0,
    judge5_id INT
);

CREATE TABLE poster_score (
    judge_id CHAR(36) NOT NULL,
    abstract_id CHAR(36) NOT NULL,
    score DOUBLE NOT NULL,
    FOREIGN KEY (judge_id) REFERENCES judges(id),
    FOREIGN KEY (abstract_id) REFERENCES abstracts(id)
)ENGINE=InnoDB;

CREATE TABLE poster_score_summary (
    abstract_id CHAR(36) NOT NULL,
    average_score DOUBLE NOT NULL,
    judge_id1 CHAR(36) ,
    judge_id2 CHAR(36) ,
    num_of_scores INT NOT NULL,
    PRIMARY KEY (abstract_id),
    FOREIGN KEY (abstract_id) REFERENCES abstracts(id)
) ENGINE=InnoDB;

DELIMITER //

CREATE TRIGGER after_insert_poster_score
AFTER INSERT ON poster_score
FOR EACH ROW
BEGIN
    DECLARE avg_score DOUBLE;
    DECLARE num_scores INT;
    DECLARE judge1 CHAR(36);
    DECLARE judge2 CHAR(36);

    -- Calculate the average score and count the number of scores for the given abstract_id
    SELECT AVG(score), COUNT(*) INTO avg_score, num_scores
    FROM poster_score
    WHERE abstract_id = NEW.abstract_id;

    -- Fetch the two most recent judge_ids who scored this abstract_id
    SELECT judge_id INTO judge1
    FROM poster_score
    WHERE abstract_id = NEW.abstract_id
    ORDER BY score DESC
    LIMIT 1 OFFSET 0;

    SELECT judge_id INTO judge2
    FROM poster_score
    WHERE abstract_id = NEW.abstract_id
    ORDER BY score DESC
    LIMIT 1 OFFSET 1;

    -- Check if the abstract_id already exists in the poster_score_summary table
    IF EXISTS (SELECT 1 FROM poster_score_summary WHERE abstract_id = NEW.abstract_id) THEN
        -- Update the summary if it already exists
        UPDATE poster_score_summary
        SET average_score = avg_score,
            num_of_scores = num_scores,
            judge_id1 = judge1,
            judge_id2 = judge2
        WHERE abstract_id = NEW.abstract_id;
    ELSE
        -- Insert a new summary entry if it doesn't exist
        INSERT INTO poster_score_summary (abstract_id, average_score, num_of_scores, judge_id1, judge_id2)
        VALUES (NEW.abstract_id, avg_score, num_scores, judge1, judge2);
    END IF;
END //

DELIMITER ;

