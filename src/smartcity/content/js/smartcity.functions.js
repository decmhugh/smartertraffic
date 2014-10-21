var polyline_click_init_events = function( i, poly ) {
	google.maps.event.addListener(poly, 'mouseover', function (event) {
		console.log("location : " + poly['id']);
	});
}


var polyline_click_events = function(i, poly) {
	 poly.setMap(map);
    google.maps.event.addListener(poly, 'click', function (event) {
      	 analyseRoute(0,poly);
    });
}

var addCirc = function(i,poly){
	var j1 = poly.objects[0].junction2.point.split(",");
    var p1 = new google.maps.LatLng(j1[1] , j1[0]);
    var j2 = poly.objects[0].junction1.point.split(",");
    var p2 = new google.maps.LatLng(j2[1] , j2[0]);
	poly.strokeColor = color;
	var latlngbounds = new google.maps.LatLngBounds();
	latlngbounds.extend(p1);
	latlngbounds.extend(p2);
	
	var populationOptions = {
	  type: "CORRVAR",
      //strokeOpacity: 0.8,
      strokeWeight: 0,
      fillColor: '#000',
      fillOpacity: 0.35,
      map: map,
      center: latlngbounds.getCenter(),
      radius: mc.sliderValue
    };
    // Add the circle for this city to the map.
    cityCircle = new google.maps.Circle(populationOptions);
	poly.circ = cityCircle;
	google.maps.event.addListener(poly.circ, 'click', function (event) {
		alert(poly.id);
		//var e = window.event;
		//var position = {
		//	x : 10,
		//	y : 10
		//};
		//customTxt = "<div>Blah blah sdfsddddddddddddddd ddddddddddddddddddddd<ul><li>Blah 1<li>blah 2 </ul></div>"
        //txt = new TxtOverlay(position,customTxt,"customBox",map )
    });
}

var analyseRoute = function(i,poly){
	var analyseAPI = "/api/analyse/";
	
	//for (item in items){
	$.getJSON( analyseAPI, {
	   format: "json",
	   id: poly.id
	}).done(
			function( data ) {
				//console.log(poly.id + " " + data.args)
			  	color = mc.modelColor(data.results[0].classifier);
			  	var j1 = poly.objects[0].junction2.point.split(",");
		        var p1 = new google.maps.LatLng(j1[1] , j1[0]);
		        var j2 = poly.objects[0].junction1.point.split(",");
		        var p2 = new google.maps.LatLng(j2[1] , j2[0]);
			  	poly.fillColor = color;
            	poly.strokeColor = color;
            	poly.data = data;
            	
            	var latlngbounds = new google.maps.LatLngBounds();
            	latlngbounds.extend(p1);
            	latlngbounds.extend(p2);
            	
            	var populationOptions = {
			      strokeColor: mc.directionColor(poly.objects[0].direction),
			      strokeOpacity: 0.8,
			      strokeWeight: 2,
			      fillColor: mc.directionColor(poly.objects[0].direction),
			      fillOpacity: 0.35,
			      map: map,
			      center: p1,//latlngbounds.getCenter(),
			      radius: mc.sliderValue * data.results[0].coef[3]
			    };
			    // Add the circle for this city to the map.
			    cityCircle = new google.maps.Circle(populationOptions);
            	poly.circ = cityCircle;
            	google.maps.event.addListener(poly.circ, 'click', function (event) {
            		$("#LinkName").html(poly.id);
            		alert(poly.id);
               	 	this.setMap(null);
                });
            	google.maps.event.addListener(poly.circ, 'mouseover', function (event) {
            		var content = poly.id + " " + poly.data.args + "\n";
            		content += poly.objects[0].junction2.point + "\n"
            		content += poly.objects[0].junction2.desc + "\n"
            		$("#LinkName").html(content);
                });
            	poly.setMap(null);
            	if (parseInt(poly.objects[0].direction) === mc.direction()){
            		poly.setMap(map);
                	poly.circ.setMap(map);
            	}
            	mc.populateDetails(poly);
			}
	);
	//}
	}
	
var map_event_junc = function( data ) {
	  polyline = {}
	  
	  mc.distribution(data);
	  $.getJSON( flickerAPI, {
	      format: "json",
	      direction: mc.direction()
	    }).done(map_layout);   	  
}

