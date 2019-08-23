DROP TABLE if exists easy_feedback;
CREATE TABLE easy_feedback (
	id SERIAL PRIMARY KEY,
	name VARCHAR,
	experience VARCHAR,
	functionality VARCHAR,
	aesthetics VARCHAR,
	comment VARCHAR
);