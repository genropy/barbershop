#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('cliente_id')
        r.fieldcell('staff_id')
        r.fieldcell('data')
        r.fieldcell('ora_inizio')
        r.fieldcell('ora_fine')

    def th_order(self):
        return 'cliente_id'

    def th_query(self):
        return dict(column='cliente_id', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('cliente_id')
        fb.field('staff_id')
        fb.field('data')
        fb.field('ora_inizio')
        fb.field('ora_fine')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class FormDashboard(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('cognome',validate_notnull=True)
        fb.field('nome')
        fb.field('telefono',validate_notnull=True)
        fb.field('email')
        fb.field('ora_inizio')
        fb.field('ora_fine')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px',modal=True)

    @public_method
    def th_onLoading(self,record,newrecord,loadingParameters,recInfo,**kwargs):
        if newrecord and record['calendario_id']:
            record['data'] = record['@calendario_id.data']
