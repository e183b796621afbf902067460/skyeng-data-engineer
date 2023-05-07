import os
from urllib.parse import quote_plus

from resources.datasource import PgDataSourceResource


class PgDataWarehouseResource(PgDataSourceResource):

    # db creds
    DB_ADDRESS = os.getenv('PG_DATAWAREHOUSE_HOST', None)
    DB_PORT = os.getenv('PG_DATAWAREHOUSE_PORT', None)
    DB_USER = os.getenv('PG_DATAWAREHOUSE_USER', None)
    DB_PASSWORD = quote_plus(os.getenv('PG_DATAWAREHOUSE_PASSWORD', None))
    DB_NAME = os.getenv('PG_DATAWAREHOUSE_DB', None)

    DB_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_ADDRESS}:{DB_PORT}/{DB_NAME}'

    # entities info hubs
    H_COURSES_TABLE, H_COURSE_RECORD_SOURCE_COLUMN, H_COURSE_TITLE_COLUMN, H_COURSE_ID_COLUMN = 'h_courses', 'h_course_record_source', 'h_course_title', 'h_course_id'
    H_MODULES_TABLE, H_MODULE_RECORD_SOURCE_COLUMN, H_MODULE_TITLE_COLUMN, H_MODULE_ID_COLUMN = 'h_modules', 'h_module_record_source', 'h_module_title', 'h_module_id'
    H_LESSONS_TABLE, H_LESSON_RECORD_SOURCE_COLUMN, H_LESSON_TITLE_COLUMN, H_LESSON_ID_COLUMN = 'h_lessons', 'h_lesson_record_source', 'h_lesson_title', 'h_lesson_id'
    H_STREAMS_TABLE, H_STREAM_RECORD_SOURCE_COLUMN, H_STREAM_NAME_COLUMN, H_STREAM_ID_COLUMN = 'h_streams', 'h_stream_record_source', 'h_stream_name', 'h_stream_id'

    # entities info satellites
    S_COURSES_TABLE, S_COURSE_RECORD_SOURCE_COLUMN, S_COURSE_ICON_URL_COLUMN, S_COURSE_IS_AUTO_COURSE_ENROLL_COLUMN, S_COURSE_IS_DEMO_ENROLL_COLUMN = 's_courses', 's_course_record_source', 's_course_icon_url', 's_course_is_auto_course_enroll', 's_course_is_demo_enroll'
    S_COURSE_CREATED_AT_COLUMN, S_COURSE_UPDATED_AT_COLUMN, S_COURSE_DELETED_AT_COLUMN = 's_course_created_at', 's_course_updated_at', 's_course_deleted_at'

    S_MODULES_TABLE, S_MODULE_RECORD_SOURCE_COLUMN = 's_modules', 's_module_record_source'
    S_MODULE_CREATED_AT_COLUMN, S_MODULE_UPDATED_AT_COLUMN, S_MODULE_DELETED_AT_COLUMN = 's_module_created_at', 's_module_updated_at', 's_module_deleted_at'

    S_LESSONS_TABLE, S_LESSON_RECORD_SOURCE_COLUMN = 's_lessons', 's_lesson_record_source'
    S_LESSON_DESCRIPTION_COLUMN, S_LESSON_TEACHER_ID_COLUMN = 's_lesson_description', 's_lesson_teacher_id'
    S_LESSON_START_AT_COLUMN, S_LESSON_END_AT_COLUMN = 's_lesson_start_at', 's_lesson_end_at'
    S_LESSON_HOMEWORK_URL_COLUMN = 's_lesson_homework_url'
    S_LESSON_ONLINE_LESSON_JOIN_URL_COLUMN, S_LESSON_ONLINE_LESSON_RECORDING_URL_COLUMN = 's_lesson_online_lesson_join_url', 's_lesson_online_lesson_recording_url'
    S_LESSON_DELETED_AT_COLUMN = 's_lesson_deleted_at'

    S_STREAMS_TABLE, S_STREAM_RECORD_SOURCE_COLUMN = 's_streams', 's_stream_record_source'
    S_STREAM_IS_OPEN_COLUMN, S_STREAM_HOMEWORK_DEADLINE_DAYS_COLUMN = 's_stream_is_open', 's_stream_homework_deadline_days'
    S_STREAM_START_AT_COLUMN, S_STREAM_END_AT_COLUMN = 's_stream_start_at', 's_stream_end_at'
    S_STREAM_CREATED_AT_COLUMN, S_STREAM_UPDATED_AT_COLUMN, S_STREAM_DELETED_AT_COLUMN = 's_stream_created_at', 's_stream_updated_at', 's_stream_deleted_at'

    # entities info links
    L_MODULE_ORDER_IN_STREAM_COLUMN = 'l_module_order_in_stream'


def pg_datawarehouse():
    return PgDataWarehouseResource()
