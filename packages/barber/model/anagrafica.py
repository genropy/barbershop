#!/usr/bin/env python
# encoding: utf-8
# VISTOAL: 291008
# 
from gnr.core.gnrdecorator import metadata
from gnr.core.gnrbag import Bag

class Table(object):

    def config_db(self, pkg):
        """gesser.anagrafica"""
        tbl =  pkg.table('anagrafica',pkey='id',name_plural='!![it]Anagrafiche',
                          name_long=u'!![it]Anagrafica', rowcaption='$ragione_sociale',
                          caption_field='ragione_sociale',
                          unifyRecordsTag='admin')
        self.sysFields(tbl)
        tbl.column('ragione_sociale',name_long ='!![it]Ragione sociale',
                    indexed=True,group='001',unaccent=True)
        tbl.column('cognome',name_long='!![it]Cognome',
                    _sendback=True,validate_case='c',group='002')
        tbl.column('soprannome', name_long='!![it]Soprannome')
        tbl.column('nome',name_long='!![it]Nome',_sendback=True,validate_case='c',group='003')
        tbl.column('indirizzo_esteso',name_long='!![it]Indirizzo esteso',group='*')
        tbl.column('geocoords', name_long='!![it]Geocoder coords',group='_')
        tbl.column('societa','B',name_long=u'!![it]Società',_sendback=True,group='004')
        tbl.column('indirizzo',name_long='!![it]Indirizzo',validate_regex='![?]{2,2}', validate_regex_error='!![it]Civico invalido',group='b_indirizzi.01')
        tbl.column('numero_civico',name_long='!![it]Numero Civico',group='*')
        tbl.column('cap',name_long='!![it]Cap',indexed=True,group='b_indirizzi.02')
        tbl.column('localita',name_long=u'!![it]Località',indexed=True,group='b_indirizzi.03')
        tbl.column('provincia',size='2',name_long=u'!![it]Provincia',
                    name_short='Prov.',indexed=True, stats=True,
                    group='b_indirizzi.04').relation('glbl.provincia.sigla',
                    mode='foreignkey',one_group='_',many_group='_')
        tbl.column('comune_id',size='22',name_long='!![it]Comune',group='_').relation('glbl.comune.id',mode='foreignkey',relation_name='anagrafiche',one_group='b_indirizzi.05')

        tbl.column('nazione',size='2',name_long='!![it]Nazione',
                    group='b_indirizzi.06').relation('glbl.nazione.code',mode='foreignkey',one_group='_',many_group='_')
        tbl.column('titolo',name_long='!![it]Titolo',group='*')
        tbl.column('codice_fiscale',size=':16',name_long='!![it]Codice fiscale',indexed=True,group='c_datifiscali.01')
        tbl.column('partita_iva',size=':20',name_long='!![it]Partita Iva',indexed=True,group='c_datifiscali.02')
        tbl.column('rea',name_long='!![it]REA',group='c_datifiscali.03')
        tbl.column('rea_provincia',size='2',name_long=u'!![it]Provincia REA',name_short='Pr. REA',indexed=True,group='b_indirizzi.07').relation('glbl.provincia.sigla',
                    mode='foreignkey',one_group='_',many_group='_')
        tbl.column('data_nascita','D',name_long='!![it]Data di nascita',group='c_datifiscali.04')
        tbl.column('luogo_nascita',name_long='!![it]Luogo di nascita',group='c_datifiscali.05')
        tbl.column('provincia_nascita',size='2',name_long='!![it]Provincia di nascita',group='c_datifiscali.06').relation('glbl.provincia.sigla',
                    mode='foreignkey',one_group='_',many_group='_')
        tbl.column('sesso',size=':2',name_long='!![it]Sesso',group='c_datifiscali.07')
        tbl.column('note',name_long='!![it]Note',group='*')
        tbl.column('telefono',name_long='!![it]Telefono',group='d_comunicazioni.001')
        tbl.column('cellulare',name_long='!![it]Cellulare',group='d_comunicazioni.003')
        tbl.column('chat',name_long='!![it]Chat',group='d_comunicazioni.007')
        tbl.column('email',name_long='!![it]Email principale',group='d_comunicazioni.012')
        tbl.column('www',name_long='!![it]Internet',group='d_comunicazioni.014',)
        tbl.formulaColumn('indirizzo_completo',"$ragione_sociale||' - '||$indirizzo||' - '||$cap||' '||$localita||' '||$provincia",group='*') 
        tbl.formulaColumn('cap_loc_pr',"coalesce($cap,'')||' '||coalesce($localita,'')||' '||coalesce($provincia,'')",group='*') 
        tbl.formulaColumn('cognome_nome',"$cognome||' '||$nome",group='*') 
        tbl.formulaColumn('eta', "extract(YEAR FROM age($data_nascita))", dtype='L', name_long=u'!![it]Età')
        tbl.formulaColumn('ragione_sociale_norm',self.normalizeText('$ragione_sociale'),name_long='!![it]Rag.Soc Normalizzata',group='005')  

    def defaultValues(self):
        return dict(nazione='IT')



    def communication_quicksender(self,record=None):
        return dict(email='$email',mobile='$cellulare')

 
