# -*- coding: UTF-8 -*-
            
class GnrCustomWebPage(object):
    py_requires = 'plainindex,public:Public,component_appuntamenti:AppuntamentiManager'

    def index_appuntamenti(self,root,**kwargs):
        pblroot = root.rootBorderContainer(title='Gestione appuntamenti', datapath='main',design='sidebar')
        pblroot.appuntamentiManager(region='center')
    

    def index_barber(self,root,**kwargs):
        pblroot = root.rootBorderContainer(title='Gestione appuntamenti', datapath='main',design='sidebar')
        pblroot.appuntamentiManager(region='center')
    