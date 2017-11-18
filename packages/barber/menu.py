#!/usr/bin/python
# -*- coding: UTF-8 -*-

def config(root,application=None):
    barber = root.branch('Barbershop')
    barber.thpage('Configurazione',table='barber.aderente')
    #barber.thpage('Negozi',table='barber.negozio')
    #barber.thpage('Lavoranti',table='barber.lavorante')
    #barber.thpage('Listino',table='barber.listino')
