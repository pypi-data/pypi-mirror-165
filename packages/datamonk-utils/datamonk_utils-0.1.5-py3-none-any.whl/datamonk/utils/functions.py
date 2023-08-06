
import numpy as np
import pandas as pd
import datetime as dt
import os
import json

class dictionary:
    def __init__(self,input):
        self.object = input

    def get_value_from_path(self,path):
        path_string="["+"][".join(path.split("."))+"]"
        dict_object=self.object
        exec("output=dict_object"+path_string,globals(),locals())
        return output
    def get_elements(self, position, **kwargs):
        keys = list({k for d in self.object for k in d.keys()})
        values = list({k for d in self.object for k in d.values()})
        if position == "k":
            return keys
        elif position == "v":
            return values
        elif position == "b":
            separator = kwargs.get("separator", '')
            return [k + separator + v for k, v in zip(keys, values)]


    def keys_filtering(self, filter_list):
        """User defined function to filter in dictionary over keys and return values"""
        return list([list(item.values())[0] for item in self.object if list(item.keys())[0] in filter_list])

    def formatting(self,formatting_type,**kwargs):
        import re

        if formatting_type== "bq_conversion":
            schema_master = kwargs["schema"]
            if type(self.object) != list and type(schema_master) == list:
                self.object =  [self.object]

        if type(self.object) == list:
            output=[]

            if formatting_type == "types_parsing":
                if type(self.object[0]) == dict:
                    rows_union = {}
                    for idx,row in enumerate(input):
                            row_formatted = dictionary.formatting(row, formatting_type, **kwargs)
                            rows_union=dictionary.merge(rows_union,row_formatted)
                    output = [rows_union]
                else:
                    rows_union=[]
                    for idx,row in enumerate(self.object):
                            row_formatted = dictionary.formatting(row, formatting_type, **kwargs)
                            rows_union= list({s for s in rows_union + [row_formatted]})
                    output = rows_union

            else:
                for idx, row in enumerate(self.object):
                    if formatting_type == "bq_conversion":
                        kwargs["schema"]=kwargs["schema"][0] if type(kwargs["schema"]) == list else kwargs["schema"]
                    row_formatted=dictionary.formatting(row,formatting_type,**kwargs)
                    output.append(row_formatted)

        elif type(self.object) == dict:

            output={}

            for k,v in dict(self.object).items():
                if v in [None,{},'None']:
                    pass

                else:
                    if formatting_type == "bq_conversion":
                        if type(schema_master) == list:
                            if type(input) != list:
                                output = dictionary.formatting([self.object], formatting_type, schema=schema_master[0])
                            else:
                                output = dictionary.formatting(self.object, formatting_type, schema=schema_master[0])
                        else:
                            try:
                                kwargs["schema"] = schema_master[k]
                                output[k] = dictionary.formatting(v, formatting_type, **kwargs)
                                if not re.match(r'^\w+$', k):
                                    k_new = re.sub(r'\W+', '', k)
                                    output[k_new] = output.pop(k)
                            except KeyError as e:
                                if kwargs["pass_unknown_values"]==True:
                                    pass
                    else:
                        output[k] = dictionary.formatting(v, formatting_type, **kwargs)

                        if not re.match(r'^\w+$', k) and formatting_type =="key_normalization" :
                            k_new = re.sub(r'\W+', '', k)
                            output[k_new] = output.pop(k)

        else:
            if formatting_type == "bq_conversion" and schema_master != type(input).__name__:
                output_type = kwargs["schema"]
                output = dictionary.type_converting(self.object,manual_type=output_type)
            elif formatting_type == "types_parsing":
                output = type(self.object).__name__
            elif formatting_type == "custom_conversion":
                    output=kwargs["conversion_dict"][self.object]
            else:
                output = self.object

        return output


    @staticmethod
    def type_converting(value,**kwargs):
        import uuid
        import datetime
        import decimal
        if type(value) in [uuid.UUID,datetime.datetime,datetime.date]:
            value = str(value)
        elif value in [[],{}]:
            value = None
        elif type(value) in [decimal.Decimal]:
            value = float(value)
        elif "manual_type" in kwargs:
            try:

                local_dict={"value":value}
                exec("value = " + kwargs["manual_type"] + "(value)",globals(),local_dict)
                value = local_dict["value"]
            except Exception as e:
                str(e)
        return value

    @staticmethod
    def merge(dict_1,dict_2):
        for key, value in dict_2.items():
            if key in dict_1:
                if isinstance(dict_1[key], dict) and isinstance(dict_2[key], dict):
                    dictionary.merge(dict_1[key],dict_2[key])
                elif isinstance(dict_1[key],dict) and isinstance(dict_2[key],list):
                    dict_1[key]=dict_2[key]
            else:
                dict_1[key] = value
        return dict_1


class lists:
    def __init__(self,list_object):
        self.object=list_object

    def join_string(self,separator=','):
        """Compiler of list of strings of code into string chain (in case of >1 elements) or simple value given by
        returned data type. """
        if len(self.object) == 1:
            return eval(self.object[0])
        else:
            return separator.join([str(eval(i)) for i in self.object])

    def clean_currency(self):
        return self.object.str.replace(",", ".").str.replace("Kč", "").str.replace(" ", "").astype(float)

    def remove_duplicates(self):
        return list(set([i for i in self.object]))

    def get_values_by_key(self,key="name"):
        return list(set([i[key] for i in self.object if key in i.keys()]))
    def get_element_by_name(self,name="",key="name"):
        return [i for i in self.object if name in i[key]][0]


