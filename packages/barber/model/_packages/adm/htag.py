#!/usr/bin/env python
# encoding: utf-8
from gnr.core.gnrdecorator import metadata

class Table(object):

    @metadata(mandatory=True)
    def sysRecord_barber(self):
        return self.newrecord(code='barber',description='barber',
                                hierarchical_code='barber')

        

    @metadata(mandatory=True)
    def sysRecord_segr(self):
        return self.newrecord(code='segr',description='segr',
                                hierarchical_code='segr')

    @metadata(mandatory=True)
    def sysRecord_conf(self):
        return self.newrecord(code='conf',description='Configurazione',
                                hierarchical_code='conf')