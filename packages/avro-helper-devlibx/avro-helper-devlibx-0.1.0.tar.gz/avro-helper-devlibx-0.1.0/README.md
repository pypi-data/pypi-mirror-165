### How to use

Install ```pip install avro-helper-devlibx```

#### Quick example

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper

base64Str = "BgY3LTMCBjYtNgIGNy01BAAAAAI="
helper = MonthDataAvroHelper()
result = helper.process(base64Str)
print(result)

# Result
# {'days': {'8-16': 110, '8-17': 111, '8-14': 108, '8-15': 109, '8-18': 112, '8-19': 113, '8-30': 124, '8-31': 125, '8-12': 106, '8-13': 107, '8-10': 104, '8-11': 105, '9-1': 126, '9-2': 127, '9-3': 128, '8-27': 121, '9-4': 129, '8-6': 100, '8-28': 122, '8-7': 101, '8-25': 119, '8-8': 102, '8-26': 120, '8-9': 103, '8-29': 123, '8-20': 114, '8-23': 117, '8-24': 118, '8-21': 115, '8-22': 116}, 'entity_id': 'harish_1'}
```

### Get data for this month

In this example we would have data in base 64 encoding. We will get aggregated data for this month

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_aggregation_for_month(self):
    base64Str = "AgoGNy0xAgY3LTICBjctMwIGNy00AgY3LTUKAAAAAAI="
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'days': {'7-1': 1, '7-2': 1, '7-3': 1, '7-4': 1, '7-5': 5}, 'days_str': None, 'entity_id': None, 'sub_entity_id': None, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_month(base64Str)
    result = helper.process_and_return_aggregation_for_month(date_time_obj, base64Str)
    self.assertEqual(9, result, "result should be 9")
    # Output = 9
```

### Get data for this week (last 7 days)

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_aggregation_for_week(self):
    # Test 1 - data from generateDataFor_test_parsing_Test_2
    base64Str = "Ag4INi0yOQIGNy0xAgY3LTICCDYtMzACBjctMwIGNy00AgY3LTUKAAAAAAI=="
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'days': {'6-29': 1, '7-1': 1, '7-2': 1, '6-30': 1, '7-3': 1, '7-4': 1, '7-5': 5}, 'days_str': None, 'entity_id': None, 'sub_entity_id': None, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_week(base64Str)
    result = helper.process_and_return_aggregation_for_week(date_time_obj, base64Str)
    self.assertEqual(11, result, "result should be 9")
    # Output = 11
```

### Get data for this week (last 7 days)

```python
from devlibx_avro_helper.month_data import MonthDataAvroHelper
from datetime import datetime


def test_process_and_return_for_day(self):
    # Test 1 - data from generateDataFor_test_parsing_Test_2
    base64Str = "Ag4INi0yOQIGNy0xAgY3LTICCDYtMzACBjctMwIGNy00AgY3LTUKAAAAAAI=="
    helper = MonthDataAvroHelper()
    result = helper.process(base64Str)
    print(result)
    # Output = {'days': {'6-29': 1, '7-1': 1, '7-2': 1, '6-30': 1, '7-3': 1, '7-4': 1, '7-5': 5}, 'days_str': None, 'entity_id': None, 'sub_entity_id': None, 'version': 1}

    date_time_str = '05/07/22 01:55:19'
    date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y %H:%M:%S')

    # if you are looking for data for this month then use can use
    # helper.process_and_return_aggregation_for_this_month(base64Str)
    result = helper.process_and_return_for_today(date_time_obj, base64Str)
    self.assertEqual(5, result, "result should be 9")
    # Output = 5
```