# Week 3 Assignment Evidence

Group name: 21
Group leader: CHIME DIVINE CHIAGOZIE

## Task 3 query analysis
The query for open or assigned Electrical requests, ordered by priority and created date, used the composite index req_cat_status_idx (index range scan on category_id and status, estimated cost 2.31, 4 rows). MySQL then sorted the rows by priority and created_at.

Full generated SQL and explain output: backend/lab_week3_output.txt