# -*- coding: UTF-8 -*-
# th_cliente.py

from gnr.web.gnrwebpage import BaseComponent
from gnr.core.gnrdecorator import customizable

class View(BaseComponent):
    def th_hiddencolumns(self):
        return '$codice_negozio'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('codice_negozio', width='8em',name='Codice')
        r.fieldcell('identificativo', width='15em',name='Identificativo')
        r.fieldcell('indirizzo', width='15em',name='Indirizzo')
        r.fieldcell('cap', width='4em',name='Cap')
        r.fieldcell('localita', width='15em',name=u'Località')
        r.fieldcell('provincia', width='3em',name='Pr.')
        r.fieldcell('nazione', width='3em',name='Naz.')

    def th_order(self):
        return 'codice_negozio'

    def th_query(self):
        return dict(column='codice_negozio',op='contains',val='')


class Form(BaseComponent):
    py_requires="""component_anag:AnagraficaComponent""" 
    def th_form(self, form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top',datapath='.record').formbuilder(cols=3)
        fb.field('codice_negozio',validate_notnull=True,validate_nodup=True,
                validate_case='upper',validate_regex='![^A-Z0-9_]',width='10em')
        fb.field('identificativo',width='20em',validate_notnull=True)
        bc.contentPane(region='center',datapath='.record').anagraficaPane(tipo_anagrafica='societa')
        bottom = bc.tabContainer(region='bottom',height='260px',margin='2px')
        self.negozioLavoranti(bottom.contentPane(title='Lavoranti'))
        self.negozioLavoranti(bottom.contentPane(title='Listini'))

    def negozioLavoranti(self,pane):
        pane.dialogTableHandler(relation='@lavoranti',pbl_classes='True')


    def negozioListini(self,pane):
        pane.dialogTableHandler(relation='@listini',pbl_classes='True')

    def th_options(self):
        return dict(dialog_parentRatio=.9)
