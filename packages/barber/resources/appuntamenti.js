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

};