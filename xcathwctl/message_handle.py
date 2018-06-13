#!/usr/bin/env python

class Messager():

    def __init__(self, verbose):
        self.verbose = verbose

    def info(self, msg):
        if self.verbose:
            print (msg)

    def warn(self, msg):
        if self.verbose:
            print (msg)

    def error(self, msg, node=''):
        if self.verbose:
            print ('%s: %s' % (node, msg))

    def syslog(self, msg):
        pass

    def update_node_attributes(self, attribute, node, data):
        pass