var map_event_quantjunc = function( data ) {
	  polyline = {}
	  
	  mc.distribution(data);
	  $.getJSON( flickerAPI, {
	      format: "json",
	      direction: mc.direction()
	    }).done(map_quantlayout);   	  
	}
	
	var map_event = function( data ) {
		  polyline = {}
	    $.each(data, json_junction_event);
		  $.each(polyline, polyline_click_init_events); 
	    $.each(polyline, analyseRoute);
	    //$.each(polyline, polyline_events);  
	    //$.each(polyline, polyline_click_events);  
	}
	var map_event_predict = function( data ) {
		polyline = {}
	    $.each(data, json_junction_event);
		$.each(polyline, polyline_click_init_events); 
	}
		
	var map_quantlayout = function( data ) {
		  polyline = {}
		  $.each(data, json_junction_event);
		  for (p in polyline){
			  //console.log(polyline[p]["id"]);
			  d = mc.distributionItem(polyline[p]["id"]);
			  //&& parseInt(d["obs_count"]) > 90000
			  if (d != undefined ){
				  
			  
				  console.log(d["_id"]);
				  i = parseInt(d["obs_quantile"][mc.quantile()])
				  color = mc.color_range_quant(i);
				  //console.log(color)
				  polyline[p].fillColor = color;
			  	  polyline[p].strokeColor = color;
			  	  polyline[p].setMap(map);
			  	  polyline[p].dist = d;
			  	  line = polyline[p]
			  	  google.maps.event.addListener(line, 'mouseover', function (event) {
			  		console.log(line.id)
			  	  });
			  	  google.maps.event.addListener(line, 'click', function (event) {
			  		if (!this.windowopen == undefined){polyline[p].windowopen = false}
			  		if (!this.windowopen){
			  			var j1 = this.objects[0].junction1.point.split(",");
			  			
				        var p1 = new google.maps.LatLng(j1[1] , j1[0]);
			  			d = this.dist
			  			var marker = new google.maps.Marker({
			  			    position: p1,
			  			    map: map,
			  			    title:d["_id"]
			  			});
			  			google.maps.event.addListener(marker, 'click', function (event) {
			  				marker.setMap(null);
			  			});
			  			
			  			
			  			q = d["obs_quantile"]
			  			c =  "" + d["_id"];
			  			c+=  "<br>std : " + d["obs_std"] + "";
			  			c+=  "<br>quantile " + mc.quantile() + " : " + q[mc.quantile()] + "";
			  			//c+=  "<br>quatile : 20:" + q[20] + ", 50:" + q[50] +", 80:" + q[80] + "";
			  			
			  			var infowindow = new google.maps.InfoWindow({
			  	  		  content:c
			  	  		  });
			  			infowindow.setPosition(this.position);
			  			infowindow.open(map,marker);
			  		}else{
			  			polyline[p].windowopen = !polyline[p].windowopen;
			  			//polyline[p].infoWindow.close(map);
			  		}
			  		
	              });
			 }
		 }
		   
	}
	
	
	var map_layout = function( data ) {
		  polyline = {}
		  $.each(data, json_junction_event);
		  for (p in polyline){
			  //console.log(polyline[p]["id"]);
			  d = mc.distributionItem(polyline[p]["id"]);
			  //&& parseInt(d["obs_count"]) > 90000
			  if (d != undefined ){
				  
			  
				  console.log(d["_id"]);
				  i = parseInt(d["obs_std"])
				  color = mc.color_range(i);
				  //console.log(color)
				  polyline[p].fillColor = color;
			  	  polyline[p].strokeColor = color;
			  	  polyline[p].setMap(map);
			  	  polyline[p].dist = d;
			  	  line = polyline[p]
			  	  google.maps.event.addListener(line, 'mouseover', function (event) {
			  		console.log(line.id)
			  	  });
			  	  google.maps.event.addListener(line, 'click', function (event) {
			  		if (!this.windowopen == undefined){polyline[p].windowopen = false}
			  		if (!this.windowopen){
			  			var j1 = this.objects[0].junction1.point.split(",");
			  			
				        var p1 = new google.maps.LatLng(j1[1] , j1[0]);
			  			d = this.dist
			  			var marker = new google.maps.Marker({
			  			    position: p1,
			  			    map: map,
			  			    title:d["_id"]
			  			});
			  			google.maps.event.addListener(marker, 'click', function (event) {
			  				marker.setMap(null);
			  			});
			  			
			  			
			  			q = d["obs_quantile"]
			  			c =  "" + d["_id"];
			  			c+=  "<br>std : " + d["obs_std"] + "";
			  			//c+=  "<br>quatile : 20:" + q[20] + ", 50:" + q[50] +", 80:" + q[80] + "";
			  			
			  			var infowindow = new google.maps.InfoWindow({
			  	  		  content:c
			  	  		  });
			  			infowindow.setPosition(this.position);
			  			infowindow.open(map,marker);
			  		}else{
			  			polyline[p].windowopen = !polyline[p].windowopen;
			  			//polyline[p].infoWindow.close(map);
			  		}
			  		
	              });
			 }
		 }
		   
	}
		
