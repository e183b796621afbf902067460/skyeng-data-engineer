from airflow.decorators import task, dag
from airflow.exceptions import AirflowSkipException
from airflow.utils.trigger_rule import TriggerRule

import pendulum
import datetime


@task()
def e_from_pg_datasource() -> dict:
    import pandas as pd
    import logging
    from resources.datasource import pg_datasource

    Q = '''
        SELECT
            course.title AS h_course_title,
            TO_CHAR(course.created_at, 'YYYY-MM-DD HH24:MI:SS') AS s_course_created_at,
            TO_CHAR(course.updated_at, 'YYYY-MM-DD HH24:MI:SS') AS s_course_updated_at,
            TO_CHAR(course.deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_course_deleted_at,
            course.icon_url AS s_course_icon_url,
            course.is_auto_course_enroll AS s_course_is_auto_course_enroll,
            course.is_demo_enroll AS s_course_is_demo_enroll,
            stream.name AS h_stream_name,
            stream.is_open AS s_stream_is_open,
            stream.homework_deadline_days AS s_stream_homework_deadline_days,
            TO_CHAR(stream.start_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_start_at,
            TO_CHAR(stream.end_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_end_at,
            TO_CHAR(stream.created_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_created_at,
            TO_CHAR(stream.updated_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_updated_at,
            TO_CHAR(stream.deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_deleted_at,
            stream_module.title AS h_module_title,
            stream_module.order_in_stream AS l_module_order_in_stream,
            TO_CHAR(stream_module.created_at, 'YYYY-MM-DD HH24:MI:SS') AS s_module_created_at,
            TO_CHAR(stream_module.updated_at, 'YYYY-MM-DD HH24:MI:SS') AS s_module_updated_at,
            TO_CHAR(stream_module.deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_module_deleted_at,
            stream_module_lesson.title AS h_lesson_title,
            stream_module_lesson.description AS s_lesson_description,
            TO_CHAR(stream_module_lesson.start_at, 'YYYY-MM-DD HH24:MI:SS') AS s_lesson_start_at,
            TO_CHAR(stream_module_lesson.end_at, 'YYYY-MM-DD HH24:MI:SS') AS s_lesson_end_at,
            stream_module_lesson.homework_url AS s_lesson_homework_url,
            stream_module_lesson.teacher_id AS s_lesson_teacher_id,
            stream_module_lesson.online_lesson_join_url AS s_lesson_online_lesson_join_url,
            stream_module_lesson.online_lesson_recording_url AS s_lesson_online_lesson_recording_url,
            TO_CHAR(stream_module_lesson.deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_lesson_deleted_at
        FROM
            course
        LEFT JOIN
            stream ON course.id = stream.course_id
        LEFT JOIN
            stream_module ON stream.id = stream_module.stream_id
        LEFT JOIN
            stream_module_lesson ON stream_module.id = stream_module_lesson.stream_module_id
    '''
    df = pd.read_sql(sql=Q, con=pg_datasource().get_engine()).drop_duplicates()
    logging.info(f'Current shape of dataframe is {df.shape}')
    return df.to_dict(orient='list')


