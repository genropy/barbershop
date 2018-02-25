var appuntamenti = {
    slotsInGriglia:function(row){
        var slots = row.slots.replace(/^-*|-*$/gim, "");
        return slots.split('').map(function(slot){
            if(slot=='O'){
                return '<div class="gridslot freeslot"></div>';
            }else if(slot=='X'){
                return '<div class="gridslot busyslot"></div>';
            }else{
                return '<div class="gridslot notavailable"></div>';
            }
        }).join('');
    }
};

var builder_appuntamenti = {

    costruisciSlots:function(sourceNode,slots){
        sourceNode.getValue().popNode('slots_root');
        var root = sourceNode._('div',{_class:'root_appuntamenti'});
        var root_header = root._('div',{_class:'root_header'});
        var root_content = root._('div',{_class:'root_content'});

        slots.getNodes().forEach(function(n){

        });
    }
};


//########################   TIMEVIEWER FROM DOCTOR PAGE  ###################################################################################################


dojo.declare('ViewerAppuntamenti',null,{
    constructor:function(sourceNode,kw){
        //this.data = data;
        var data = this.data();
        this.sourceNode = sourceNode;
        this.rowHeight = 40;
        this.nrows = data.len();
        this.sx = 2;
        this.slotCell=null;
        this.leftColWidth = 60;
        this.headerHeight = 20;
        this.rounded=6;
        this.location_bag = new gnr.GnrBag();
        this.totheight = (this.rowHeight*this.nrows)+'px';

    },
    data:function(){
        return genro.getData('timetable.slots') || new gnr.GnrBag();
    },


    toStrTime:function(t){
        return dojo.number.format(t[0],{pattern:'00'})+':'+dojo.number.format(t[1],{pattern:'00'});
    },

    showUnifiedLocations:function(){
        this.sourceNode.freeze().clearValue();
        this.buildViewer(this.sourceNode,this.data());
        this.buildLocationColorKeys(this.footerSourceNode);
        this.sourceNode.unfreeze();
    },
    
    buildLocationColorKeys:function(footerNode){
        footerNode.freeze().clearValue();
        var location_keys = this.location_bag.keys();
        var slotbarAttr = {slots:'*',margin_top:'2px',toolbar:true};
        var i=1;
        this.location_bag.forEach(function(n){
            slotbarAttr['slots'] += ','+n.label;
            slotbarAttr[n.label] = n._value;
            slotbarAttr[n.label+'__class'] = 'location_'+i +' legendNode'
            i++;
        })
        slotbarAttr['slots'] += ',*'
        footerNode._('slotBar',slotbarAttr);
        footerNode.unfreeze();

    },
    
    showLocationTabs:function(){
        this.sourceNode.freeze().clearValue();
        var that = this;
        var tc = this.sourceNode._('tabContainer',{'height':'100%'});
        var i = 1;
        this.data().forEach(function(locationNode){
            pane = tc._('contentPane', {title:locationNode.attr.location_name});
            that.buildViewer(pane,locationNode.getValue(),i);
            i++;
        }, 'static');
        this.sourceNode.unfreeze()
    },
    
    buildViewer:function(pane,data,counter){     
        var min_h=100;
        var max_h=0;
        var slots,start_hour,end_hour;
        data.walk(function(n){
            slots = n.attr.slots;
            if(slots){
                start_hour = slots[0]['s_time'][0]
                end_hour = slots[(slots.length-1)]['e_time'][0]
                min_h = Math.min(min_h,start_hour);
                max_h = Math.max(max_h,end_hour);
            }
        });
        max_h++;
        min_h--;
        var maxhour = max_h-min_h;
           
        counter = counter || 'unified';
        var rl,rr,leftCell;
        var cont = pane._('div',{_class:'timerule_container'});
        
        var ruler = pane._('div',{'position':'absolute',top:0,left:this.leftColWidth+'px',right:0,id:'timerule_ruler_' + counter,
                             height:this.headerHeight+'px',background:'white',overflow:'hidden'});
        ruler = ruler._('div',{'top':0,left:0,bottom:0,width:(max_h*60*this.sx)+'px'});
        
        
        var lc = cont._('div',{'_class':'timerule_lc','id':'timerule_lc_'+counter,'width':this.leftColWidth-1+'px',border_right:'1px solid gray',top:this.headerHeight+'px'});
        var lc_inner = lc._('div',{'height':this.totheight,'position':'absolute', 
                                    'left':'0','top':'0','right':'0'});
        
        var rc = cont._('div',{'_class':'timerule_rc','left':this.leftColWidth+'px',top:this.headerHeight+'px',
                            'onscroll':'dojo.byId("timerule_lc_'+counter+'").scrollTop=event.target.scrollTop; dojo.byId("timerule_ruler_'+counter+'").scrollLeft=event.target.scrollLeft;'});

        var rc_inner = rc._('div',{'height':this.totheight,'position':'absolute', 
                              'left':'0','top':'0','width':(maxhour*60*this.sx)+'px'});
        var ruler_slot;
        for (var i=min_h; i <= max_h; i++) {
            ruler_slot = ruler._('div',{'width':60*this.sx+'px',height:this.headerHeight+'px',position:'relative',display:'inline-block'});
            ruler_slot._('div',{innerHTML:i+':00','position':'absolute',top:'1px',left:'1px',right:'0px',
                                bottom:'1px',background:'gray',color:'white',text_align:'center',font_size:'12px'});
        };
        ruler_slot = ruler._('div',{'width':'18px',height:this.headerHeight+'px',position:'relative',display:'inline-block'});
        var that = this;
        data.forEach(function(n){
            rl = lc_inner._('div',{_class:'timerule_row',height:that.rowHeight+'px'});
            leftCell = rl._('div',{_class:'timerule_cell',right:'2px',left:0})._('div',{'_class':'timerule_slot'});
            leftCell._('div',{'innerHTML':genro.format(n.attr.day,{selector:'date',formatLength:'short',rounded_top:that.rounded}),_class:'timerule_date'});
            leftCell._('div',{'innerHTML':n.attr.weekday,_class:'timerule_wd',rounded_bottom:that.rounded-2,border:'1px solid darkred'});
            that.buildSlots(rc_inner,n,min_h)
        });
    },

    buildSlots:function(pane,n,min_h){
        var that = this;
        var row = pane._('div',{_class:'timerule_row',height:this.rowHeight+'px'});
        dojo.forEach(n.attr.slots,function(slot){
            slot['day'] = n.attr.day;
            slot['doctor_id'] = that.doctor_id;
            try{
                that.buildOneSlot(row,slot,min_h);
            }catch(e){
                console.log('errore',slot)
            }
            
        });        
    },

    getLocationCounter:function(slot){
        var location_id = slot.location_id;
        var location_name = slot.location_name;
        var result;
        var counter = this.location_bag.index(location_id);
        if(counter<0){
            counter =this.location_bag.len();
            this.location_bag.setItem(location_id,location_name);
        }
        return counter+1;
    },
    
    buildOneSlot:function(pane,n,min_h){
        var sminutes = n.s_time[0]*60+n.s_time[1]-(min_h*60);
        var left = sminutes*this.sx;
        var width = n.duration*this.sx;
        var cell = pane._('div',{_class:'timerule_cell location_'+this.getLocationCounter(n),'left':left+'px','width':width+'px'});
        var slotType = 'production_rule';
        if(n.denied){
             slotType = 'denied_rule';
        }
        if (n.case_code){
            slotType = 'busy_slot'
        }
        var sourceNode = this.sourceNode;
        var that = this;
        var slot = cell._('div',{'_class':'timerule_slot freeslot',font_size:'9px',text_align:'left',
                                rounded:this.rounded,border:'1px solid silver'});
        var slotAttr = slot.getParentNode().attr;
        var start_time = dojo.number.format(n.s_time[0],{pattern:'00'})+':'+dojo.number.format(n.s_time[1],{pattern:'00'});
        var end_time = dojo.number.format(n.e_time[0],{pattern:'00'})+':'+dojo.number.format(n.e_time[1],{pattern:'00'});
        var tpltime = start_time+'-'+end_time+" ("+n.duration+"')";  

        slot._('div',{'innerHTML':n.location_name,_class:'timerule_slot_location',rounded_top:this.rounded});
        var slotBody = slot._('div',{_class:'timerule_slot_body'});
        if(n.case_code){
            slotBody._('div',{'innerHTML':'Case:'+n.case_code});
            slotAttr['background'] = 'red';
            slotAttr['color'] = 'white';
            slotAttr['slotType'] = 'evt'
            slotAttr['pkey'] = n.event_id;
            slotAttr['case_id'] = n.case_id;
        }
        else if(n.denied){
            slotAttr['background'] = 'silver';
            slotAttr['opacity'] = .2;
            slotAttr['slotType'] = 'denied'

            objectPop(slotAttr,'connect_ondblclick');
            slotBody._('div',{'innerHTML':n.deny_reason,_class:'timerule_slot_body'});
        }
        else if(n.activity_type){
            slotAttr['slotType'] = 'activity';
            slotAttr['pkey'] = n.event_id;
            slotBody._('div',{'innerHTML':n.activity_type,_class:'timerule_slot_body'});
        }
        else{
            slotAttr['slot'] = n;
            slotAttr['slotType'] = 'freeSlot';
        }

        var slotFooter = slot._('div',{_class:'timerule_slot_time',rounded_bottom:this.rounded});
        slotFooter._('span',{'innerHTML':tpltime});
        if(n.room_name){
             slotFooter._('span',{'innerHTML':' Room:'+n.room_name});
        }
    },

    getDateDataNode:function(date,bag){
        var result = null;
        bag = bag || this.data();
        bag.walk(
            function(n){
                var day = n.attr.day;
                if( day.getMonth()==date.getMonth() && day.getDate()==date.getDate() ){
                result = n;
                return false;
            }
        });
        return result;
    }
});