from airflow.decorators import task, dag

import pendulum
import datetime


@task()
def e_from_pg_datasource():
    import pandas as pd
    import logging
    from resources.datasource import PgDataSourceResource

    Q = '''
        SELECT
            course.title AS h_course_title,
            course.created_at AS s_course_created_at,
            course.updated_at AS s_course_updated_at,
            course.deleted_at AS s_course_deleted_at,
            course.icon_url AS s_course_icon_url,
            course.is_auto_course_enroll AS s_course_is_auto_course_enroll,
            course.is_demo_enroll AS s_course_is_demo_enroll,
            stream.name AS h_stream_name,
            stream.is_open AS s_stream_is_open,
            stream.homework_deadline_days AS s_stream_homework_deadline_days,
            stream.start_at AS s_stream_start_at,
            stream.end_at AS s_stream_end_at,
            stream.created_at AS s_stream_created_at,
            stream.updated_at AS s_stream_updated_at,
            stream.deleted_at AS s_stream_deleted_at,
            stream_module.title AS h_module_title,
            stream_module.order_in_stream AS s_course_module_lesson_stream_order_in_stream,
            stream_module.created_at AS s_module_created_at,
            stream_module.updated_at AS s_module_updated_at,
            stream_module.deleted_at AS s_module_deleted_at,
            stream_module_lesson.title AS h_lesson_title,
            stream_module_lesson.description AS s_lesson_description,
            stream_module_lesson.start_at AS s_lesson_start_at,
            stream_module_lesson.end_at AS s_lesson_end_at,
            stream_module_lesson.homework_url AS s_lesson_homework_url,
            stream_module_lesson.teacher_id AS s_lesson_teacher_id,
            stream_module_lesson.online_lesson_join_url AS s_lesson_online_lesson_join_url,
            stream_module_lesson.online_lesson_recording_url AS s_lesson_online_lesson_recording_url,
            stream_module_lesson.deleted_at AS s_lesson_deleted_at
        FROM
            course
        LEFT JOIN
            stream ON course.id = stream.course_id
        LEFT JOIN
            stream_module ON stream.id = stream_module.stream_id
        LEFT JOIN
            stream_module_lesson ON stream_module.id = stream_module_lesson.stream_module_id
    '''
    df = pd.read_sql(sql=Q, con=PgDataSourceResource.get_engine())
    logging.info(f'Current shape of dataframe is {df.shape}')
    return df


@task()
def e_from_pg_datawarehouse():
    import pandas as pd
    import logging
    from resources.datawarehouse import PgDataWarehouseResource

    Q = '''
        SELECT
            h_course_title,
            s_course_created_at,
            s_course_updated_at,
            s_course_deleted_at,
            s_course_icon_url,
            s_course_is_auto_course_enroll,
            s_course_is_demo_enroll,
            h_stream_name,
            s_stream_is_open,
            s_stream_homework_deadline_days,
            s_stream_start_at,
            s_stream_end_at,
            s_stream_created_at,
            s_stream_updated_at,
            s_stream_deleted_at,
            h_module_title,
            s_course_module_lesson_stream_order_in_stream,
            s_module_created_at,
            s_module_updated_at,
            s_module_deleted_at,
            h_lesson_title,
            s_lesson_description,
            s_lesson_start_at,
            s_lesson_end_at,
            s_lesson_homework_url,
            s_lesson_teacher_id,
            s_lesson_online_lesson_join_url,
            s_lesson_online_lesson_recording_url,
            s_lesson_deleted_at
        FROM
            l_courses_modules_lessons_streams
        LEFT JOIN
            h_streams USING(h_stream_id)
        LEFT JOIN
            s_streams USING(h_streams.h_stream_id)
        LEFT JOIN
            s_courses_modules_lessons_streams USING(l_course_module_lesson_stream_id)
        LEFT JOIN
            l_courses_modules_lessons USING(l_course_module_lesson_id)
        LEFT JOIN
            h_lessons USING(h_lesson_id)
        LEFT JOIN
            s_lessons USING(h_lessons.h_lesson_id)
        LEFT JOIN
            l_courses_modules USING(l_course_module_id)
        LEFT JOIN
            h_courses USING(h_course_id)
        LEFT JOIN
            s_courses USING(h_courses.h_course_id)
        LEFT JOIN
            h_modules USING(h_module_id)
        LEFT JOIN
            s_modules USING(h_modules.h_module_id)
    '''
    df = pd.read_sql(sql=Q, con=PgDataWarehouseResource.get_engine())
    logging.info(f'Current shape of dataframe is {df.shape}')
    return df


@task
def t_compare_df():
    ...


@dag(
    dag_id='to_datawarehouse',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval='*/10 * * * *',
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=datetime.timedelta(minutes=10)
)
def to_datawarehouse():
    df_from_datasource = e_from_pg_datasource()
    df_from_datawarehouse = e_from_pg_datawarehouse()