# -*- coding: UTF-8 -*-

from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrdecorator import public_method

class View(BaseComponent):

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('data')
        r.fieldcell('staff_id')
        r.fieldcell('slots',width='100%')

    def th_order(self):
        return 'data'

    def th_query(self):
        return dict(column='data', op='contains', val='')


class ViewDashboard(BaseComponent):
    js_requires='appuntamenti'
    css_requires='appuntamenti'

    def th_struct(self,struct):
        r = struct.view().rows()
        r.fieldcell('data')
        r.fieldcell('staff_id')
        r.fieldcell('slots',_customGetter='function(row){return appuntamenti.slotsInGriglia(row)}',width='100%')

    def th_order(self):
        return 'data'

 
    def free_slot(self):
        return '<div class="freeslot"></div>'
        

    def th_view(self, view):
        store = view.store
        view.grid.attributes.update(canSort=False,multiSelect=False,
                                    autoSelect="var r = this.indexByRowAttr('slots','%s','%%'); return r<0?0:r;" %self.free_slot())

    def th_condition(self):
        return dict(condition="""(CASE WHEN :st_id IS NOT NULL THEN $staff_id=:st_id ELSE TRUE END) AND 
                    $data>=:env_workdate""",condition_st_id='^.staff_id')
    


class FormDashboard(BaseComponent):
    def th_form(self,form):
        pane = form.center.contentPane()
        pane.dialogTableHandler(relation='@appuntamenti',formResource='FormDashboard')

    def th_options(self):
        return dict(showtoolbar=False)


class Form(BaseComponent):

    def th_form(self, form):
        pane = form.record
        fb = pane.formbuilder(cols=2, border_spacing='4px')
        fb.field('data')
        fb.field('staff_id')
        fb.field('slots')


    def th_options(self):
        return dict(dialog_height='400px', dialog_width='600px')

