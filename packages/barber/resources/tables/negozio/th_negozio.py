# -*- coding: UTF-8 -*-
# th_cliente.py

from gnr.web.gnrwebpage import BaseComponent
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag

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
        self.full_form(form)
    
    def full_form(self,form):
        bc = form.center.borderContainer()
        fb = bc.contentPane(region='top',datapath='.record').formbuilder(cols=3)
        fb.field('codice_negozio',validate_notnull=True,validate_nodup=True,
                validate_case='upper',validate_regex='![^A-Z0-9_]',width='10em')
        fb.field('identificativo',width='20em',validate_notnull=True)
        fb.field('aderente_id',lbl='Gruppo')
        bc.contentPane(region='center',datapath='.record').anagraficaPane(tipo_anagrafica='societa')
        frame = bc.contentPane(region='right',width='400px').bagGrid(storepath='#FORM.record.orario',title='Orario',
                                                                pbl_classes='*',struct=self.struct_orario,
                                                                margin='2px',addrow=False,delrow=False)
        bar = frame.bottom.slotToolbar('*,genera_cal,2')
        bar.genera_cal.slotButton('Genera calendario',ask=dict(title='Genera calendario',
                                                                fields=[dict(name='data_fine',lbl='Fino al',tag='dateTextBox')],
                                                                onEnter=False),action="""FIRE #FORM.generaCalendario=data_fine;""")
        bar.dataRpc(None,self.generaCalendarioNegozio,data_fine='^#FORM.generaCalendario',_onCalling="genro.bp(true)")
        bottom = bc.tabContainer(region='bottom',height='260px',margin='2px')
        self.negozioLavoranti(bottom.contentPane(title='Lavoranti'))
        self.negozioListini(bottom.contentPane(title='Listini'))
        #self.negozioListini(bottom.contentPane(title='Listini'))
    
    @public_method
    def generaCalendarioNegozio(self,data_fine=None):
        tblcal = self.db.table('barber.calendario')
        for staff in self.db.table('barber.staff').query(where="""@user_id.@tags.@tag_id.hierarchical_code=:btag""",
                                                            btag='barber').fetch():
            tblcal.generaCalendario(staff['id'],data_fine=data_fine)

    def struct_orario(self,struct):
        r=struct.view().rows()
        r.cell('giorno',width='4em')
        r.cell('orario',width='100%',edit=True)

    def negozioLavoranti(self,pane):
        pane.dialogTableHandler(relation='@lavoranti',pbl_classes='True')

    def negozioListini(self,pane):
        pane.dialogTableHandler(relation='@listino',pbl_classes='True')

 
    @public_method
    def th_onLoading(self,record,newrecord,loadingParameters,recInfo,**kwargs):
        if not record['orario']:
            orario = Bag()
            for i,giorno in enumerate(('Lun','Mar','Mer','Gio','Ven','Sab','Dom')):
                orario.setItem('d_%i.giorno' %i,giorno)
                orario.setItem('d_1.orario',None)
            record['orario'] = orario

    def th_options(self):
        return dict(dialog_parentRatio=.9)


class ProfiloNegozio(Form):
    def th_form(self,form):
        form.store.attributes.update(startKey=self.rootenv.getItem('current_negozio_id'))
        self.full_form(form)



