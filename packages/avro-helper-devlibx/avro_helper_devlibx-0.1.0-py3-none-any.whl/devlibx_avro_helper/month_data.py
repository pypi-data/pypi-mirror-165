import io
import avro.schema
import avro.io
import base64
from datetime import datetime
from datetime import timedelta

schema_string = '''
{
  "namespace": "io.gitbub.devlibx.avro",
  "type": "record",
  "name": "MonthDataAvro",
  "fields": [
    {
      "name": "ParentContainer",
      "type": {
        "type": "array",
        "items": {
          "type": "record",
          "namespace": "io.gitbub.devlibx.avro.child",
          "name": "Container",
          "fields": [
            {
              "name": "counter",
              "type": [
                "null",
                "int"
              ],
              "default": null
            },
            {
              "name": "aggregate",
              "type": [
                "null",
                "double"
              ],
              "default": null
            },
            {
              "name": "counter_secondary",
              "type": [
                "null",
                "int"
              ],
              "default": null
            },
            {
              "name": "aggregate_secondary",
              "type": [
                "null",
                "double"
              ],
              "default": null
            },
            {
              "name": "str",
              "type": [
                "null",
                "string"
              ],
              "default": null
            },
            {
              "name": "udf1",
              "type": [
                "null",
                "string",
                "int",
                "double"
              ],
              "default": null
            },
            {
              "name": "udf2",
              "type": [
                "null",
                "string",
                "int",
                "double"
              ],
              "default": null
            },
            {
              "name": "udf3",
              "type": [
                "null",
                "string",
                "int",
                "double"
              ],
              "default": null
            },
            {
              "name": "udf4",
              "type": [
                "null",
                "string",
                "int",
                "double"
              ],
              "default": null
            },
            {
              "name": "udf5",
              "type": [
                "null",
                "string",
                "int",
                "double"
              ],
              "default": null
            }
          ]
        }
      },
      "default": []
    },
    {
      "name": "data",
      "type": [
        "null",
        {
          "type": "map",
          "values": "io.gitbub.devlibx.avro.child.Container"
        }
      ],
      "default": null
    },
    {
      "name": "version",
      "type": "int",
      "default": 1
    }
  ]
}
'''

month_data_schema_parsed = avro.schema.parse(schema_string)


