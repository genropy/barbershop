#!/usr/bin/env python
# encoding: utf-8
from gnr.app.gnrdbo import GnrDboTable, GnrDboPackage

class Package(GnrDboPackage):
    def config_attributes(self):
        return dict(comment='barber package',sqlschema='barber',sqlprefix=True,
                    name_short='Barber', name_long='Barbershop', name_full='Barber')
                    
    def config_db(self, pkg):
        pass

    def custom_type_cambio(self):
        return dict(dtype='N',size='12,6',format='#,###.000000')

    def custom_type_money(self):
        return dict(dtype='N', size='12,2', format='###.00', default=0)


        
class Table(GnrDboTable):
    def anagraficaAliases(self,tbl,group=None,group_contatti=None,group_indirizzo=None):
        tbl.aliasColumn('ragione_sociale',relation_path='@anagrafica_id.ragione_sociale',group=group)
        tbl.aliasColumn('cognome',relation_path='@anagrafica_id.cognome',group=group)
        tbl.aliasColumn('nome',relation_path='@anagrafica_id.nome',group=group)
        tbl.aliasColumn('eta',relation_path='@anagrafica_id.eta',group=group)
        tbl.aliasColumn('codice_fiscale',relation_path='@anagrafica_id.codice_fiscale',group=group)
        tbl.aliasColumn('partita_iva',relation_path='@anagrafica_id.partita_iva',group=group)
        tbl.aliasColumn('data_nascita',relation_path='@anagrafica_id.data_nascita',group=group)
        tbl.aliasColumn('luogo_nascita',relation_path='@anagrafica_id.luogo_nascita',group=group)
        tbl.aliasColumn('ragione_sociale_norm',relation_path='@anagrafica_id.ragione_sociale_norm',group='_')
        tbl.aliasColumn('indirizzo',relation_path='@anagrafica_id.indirizzo',group=group_indirizzo or group)
        tbl.aliasColumn('cap',relation_path='@anagrafica_id.cap',group=group_indirizzo or group)
        tbl.aliasColumn('localita',relation_path='@anagrafica_id.localita',group=group_indirizzo or group)   
        tbl.aliasColumn('provincia',relation_path='@anagrafica_id.provincia',group=group_indirizzo or group) 
        tbl.aliasColumn('nazione',relation_path='@anagrafica_id.nazione',group=group_indirizzo or group) 
        tbl.aliasColumn('provincia_nascita',relation_path='@anagrafica_id.provincia_nascita',group=group)
        tbl.aliasColumn('societa',relation_path='@anagrafica_id.societa',group=group) 
        tbl.aliasColumn('telefono',relation_path='@anagrafica_id.telefono',
                        group=group_contatti or group) 
        tbl.aliasColumn('cellulare',relation_path='@anagrafica_id.cellulare',
                        group=group_contatti or group) 
        tbl.aliasColumn('email',relation_path='@anagrafica_id.email',
                        group=group_contatti or group) 

    def onLoading_negozio(self,record,newrecord,loadingParameters,recInfo,**kwargs):
        currentEnv = self.db.currentEnv
        if newrecord and 'negozio_id' in record and currentEnv.get('current_negozio_id'):
            record['negozio_id'] = self.db.currentEnv['current_negozio_id']
