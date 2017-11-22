#!/usr/bin/python
# -*- coding: UTF-8 -*-

def config(root,application=None):
    root.thpage('Negozi',table='barber.negozio',tags='superadmin')
    
    root.thpage('Dati negozio',table='barber.negozio',checkenv='current_negozio_id',
                url_main_call="main_form", formResource="ProfiloNegozio",tags='conf')
                
    root.thpage('Staff',table='barber.staff',checkenv='current_negozio_id',tags='conf')
    root.thpage('Listino',table='barber.listino',checkenv='current_negozio_id',tags='conf')

    root.webpage('Appuntamenti',filepath="/barber/appuntamenti",checkenv='current_negozio_id',tags='segr')

    root.thpage('I miei dati',table='barber.staff',checkenv='staff_id',
                url_main_call="main_form", formResource="ProfiloStaff",
                tags='user')
    
    root.webpage('I miei appuntamenti',table='barber.staff',checkenv='staff_id',
                tags='barber',filepath="/barber/appuntamenti")