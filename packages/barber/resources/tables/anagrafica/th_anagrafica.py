#!/usr/bin/python
# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('ragione_sociale')
        r.fieldcell('cognome')
        r.fieldcell('soprannome')
        r.fieldcell('nome')
        r.fieldcell('indirizzo_esteso')
        r.fieldcell('geocoords')
        r.fieldcell('societa')
        r.fieldcell('indirizzo')
        r.fieldcell('numero_civico')
        r.fieldcell('cap')
        r.fieldcell('localita')
        r.fieldcell('provincia')
        r.fieldcell('comune_id')
        r.fieldcell('nazione')
        r.fieldcell('titolo')
        r.fieldcell('codice_fiscale')
        r.fieldcell('partita_iva')
        r.fieldcell('rea')
        r.fieldcell('rea_provincia')
        r.fieldcell('data_nascita')
        r.fieldcell('luogo_nascita')
        r.fieldcell('provincia_nascita')
        r.fieldcell('sesso')
        r.fieldcell('note')
        r.fieldcell('telefono')
        r.fieldcell('cellulare')
        r.fieldcell('chat')
        r.fieldcell('email')
        r.fieldcell('www')

    def th_order(self):
        return 'ragione_sociale'

    def th_query(self):
        return dict(column='ragione_sociale', op='contains', val='')



class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('ragione_sociale')
        fb.field('cognome')
        fb.field('soprannome')
        fb.field('nome')
        fb.field('indirizzo_esteso')
        fb.field('geocoords')
        fb.field('societa')
        fb.field('indirizzo')
        fb.field('numero_civico')
        fb.field('cap')
        fb.field('localita')
        fb.field('provincia')
        fb.field('comune_id')
        fb.field('nazione')
        fb.field('titolo')
        fb.field('codice_fiscale')
        fb.field('partita_iva')
        fb.field('rea')
        fb.field('rea_provincia')
        fb.field('data_nascita')
        fb.field('luogo_nascita')
        fb.field('provincia_nascita')
        fb.field('sesso')
        fb.field('note')
        fb.field('telefono')
        fb.field('cellulare')
        fb.field('chat')
        fb.field('email')
        fb.field('www')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')
