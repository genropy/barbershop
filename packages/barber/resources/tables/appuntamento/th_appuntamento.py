#!/usr/bin/python
# -*- coding: UTF-8 -*-

from datetime import datetime
from dateutil.relativedelta import relativedelta
from gnr.core.gnrbag import Bag

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
        fb.checkBoxText(value='^#FORM.record.listini_pkeys',table='barber.listino',colspan=2)
        fb.dataRpc(None,self.calcolaOrarioNecessario,
                        listini_pkeys='^#FORM.record.listini_pkeys',
                        _if='listini_pkeys',calendario_id='=#FORM.record.calendario_id',
                        _onResult="""SET #FORM.record.ora_inizio = result.getItem('ora_inizio');
                                    SET #FORM.record.ora_fine = result.getItem('ora_fine');
                        """)
        fb.field('ora_inizio')
        fb.field('ora_fine')

    @public_method
    def calcolaOrarioNecessario(self,listini_pkeys=None,calendario_id=None):
        listini = self.db.table('barber.listino').query(where='$id IN :listini_pkeys',listini_pkeys=listini_pkeys.split(',')).fetch()
        durata = sum([(r['durata_media'] or 1) for r in listini])
        record_calendario = self.db.table('barber.calendario').record(calendario_id).output('record')
        slots = record_calendario['slots']
        pos = slots.index(durata*'O')
        data = record_calendario['data']
        ts_inizio_giornata = datetime(data.year,data.month,data.day,0,0)
        ora_inizio_app = ts_inizio_giornata + relativedelta(minutes=10*pos)
        ora_fine_app = ora_inizio_app + relativedelta(minutes=10*durata)
        return Bag(dict(ora_inizio=ora_inizio_app.time(),ora_fine=ora_fine_app.time()))


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px',modal=True)

    @public_method
    def th_onLoading(self,record,newrecord,loadingParameters,recInfo,**kwargs):
        if newrecord and record['calendario_id']:
            record['data'] = record['@calendario_id.data']
