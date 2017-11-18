# -*- coding: UTF-8 -*-
# th_cliente.py

from gnr.web.gnrwebpage import BaseComponent
from gnr.core.gnrdecorator import customizable

class View(BaseComponent):
    def th_hiddencolumns(self):
        return '$identificativo'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('identificativo', width='15em',name='Identificativo')
        r.fieldcell('indirizzo', width='15em',name='Indirizzo')
        r.fieldcell('cap', width='4em',name='Cap')
        r.fieldcell('localita', width='15em',name=u'Località')
        r.fieldcell('provincia', width='3em',name='Pr.')
        r.fieldcell('nazione', width='3em',name='Naz.')

    def th_order(self):
        return 'identificativo'

    def th_query(self):
        return dict(column='identificativo',op='contains',val='')


class Form(BaseComponent):
    py_requires="""component_anag:AnagraficaComponent""" 
    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top',datapath='.record').formbuilder(cols=2)
        fb.field('identificativo',width='20em',validate_notnull=True)
        bc.contentPane(region='center',datapath='.record').anagraficaPane(tipo_anagrafica='persona')

    def th_options(self):
        return dict(dialog_parentRatio=.9)
