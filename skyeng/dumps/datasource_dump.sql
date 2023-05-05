CREATE TABLE IF NOT EXISTS course
(
   id                    INTEGER NOT NULL,
   title                 VARCHAR(255),
   created_at            TIMESTAMP DEFAULT now(),
   updated_at            TIMESTAMP DEFAULT 0,
   deleted_at            TIMESTAMP(0) DEFAULT 0,
   icon_url              VARCHAR(255),
   is_auto_course_enroll BOOLEAN,
   is_demo_enroll        BOOLEAN,
   CONSTRAINT course_pkey PRIMARY KEY (id),
);

CREATE TABLE IF NOT EXISTS stream
(
   id                     INTEGER NOT NULL,
   course_id              INTEGER,
   start_at               TIMESTAMP,
   end_at                 TIMESTAMP,
   created_at             TIMESTAMP DEFAULT now(),
   updated_at             TIMESTAMP DEFAULT 0,
   deleted_at             TIMESTAMP DEFAULT 0,
   is_open                BOOLEAN,
   name                   VARCHAR(255),
   homework_deadline_days INTEGER DEFAULT 7,
   CONSTRAINT stream_pkey PRIMARY KEY (id),
   CONSTRAINT fk_course
       FOREIGN KEY(course_id)
	       REFERENCES course(course_id)
);

CREATE TABLE IF NOT EXISTS stream_module
(
   id              INTEGER NOT NULL,
   stream_id       INTEGER,
   title           VARCHAR(255),
   created_at      TIMESTAMP DEFAULT now(),
   updated_at      TIMESTAMP, DEFAULT 0,
   order_in_stream INTEGER,
   deleted_at      TIMESTAMP DEFAULT 0,
   CONSTRAINT stream_module_pkey PRIMARY KEY (id),
   CONSTRAINT fk_stream
       FOREIGN KEY(stream_id)
	       REFERENCES stream(stream_id)
);

CREATE TABLE IF NOT EXISTS stream_module_lesson
(
   id                          INTEGER NOT NULL,
   title                       VARCHAR(255),
   description                 TEXT,
   start_at                    TIMESTAMP,
   end_at                      TIMESTAMP,
   homework_url                VARCHAR(500),
   teacher_id                  INTEGER,
   stream_module_id            INTEGER,
   deleted_at                  TIMESTAMP(0) DEFAULT 0,
   online_lesson_join_url      VARCHAR(255),
   online_lesson_recording_url VARCHAR(255),
   CONSTRAINT stream_module_lesson_pkey PRIMARY KEY (id),
   CONSTRAINT fk_stream_module
       FOREIGN KEY(stream_module_id)
	       REFERENCES stream_module(stream_module_id)
);

INSERT INTO
    course (title, icon_url, is_auto_course_enroll, is_demo_enroll)
VALUES
    ('Data Science', 'http://example.com/bite', TRUE, TRUE),
    ('Data Engineering', 'https://www.example.org/', FALSE, FALSE),
    ('Data Analysis', 'http://www.example.com/', FALSE, TRUE);

INSERT INTO
    stream (course_id, start_at, end_at, is_open, name)
VALUES
    (1, '2023-04-21', '2023-06-18', TRUE, 'DS_Stream_1'),
    (2, '2023-02-19', '2023-04-24', TRUE, 'DE_Stream_2'),
    (2, '2022-03-14', '2022-05-15', FALSE, 'DE_Stream_1'),
    (3, '2023-02-07', '2023-03-27', TRUE, 'DA_Stream_3'),
    (3, '2023-01-22', '2023-03-24', TRUE, 'DA_Stream_2'),
    (3, '2022-10-25', '2022-12-19', FALSE, 'DS_Stream_1');

INSERT INTO
    stream_module (stream_id, title, order_in_stream)
VALUES
    (1, 'Python', 1),
    (1, 'Math', 2),
    (1, 'Machine Learning', 3),
    (2, 'Python', 1),
    (2, 'Databases', 2),
    (2, 'ETL', 3),
    (3, 'Python', 1),
    (3, 'Databases', 2),
    (3, 'ETL', 3),
    (4, 'Python', 1),
    (4, 'BI', 2),
    (4, 'Jupyter Notebook', 3),
    (5, 'Python', 1),
    (5, 'BI', 2),
    (5, 'Jupyter Notebook', 3),
    (6, 'Python', 1),
    (6, 'BI', 2),
    (6, 'Jupyter Notebook', 3);

INSERT INTO
    stream_module_lesson (
        title, description,
        start_at, end_at,
        homework_url, teacher_id,
        stream_module_id, online_lesson_join_url,
        online_lesson_recording_url
    )
