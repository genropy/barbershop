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
        fb.field('data')
        fb.field('ora_inizio')
        fb.field('ora_fine')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')


class FormDashboard(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.div(margin='10px').formbuilder(cols=2, border_spacing='4px')
        fb.field('tipo_appuntamento',hasDownArrow=True,selected_indisponibile='.indisponibile')
        fb.br()
        fb.field('cognome',hidden='^.indisponibile')
        fb.field('nome',hidden='^.indisponibile')
        fb.field('telefono',hidden='^.indisponibile')
        fb.field('email',hidden='^.indisponibile')
        fb.div(colspan=2,hidden='^.indisponibile').checkBoxText(value='^#FORM.record.listini_pkeys',cols=2,table='barber.listino')

        fb.dataRpc('#FORM.record.durata',self.proponiDurata,
                        listini_pkeys='^#FORM.record.listini_pkeys',
                        _indisponibile='=.indisponibile',
                        _if='listini_pkeys && !_indisponibile',_userChanges=True,_delay=300)


        fb.dataRpc(None,self.proponiOrario,
                        durata='^#FORM.record.durata',ora_inizio='^#FORM.record.ora_inizio',
                        calendario_id='=#FORM.record.calendario_id',
                        _onResult="""this.setRelativeData('#FORM.record.ora_inizio',result.getItem('ora_inizio'),null,null,'proposta_ora_inizio');
                                    this.setRelativeData('#FORM.record.ora_fine',result.getItem('ora_fine'));
                        """,_userChanges=True,_onCalling="""
                            if(_triggerpars.kw.reason=='proposta_ora_inizio'){
                                return false;
                            }
                            if(kwargs.ora_inizio){
                                kwargs.ora_inizio = asTypedTxt(kwargs.ora_inizio,'H');
                            }
                        """,_indisponibile='=.indisponibile',_if='durata && !_indisponibile')
        fb.field('ora_inizio',validate_notnull=True)
        fb.field('ora_fine',disabled='^.indisponibile?=!#v',validate_notnull=True)


    @public_method
    def proponiDurata(self,listini_pkeys=None):
        listini = self.db.table('barber.listino').query(where='$id IN :listini_pkeys',listini_pkeys=listini_pkeys.split(',')).fetch()
        return sum([(r['durata_media'] or 1) for r in listini])

    @public_method
    def proponiOrario(self,durata=None,calendario_id=None,ora_inizio=None):
        record_calendario = self.db.table('barber.calendario').record(calendario_id).output('record')
        data = record_calendario['data']
        ts_inizio_giornata = datetime(data.year,data.month,data.day,0,0)
        offset = None
        if ora_inizio:
            offset = (ora_inizio.hour*60 + ora_inizio.minute)/10
        slots = record_calendario['slots']
        pos = slots.index(durata*'O',offset)
        ora_inizio_app = ts_inizio_giornata + relativedelta(minutes=10*pos)
        ora_fine_app = ora_inizio_app + relativedelta(minutes=10*durata)
        return Bag(dict(ora_inizio=ora_inizio_app.time(),ora_fine=ora_fine_app.time()),durata=durata)

    def th_bottom_custom(self,bottom):
        bar = bottom.bar.replaceSlots('revertbtn','revertbtn,deletebtn')
        bar.deletebtn.button('!!Elimina',action='this.form.do_deleteItem(); this.form.abort();')

    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px',modal=True,newTitleTemplate='Appuntamento di $@calendario_id.@staff_id.identificativo del $data',titleTemplate='Appuntamento di $@staff_id.identificativo del $data')

    @public_method
    def th_onLoading(self,record,newrecord,loadingParameters,recInfo,**kwargs):
        if newrecord and record['calendario_id']:
            record['data'] = record['@calendario_id.data']
