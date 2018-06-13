#!/usr/bin/env python

class SelfServerException(Exception) :
    def __init__(self, message, detail_msg= "", host_and_port="") :
        super(Exception, self).__init__(message)
        self.host_and_port = host_and_port
        self.detail_msg = detail_msg

class SelfClientException(Exception) :
    def __init__(self, message, code) :
        super(Exception, self).__init__(message)
        self.code = code
