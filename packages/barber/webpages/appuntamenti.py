# -*- coding: UTF-8 -*-

""" Gestione appuntamenti"""
from gnr.core.gnrbag import Bag
from gnr.core.gnrdecorator import public_method


# --------------------------- GnrWebPage subclass ---------------------------
class GnrCustomWebPage(object):
    py_requires="""public:Public,component_appuntamenti:AppuntamentiManager"""
    js_requires='appuntamenti'
    css_requires='appuntamenti'
    maintable='barber.calendario'
    pageOptions={'openMenu':False,'enableZoom':False,'liveUpdate':True}
    auth_main='user,segr'




    def main(self, root, **kwargs):       
        pblroot = root.rootBorderContainer(title='Gestione appuntamenti', datapath='main',design='sidebar')
        pblroot.appuntamentiManager(region='center')
