/*
Created: 02.03.2022
Modified: 02.03.2022
Model: DB2 v.11.1 (LUW)
Database: DB2 v.11.1 (LUW)
*/


-- Create tables section -------------------------------------------------

-- Table location_info


CREATE TABLE location_info(
  lon Double NOT NULL,
  lat Double NOT NULL,
  message NVarchar(400),
  is_danger Boolean NOT NULL,
  date_of_answer Timestamp NOT NULL,
  road NVarchar(90) NOT NULL,
  name NVarchar(50) NOT NULL
)
;


-- Create indexes for table location_info

CREATE INDEX IX_Relationship123 ON location_info (name)
DISALLOW REVERSE SCANS
COMPRESS NO
;
-- Table region

CREATE TABLE region(
  name NVarchar(50) NOT NULL
)
;


-- Add keys for table region

ALTER TABLE region ADD CONSTRAINT PK_region PRIMARY KEY (name)
;

-- Create foreign keys (relationships) section ------------------------------------------------- 

ALTER TABLE location_info ADD CONSTRAINT exist FOREIGN KEY (name) REFERENCES region (name)
;


INSERT INTO region values (	'Чернівецька область'),
                          ('Закарпатська область'),
                          ('Тернопільська область'),
                          ('Івано-Франківська область'),
                          ('Рівненська область'),
                          ('Волинська область'),
                          ('Хмельницька область'),
                          ('Черкаська область'),
                          ('Львівська область'),
                          ('Сумська область'),
                          ('Кіровоградська область'),
                          ('Миколаївська область'),
                          ('Автономна Республіка Крим'),
                          ('Вінницька область'),
                          ('Донецька область'),
                          ('Луганська область'),
                          ('Запорізька область'),
                          ('Київська область'),
                          ('Херсонська область'),
                          ('Полтавська область'),
                          ('Житомирська область'),
                          ('Харківська область'),
                          ('Чернігівська область'),
                          ('Дніпровська область'),
                          ('Одеська область');

commit;