@task()
def e_from_pg_datawarehouse() -> dict:
    import pandas as pd
    import logging
    from resources.datawarehouse import pg_datawarehouse

    Q = '''
        SELECT
            h_course_title,
            TO_CHAR(s_course_created_at, 'YYYY-MM-DD HH24:MI:SS') AS s_course_created_at,
            TO_CHAR(s_course_updated_at, 'YYYY-MM-DD HH24:MI:SS') AS s_course_updated_at,
            TO_CHAR(s_course_deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_course_deleted_at,
            s_course_icon_url,
            s_course_is_auto_course_enroll,
            s_course_is_demo_enroll,
            h_stream_name,
            s_stream_is_open,
            s_stream_homework_deadline_days,
            TO_CHAR(s_stream_start_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_start_at,
            TO_CHAR(s_stream_end_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_end_at,
            TO_CHAR(s_stream_created_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_created_at,
            TO_CHAR(s_stream_updated_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_updated_at,
            TO_CHAR(s_stream_deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_stream_deleted_at,
            h_module_title,
            l_module_order_in_stream,
            TO_CHAR(s_module_created_at, 'YYYY-MM-DD HH24:MI:SS') AS s_module_created_at,
            TO_CHAR(s_module_updated_at, 'YYYY-MM-DD HH24:MI:SS') AS s_module_updated_at,
            TO_CHAR(s_module_deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_module_deleted_at,
            h_lesson_title,
            s_lesson_description,
            TO_CHAR(s_lesson_start_at, 'YYYY-MM-DD HH24:MI:SS') AS s_lesson_start_at,
            TO_CHAR(s_lesson_end_at, 'YYYY-MM-DD HH24:MI:SS') AS s_lesson_end_at,
            s_lesson_homework_url,
            s_lesson_teacher_id,
            s_lesson_online_lesson_join_url,
            s_lesson_online_lesson_recording_url,
            TO_CHAR(s_lesson_deleted_at, 'YYYY-MM-DD HH24:MI:SS') AS s_lesson_deleted_at
        FROM
            l_courses_modules_lessons_streams
        LEFT JOIN
            h_streams USING(h_stream_id)
        LEFT JOIN
            s_streams USING(h_stream_id)
        LEFT JOIN
            h_courses USING(h_course_id)
        LEFT JOIN
            s_courses USING(h_course_id)
        LEFT JOIN
            h_modules USING(h_module_id)
        LEFT JOIN
            s_modules USING(h_module_id)
        LEFT JOIN
            h_lessons USING(h_lesson_id)
        LEFT JOIN
            s_lessons USING(h_lesson_id)
    '''
    df = pd.read_sql(sql=Q, con=pg_datawarehouse().get_engine()).drop_duplicates()
    logging.info(f'Current shape of dataframe is {df.shape}')
    return df.to_dict(orient='list')


@task()
def t_find_new_rows(df_main_to_compare: dict, df_slave_to_compare: dict) -> dict:
    import pandas as pd

    df_main_to_compare, df_slave_to_compare = pd.DataFrame.from_dict(df_main_to_compare).drop_duplicates(), pd.DataFrame.from_dict(df_slave_to_compare).drop_duplicates()

    df_merge: pd.DataFrame = df_main_to_compare.merge(
        df_slave_to_compare,
        on=df_main_to_compare.columns.to_list(),
        how='left',
        indicator=True
    )
    df_merge: pd.DataFrame = df_merge[df_merge['_merge'] == 'left_only']
    return df_merge.to_dict(orient='list')


