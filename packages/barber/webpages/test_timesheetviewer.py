# -*- coding: UTF-8 -*-

""" Gestione appuntamenti"""
from gnr.core.gnrbag import Bag
from gnr.core.gnrdecorator import public_method


# --------------------------- GnrWebPage subclass ---------------------------
class GnrCustomWebPage(object):
    py_requires="""public:Public,th/th:TableHandler,
                  gnrcomponents/timesheet_viewer/timesheet_viewer:TimesheetViewer"""
    js_requires='appuntamenti'
    css_requires='appuntamenti'
    maintable='barber.calendario'
    pageOptions={'openMenu':False,'enableZoom':False,'liveUpdate':True}
    auth_main='user,segr'


    @property
    def formAppuntamento(self):
        if not hasattr(self,'_formAppuntamento'):
            page = self.pageSource()
            form = page.thFormHandler(table='barber.appuntamento',formResource='FormDashboard',modal=True,
                        dialog_height='250px',dialog_width='600px',
                        formId='event',datapath='main.event')
            self._formAppuntamento = form
        return self._formAppuntamento

    def main(self, root, **kwargs):       
        pblroot = root.rootBorderContainer(title='Gestione appuntamenti', datapath='main',design='sidebar')
        #pblroot.dataFormula('.data_selezionata','oggi',oggi=self.workdate,_onStart=True)
        pblroot.dataRpc('.calendario',self.getCalendario,_onStart=True,_fired='^.rebuild_calendario')
        pblroot.dataController("""frm.load({destPkey:appuntamento_id})""",
                        frm=self.formAppuntamento.js_form,
                        subscribe_modifica_appuntamento=True)
        pblroot.dataController("""frm.newrecord({calendario_id:calendario_id})""",
                        frm=self.formAppuntamento.js_form,
                        subscribe_nuovo_appuntamento=True)
        frame = pblroot.timesheetViewer(region='center',value='^.calendario',
                                selfsubscribe_edit_calendar="""
                                PUBLISH nuovo_appuntamento = {calendario_id:$1.calendario_id};
                                """,
                                selfsubscribe_edit_slot="PUBLISH modifica_appuntamento = {appuntamento_id:$1.appuntamento_id}",
                                slotFiller='timetable',work_start=8,work_end=22,
                                slot_duration=20)
        pblroot.onDbChanges("""FIRE .rebuild_calendario""", table='barber.appuntamento',frame=frame)
    
    @public_method
    def getCalendario(self):
        tblcal = self.db.table('barber.calendario')
        tblapp = self.db.table('barber.appuntamento')

        calendario = tblcal.query(where='$data>=:env_workdate',
                    columns="""$id,$staff_id,$slots,$ora_inizio,$ora_fine,$data,$barber""",
                                order_by='$data').fetch()
        barber_cols = sorted(list(set([r['barber'] for r in calendario])))
        
        result = Bag()
        appuntamenti = self.db.table('barber.appuntamento').query(where='$data>=:env_workdate',
                                                                 columns="""$id,$cognome,$nome,$telefono,
                                                                 $ora_inizio,$ora_fine,
                                                                 $prestazioni_prenotate,$calendario_id,
                                                                 $colore""").fetchGrouped('calendario_id')
        tpl = """<div style="font-size:.8em;line-height:10px;">$nome $cognome<br><i>$prestazioni_prenotate</i></div>"""

        for cal_day in calendario:
            daylabel = self.toText(cal_day['data'],format='yyyy_MM_dd')
            calcontent = result.getItem(daylabel)
            if calcontent is None:
                calcontent = Bag()
                for barber in barber_cols:
                    calcontent.setItem(barber,Bag(),name=barber)
                result.setItem(daylabel,calcontent,day=cal_day['data'])
            appuntamentiNode = calcontent.getNode(cal_day['barber'])
            appuntamentiNode.attr.update(time_start=cal_day['ora_inizio'],
                                     time_end=cal_day['ora_fine'],
                                      calendario_id=cal_day['id'])
            cal_appuntamenti = appuntamenti.get(cal_day['id'],[])
            val = appuntamentiNode.value
            for r in cal_appuntamenti:
                val.setItem(self.toText(r['ora_inizio'],format='HH_mm'),
                                                None,time_start=r['ora_inizio'],
                                                time_end=r['ora_fine'],
                                                appuntamento_id=r['id'],
                                                background_color=r['colore'],
                                                template=tpl,nome=r['nome'],
                                                cognome=r['cognome'],
                                                prestazioni_prenotate=r['prestazioni_prenotate'])
        return result,dict(channels=barber_cols)
