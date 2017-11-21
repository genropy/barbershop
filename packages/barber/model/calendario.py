#!/usr/bin/env python
# encoding: utf-8

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('calendario', pkey='id', name_long='!!Calendario', 
                        name_plural='!!Calendario',caption_field='',
                        partition_negozio_id='negozio_id')
        self.sysFields(tbl)
        tbl.column('data', dtype='D', name_long='!!Data')
        tbl.column('staff_id',size='22', group='_', name_long='!!Staff'
                    ).relation('staff.id', relation_name='calendario', mode='foreignkey', onDelete='raise')
        tbl.column('occupazione', size=':144', name_long='!!Occupazione')
        
        tbl.aliasColumn('negozio_id','@staff_id.negozio_id',group='_')

        tbl.aliasColumn('caption_calendario',"""@staff_id.identificativo || ' ' || to_char($ts,'YYYY-MM-DD') """,group='_')


    def genera_calendario(self,staff_id=None,data_fine=None):
        pass

