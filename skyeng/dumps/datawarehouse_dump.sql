create TABLE IF NOT EXISTS h_courses
(
   h_course_id                  SERIAL4 NOT NULL,
   h_course_title               VARCHAR(255),
   h_course_record_source       VARCHAR(255),
   h_course_load_ts             TIMESTAMP DEFAULT now(),
   CONSTRAINT h_course_pkey     PRIMARY KEY (h_course_id)
);

create TABLE IF NOT EXISTS s_courses
(
   s_course_id                          SERIAL4 NOT NULL,
   h_course_id                          INTEGER,
   s_course_record_source               VARCHAR(255),
   s_course_icon_url                    VARCHAR(255),
   s_course_is_auto_course_enroll       BOOLEAN,
   s_course_is_demo_enroll              BOOLEAN,
   s_course_created_at                  TIMESTAMP,
   s_course_updated_at                  TIMESTAMP,
   s_course_deleted_at                  TIMESTAMP(0),
   s_course_load_ts                     TIMESTAMP DEFAULT now(),
   CONSTRAINT s_course_pkey             PRIMARY KEY (s_course_id),
   CONSTRAINT fk_h_course
       FOREIGN KEY(h_course_id)
	       REFERENCES h_courses(h_course_id)
);

create TABLE IF NOT EXISTS h_streams
(
   h_stream_id                     SERIAL4 NOT NULL,
   h_stream_name                   VARCHAR(255),
   h_stream_record_source          VARCHAR(255),
   h_stream_load_ts                TIMESTAMP DEFAULT now(),
   CONSTRAINT h_stream_pkey        PRIMARY KEY (h_stream_id)
);

create TABLE IF NOT EXISTS s_streams
(
   s_stream_id                      SERIAL4 NOT NULL,
   h_stream_id                      INTEGER,
   s_stream_record_source           VARCHAR(255),
   s_stream_is_open                 BOOLEAN,
   s_stream_homework_deadline_days  INTEGER,
   s_stream_start_at                TIMESTAMP,
   s_stream_end_at                  TIMESTAMP,
   s_stream_created_at              TIMESTAMP,
   s_stream_updated_at              TIMESTAMP,
   s_stream_deleted_at              TIMESTAMP(0),
   s_stream_load_ts                 TIMESTAMP DEFAULT now(),
   CONSTRAINT s_stream_pkey         PRIMARY KEY (s_stream_id),
   CONSTRAINT fk_h_stream
       FOREIGN KEY(h_stream_id)
	       REFERENCES h_streams(h_stream_id)
);

create TABLE IF NOT EXISTS h_modules
(
   h_module_id                       SERIAL4 NOT NULL,
   h_module_title                    VARCHAR(255),
   h_module_record_source            VARCHAR(255),
   h_module_load_ts                  TIMESTAMP DEFAULT now(),
   CONSTRAINT h_module_pkey          PRIMARY KEY (h_module_id)
);

create TABLE IF NOT EXISTS s_modules
(
   s_module_id                             SERIAL4 NOT NULL,
   h_module_id                             INTEGER,
   s_module_record_source                  VARCHAR(255),
   s_module_created_at                     TIMESTAMP,
   s_module_updated_at                     TIMESTAMP,
   s_module_deleted_at                     TIMESTAMP(0),
   s_module_load_ts                        TIMESTAMP DEFAULT now(),
   CONSTRAINT s_module_pkey                PRIMARY KEY (s_module_id),
   CONSTRAINT fk_h_module
       FOREIGN KEY(h_module_id)
	       REFERENCES h_modules(h_module_id)
);

create TABLE IF NOT EXISTS h_lessons
(
   h_lesson_id                                  SERIAL4 NOT NULL,
   h_lesson_title                               VARCHAR(255),
   h_lesson_record_source                       VARCHAR(255),
   h_lesson_load_ts                             TIMESTAMP DEFAULT now(),
   CONSTRAINT h_lesson_pkey                     PRIMARY KEY (h_lesson_id)
);

create TABLE IF NOT EXISTS s_lessons
(
   s_lesson_id                             SERIAL4 NOT NULL,
   h_lesson_id                             INTEGER,
   s_lesson_record_source                  VARCHAR(255),
   s_lesson_description                    TEXT,
   s_lesson_teacher_id                     INTEGER,
   s_lesson_start_at                       TIMESTAMP,
   s_lesson_end_at                         TIMESTAMP,
   s_lesson_homework_url                   VARCHAR(500),
   s_lesson_online_lesson_join_url         VARCHAR(255),
   s_lesson_online_lesson_recording_url    VARCHAR(255),
   s_lesson_deleted_at                     TIMESTAMP,
   s_lesson_load_ts                        TIMESTAMP DEFAULT now(),
   CONSTRAINT s_lesson_pkey                PRIMARY KEY (s_lesson_id),
   CONSTRAINT fk_h_lesson
       FOREIGN KEY(h_lesson_id)
           REFERENCES h_lessons(h_lesson_id)
);

create TABLE IF NOT EXISTS l_courses_modules
(
    l_course_module_id                  SERIAL4 NOT NULL,
    h_course_id                         INTEGER,
    h_module_id                         INTEGER,
    CONSTRAINT l_course_module_pkey     PRIMARY KEY (l_course_module_id),
    CONSTRAINT fk_h_course
        FOREIGN KEY(h_course_id)
            REFERENCES h_courses(h_course_id),
    CONSTRAINT fk_h_module
        FOREIGN KEY(h_module_id)
            REFERENCES h_modules(h_module_id)
);

create TABLE IF NOT EXISTS l_courses_modules_lessons
(
    l_course_module_lesson_id                   SERIAL4 NOT NULL,
    l_course_module_id                          INTEGER,
    h_lesson_id                                 INTEGER,
    CONSTRAINT l_course_module_lesson_pkey      PRIMARY KEY (l_course_module_lesson_id),
    CONSTRAINT fk_l_course_module
        FOREIGN KEY(l_course_module_id)
            REFERENCES l_courses_modules(l_course_module_id),
    CONSTRAINT fk_h_lesson
        FOREIGN KEY(h_lesson_id)
            REFERENCES h_lessons(h_lesson_id)
);

create TABLE IF NOT EXISTS l_courses_modules_lessons_streams
(
    l_course_module_lesson_stream_id                   SERIAL4 NOT NULL,
    l_course_module_lesson_id                          INTEGER,
    h_stream_id                                        INTEGER,
    CONSTRAINT l_course_module_lesson_stream_pkey      PRIMARY KEY (l_course_module_lesson_stream_id),
    CONSTRAINT fk_l_course_module_lesson
        FOREIGN KEY(l_course_module_lesson_id)
            REFERENCES l_courses_modules_lessons(l_course_module_lesson_id),
    CONSTRAINT fk_h_stream
        FOREIGN KEY(h_stream_id)
            REFERENCES h_streams(h_stream_id)
);

create TABLE IF NOT EXISTS s_courses_modules_lessons_streams
(
    s_course_module_lesson_stream_id                   SERIAL4 NOT NULL,
    l_course_module_lesson_stream_id                   INTEGER,
    s_course_module_lesson_stream_order_in_stream      INTEGER,
    CONSTRAINT s_course_module_lesson_stream_pkey      PRIMARY KEY (s_course_module_lesson_stream_id),
    CONSTRAINT fk_l_course_module_lesson_stream
        FOREIGN KEY(l_course_module_lesson_stream_id)
            REFERENCES l_courses_modules_lessons_streams(l_course_module_lesson_stream_id)
);
