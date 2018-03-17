create grain example version '1.0';

CREATE TABLE Example(
/** {"width": 20}*/
guid varchar(50) NOT NULL,
first_column INT,
second_column VARCHAR(100),
third_column TEXT,
fourth_column BIT,
fifth_column  DATETIME,
CONSTRAINT Example_primary_key PRIMARY KEY (guid)
);
