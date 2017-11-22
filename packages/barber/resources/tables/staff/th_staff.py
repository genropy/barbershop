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
        top = bc.borderContainer(region='top',height='120px',datapath='.record')
        fb = top.contentPane(region='center').formbuilder(cols=2)
        fb.field('identificativo',width='20em',validate_notnull=True)
        topright = top.borderContainer(region='right',width='500px')
        topright.contentPane(region='center').linkerBox('user_id',openIfEmpty=True,
                                                        formUrl='/adm/user_page',
                                                        dialog_height='400px',
                                                        dialog_width='650px')
        topright.roundedGroup(region='right',width='200px',title='Foto')                                       
        
        tc = bc.tabContainer(region='center',margin='2px')
        tc.contentPane(title='Dati anagrafici',datapath='.record').anagraficaPane(tipo_anagrafica='persona')
        tc.contentPane(title='Calendario').plainTableHandler(relation='@calendario')




    def th_options(self):
        return dict(dialog_parentRatio=.9)