# This class helps to read avro object from given Base64 string
# noinspection PyMethodMayBeStatic
class MonthDataAvroHelper:
    def __int__(self):
        pass

    def process(self, avro_base64_str):
        """
        Process the input Base64 data

        :param avro_base64_str: Base46 coded data
        :return: Deserialize Avro object
        """
        bytes_reader = io.BytesIO(base64.b64decode(avro_base64_str))
        decoder = avro.io.BinaryDecoder(bytes_reader)
        reader = avro.io.DatumReader(month_data_schema_parsed, month_data_schema_parsed)
        return reader.read(decoder)

    def process_and_return_last_n_days_from_time(self, time, avro_base64_str, days):
        """
        Return N days in past (including today) data from the time given in "time"

        :param datetime time: Time from where we need to calculate N days
        :param str avro_base64_str: Base64 data of month data
        :param int days: How many days in past
        :return: Array containing N items (N = days)
        """

        data = self.process(avro_base64_str)
        days_to_add = self.get_last_n_days_keys(time, days)
        result = []
        for day in days_to_add:
            try:
                result.append(data["days"][day])
            except KeyError as error:
                pass
        return result

    def process_and_return_last_n_days(self, avro_base64_str, days):
        """
        Return N days in past (including today) data from today

        :param str avro_base64_str: Base64 data of month data
        :param int days: How many days in past
        :return: Array containing N items (N = days)
        """
        return self.process_and_return_last_n_days_from_time(datetime.now(), avro_base64_str, days)

    def get_last_n_days_keys(self, time, days):
        """
        Give key from given time to N days - you can use these keys to get data from avro data

        :param time: time to start
        :param days: no of days
        :return: array containing keys for past N days (including given time)
        """
        result = []
        end = time
        start = time - timedelta(days=days)
        while start < end:
            start = start + timedelta(days=1)
            result.append("{}-{}".format(start.month, start.day))
        return result

    def get_last_n_days_keys_from_now(self, days):
        """
       Give key from now to N days - you can use these keys to get data from avro data

       :param time: time to start
       :param days: no of days
       :return: array containing keys for past N days (including today)
       """
        time = datetime.now()
        return self.get_last_n_days_keys(time, days)

    def get_keys_for_month(self, time):
        """
        Give key month given by time - you can use these keys to get data from avro data

        :param time: month to use
        :return: array containing keys for this month (including given time)
        """
        result = []
        end = time
        start = time.replace(day=1)
        while start <= end:
            result.append("{}-{}".format(start.month, start.day))
            start = start + timedelta(days=1)
        return result

    def get_keys_for_this_month(self):
        """
        Give key month this month

        :return: array containing keys for this month (including given time)
        """
        return self.get_keys_for_month(datetime.now())

    def get_keys_for_week(self, time):
        """
        Give key month given by time - you can use these keys to get data from avro data

        :param time: month to use
        :return: array containing keys for this month (including given time)
        """
        result = []
        end = time
        start = time - timedelta(days=6)
        while start <= end:
            result.append("{}-{}".format(start.month, start.day))
            start = start + timedelta(days=1)
        return result

    def get_keys_for_this_week(self):
        """
        Give key month this month

        :return: array containing keys for this month (including given time)
        """
        return self.get_keys_for_week(datetime.now())

    def process_and_return_aggregation_for_month(self, time, avro_base64_str, aggregate=True, field="counter"):
        """
        Return data for month given by time (including today)

        :param datetime time: Time from where we need to calculate N days
        :param str avro_base64_str: Base64 data of month data
        :param aggregate if true add and return sum, otherwise array
        :param field if passed perform aggregation on that field default value is counter
        :return: Array containing N items (N = days) OR aggregated sum if aggregate=true
        """

        data = self.process(avro_base64_str)
        days_to_add = self.get_keys_for_month(time)
        result = []
        for day in days_to_add:
            try:
                result.append(data["data"][day][field])
            except KeyError as error:
                pass
        if aggregate is False:
            return result
        else:
            sum = 0
            for i in result:
                sum = sum + i
            return sum

    def process_and_return_aggregation_for_this_month(self, avro_base64_str, aggregate=True, field="counter"):
        """
        Return data for this month (including today)

        :param str avro_base64_str: Base64 data of month data
        :param aggregate if true add and return sum, otherwise array
        :param field if passed perform aggregation on that field default value is counter
        :return: Array containing N items (N = days) OR aggregated sum if aggregate=true
        """
        return self.process_and_return_aggregation_for_month(datetime.now(), avro_base64_str, aggregate, field)

    def process_and_return_aggregation_for_week(self, time, avro_base64_str, aggregate=True, field="counter"):
        """
        Return data for week given by time (including today)

        :param datetime time: Time from where we need to calculate N days
        :param str avro_base64_str: Base64 data of month data
        :param aggregate if true add and return sum, otherwise array
        :param field if passed perform aggregation on that field default value is counter
        :return: Array containing N items (N = days) OR aggregated sum if aggregate=true
        """

        data = self.process(avro_base64_str)
        days_to_add = self.get_keys_for_week(time)
        result = []
        for day in days_to_add:
            try:
                result.append(data["data"][day][field])
            except KeyError as error:
                pass
        if aggregate is False:
            return result
        else:
            sum = 0
            for i in result:
                sum = sum + i
            return sum

    def process_and_return_aggregation_for_this_week(self, avro_base64_str, aggregate=True, field="counter"):
        """
        Return data for this week (including today)

        :param str avro_base64_str: Base64 data of month data
        :param aggregate if true add and return sum, otherwise array
        :param field if passed perform aggregation on that field default value is counter
        :return: Array containing N items (N = days) OR aggregated sum if aggregate=true
        """
        return self.process_and_return_aggregation_for_week(datetime.now(), avro_base64_str, aggregate, field)

    def process_and_return_for_day(self, time, avro_base64_str, field="counter"):
        """
        Return data for day given by time (including today)

        :param datetime time: Time from where we need to calculate for any day
        :param str avro_base64_str: Base64 data of month data
        :param field if passed return data for that field default value is counter
        :return: return data for today
        """
        data = self.process(avro_base64_str)
        try:
            return data["data"]["{}-{}".format(time.month, time.day)][field]
        except KeyError as error:
            return 0

    def process_and_return_for_today(self, avro_base64_str, field="counter"):
        """
        Return data for day given by time (including today)

        :param str avro_base64_str: Base64 data of month data
        :param field if passed return data for that field default value is counter
        :return: return data for today
        """
        return self.process_and_return_for_day(datetime.now(), avro_base64_str, field)

    def process_and_return_string_data_for_month(self, time, avro_base64_str, aggregate=True, union=True, separator=";", field="str"):
        """
        Return data for month given by time (including today)

        :param datetime time: Time from where we need to calculate N days
        :param str avro_base64_str: Base64 data of month data
        :param aggregate: if true add and return count, otherwise array
        :param union: if true return union of the string data for days else intersection
        :param separator: how to separate items in string data
        :param field: if passed perform result on that field default value is str
        :return: Array containing N items (N = days) OR count if aggregate=true
        """

        data = self.process(avro_base64_str)
        days_to_add = self.get_keys_for_month(time)
        list_days = []
        for day in days_to_add:
            try:
                string_data = data["data"][day][field]
                if isinstance(string_data, str):
                    list_days.append(string_data.split(separator))
            except KeyError as error:
                pass
        final_set = set()
        for list_day in list_days:
            if union:
                final_set = final_set.union(set(list_day))
            else:
                final_set = final_set.intersection(set(list_day))

        if aggregate:
            return len(final_set)
        else:
            return list(final_set)

    def process_and_return_string_data_for_this_month(self, avro_base64_str, aggregate=True, union=True, separator=";", field="str"):
        """
        Return data for this month (including today)

        :param str avro_base64_str: Base64 data of month data
        :param aggregate: if true add and return count, otherwise array
        :param union: if true return union of the string data for days else intersection
        :param separator: how to separate items in string data
        :param field: if passed perform result on that field default value is str
        :return: Array containing N items (N = days) OR count if aggregate=true
        """
        return self.process_and_return_aggregation_for_month(datetime.now(), avro_base64_str, aggregate, union, separator, field)

    def process_and_return_string_data_for_week(self, time, avro_base64_str, aggregate=True, union=True, separator=";", field="str"):
        """
        Return data for week given by time (including today)

        :param datetime time: Time from where we need to calculate N days
        :param str avro_base64_str: Base64 data of month data
        :param aggregate: if true add and return count, otherwise array
        :param union: if true return union of the string data for days else intersection
        :param separator: how to separate items in string data
        :param field: if passed perform result on that field default value is str
        :return: Array containing N items (N = days) OR count if aggregate=true
        """

        data = self.process(avro_base64_str)
        days_to_add = self.get_keys_for_week(time)
        list_days = []
        for day in days_to_add:
            try:
                string_data = data["data"][day][field]
                if isinstance(string_data, str):
                    list_days.append(string_data.split(separator))
            except KeyError as error:
                pass
        final_set = set()
        for list_day in list_days:
            if union:
                final_set = final_set.union(set(list_day))
            else:
                final_set = final_set.intersection(set(list_day))

        if aggregate:
            return len(final_set)
        else:
            return list(final_set)

    def process_and_return_string_data_for_this_week(self, avro_base64_str, aggregate=True, union=True, separator=";", field="str"):
        """
        Return data for this week (including today)

        :param str avro_base64_str: Base64 data of month data
        :param aggregate: if true add and return count, otherwise array
        :param union: if true return union of the string data for days else intersection
        :param separator: how to separate items in string data
        :param field: if passed perform result on that field default value is str
        :return: Array containing N items (N = days) OR count if aggregate=true
        """
        return self.process_and_return_aggregation_for_week(datetime.now(), avro_base64_str, aggregate, union, separator, field)

    def process_and_return_string_data_for_day(self, time, avro_base64_str, aggregate=True, separator=";", field="str"):
        """
        Return data for day given by time (including today)

        :param datetime time: Time from where we need to calculate for any day
        :param str avro_base64_str: Base64 data of month data
        :param aggregate: if true add and return count, otherwise array
        :param separator: how to separate items in string data
        :param field: if passed perform result on that field default value is str
        :return: return data for today OR count if aggregate=true
        """
        data = self.process(avro_base64_str)
        try:
            result = data["data"]["{}-{}".format(time.month, time.day)][field]
            result = set(result.split(separator))
            if aggregate:
                return len(result)
            else:
                return list(result)
        except KeyError as error:
            if aggregate:
                return 0
            else:
                return []

    def process_and_return_string_data_for_today(self, avro_base64_str, aggregate=True, separator=";", field="str"):
        """
        Return data for day given by time (including today)

        :param str avro_base64_str: Base64 data of month data
        :param aggregate: if true add and return count, otherwise array
        :param separator: how to separate items in string data
        :param field: if passed perform result on that field default value is str
        :return: return data for today
        """
        return self.process_and_return_for_day(datetime.now(), avro_base64_str, aggregate, separator, field)
