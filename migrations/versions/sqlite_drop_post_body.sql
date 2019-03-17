BEGIN TRANSACTION;

ALTER TABLE post RENAME TO temp_post;

CREATE TABLE post (
    id INTEGER NOT NULL,
    title VARCHAR(100),
    timestamp DATETIME,
    user_id INTEGER, 
    public BOOLEAN,
    simple_title VARCHAR(100),
    PRIMARY KEY (id),
    FOREIGN KEY(user_id) REFERENCES user (id)
);

CREATE UNIQUE INDEX ix_post_simple_title ON post (simple_title)
CREATE INDEX ix_post_timestamp ON post (timestamp)

INSERT INTO post
SELECT 
  id, title, timestamp, user_id, public, simple_title
FROM
  temp_post;

DROP TABLE temp_post;

COMMIT;