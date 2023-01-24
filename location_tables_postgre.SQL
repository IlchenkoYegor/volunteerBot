/*
Created: 13.03.2022
Modified: 13.03.2022
Model: PostgreSQL 12
Database: PostgreSQL 12
*/

-- Create tables section -------------------------------------------------

-- Table location_info

CREATE TABLE location_info
(
  lon Double precision NOT NULL,
  lat Double precision NOT NULL,
  message Character varying(400),
  is_danger Boolean NOT NULL,
  date_of_answer Timestamp(9) NOT NULL,
  road Character varying(90) NOT NULL,
  name Character varying(50) NOT NULL
)
WITH (
  autovacuum_enabled=true)
;

CREATE INDEX IX_Relationship2 ON location_info (name)
;

-- Table region

CREATE TABLE region
(
  name Character varying(50) NOT NULL
)
WITH (
  autovacuum_enabled=true)
;

ALTER TABLE region ADD CONSTRAINT PK_region PRIMARY KEY (name)
;

-- Create foreign keys (relationships) section -------------------------------------------------

ALTER TABLE location_info
  ADD CONSTRAINT exist
    FOREIGN KEY (name)
    REFERENCES region (name)
      ON DELETE NO ACTION
      ON UPDATE NO ACTION
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

