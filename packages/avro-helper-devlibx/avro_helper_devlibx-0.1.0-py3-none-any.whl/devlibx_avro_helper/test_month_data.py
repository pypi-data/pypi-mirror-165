import unittest
from datetime import datetime

from month_data import MonthDataAvroHelper


class TestingMonthDataAvroHelper(unittest.TestCase):

    def test_get_keys_for_month(self):
        date_time_str = '05/08/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        helper = MonthDataAvroHelper()
        results = helper.get_keys_for_month(date_time_obj)
        print(results)
        self.assertEqual(5, len(results))
        self.assertEqual("8-1", results[0])
        self.assertEqual("8-2", results[1])
        self.assertEqual("8-3", results[2])
        self.assertEqual("8-4", results[3])
        self.assertEqual("8-5", results[4])

    def test_get_keys_for_week(self):
        date_time_str = '05/08/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        helper = MonthDataAvroHelper()
        results = helper.get_keys_for_week(date_time_obj)
        print(results)
        self.assertEqual(7, len(results))
        self.assertEqual("7-30", results[0])
        self.assertEqual("7-31", results[1])
        self.assertEqual("8-1", results[2])
        self.assertEqual("8-2", results[3])
        self.assertEqual("8-3", results[4])
        self.assertEqual("8-4", results[5])
        self.assertEqual("8-5", results[6])

    def test_parsing(self):
        # Test 1 - from generateDataFor_test_parsing_Test_1
        base64Str = "AAICBjctNQIEAAAAAAAAAAAAAAI="
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        self.assertEqual(2, result["data"]["7-5"]["counter"], "It should be 2")

        # Test 2 - data from generateDataFor_test_parsing_Test_2
        base64Str = "AAIOCDYtMjkCAgAAAAAAAAAAAAY3LTECAgAAAAAAAAAAAAY3LTICAgAAAAAAAAAAAAg2LTMwAgIAAAAAAAAAAAAGNy0zAgIAAAAAAAAAAAAGNy00AgIAAAAAAAAAAAAGNy01AgoAAAAAAAAAAAAAAg=="
        result = helper.process(base64Str)
        print(result)
        self.assertEqual(1, result["data"]["7-1"]["counter"], "It should be 1")
        self.assertEqual(1, result["data"]["7-2"]["counter"], "It should be 1")
        self.assertEqual(1, result["data"]["7-3"]["counter"], "It should be 1")
        self.assertEqual(1, result["data"]["7-1"]["counter"], "It should be 1")
        self.assertEqual(5, result["data"]["7-5"]["counter"], "It should be 1")
        self.assertEqual(7, len(result["data"]), "It should be 7")

    def test_process_and_return_aggregation_for_month(self):
        # Test 1 - data from generateDataFor_test_parsing_Test_2
        base64Str = "AAIOCDYtMjkCAgAAAAAAAAAAAAY3LTECAgAAAAAAAAAAAAY3LTICAgAAAAAAAAAAAAg2LTMwAgIAAAAAAAAAAAAGNy0zAgIAAAAAAAAAAAAGNy00AgIAAAAAAAAAAAAGNy01AgoAAAAAAAAAAAAAAg=="
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 5, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

        # if you are looking for data for this month then use can use
        # helper.process_and_return_aggregation_for_this_month(base64Str)
        result = helper.process_and_return_aggregation_for_month(date_time_obj, base64Str)
        self.assertEqual(9, result, "result should be 9")
        # Output = 9

        # Test 2 - aggregation result
        base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        result = helper.process_and_return_aggregation_for_month(date_time_obj, base64Str, field="aggregate")
        self.assertAlmostEqual(29.9, result, delta=0.0001, msg="result should be 29.9")
        # Output = 29.9

    def test_process_and_return_aggregation_for_week(self):
        # Test 1 - data from generateDataFor_test_parsing_Test_2
        base64Str = "AAIOCDYtMjkCAgAAAAAAAAAAAAY3LTECAgAAAAAAAAAAAAY3LTICAgAAAAAAAAAAAAg2LTMwAgIAAAAAAAAAAAAGNy0zAgIAAAAAAAAAAAAGNy00AgIAAAAAAAAAAAAGNy01AgoAAAAAAAAAAAAAAg=="
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 5, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

        # if you are looking for data for this month then use can use
        # helper.process_and_return_aggregation_for_this_month(base64Str)
        result = helper.process_and_return_aggregation_for_week(date_time_obj, base64Str)
        self.assertEqual(11, result, "result should be 11")
        # Output = 11

        # Test 2 - aggregation result
        base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        result = helper.process_and_return_aggregation_for_week(date_time_obj, base64Str, field="aggregate")
        self.assertAlmostEqual(33.3, result, delta=0.0001, msg="result should be 33.3")
        # Output = 33.3

    def test_process_and_return_for_day(self):
        # Test 1 - data from generateDataFor_test_parsing_Test_2
        base64Str = "AAIOCDYtMjkCAgAAAAAAAAAAAAY3LTECAgAAAAAAAAAAAAY3LTICAgAAAAAAAAAAAAg2LTMwAgIAAAAAAAAAAAAGNy0zAgIAAAAAAAAAAAAGNy00AgIAAAAAAAAAAAAGNy01AgoAAAAAAAAAAAAAAg=="
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 1, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 5, 'aggregate': None, 'counter_secondary': None, 'aggregate_secondary': None, 'str': None, 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

        # if you are looking for data for this month then use can use
        # helper.process_and_return_aggregation_for_this_month(base64Str)
        result = helper.process_and_return_for_day(date_time_obj, base64Str)
        self.assertEqual(5, result, "result should be 5")
        # Output = 5

        # Test 2 - aggregation result
        base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')
        result = helper.process_and_return_for_day(date_time_obj, base64Str, field="aggregate")
        self.assertAlmostEqual(8.9, result, delta=0.0001, msg="result should be 8.9")
        # Output = 8.9

    def test_process_and_return_string_data_for_month(self):
        # Test 1 - data from generateDataFor_test_parsing_Test_2
        base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

        # if you are looking for data for this month then use can use
        # helper.process_and_return_aggregation_for_this_month(base64Str)
        result = helper.process_and_return_string_data_for_month(date_time_obj, base64Str)
        self.assertEqual(8, result, "result should be 8")
        # Output = 8

        date_time_str = '30/06/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

        result = helper.process_and_return_string_data_for_month(date_time_obj, base64Str)
        self.assertEqual(4, result, "result should be 4")
        # Output = 8

    def test_process_and_return_string_data_for_week(self):
        # Test 1 - data from generateDataFor_test_parsing_Test_2
        base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

        # if you are looking for data for this month then use can use
        # helper.process_and_return_aggregation_for_this_month(base64Str)
        result = helper.process_and_return_string_data_for_week(date_time_obj, base64Str)
        print(result)
        self.assertEqual(10, result, "result should be 10")
        # Output = 10

    def test_process_and_return_string_data_for_day(self):
        # Test 1 - data from generateDataFor_test_parsing_Test_2
        base64Str = "AAIOCDYtMjkCAgKamZmZmZnxPwAAAg5tLTE7bS0zAAAAAAAGNy0xAgYCMzMzMzMzC0AAAAIWbS0zO20tNDttLTYAAAAAAAY3LTICCALNzMzMzMwQQAAAAhZtLTQ7bS03O20tOAAAAAAACDYtMzACBAJmZmZmZmYCQAAAAhhtLTI7bS0xO20tMTEAAAAAAAY3LTMCCgJmZmZmZmYWQAAAAhZtLTM7bS02O20tOAAAAAAABjctNAIMAjMzMzMzMx9AAAACGG0tMjttLTc7bS0xMAAAAAAABjctNQIOAs3MzMzMzCFAAAACIG0tMjttLTU7bS03O20tMTAAAAAAAAAC"
        helper = MonthDataAvroHelper()
        result = helper.process(base64Str)
        print(result)
        # Output = {'ParentContainer': [], 'data': {'6-29': {'counter': 1, 'aggregate': 1.1, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-3', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-1': {'counter': 3, 'aggregate': 3.4, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-4;m-6', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-2': {'counter': 4, 'aggregate': 4.2, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-4;m-7;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '6-30': {'counter': 2, 'aggregate': 2.3, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-1', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-3': {'counter': 5, 'aggregate': 5.6, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-3;m-6;m-8', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-4': {'counter': 6, 'aggregate': 7.8, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-2;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}, '7-5': {'counter': 7, 'aggregate': 8.9, 'counter_secondary': None, 'aggregate_secondary': None, 'str': 'm-1;m-2;m-5;m-7;m-10', 'udf1': None, 'udf2': None, 'udf3': None, 'udf4': None, 'udf5': None}}, 'version': 1}

        date_time_str = '05/07/22 01:55:19'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

        # if you are looking for data for this month then use can use
        # helper.process_and_return_aggregation_for_this_month(base64Str)
        result = helper.process_and_return_string_data_for_day(date_time_obj, base64Str)
        self.assertEqual(4, result, "result should be 4")
        # Output = 4


if __name__ == '__main__':
    unittest.main()
