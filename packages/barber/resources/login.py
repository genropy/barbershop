from gnr.web.gnrbaseclasses import BaseComponent

class LoginComponent(BaseComponent):
    login_title = '!!Barbertime Login' #here the title

    def loginSubititlePane(self,pane):#here you can define the sub title as you required a 
        pane.div('Barbertime log in',text_align='center',font_size='.9em',font_style='italic')

    def onUserSelected_barber(self,avatar,data):
        staff_id,negozio_id = self.db.table('barber.staff').readColumns(columns="""$id,$negozio_id""", 
                                                                            where='$user_id=:u_id', 
                                                                            u_id=avatar.user_id)
        if staff_id:
            data['staff_id'] = staff_id
        else:
            cliente_id,negozio_id = self.db.table('barber.cliente').readColumns(columns="""$id,$negozio_id""", 
                                                                            where='$user_id=:u_id', 
                                                                            u_id=avatar.user_id)
            data['cliente_id'] = cliente_id


                                                               
        if negozio_id:
            data.setItem('current_negozio_id', negozio_id)
       #else:
       #    data.setItem('current_aderente_id', aderente_id)        
        