VALUES
('Variables', 'TL;DR', '2023-04-22', '2023-04-27', 'https://www.example.edu/boot/ants', 1, 1, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Data Structures', 'TL;DR', '2023-04-28', '2023-05-04', 'https://www.example.edu/boot/ants', 1, 1, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Calculus', 'TL;DR', '2023-05-05', '2023-05-12', 'https://www.example.edu/boot/ants', 1, 2, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Linear Algebra', 'TL;DR', '2023-05-12', '2023-05-18', 'https://www.example.edu/boot/ants', 1, 2, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('PyTorch', 'TL;DR', '2023-05-19', '2023-05-26', 'https://www.example.edu/boot/ants', 1, 3, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('TensorFlow', 'TL;DR', '2023-05-27', '2023-06-04', 'https://www.example.edu/boot/ants', 1, 3, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
('Variables', 'TL;DR', '2023-02-19', '2023-02-27', 'https://www.example.edu/boot/ants', 1, 4, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Data Structures', 'TL;DR', '2023-02-28', '2023-03-06', 'https://www.example.edu/boot/ants', 1, 4, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('SQL', 'TL;DR', '2023-03-07', '2023-03-15', 'https://www.example.edu/boot/ants', 1, 5, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('PostgreSQL', 'TL;DR', '2023-03-16', '2023-03-24', 'https://www.example.edu/boot/ants', 1, 5, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Cron', 'TL;DR', '2023-03-25', '2023-04-04', 'https://www.example.edu/boot/ants', 1, 6, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Apache Airflow', 'TL;DR', '2023-04-05', '2023-04-14', 'https://www.example.edu/boot/ants', 1, 6, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
('Variables', 'TL;DR', '2022-03-14', '2022-03-21', 'https://www.example.edu/boot/ants', 1, 7, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Data Structures', 'TL;DR', '2022-03-22', '2022-03-29', 'https://www.example.edu/boot/ants', 1, 7, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('SQL', 'TL;DR', '2022-03-30', '2022-04-13', 'https://www.example.edu/boot/ants', 1, 8, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('PostgreSQL', 'TL;DR', '2022-04-14', '2022-04-21', 'https://www.example.edu/boot/ants', 1, 8, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Cron', 'TL;DR', '2022-04-22', '2022-04-27', 'https://www.example.edu/boot/ants', 1, 9, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Apache Airflow', 'TL;DR', '2022-04-28', '2022-05-05', 'https://www.example.edu/boot/ants', 1, 9, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
('Variables', 'TL;DR', '2023-02-07', '2023-02-14', 'https://www.example.edu/boot/ants', 1, 10, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Data Structures', 'TL;DR', '2023-02-15', '2023-02-23', 'https://www.example.edu/boot/ants', 1, 10, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Apache Superset', 'TL;DR', '2023-02-24', '2023-03-01', 'https://www.example.edu/boot/ants', 1, 11, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Power BI', 'TL;DR', '2023-03-02', '2023-03-10', 'https://www.example.edu/boot/ants', 1, 11, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Reporting', 'TL;DR', '2023-03-11', '2023-03-17', 'https://www.example.edu/boot/ants', 1, 12, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Analytics', 'TL;DR', '2023-03-18', '2023-03-25', 'https://www.example.edu/boot/ants', 1, 12, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
('Variables', 'TL;DR', '2023-01-22', '2023-01-29', 'https://www.example.edu/boot/ants', 1, 13, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Data Structures', 'TL;DR', '2023-01-30', '2023-02-07', 'https://www.example.edu/boot/ants', 1, 13, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Apache Superset', 'TL;DR', '2023-02-08', '2023-02-15', 'https://www.example.edu/boot/ants', 1, 14, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Power BI', 'TL;DR', '2023-02-16', '2023-02-24', 'https://www.example.edu/boot/ants', 1, 14, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Reporting', 'TL;DR', '2023-02-25', '2023-03-05', 'https://www.example.edu/boot/ants', 1, 15, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Analytics', 'TL;DR', '2023-03-06', '2023-03-14', 'https://www.example.edu/boot/ants', 1, 15, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
('Variables', 'TL;DR', '2022-10-25', '2022-11-04', 'https://www.example.edu/boot/ants', 1, 16, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Data Structures', 'TL;DR', '2022-11-05', '2022-11-12', 'https://www.example.edu/boot/ants', 1, 16, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Apache Superset', 'TL;DR', '2022-11-13', '2022-11-20', 'https://www.example.edu/boot/ants', 1, 17, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Power BI', 'TL;DR', '2022-11-21', '2022-11-27', 'https://www.example.edu/boot/ants', 1, 17, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Reporting', 'TL;DR', '2022-11-28', '2022-12-04', 'https://www.example.edu/boot/ants', 1, 18, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec'),
    ('Analytics', 'TL;DR', '2022-12-05', '2022-12-15', 'https://www.example.edu/boot/ants', 1, 18, 'https://www.example.edu/boot/', 'https://www.example.edu/boot/rec');

