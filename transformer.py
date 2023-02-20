from dateutil import parser
import time
import json

class JsonTransformer:
    def __init__(self, input_path):
        self.input_path = input_path
        self.input_dict = self._load_input_data()
        self.output = []
        
    def _load_input_data(self):
        try:
            with open(self.input_path, "r") as f:
                input_dict = json.load(f)
            return input_dict
        except json.JSONDecodeError:
            return None
        
    def _sanitize_string(self, s):
        if s is None:
            return None
        return s.strip()

    def _transform_string(self, val):
        s = self._sanitize_string(val)
        if s is None or len(s)==0:
            return None
        try:
            datetime_obj = parser.isoparse(s)
            unix_epoch_time = int(datetime_obj.timestamp())
            return unix_epoch_time
        except (ValueError, TypeError):
            return str(s)

    def _transform_numeric(self, val):
        s = self._sanitize_string(val)
        if s is None or len(s)==0:
            return None
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return None

    def _transform_bool(self, val):
        s = self._sanitize_string(val)
        if s is None or len(s)==0:
            return None
        if s.lower() in ['1', 't', 'T', 'true', 'True', 'TRUE']: 
            return True
        if s.lower() in ['0', 'f', 'F', 'false', 'False', 'FALSE']: 
            return False

    def _transform_null(self, val):
        s = self._sanitize_string(val)
        if s is None or len(s)==0:
            return None
        if s.lower() in ['1', 't', 'T', 'true', 'True', 'TRUE']: 
            return 'null'
        else: return None

    def _transform_value(self, val):
        if type(val) is not dict: return None
        keys = {key.strip():key for key in val.keys()}
        if 'S' in keys:
            return self._transform_string(val[keys['S']])

        elif 'N' in keys:
            return self._transform_numeric(val[keys['N']])

        elif 'BOOL' in keys:
            return self._transform_bool(val[keys['BOOL']])

        elif 'NULL' in keys:
            return self._transform_null(val[keys['NULL']])

        elif 'L' in keys:
            lst = val[keys['L']]
            if lst is None:
                return None
            out = [self._transform_value(x) for x in lst if x is not None and self._transform_value(x)!=None]
            if len(out) > 0: return out
            else: return None
        elif 'M' in val:
            d = {}
            for k, v in sorted(val[keys['M']].items()):
                k = self._sanitize_string(k)
                if k is not None and len(k) > 0:
                    out = self._transform_value(v)
                    if out!=None: d[k] = out
            return d
        else:
            return None

    def transform(self):
        if isinstance(self.input_dict, dict):
            self.input_dict = [self.input_dict]
        for obj in self.input_dict:
            new_obj = {}
            for k, v in sorted(obj.items()):
                k = self._sanitize_string(str(k))
                if k is not None and len(k) > 0:
                    out = self._transform_value(v)
                    if out!=None: new_obj[k] = out
            if len(new_obj) > 0:
                self.output.append(new_obj)
        print(json.dumps(self.output, indent=2))


input_path = 'sample1.json'
start_time = time.time()
JsonTransformer(input_path).transform()
print("Running time duration",time.time()-start_time)

        