class time:

    def __init__(self,input=dt.datetime.now(),
                 output_type='string',
                 output_format='%Y-%m-%dT%H:%M:%S',
                 input_tz='Europe/Prague',
                 output_tz="Europe/Prague"):
        from dateutil.parser import parse
        self.output_type=output_type
        self.input=input
        self.input_datetime=self.input if isinstance(self.input,dt.datetime) else parse(self.input,ignoretz=True)
        self.input_timezone=input_tz
        self.output_type = output_type
        self.output_timezone = output_tz
        self.output_format = output_format
        self.output_datetime=self.input_datetime
        self.output = self.output_datetime if self.output_type == 'datetime' else self.output_datetime.strftime(
            format=self.output_format)
    @staticmethod
    def is_parsable(input):
        from dateutil.parser import parse
        try:
            parse(input)
            return True
        except:
            return False
    @property
    def output_datetime(self):
        return self._output_datetime

    @output_datetime.setter
    def output_datetime(self,output_datetime):
        self._output_datetime = output_datetime
        self.output = self.output_datetime if self.output_type == 'datetime' else self.output_datetime.strftime(
            format=self.output_format)

    def convert_timezone(self):
        import pytz
        output_tz = pytz.timezone(self.output_timezone)
        input_tz=pytz.timezone(self.input_timezone)
        self.output_datetime= output_tz.localize(self.output_datetime).astimezone(input_tz)
        return self.output


    def timedelta(self,relativedelta_object):
        from dateutil.relativedelta import relativedelta
        relativedelta_arguments=",".join([f"{element[0]}={element[1]}" for element in relativedelta_object.items()])
        exec(f"change = relativedelta({relativedelta_arguments})", locals(), globals())
        self.output_datetime=self.output_datetime+change
        return self.output

    def get_rel_date(self,input):
        import datetime as dt

        if input == "today":
            self.output_datetime = dt.datetime.now()

        return self.output

    def infer_function(self,input):
        if isinstance(input, dict):
            output = self.timedelta(relativedelta_object=input)

        elif time.is_parsable(input):
            output = time(input=input,
                                          output_type=self.output_type,
                                          output_format=self.output_format,
                                          input_tz=self.input_timezone,
                                          output_tz=self.output_timezone).output
        else:
            output = self.get_rel_date(input=input)
        return output

    def get_time_range(self,**kwargs):
        import numpy as np
        from dateutil.parser import parse
        range_object = {"bound":{},"range":{}}
        _range=range_object["range"]
        range_object["bound"]["names"]=["start", "end"]
        _defined=np.intersect1d(list(kwargs.keys()),range_object["bound"]["names"])
        if len(_defined) == 0:
            raise KeyError("at least one of start , end arguments must be used")
        elif len(_defined) == 1:

            _unknown=next(iter(set(range_object["bound"]["names"])-set(_defined)))
            _range[_unknown]=self.output
            _known=_defined[0]
            input=kwargs[_known]
            _range[_known]=self.infer_function(input)

        elif len(_defined)==2:
            _known=[i for i in _defined if str(kwargs[i]) in "today" or time.is_parsable(kwargs[i])]
            _unknown=next(iter(set(range_object["bound"]["names"])-set(_known)))
            for i in _known:
                _range[i]=self.infer_function(kwargs[i])
            if _unknown:
                _range[_unknown]=time(input=_range[_known[0]],
                                      input_tz=self.input_timezone,
                                      output_tz=self.output_timezone,
                                      output_format=self.output_format,
                                      output_type=self.output_type).infer_function(kwargs[_unknown])


        return _range

class pandas:
    @staticmethod
    def range_join(config, values):
        a = config["main_table"][values].values
        bh = config["matching_table"]["max"].values
        bl = config["matching_table"]["min"].values

        i, j = np.where((a[:, None] >= bl) & (a[:, None] <= bh))

        return pd.DataFrame(
            np.column_stack([config["main_table"].values[i], config["matching_table"].values[j]]),
            columns=config["main_table"].columns.append(config["matching_table"].columns),
            index=config["main_table"].index
        )


class local:
    @staticmethod
    def read_configJSON(path,output_type="dict"):
        with open("./" + os.environ.get("CONFIG_PATH",'') + path + ".json") as f:
            if output_type == "dict":
                return json.load(f)
            elif output_type == "string":
                return f.read()

    @staticmethod
    def read_keysJSON(path,output_type="dict"):
        with open("./" + os.environ.get("KEYS_PATH",'') + path + ".json") as f:
            if output_type == "dict":
                return json.load(f)
            elif output_type == "string":
                return f.read()


class query:
    @staticmethod
    def get_last_value(column,tablePath):
        query_string = 'SELECT MAX({}) FROM {}'.format(column,tablePath)
        return query_string


def timeit(method):
    import time
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        if 'log_time' in kw:
            name = kw.get('log_name', method.__name__.upper())
            kw['log_time'][name] = int((te - ts))
        else:
            print('%r  %2.2f s' % \
                  (method.__name__, (te - ts)))
        return result
    return timed