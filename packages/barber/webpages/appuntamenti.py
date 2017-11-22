# -*- coding: UTF-8 -*-

""" Gestione appuntamenti"""

# --------------------------- GnrWebPage subclass ---------------------------
class GnrCustomWebPage(object):
    py_requires='public:Public,th/th:TableHandler'
    js_requires='appuntamenti'
    css_requires='appuntamenti'
    pageOptions={'openMenu':False,'enableZoom':False,'liveUpdate':True}
    auth_main='user,segr'

    def main(self, root, **kwargs):       
        pblroot = root.rootBorderContainer(title='Gestione appuntamenti', datapath='main')
        self.presaAppuntamenti(pblroot.contentPane(region='top',height='50%',datapath='.presaAppuntamenti'))
        self.appuntamentiDelGiorno(pblroot.borderContainer(region='center',datapath='.appuntamentiDelGiorno'))
    
    def presaAppuntamenti(self,pane):
        pane.borderTableHandler(table='barber.calendario',datapath='.calendario',
                                                                viewResource='ViewDashboard',
                                                                formResource='FormDashboard',
                                                                configurable=False,
                                                                vpane_region='left',
                                                                view_store__onStart=True)
        #bc.contentPane(region='center').
        #bc.dataController("""""",
        #                    slots='^.calendario.view.grid.selectedId?slots')

    def appuntamentiDelGiorno(self,bc):
        bc.contentPane(region='center')
