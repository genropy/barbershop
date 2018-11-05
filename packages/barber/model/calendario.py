# encoding: utf-8
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbag import Bag
from dateutil.relativedelta import relativedelta

class Table(object):
    def config_db(self,pkg):
        tbl=pkg.table('calendario', pkey='id', name_long='!![it]Calendario', 
                        name_plural='!![it]Calendario',
                        partition_negozio_id='negozio_id')
        self.sysFields(tbl)
        tbl.column('data', dtype='D', name_long='!![it]Data')
        tbl.column('staff_id',size='22', group='_', name_long='!![it]Staff'
                    ).relation('staff.id', relation_name='calendario', mode='foreignkey', onDelete='raise')
        tbl.column('slots', size=':144', name_long='!![it]Slots')
        tbl.column('ora_inizio', dtype='H', name_long='!![it]Ora inizio')
        tbl.column('ora_fine', dtype='H', name_long='!![it]Ora Fine')

        tbl.aliasColumn('negozio_id','@staff_id.negozio_id',group='_')
        tbl.aliasColumn('barber','@staff_id.identificativo',group='_')

       # tbl.aliasColumn('caption_calendario',"""@staff_id.identificativo || ' ' || to_char($ts,'YYYY-MM-DD')""",group='_')

    @public_method
    def generaCalendario(self,staff_id=None,data_fine=None):
        rec_staff = self.db.table('barber.staff').record(staff_id).output('record')
        rec_negozio = self.db.table('barber.negozio').record(self.db.currentEnv['current_negozio_id']).output('record')
        orario = rec_staff['orario'] or rec_negozio['orario']
        ultimo_cal = self.query(where='$staff_id=:sid',sid=staff_id,order_by='$data desc',limit=1).fetch()
        data = ultimo_cal[0]['data'] if ultimo_cal else self.db.workdate
        dt_giorno = relativedelta(days=1)
        while data<data_fine:
            stringa_orario = orario.getItem('d_%i.orario' %data.weekday())
            if stringa_orario:
                self.creaGiornata(staff_id=staff_id,data=data,stringa_orario=stringa_orario)
            data+=dt_giorno
        self.db.commit()

    def creaGiornata(self,staff_id=None,data=None,stringa_orario=None):
        record = self.newrecord(staff_id=staff_id,data=data)
        ftt = self.db.application.catalog.fromTypedText
        ora_inizio_giornata,ora_fine_giornata = None,None
        for chunk in stringa_orario.split(','):
            ora_inizio,ora_fine = chunk.split('-')
            ora_inizio = ftt('%s::H' %ora_inizio)
            ora_fine=ftt('%s::H' %ora_fine)
            if not ora_inizio_giornata:
                ora_inizio_giornata = ora_inizio
            self.setSlotInterval(record,ora_inizio=ora_inizio, ora_fine=ora_fine,
                                        status='O')
        ora_fine_giornata = ora_fine
        record['ora_inizio'] = ora_inizio_giornata
        record['ora_fine'] = ora_fine_giornata
        self.insert(record)


    def aggiornaSlots(self,calendario_id=None):
        with self.recordToUpdate(calendario_id) as record:
            record['slots'] = record['slots'].replace('X','O')
            appuntamenti = self.db.table('barber.appuntamento').query(where='$calendario_id=:calid',calid=calendario_id,
                                                                    order_by='$ora_inizio').fetch()
            
            for app in appuntamenti:
                self.setSlotInterval(record,ora_inizio=app['ora_inizio'],ora_fine=app['ora_fine'],status='X')

    def setSlotInterval(self,record,ora_inizio=None,ora_fine=None,status=None):
        slots = list(record['slots'])
        def getTimeIndex(t):
            return  (t.hour*60 + t.minute)/10
        for k in range(getTimeIndex(ora_inizio),getTimeIndex(ora_fine)):
            if status=='X' and slots[k]=='X':
                raise self.exception('business_logic',msg='Orario non disponibile')

            slots[k] = status
        record['slots'] = ''.join(slots)

    def defaultValues(self):
        return dict(slots='-'*144)
    
    @public_method
    def ottieniDettaglioGiornata(self,data_selezionata=None):
        result = Bag()
        cal = self.query(where='$data=:data_selezionata',data_selezionata=data_selezionata,
                    columns="""$id,$staff_id,$barber,
                                $slots,$ora_inizio,$ora_fine""",order_by='$barber').fetch()
        appuntamenti = self.db.table('barber.appuntamento').query(where='$data=:data_selezionata',
                                                                 data_selezionata=data_selezionata,
                                                                 columns="""$id,$cognome,$nome,$telefono,
                                                                 $ora_inizio,$ora_fine,
                                                                 $prestazioni_prenotate
                                                                 """).fetchGrouped('calendario_id')

        for giornata in cal:
            result.setItem(giornata['staff_id'],
                            self.appuntamentiBarber(giornata,appuntamenti.get(giornata['id'],[])),
                            barber=giornata['barber'],
                            ora_inizio=giornata['ora_inizio'],
                            ora_fine=giornata['ora_fine'],
                            slots=giornata['slots'])
        return result
        
    def appuntamentiBarber(self,giornata,appuntamenti):
        result = Bag()
        for app in appuntamenti:
            result.setItem(app['id'],None,
                            appuntamento_id=app['id'],
                            cognome=app['cognome'],
                            nome=app['nome'],
                            telefono=app['telefono'],
                            ora_inizio=app['ora_inizio'],
                            ora_fine=app['ora_fine'],
                            calendario_id=giornata['id'],
                            prestazioni_prenotate=app['prestazioni_prenotate'])
        return result