#!/usr/bin/env python
# encoding: utf-8

from gnr.web.gnrwebpage import BaseComponent
from gnr.web.gnrwebstruct import struct_method
from gnr.core.gnrdecorator import extract_kwargs,public_method

class AnagraficaComponent(BaseComponent):
    js_requires='anag'
    css_requires='anag'
    @extract_kwargs(fb=True)
    @struct_method
    def anagrafica_anagraficaPane(self,pane,tipo_anagrafica=None,fb_kwargs=None,
                            linkerBar=True,datapath='.@anagrafica_id',excludeList=None,
                            fldExtraKwargs=None,
                            title=None,openIfEmpty=None,saveIndirizzoEsteso=True,**kwargs):
        frame = pane.roundedGroupFrame(datapath=datapath, title=title, **kwargs)
        if linkerBar:
            frame.top.linkerBar(field='anagrafica_id',label=title or '!![it]Dati anagrafici',table='barber.anagrafica',newRecordOnly=linkerBar=='newRecordOnly', openIfEmpty=openIfEmpty)
        fbkw = dict(cols=2,border_spacing='4px',fld_width='100%',
                    width='100%',colswidth='auto',
                    dbtable='barber.anagrafica',fld_html_label=True,lbl_margin_left='10px')
        fbkw.update(fb_kwargs)
        fb = frame.div(margin_top='5px',margin_right='20px').formbuilder(**fbkw)
        fb._excludedFieldList = excludeList or []
        fb._fldExtraKwargs = fldExtraKwargs or []

        fb.controllerAnagrafica(tipo_anagrafica=tipo_anagrafica)
        if not tipo_anagrafica:
            fb.fieldAnagrafica('societa', lbl_width='9em',lbl=u'!![it]Società')
            fb.fieldAnagrafica('titolo', lbl='!![it]Titolo',tag='dbComboBox',
                                lbl_width='9em',dbtable='barber.titolo')
            fb.fieldAnagrafica('nome',row_hidden='^.societa',
                validate_notnull='^.societa?=!#v',validate_notnull_error='!![it]Campo richiesto')
            fb.fieldAnagrafica('cognome',
                validate_notnull='^.societa?=!#v',validate_notnull_error='!![it]Campo richiesto')
            fb.fieldAnagrafica('ragione_sociale',row_hidden='^.societa?=!#v',
                validate_notnull=True,
                validate_notnull_error='!![it]Campo richiesto',
                lbl='!![it]Ragione sociale',colspan=fbkw.get('cols'))
        
        if tipo_anagrafica == 'persona':
            fb.br()
            fb.fieldAnagrafica('nome',
                validate_notnull=True,
                validate_notnull_error='!![it]Campo richiesto')
            fb.fieldAnagrafica('cognome',
                validate_notnull=True,
                validate_notnull_error='!![it]Campo richiesto')
        if tipo_anagrafica == 'societa':
            fb.br()
            fb.fieldAnagrafica('ragione_sociale',
                validate_notnull=True,
                validate_notnull_error='!![it]Campo richiesto',
                lbl='!![it]Ragione sociale',colspan=fbkw.get('cols'))
    
        gestione_comuni = self.getPreference('dati_glbl.comuni_istat',pkg='barber')
        if saveIndirizzoEsteso:
            fb.fieldAnagrafica('indirizzo_esteso', tag='geoCoderField',
                 colspan=fbkw.get('cols'),
                 lbl='Indirizzo esteso',
                 selected_street_address='.indirizzo',
                 selected_locality='.localita',
                 selected_postal_code='.cap',
                 selected_administrative_area_level_2 ='.$area_level_2',
                 selected_administrative_area_level_3 = '.$comune_denominazione' if gestione_comuni else None,
                 selected_country='.nazione',
                 selected_position='.geocoords',
                 country='=.nazione',
                 ghost='Strada, Numero, Località')
        else:
            if 'indirizzo_esteso' not in fb._excludedFieldList:
                fb.geoCoderField('^.$indirizzo_esteso', 
                 colspan=fbkw.get('cols'),
                 lbl='Cerca Indirizzo',
                 selected_street_address='.indirizzo',
                 selected_locality='.localita',
                 selected_postal_code='.cap',
                 selected_administrative_area_level_2 ='.$area_level_2',
                 selected_administrative_area_level_3 = '.$comune_denominazione' if gestione_comuni else None,
                 selected_country='.nazione',
                 selected_position='.geocoords',
                 country='=.nazione',
                 ghost='Strada, Numero, Località')
        fb.dataFormula(".provincia","provincia",provincia='^.$area_level_2',nazione='=.nazione',
            _if='nazione=="IT"',_else='null',_userChanges=True)

        fb.fieldAnagrafica('indirizzo',colspan=fbkw.get('cols'))
        fb.fieldAnagrafica('provincia')
        if gestione_comuni:
            fb.dataRpc('.comune_id',self.db.table('glbl.comune').pkeyFromCaption,caption='^.$comune_denominazione',_if='caption&&!_comune_id',_comune_id='=.comune_id')
            fb.field('comune_id',selected_sigla_provincia='.provincia')
        fb.fieldAnagrafica('localita',tag='dbCombobox',dbtable='glbl.localita',
                auxColumns='$provincia',
                selected_provincia='.provincia',
                selected_cap='.cap',
                rowcaption='nome')
        fb.fieldAnagrafica('cap')
        fb.fieldAnagrafica('nazione',default_value='IT')
        fb.fieldAnagrafica('telefono')
        fb.fieldAnagrafica('cellulare')
        fb.fieldAnagrafica('email',colspan=2,validate_email=True)
        fb.fieldAnagrafica('chat')
        fb.fieldAnagrafica('www')
        #fb.field('telefono_mv',tag='div')
        if tipo_anagrafica=='persona':
            fb.fieldAnagrafica('sesso',tag='filteringSelect',values='M:Maschio,F:Femmina')
            fb.fieldAnagrafica('data_nascita',popup=False)
            fb.fieldAnagrafica('luogo_nascita')
        fb.fieldAnagrafica('codice_fiscale',
                validate_call="""if(value){return anag_methods.checkCodiceFiscale(value,nazione)} return true;""",
                validate_nazione='=.nazione',
                validate_nodup=True,validate_nodup_warning='Codice fiscale esistente')
        fb.fieldAnagrafica('partita_iva',
                validate_call="""if(value){anag_methods.checkPartitaIva(value,nazione)} return true;""",
                validate_nazione='=.nazione',
                validate_nodup=True,validate_nodup_warning='Partita IVA esistente')
        frame._fb = fb
        return frame

    @struct_method
    def anag_fieldAnagrafica(self, fb, field_name, **kwargs):
        if field_name not in fb._excludedFieldList:
            if field_name in fb._fldExtraKwargs:
                kwargs.update(fb._fldExtraKwargs[field_name])
            fb.field(field_name, **kwargs)

    @struct_method
    def anagrafica_controllerAnagrafica(self,pane,tipo_anagrafica=None):  
        pane.data('#FORM.anagrafica.upCityname','')
        pane.dataFormula('#FORM.anagrafica.upCityname','city.toUpperCase();',city='^.localita',_if='city')
        pane.dataController("""
                            console.log('set ragione sociale', cognome, nome);
                            if (cognome &&  nome){
                                SET .ragione_sociale=cognome+' '+nome;
                            }else{
                                 SET .ragione_sociale=cognome;
                            }
                            """,
                            cognome='^.cognome',
                            nome='^.nome',
                            _if='cognome')

        if tipo_anagrafica:
            pane.dataController("SET .societa = tipo_anagrafica=='societa';",_fired="^.id",
                            tipo_anagrafica=tipo_anagrafica)
        pane.dataController("SET .denominazione_cortesia = ragsoc;",
                          ragsoc='^.ragione_sociale',societa='^.societa',
                          _if='!denominazione_cortesia&&societa',denominazione_cortesia='=.denominazione_cortesia')
        pane.dataController("SET .denominazione_cortesia = (nome||'')+' '+(cognome||'');",
                          cognome='^.cognome',nome='^.nome',societa='^.societa',
                          _if='!denominazione_cortesia&&!societa&&(nome||cognome)',
                          denominazione_cortesia='=.denominazione_cortesia')
