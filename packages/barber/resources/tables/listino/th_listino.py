#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('nome')
        r.fieldcell('descrizione')
        r.fieldcell('durata_media')
        r.fieldcell('prezzo')

    def th_order(self):
        return 'nome'

    def th_query(self):
        return dict(column='nome', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=3, border_spacing='4px',margin='10px')
        fb.field('nome',width='20em',validate_case='t')
        fb.field('durata_media',values='1:10,2:20,3:30,4:40,5:50,6:60',tag='filteringSelect',width='10em')
        fb.field('prezzo',width='5em')
        fb.field('descrizione',colspan=3,tag='simpleTextArea',width='100%',height='10ex')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
