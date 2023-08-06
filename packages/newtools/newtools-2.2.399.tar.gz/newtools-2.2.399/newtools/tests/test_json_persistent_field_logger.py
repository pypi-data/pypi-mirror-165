import datetime
import io
import json
import logging
import os
import unittest

from newtools.log.json_persistent_field_logger import JSONLogger, CLASS_NAME, ERROR_MESSAGE, \
    TOTAL_EXEC_TIME_IN_SECS_KEY, START_TIME_KEY, END_TIME_KEY, APPLICATION_NAME_KEY

ERROR_MESSAGE_CONSTANT = 'This is a error message.'
WARN_MESSAGE_CONSTANT = 'This is a warning message.'


class JSONLoggerTest(unittest.TestCase):

    def setUp(self):
        self.stream = io.StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.json_logger = JSONLogger('TestJsonLogger')
        self.handler.setFormatter(self.json_logger.json_formatter)
        self.json_logger._log_instance.addHandler(self.handler)

    def load_logs_from_stream(self):
        log_messages = []
        self.handler.flush()
        self.stream.seek(0)
        for stream_data in self.stream.readlines():
            log_info = json.loads(stream_data.replace('\n', ''))
            log_info.pop('time')
            log_messages.append(log_info)
        return log_messages

    def test_debug(self):
        debug_message = "Debug Logs appear only in case of explicit Debug logs enabled."
        self.json_logger.debug(debug_message)
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 0)
        self.assertTrue(debug_message not in log_messages)

    def test_info(self):
        log_message = 'This is a info message.'
        self.json_logger.info(log_message)
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)
        self.assertEqual(log_messages[0]['message'], log_message)

    def test_error(self):
        self.json_logger.error(ERROR_MESSAGE_CONSTANT)
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)
        self.assertEqual(log_messages[0]['message'], ERROR_MESSAGE_CONSTANT)

    def test_error_with_no_persistent_fields(self):
        self.json_logger.add_persistent_field('Miss_Persistent_Field', 'This is Persistent Field Value missing in Log')
        self.json_logger.remove_all_persistent_fields()
        self.json_logger.error(ERROR_MESSAGE_CONSTANT)
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)
        self.assertEqual(log_messages[0]['message'], ERROR_MESSAGE_CONSTANT)
        self.assertIsNone(log_messages[0].get('Warn_Persistent_Field', None))

    def test_error_with_exception(self):
        exception_message = 'Exception Message'
        self.json_logger.error(ERROR_MESSAGE_CONSTANT, exception_object=Exception(exception_message))
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)
        self.assertEqual(log_messages[0]['message'], ERROR_MESSAGE_CONSTANT)
        self.assertEqual(log_messages[0][CLASS_NAME], 'Exception')
        self.assertEqual(log_messages[0][ERROR_MESSAGE], exception_message)

    def test_warning(self):
        self.json_logger.add_persistent_field('Warn_Persistent_Field', 'This is Persistent Field Value in Warning Log')
        self.json_logger.warning(WARN_MESSAGE_CONSTANT)
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)
        self.assertEqual(log_messages[0]['message'], WARN_MESSAGE_CONSTANT)
        self.assertEqual(log_messages[0]['Warn_Persistent_Field'], 'This is Persistent Field Value in Warning Log')

    def test_warning_with_exception(self):
        exception_message = 'Exception Message in warning'

        start_time = datetime.datetime.utcnow()
        end_time = datetime.datetime.utcnow()
        self.json_logger.generate_time_spent(start_time, end_time)

        self.json_logger.warning(WARN_MESSAGE_CONSTANT, exception_object=Exception(exception_message))
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)
        self.assertEqual(log_messages[0]['message'], WARN_MESSAGE_CONSTANT)
        self.assertEqual(log_messages[0][CLASS_NAME], 'Exception')
        self.assertEqual(log_messages[0][ERROR_MESSAGE], exception_message)

        self.assertEqual(log_messages[0][START_TIME_KEY], str(start_time))
        self.assertEqual(log_messages[0][END_TIME_KEY], str(end_time))
        self.assertIsNotNone(log_messages[0][TOTAL_EXEC_TIME_IN_SECS_KEY])

    def test_warning_with_persistent_field(self):
        log_warn_message = 'This is a warning message.'
        self.json_logger.warning(log_warn_message,
                                 excess_persistent_dict={'Persistent_Field': 'This is Persistent Field Value'})
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)
        self.assertEqual(log_messages[0]['message'], log_warn_message)
        self.assertEqual(log_messages[0]['Persistent_Field'], 'This is Persistent Field Value')

        self.json_logger.remove_persistent_field('Persistent_Field')
        # Default persistent key is application name.
        self.assertTrue(len(self.json_logger._persistent_fields) == 1)

    def test_remove_application_name_from_log(self):
        self.json_logger.info('Test message to try to remove application name')
        log_messages = self.load_logs_from_stream()
        self.assertTrue(len(log_messages) == 1)

        self.json_logger.remove_persistent_field(APPLICATION_NAME_KEY)
        # Application name can't be removed from any of the logs
        self.assertIsNotNone(self.json_logger._persistent_fields[APPLICATION_NAME_KEY])

    def test_default(self):
        json_log_file = None
        file_path = f'{os.getcwd()}/test_file.log'
        try:
            json_logger = JSONLogger('Test initialization', log_file_path=file_path)

            sample_info_message = 'Test file logger'
            json_logger.info(sample_info_message)

            json_log_file = open(file_path)
            json_log = json.load(json_log_file)

            self.assertEqual(json_log['message'], 'Test file logger')
        except Exception:
            pass
        finally:
            if json_log_file is not None:
                json_log_file.close()
                os.remove(file_path)
