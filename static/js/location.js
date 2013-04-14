$(document).ready(function(){
var geocoder;
    geocoder=new google.maps.Geocoder();
    var suggestions=[];
    $("#id_location").autocomplete({
        source: function(request,add){
        var suggestions = [];
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
            delete suggestions;
            },//end source function
        minLength: 1,
        select : function(e, ui){
            var loc=ui.item.value;
            console.log(loc);
            geocoder.geocode({'address':loc},function(results,status){                                                      
                if(status==google.maps.GeocoderStatus.OK){
                    
                    var longitude=results[0].geometry.location.lng();
                    var latitude=results[0].geometry.location.lat();
                    $("#id_latitude").val(latitude);
                    $("#id_longitude").val(longitude);
                    var administrative_level_1 = '';
                    var administrative_level_2 = '';
                    if(results[0]['address_components'][1] && results[0]['address_components'][2]){
                        administrative_level_1 = results[0]['address_components'][1].long_name;
                        administrative_level_2 = results[0]['address_components'][2].long_name; 
                        $("#id_area_level1").val(administrative_level_1);
                        $("#id_area_level2").val(administrative_level_2);
                        }
                    if(results[0]['address_components'][2] == undefined){
                        administrative_level_1 = results[0]['address_components'][1].long_name;
                        $("#id_area_level1").val(administrative_level_1);
                    }

                }//end if                                                                                                       
        });//end geocode
        ui      
            },//end select
    }); // end autocomplete
}); // end document.ready
