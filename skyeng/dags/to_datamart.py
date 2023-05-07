import pandas as pd
from airflow.decorators import task, dag

import pendulum
import datetime


@task()
def e_from_ch_datamart() -> dict:
    import logging
    from resources.datamart import ch_datamart
    from resources.datawarehouse import PgDataWarehouseResource as info

    ch = ch_datamart()

    Q = '''
        SELECT
            h_course_title,
            if(isNull(s_course_created_at), NULL, CAST(s_course_created_at, 'String')) AS s_course_created_at,
            if(isNull(s_course_updated_at), NULL, CAST(s_course_updated_at, 'String')) AS s_course_updated_at,
            if(isNull(s_course_deleted_at), NULL, CAST(s_course_deleted_at, 'String')) AS s_course_deleted_at,
            s_course_icon_url,
            s_course_is_auto_course_enroll,
            s_course_is_demo_enroll,
            h_stream_name,
            s_stream_is_open,
            s_stream_homework_deadline_days,
            if(isNull(s_stream_start_at), NULL, CAST(s_stream_start_at, 'String')) AS s_stream_start_at,
            if(isNull(s_stream_end_at), NULL, CAST(s_stream_end_at, 'String')) AS s_stream_end_at,
            if(isNull(s_stream_created_at), NULL, CAST(s_stream_created_at, 'String')) AS s_stream_created_at,
            if(isNull(s_stream_updated_at), NULL, CAST(s_stream_updated_at, 'String')) AS s_stream_updated_at,
            if(isNull(s_stream_deleted_at), NULL, CAST(s_stream_deleted_at, 'String')) AS s_stream_deleted_at,
            h_module_title,
            l_module_order_in_stream,
            if(isNull(s_module_created_at), NULL, CAST(s_module_created_at, 'String')) AS s_module_created_at,
            if(isNull(s_module_updated_at), NULL, CAST(s_module_updated_at, 'String')) AS s_module_updated_at,
            if(isNull(s_module_deleted_at), NULL, CAST(s_module_deleted_at, 'String')) AS s_module_deleted_at,
            h_lesson_title,
            s_lesson_description,
            if(isNull(s_lesson_start_at), NULL, CAST(s_lesson_start_at, 'String')) AS s_lesson_start_at,
            if(isNull(s_lesson_end_at), NULL, CAST(s_lesson_end_at, 'String')) AS s_lesson_end_at,
            s_lesson_homework_url,
            s_lesson_teacher_id,
            s_lesson_online_lesson_join_url,
            s_lesson_online_lesson_recording_url,
            if(isNull(s_lesson_deleted_at), NULL, CAST(s_lesson_deleted_at, 'String')) AS s_lesson_deleted_at
        FROM
            dm_courses_modules_lessons_streams
    '''
    map_ = {'true': True, 'false': False}

    df = pd.read_sql_query(sql=Q, con=ch.get_engine()).drop_duplicates()

    df[info.S_COURSE_IS_AUTO_COURSE_ENROLL_COLUMN] = df[info.S_COURSE_IS_AUTO_COURSE_ENROLL_COLUMN].map(map_)
    df[info.S_COURSE_IS_DEMO_ENROLL_COLUMN] = df[info.S_COURSE_IS_DEMO_ENROLL_COLUMN].map(map_)
    df[info.S_STREAM_IS_OPEN_COLUMN] = df[info.S_STREAM_IS_OPEN_COLUMN].map(map_)

    logging.info(f'Current shape of dataframe is {df.shape}')
    return df.to_dict(orient='list')


@task()
def l_update_datamart(df_with_new_rows: dict) -> None:
    import pandas as pd
    from resources.datamart import ch_datamart
    from resources.datawarehouse import PgDataWarehouseResource as info

    dm = ch_datamart()

    df_with_new_rows = pd.DataFrame.from_dict(df_with_new_rows).drop_duplicates()
    for column_name in [
        info.S_COURSE_CREATED_AT_COLUMN, info.S_COURSE_UPDATED_AT_COLUMN, info.S_COURSE_DELETED_AT_COLUMN,
        info.S_MODULE_CREATED_AT_COLUMN, info.S_MODULE_UPDATED_AT_COLUMN, info.S_MODULE_DELETED_AT_COLUMN,
        info.S_LESSON_START_AT_COLUMN, info.S_LESSON_END_AT_COLUMN, info.S_LESSON_DELETED_AT_COLUMN,
        info.S_STREAM_START_AT_COLUMN, info.S_STREAM_END_AT_COLUMN,
        info.S_STREAM_CREATED_AT_COLUMN, info.S_STREAM_UPDATED_AT_COLUMN, info.S_STREAM_DELETED_AT_COLUMN
    ]:
        df_with_new_rows[column_name] = pd.to_datetime(df_with_new_rows[column_name])

    df_with_new_rows = df_with_new_rows[
        [
            info.H_COURSE_TITLE_COLUMN, info.S_COURSE_ICON_URL_COLUMN,
            info.S_COURSE_IS_AUTO_COURSE_ENROLL_COLUMN, info.S_COURSE_IS_DEMO_ENROLL_COLUMN,
            info.S_COURSE_CREATED_AT_COLUMN, info.S_COURSE_UPDATED_AT_COLUMN, info.S_COURSE_DELETED_AT_COLUMN,
            info.H_MODULE_TITLE_COLUMN, info.L_MODULE_ORDER_IN_STREAM_COLUMN,
            info.S_MODULE_CREATED_AT_COLUMN, info.S_MODULE_UPDATED_AT_COLUMN, info.S_MODULE_DELETED_AT_COLUMN,
            info.H_LESSON_TITLE_COLUMN, info.S_LESSON_DESCRIPTION_COLUMN,
            info.S_LESSON_TEACHER_ID_COLUMN, info.S_LESSON_START_AT_COLUMN, info.S_LESSON_END_AT_COLUMN,
            info.S_LESSON_HOMEWORK_URL_COLUMN, info.S_LESSON_ONLINE_LESSON_JOIN_URL_COLUMN, info.S_LESSON_ONLINE_LESSON_RECORDING_URL_COLUMN,
            info.S_LESSON_DELETED_AT_COLUMN, info.H_STREAM_NAME_COLUMN, info.S_STREAM_IS_OPEN_COLUMN,
            info.S_STREAM_HOMEWORK_DEADLINE_DAYS_COLUMN, info.S_STREAM_START_AT_COLUMN, info.S_STREAM_END_AT_COLUMN,
            info.S_STREAM_CREATED_AT_COLUMN, info.S_STREAM_UPDATED_AT_COLUMN, info.S_STREAM_DELETED_AT_COLUMN
        ]
    ].drop_duplicates()
    df_with_new_rows.to_sql(name='dm_courses_modules_lessons_streams', con=dm.get_engine(), if_exists='append', index=False)


@dag(
    dag_id='to_datamart',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval='*/10 * * * *',
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=datetime.timedelta(minutes=10)
)
def to_datamart():
    from dags.to_datawarehouse import e_from_pg_datawarehouse
    from dags.to_datawarehouse import t_find_new_rows

    df_from_datawarehouse = e_from_pg_datawarehouse()
    df_from_datamart = e_from_ch_datamart()
    df_with_new_rows = t_find_new_rows(df_main_to_compare=df_from_datawarehouse, df_slave_to_compare=df_from_datamart)

    l_update_datamart(df_with_new_rows=df_with_new_rows)


to_datamart_dag = to_datamart()
