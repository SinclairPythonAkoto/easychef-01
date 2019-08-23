DROP TABLE if exists easysearch_feedback;
CREATE TABLE easysearch_feedback (
	id SERIAL PRIMARY KEY,
	name VARCHAR,
	experience VARCHAR,
	functionality VARCHAR,
	aesthetics VARCHAR,
	comment VARCHAR
);