@task()
def l_update_hubs(df_with_new_rows: dict, h_table_name: str) -> None:
    import pandas as pd
    from resources.datawarehouse import pg_datawarehouse

    dwh = pg_datawarehouse()
    h_record_source = 'pg_datasource'

    df_with_new_rows: pd.DataFrame = pd.DataFrame.from_dict(df_with_new_rows)

    if h_table_name == dwh.H_COURSES_TABLE:
        df_with_new_rows[dwh.H_COURSE_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows[[dwh.H_COURSE_TITLE_COLUMN, dwh.H_COURSE_RECORD_SOURCE_COLUMN]].drop_duplicates()

    if h_table_name == dwh.H_MODULES_TABLE:
        df_with_new_rows[dwh.H_MODULE_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows[[dwh.H_MODULE_TITLE_COLUMN, dwh.H_MODULE_RECORD_SOURCE_COLUMN]].drop_duplicates()

    if h_table_name == dwh.H_LESSONS_TABLE:
        df_with_new_rows[dwh.H_LESSON_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows[[dwh.H_LESSON_TITLE_COLUMN, dwh.H_LESSON_RECORD_SOURCE_COLUMN]].drop_duplicates()

    if h_table_name == dwh.H_STREAMS_TABLE:
        df_with_new_rows[dwh.H_STREAM_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows[[dwh.H_STREAM_NAME_COLUMN, dwh.H_STREAM_RECORD_SOURCE_COLUMN]].drop_duplicates()

    df_with_new_rows.to_sql(name=h_table_name, con=dwh.get_engine(), if_exists='append', index=False)


@task()
def e_hubs_pk_from_datawarehouse(df_with_new_rows: dict, h_table_name: str) -> dict:
    import pandas as pd
    from resources.datawarehouse import pg_datawarehouse

    dwh = pg_datawarehouse()
    df_with_new_rows: pd.DataFrame = pd.DataFrame.from_dict(df_with_new_rows)

    # if there is no new or updated rows
    if df_with_new_rows.empty:
        raise AirflowSkipException

    Q = f'''
        SELECT
            {{}},
            {{}} AS business_key
        FROM
            {h_table_name}
        WHERE
            {{}} IN ({{}})
    '''

    if h_table_name == dwh.H_COURSES_TABLE:
        values = df_with_new_rows[dwh.H_COURSE_TITLE_COLUMN].drop_duplicates().tolist()
        prepared_values = ', '.join(f"'{value}'" for value in values)

        Q = Q.format(dwh.H_COURSE_ID_COLUMN, dwh.H_COURSE_TITLE_COLUMN, dwh.H_COURSE_TITLE_COLUMN, prepared_values)

    if h_table_name == dwh.H_MODULES_TABLE:
        values = df_with_new_rows[dwh.H_MODULE_TITLE_COLUMN].drop_duplicates().tolist()
        prepared_values = ', '.join(f"'{value}'" for value in values)

        Q = Q.format(dwh.H_MODULE_ID_COLUMN, dwh.H_MODULE_TITLE_COLUMN, dwh.H_MODULE_TITLE_COLUMN, prepared_values)

    if h_table_name == dwh.H_LESSONS_TABLE:
        values = df_with_new_rows[dwh.H_LESSON_TITLE_COLUMN].drop_duplicates().tolist()
        prepared_values = ', '.join(f"'{value}'" for value in values)

        Q = Q.format(dwh.H_LESSON_ID_COLUMN, dwh.H_LESSON_TITLE_COLUMN, dwh.H_LESSON_TITLE_COLUMN, prepared_values)

    if h_table_name == dwh.H_STREAMS_TABLE:
        values = df_with_new_rows[dwh.H_STREAM_NAME_COLUMN].drop_duplicates().tolist()
        prepared_values = ', '.join(f"'{value}'" for value in values)

        Q = Q.format(dwh.H_STREAM_ID_COLUMN, dwh.H_STREAM_NAME_COLUMN, dwh.H_STREAM_NAME_COLUMN, prepared_values)

    df = pd.read_sql(sql=Q, con=dwh.get_engine()).drop_duplicates(subset='business_key')
    return df.to_dict(orient='list')


@task(trigger_rule=TriggerRule.ALL_SUCCESS)
def l_update_satellites(df_with_new_rows: dict, df_with_hubs_pk: dict, s_table_name: str) -> None:
    import pandas as pd
    from resources.datawarehouse import pg_datawarehouse

    dwh = pg_datawarehouse()
    h_record_source = 'pg_datasource'

    df_with_new_rows, df_with_hubs_pk = pd.DataFrame.from_dict(df_with_new_rows), pd.DataFrame.from_dict(df_with_hubs_pk)

    if s_table_name == dwh.S_COURSES_TABLE:
        df_with_new_rows[dwh.S_COURSE_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows.merge(
            df_with_hubs_pk,
            left_on=dwh.H_COURSE_TITLE_COLUMN,
            right_on='business_key',
            how='left'
        )
        df_with_new_rows = df_with_new_rows[
            [
                dwh.H_COURSE_ID_COLUMN, dwh.S_COURSE_RECORD_SOURCE_COLUMN,
                dwh.S_COURSE_ICON_URL_COLUMN,
                dwh.S_COURSE_IS_AUTO_COURSE_ENROLL_COLUMN, dwh.S_COURSE_IS_DEMO_ENROLL_COLUMN,
                dwh.S_COURSE_CREATED_AT_COLUMN, dwh.S_COURSE_UPDATED_AT_COLUMN, dwh.S_COURSE_DELETED_AT_COLUMN
            ]
        ].drop_duplicates()

    if s_table_name == dwh.S_MODULES_TABLE:
        df_with_new_rows[dwh.S_MODULE_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows.merge(
            df_with_hubs_pk,
            left_on=dwh.H_MODULE_TITLE_COLUMN,
            right_on='business_key',
            how='left'
        )
        df_with_new_rows = df_with_new_rows[
            [
                dwh.H_MODULE_ID_COLUMN, dwh.S_MODULE_RECORD_SOURCE_COLUMN,
                dwh.S_MODULE_CREATED_AT_COLUMN, dwh.S_MODULE_UPDATED_AT_COLUMN, dwh.S_MODULE_DELETED_AT_COLUMN
            ]
        ].drop_duplicates()

    if s_table_name == dwh.S_LESSONS_TABLE:
        df_with_new_rows[dwh.S_LESSON_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows.merge(
            df_with_hubs_pk,
            left_on=dwh.H_LESSON_TITLE_COLUMN,
            right_on='business_key',
            how='left'
        )
        df_with_new_rows = df_with_new_rows[
            [
                dwh.H_LESSON_ID_COLUMN, dwh.S_LESSON_RECORD_SOURCE_COLUMN,
                dwh.S_LESSON_DESCRIPTION_COLUMN, dwh.S_LESSON_TEACHER_ID_COLUMN,
                dwh.S_LESSON_START_AT_COLUMN, dwh.S_LESSON_END_AT_COLUMN,
                dwh.S_LESSON_HOMEWORK_URL_COLUMN,
                dwh.S_LESSON_ONLINE_LESSON_JOIN_URL_COLUMN, dwh.S_LESSON_ONLINE_LESSON_RECORDING_URL_COLUMN,
                dwh.S_LESSON_DELETED_AT_COLUMN
            ]
        ].drop_duplicates()

    if s_table_name == dwh.S_STREAMS_TABLE:
        df_with_new_rows[dwh.S_STREAM_RECORD_SOURCE_COLUMN] = h_record_source
        df_with_new_rows = df_with_new_rows.merge(
            df_with_hubs_pk,
            left_on=dwh.H_STREAM_NAME_COLUMN,
            right_on='business_key',
            how='left'
        )
        df_with_new_rows = df_with_new_rows[
            [
                dwh.H_STREAM_ID_COLUMN, dwh.S_STREAM_RECORD_SOURCE_COLUMN,
                dwh.S_STREAM_IS_OPEN_COLUMN, dwh.S_STREAM_HOMEWORK_DEADLINE_DAYS_COLUMN,
                dwh.S_STREAM_START_AT_COLUMN, dwh.S_STREAM_END_AT_COLUMN,
                dwh.S_STREAM_CREATED_AT_COLUMN, dwh.S_STREAM_UPDATED_AT_COLUMN, dwh.S_STREAM_DELETED_AT_COLUMN
            ]
        ].drop_duplicates()

    df_with_new_rows.to_sql(name=s_table_name, con=dwh.get_engine(), if_exists='append', index=False)


@task(trigger_rule=TriggerRule.ALL_SUCCESS)
def l_update_links(df_with_new_rows: dict, df_with_h_course_pk: dict, df_with_h_module_pk: dict, df_with_h_lesson_pk: dict, df_with_h_stream_pk: dict) -> None:
    import pandas as pd
    from resources.datawarehouse import pg_datawarehouse

    dwh = pg_datawarehouse()

    df_with_new_rows = pd.DataFrame.from_dict(df_with_new_rows)

    df_with_h_course_pk, df_with_h_module_pk = pd.DataFrame.from_dict(df_with_h_course_pk), pd.DataFrame.from_dict(df_with_h_module_pk)
    df_with_h_lesson_pk, df_with_h_stream_pk = pd.DataFrame.from_dict(df_with_h_lesson_pk), pd.DataFrame.from_dict(df_with_h_stream_pk)

    df_with_new_rows = df_with_new_rows\
        .merge(
            df_with_h_course_pk,
            left_on=dwh.H_COURSE_TITLE_COLUMN,
            right_on='business_key',
            how='left'
        )\
        .merge(
            df_with_h_module_pk,
            left_on=dwh.H_MODULE_TITLE_COLUMN,
            right_on='business_key',
            how='left'
        )\
        .merge(
            df_with_h_lesson_pk,
            left_on=dwh.H_LESSON_TITLE_COLUMN,
            right_on='business_key',
            how='left'
        )\
        .merge(
            df_with_h_stream_pk,
            left_on=dwh.H_STREAM_NAME_COLUMN,
            right_on='business_key',
            how='left'
        )

    df_with_new_rows = df_with_new_rows[
        [
            dwh.H_COURSE_ID_COLUMN,
            dwh.H_MODULE_ID_COLUMN,
            dwh.H_LESSON_ID_COLUMN,
            dwh.H_STREAM_ID_COLUMN,
            dwh.L_MODULE_ORDER_IN_STREAM_COLUMN

        ]
    ].drop_duplicates()

    df_with_new_rows.to_sql(name='l_courses_modules_lessons_streams', con=dwh.get_engine(), if_exists='append', index=False)


@dag(
    dag_id='to_datawarehouse',
    start_date=pendulum.datetime(2023, 1, 1, tz="UTC"),
    schedule_interval='*/10 * * * *',
    catchup=False,
    max_active_runs=1,
    dagrun_timeout=datetime.timedelta(minutes=10)
)
def to_datawarehouse():
    from resources.datawarehouse import PgDataWarehouseResource

    df_from_datasource = e_from_pg_datasource()
    df_from_datawarehouse = e_from_pg_datawarehouse()
    df_with_new_rows = t_find_new_rows(df_main_to_compare=df_from_datasource, df_slave_to_compare=df_from_datawarehouse)

    update_h_course = l_update_hubs.override(task_id='l_update_h_course')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_COURSES_TABLE)
    update_h_module = l_update_hubs.override(task_id='l_update_h_module')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_MODULES_TABLE)
    update_h_lesson = l_update_hubs.override(task_id='l_update_h_lesson')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_LESSONS_TABLE)
    update_h_stream = l_update_hubs.override(task_id='l_update_h_stream')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_STREAMS_TABLE)

    df_with_h_course_pk = e_hubs_pk_from_datawarehouse.override(task_id='e_h_course_pk_from_datawarehouse')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_COURSES_TABLE)
    df_with_h_module_pk = e_hubs_pk_from_datawarehouse.override(task_id='e_h_module_pk_from_datawarehouse')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_MODULES_TABLE)
    df_with_h_lesson_pk = e_hubs_pk_from_datawarehouse.override(task_id='e_h_lesson_pk_from_datawarehouse')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_LESSONS_TABLE)
    df_with_h_stream_pk = e_hubs_pk_from_datawarehouse.override(task_id='e_h_stream_pk_from_datawarehouse')(df_with_new_rows=df_with_new_rows, h_table_name=PgDataWarehouseResource.H_STREAMS_TABLE)

    df_with_h_course_pk.set_upstream(update_h_course)
    df_with_h_module_pk.set_upstream(update_h_module)
    df_with_h_lesson_pk.set_upstream(update_h_lesson)
    df_with_h_stream_pk.set_upstream(update_h_stream)

    l_update_satellites.override(task_id='l_update_s_course')(df_with_new_rows=df_with_new_rows, s_table_name=PgDataWarehouseResource.S_COURSES_TABLE, df_with_hubs_pk=df_with_h_course_pk)
    l_update_satellites.override(task_id='l_update_s_module')(df_with_new_rows=df_with_new_rows, s_table_name=PgDataWarehouseResource.S_MODULES_TABLE, df_with_hubs_pk=df_with_h_module_pk)
    l_update_satellites.override(task_id='l_update_s_lesson')(df_with_new_rows=df_with_new_rows, s_table_name=PgDataWarehouseResource.S_LESSONS_TABLE, df_with_hubs_pk=df_with_h_lesson_pk)
    l_update_satellites.override(task_id='l_update_s_stream')(df_with_new_rows=df_with_new_rows, s_table_name=PgDataWarehouseResource.S_STREAMS_TABLE, df_with_hubs_pk=df_with_h_stream_pk)

    l_update_links(
        df_with_new_rows=df_with_new_rows,
        df_with_h_course_pk=df_with_h_course_pk,
        df_with_h_module_pk=df_with_h_module_pk,
        df_with_h_lesson_pk=df_with_h_lesson_pk,
        df_with_h_stream_pk=df_with_h_stream_pk
    )


to_datawarehouse_dag = to_datawarehouse()