var json_junction_event = function( i, item ) {
		
    var sub_id = item._id.substring(0,(item._id.length -1));
    var j1 = item.junction1.point.split(",");
    var j2 = item.junction2.point.split(",");
    var p1 = new google.maps.LatLng(j1[1] , j1[0]);
    var p2 = new google.maps.LatLng(j2[1] , j2[0]);
    
    var lineSymbol = {
	    path: google.maps.SymbolPath.FORWARD_CLOSED_ARROW
	  };
    var poly = new google.maps.Polyline({
            strokeWeight: 5,
            //fillColor: mc.linecolor(),
            fillColor:"#000",
            fillOpacity:0.4,
            strokeColor: "black",
            ids: [item._id],
            objects: [item],
            id: item._id,
            icons: [{
		      //icon: lineSymbol
		    }],
		    path:[p1,p2]
          });
          
	    polyline[item._id]=poly;
        mc.setPolyline(polyline);
	    mc.status(false);
  }

var polyline_events = function(i, poly) {
	 poly.setMap(map);
     google.maps.event.addListener(poly, 'mouseover', function (event) {
     ids = polyline[this.id].objects[0];
  	  if (ids.marker === undefined){
      	  
      	  var infowindow = new google.maps.InfoWindow({
		      content: this.id
		  });
		  $("#LinkName").html(this.id);
		  //$("#LinkName").css( "background-color", "#fff");
	  	  //$("#LinkName").css( "padding", "12px");
	  	  
	  	  //$("#LinkDetails").html(this.data);
		  //$("#LinkDetails").css("background-color","#fff");
	  	  //$("#LinkDetails").css("padding", "12px");
		  //var marker = new google.maps.Marker({
		  //    position: poly.getPath().getArray()[1],
		  //    map: map,
		  //    title: this.id
		  //});
		  //marker.setMap(map);
		  //ids.marker = marker;
	  }
  	  //this.infoWindow.setContent(contentString);
		  //this.infoWindow.setPosition(event.latLng);
	  //this.infoWindow.open(map);
        });
 }

function TxtOverlay(pos, txt, cls, map){

    // Now initialize all properties.
    this.pos = pos;
    this.txt_ = txt;
    this.cls_ = cls;
    this.map_ = map;

    // We define a property to hold the image's
    // div. We'll actually create this div
    // upon receipt of the add() method so we'll
    // leave it null for now.
    this.div_ = null;

    // Explicitly call setMap() on this overlay
    this.setMap(map);
}

TxtOverlay.prototype = new google.maps.OverlayView();



TxtOverlay.prototype.onAdd = function(){

    // Note: an overlay's receipt of onAdd() indicates that
    // the map's panes are now available for attaching
    // the overlay to the map via the DOM.

    // Create the DIV and set some basic attributes.
    var div = document.createElement('DIV');
    div.className = this.cls_;

    div.innerHTML = this.txt_;

    // Set the overlay's div_ property to this DIV
    this.div_ = div;
    var overlayProjection = this.getProjection();
    var position = overlayProjection.fromLatLngToDivPixel(this.pos);
    div.style.left = position.x + 'px';
    div.style.top = position.y + 'px';
    // We add an overlay to a map via one of the map's panes.

    var panes = this.getPanes();
    panes.floatPane.appendChild(div);
}

TxtOverlay.prototype.draw = function(){


    var overlayProjection = this.getProjection();

    // Retrieve the southwest and northeast coordinates of this overlay
    // in latlngs and convert them to pixels coordinates.
    // We'll use these coordinates to resize the DIV.
    var position = overlayProjection.fromLatLngToDivPixel(this.pos);


    var div = this.div_;
    div.style.left = position.x + 'px';
    div.style.top = position.y + 'px';



}
//Optional: helper methods for removing and toggling the text overlay.  
TxtOverlay.prototype.onRemove = function(){
    this.div_.parentNode.removeChild(this.div_);
    this.div_ = null;
}
TxtOverlay.prototype.hide = function(){
    if (this.div_) {
        this.div_.style.visibility = "hidden";
    }
}

TxtOverlay.prototype.show = function(){
    if (this.div_) {
        this.div_.style.visibility = "visible";
    }
}

TxtOverlay.prototype.toggle = function(){
    if (this.div_) {
        if (this.div_.style.visibility == "hidden") {
            this.show();
        }
        else {
            this.hide();
        }
    }
}

TxtOverlay.prototype.toggleDOM = function(){
    if (this.getMap()) {
        this.setMap(null);
    }
    else {
        this.setMap(this.map_);
    }
}
