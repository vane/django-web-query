#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'michal@vane.pl'


import json, types
from validators import SchemaValidator
from validators import DateValidator, LimitFilterValidator

'''
FILTER
'''
class Filter():
    def __init__(self, obj):
        self.clazz = obj

    def resolve(self, name, data):
        if name == "filter":
            if data.has_key('date'):
                d = data['date']
                # resolve date to format
                for key in d.keys():
                    d[key] = DateValidator.get(d[key])
                return Filter(self.clazz.filter(**d))
            return Filter(self.clazz.filter(**data))
        elif name == "exclude":
            return Filter(self.clazz.exclude(**data))
        elif name == "order_by":
            return Filter(self.clazz.order_by(data))
        elif name == "limit":
            data = LimitFilterValidator.get(data)
            if data["type"] == 0:
                return Filter(self.clazz[data["start"]:data["end"]])
            elif data["type"] == 1:
                return Filter(self.clazz[:data["end"]])
            elif data["type"] == 2:
                return Filter(self.clazz[data["start"]:])
        elif name == "get":
            return self.clazz
        raise RuntimeError("no such method")

'''
API models decorator
'''
class ObjectDecorator():
    def __init__(self, clazz, debug=True):
        self.clazz = clazz
        self.debug = debug

    def validate_fields(self, request, fields):
        data = request.data
        out = []
        for f in fields:
            if not data.has_key(f):
                out.append(f)
        return out

    def post_FIELDS(self):
        return SchemaValidator.values(self.clazz)

    def post_AUTH(self):
        return True

    def POST(self, request):
        fields = self.post_desc()
        valid = self.validate_fields(request, fields)
        if len(valid) == 0:
            obj = self.clazz()
            data = request.data
            for f in fields:
                setattr(obj, f, data[f])
            obj.save()
            return True
        return valid

    def put_AUTH(self):
        return False

    def put_GET(self, id):
        return self.clazz.objects.filter(id=id)

    def PUT(self, request):
        fields = self.post_desc()
        data = request.data
        id = data.id
        ele = self.put_GET(id)
        if ele != None:
            for f in data:
                if fields.has_key(f):
                    setattr(ele, f, data[f])
            return True
        return False

    def get_AUTH(self):
        return False

    def get_FIELDS(self):
        return SchemaValidator.values(self.clazz)

    def GET(self, request):
        data = request.GET['data']
        data = json.loads(data)

        f = Filter(self.clazz.objects)
        for d in data:
            for key in d.keys():
                f = f.resolve(key, d[key])
        v = f.resolve("get", None)
        # check if fields
        v = v.values(*self.get_FIELDS())
        if self.debug:
            operations = []
            for d in data:
                for key in d.keys():
                    operations.append(key)
                    operations.append(str(d[key]))
            print "ARGS : "+",".join(operations)
            print "QUERY : "+str(v.query)
        return list(v)

    def delete_AUTH(self):
        return True

    def delete_GET(self, id):
        return self.clazz.objects.filter(id=id)

    def DELETE(self, request):
        data = request.data
        id = data.id
        ele = self.delete_GET(id)
        if ele != None:
            ele.delete()
            return True
        return False

    def SERIALIZE(self, data):
        values = SchemaValidator.values(self.clazz)
        if type(data) is types.ListType:
            out = []
            for d in data:
                one = {}
                for val in values:
                    field = getattr(d, val)
                    one[val] = field
                out.append(one)
            return out
        else:
            out = {}
            for val in values:
                one = getattr(data, val)
                out[val] = one
            return out