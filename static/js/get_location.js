var geocoder;
geocoder=new google.maps.Geocoder();
var suggestions=[];
$("#id_location").autocomplete({
    source: function(request,add){
    geocoder.geocode( { 'address': request.term}, function(results, status) {                                                             
        if (status == google.maps.GeocoderStatus.OK){
            //console.log(results[0]['address_components'],results[0].geometry)
            for(var i=0;i<results.length;i++){
                if(results[i]['types'][1]=='political'){
                    suggestions.push(results[i]['formatted_address']);
                    }//end if
            }//end for
            add(suggestions);
            }                                                                                                                   
        });
        },//end source function
    minLength: 1,
    select : function(e, ui){
        var loc=ui.item.value;
        geocoder.geocode({'address':loc},function(results,status){                                                      
            if(status==google.maps.GeocoderStatus.OK){
                var longitude=results[0].geometry.location['Za'];
                var latitude=results[0].geometry.location["Ya"];
                $("#result").append("<input type='hidden' name='loc' id='loc' value='"+loc+"'>
                    <input type='hidden' name='longitude' id='longitude' value='"+longitude+"'>
                    <input type='hidden' name='latitude' id='latitude' value='"+latitude+"'>");
            }//end if                                                                                                       
    });//end geocode
    ui      
        },//end select
}); // end autocomplete