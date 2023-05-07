CREATE TABLE IF NOT EXISTS clickhouse.dm_courses_modules_lessons_streams
(
    dm_course_module_lesson_stream_uuid      UUID DEFAULT generateUUIDv4(),

    h_course_title                           String,
    s_course_icon_url                        String,
    s_course_is_auto_course_enroll           Bool,
    s_course_is_demo_enroll                  Bool,
    s_course_created_at                      Nullable(DateTime),
    s_course_updated_at                      Nullable(DateTime),
    s_course_deleted_at                      Nullable(DateTime),

    h_module_title                           String,
    l_module_order_in_stream                 Int256,
    s_module_created_at                      Nullable(DateTime),
    s_module_updated_at                      Nullable(DateTime),
    s_module_deleted_at                      Nullable(DateTime),

    h_lesson_title                           String,
    s_lesson_description                     String,
    s_lesson_teacher_id                      Int256,
    s_lesson_start_at                        Nullable(DateTime),
    s_lesson_end_at                          Nullable(DateTime),
    s_lesson_homework_url                    String,
    s_lesson_online_lesson_join_url          String,
    s_lesson_online_lesson_recording_url     String,
    s_lesson_deleted_at                      Nullable(DateTime),

    h_stream_name                            String,
    s_stream_is_open                         Bool,
    s_stream_homework_deadline_days          Int256,
    s_stream_start_at                        Nullable(DateTime),
    s_stream_end_at                          Nullable(DateTime),
    s_stream_created_at                      Nullable(DateTime),
    s_stream_updated_at                      Nullable(DateTime),
    s_stream_deleted_at                      Nullable(DateTime),

    dm_course_module_lesson_stream_load_ts   DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY dm_course_module_lesson_stream_load_ts;