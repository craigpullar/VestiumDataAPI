import json
from django.core.serializers.json import DjangoJSONEncoder
from tastypie.serializers import Serializer
import re

class PrettyJSONSerializer(Serializer):

    json_indent = 2
    under_pat = re.compile(r'_([a-z])')

    def underscore_to_camel(self, name):
        return self.under_pat.sub(lambda x: x.group(1).upper(), name)

    def prettifyJSON(self, j):
        out = {}
        for k in j:
            newK = self.underscore_to_camel(k)
            if isinstance(j[k],dict):
                out[newK] = self.prettifyJSON(j[k])
            elif isinstance(j[k],list):
                out[newK] = self.prettifyArray(j[k])
            else:
                out[newK] = j[k]
        return out

    def prettifyArray(self, a):
        newArr = []
        for i in a:
            if isinstance(i,list):
                newArr.append(self.prettifyArray(i))
            elif isinstance(i, dict):
                newArr.append(self.prettifyJSON(i))
            else:
                newArr.append(i)
        return newArr


    def to_json(self, data, options=None):
        options = options or {}
        data = self.to_simple(data, options)
        return json.dumps(self.prettifyJSON(data), cls=DjangoJSONEncoder,
                sort_keys=True, ensure_ascii=False, indent=self.json_indent)

