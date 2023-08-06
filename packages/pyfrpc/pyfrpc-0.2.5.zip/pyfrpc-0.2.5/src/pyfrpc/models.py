# -*- coding: utf-8 -*-

from collections import namedtuple

FrpcCall = namedtuple("FrpcCall", ["name", "args"])
FrpcResponse = namedtuple("FrpcResponse", ["data"])


class FrpcFault(Exception):
    def __init__(self, err, msg):
        if not (isinstance(err, int) and isinstance(msg, str)):
            raise Exception("bad arguments")

        self.err = err
        self.msg = msg

    def __str__(self):
        return "FrpcFault(err={}, msg={})".format(self.err, repr(self.msg))

    def __eq__(self, other):
        if not isinstance(other, FrpcFault):
            return False

        return (self.msg == other.msg) and (self.err == other.err)

    def __ne__(self, other):
        return not (self == other)
