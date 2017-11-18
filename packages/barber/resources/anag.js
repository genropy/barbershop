var anag_methods={

    checkPartitaIva:function(value, nazione){
        if (!value) { return true;}
        codnaz=nazione || 'IT';
        if (codnaz!='IT') { return true;}
        if (value.match(/^\d+/)) {
                value=codnaz+value;
        }
        if (! value.match(/^\w{2}\d+/))
        { return {errorcode:'Partita IVA non valida!'}; }
        if (value.length!=13)
            { return {errorcode:'Partita IVA di lunghezza errata!'};}
        var s = 0;
        for(var i = 2; i < 12; i += 2 ){
            var j = parseInt(value.slice(i,i+1));
            s += j;
            }
        for(var i = 3; i < 12; i += 2 ){
            var j = parseInt(value.slice(i,i+1))*2;
            if( j > 9 )  j = j - 9;
            s += j;
            }
        check_digit = parseInt(value.slice(12,13));
        if (((10 - s%10)%10)!= check_digit)
            {
                return {errorcode:'Partita IVA errata; potrebbe terminare con '+((10 - s%10)%10)};
            }
        result= {value:value};
        return result;
    },

        
    checkCodiceFiscale:function(value, nazione){
        if(value=='') return true;
        codnaz=nazione || 'IT';
        if (codnaz!='IT') return true;
        value=value.toUpperCase();
        if (value.length==11){
            aux=this.checkPartitaIva(value,nazione);

            if (aux.errorcode!=undefined){
                return {errorcode:aux.errorcode};
            }
            if (aux.value!=undefined){
                value = aux.value
                value=value.substring(2)
                return {value:value};
            }            
            return true;
        }
        if(value.length!=16){
            return {errorcode:'Lunghezza errata!'}
        }
        var validi='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        for(i=0;i<16;i++){
            if (validi.indexOf(value.charAt(i))==-1){
                return {errorcode:'Il codice fiscale contiene caratteri non validi!'};
            }
        }
        var set1='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        var set2='ABCDEFGHIJABCDEFGHIJKLMNOPQRSTUVWXYZ';
        var setpari='ABCDEFGHIJKLMNOPQRSTUVWXYZ';
        var setdisp='BAKPLCQDREVOSFTGUHMINJWZYX';
        var s=0;
        for(i=1;i<=13;i+=2){
            s+=setpari.indexOf(set2.charAt(set1.indexOf(value.charAt(i))));
        }
        for(i=0;i<=14;i+=2){
            s+=setdisp.indexOf(set2.charAt(set1.indexOf(value.charAt(i))));
        }
        if(s%26 != value.charCodeAt(15)-'A'.charCodeAt(0)){
            return {errorcode:'Codice fiscale errato; potrebbe terminare con '+setpari.charAt(s%26)};
        }
        result= {value:value};
        return result;
    }
}
