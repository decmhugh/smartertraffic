
var uluru = new google.maps.LatLng(53.346951058081927,-6.259268157760138);
var polyline = {};
var markers = [];
var path = new google.maps.MVCArray;


var flickerAPI = "/api/traffic/";
var twitterAPI = "/api/twitter/";
var colour = '#0000FF';

function MapContainer(){
	  	this.sliderValue = 50;
	  	var direction_name = ["Inbound","Outbound"];
  		var direction_color = ["#FF0000","#0000FF"];
  		var algortihm_colors = ["#FF0000","#6666FF","#00FF00","#FF00FF","#FFFF00","#00FFFF",
  		                      "#CC0000","#FFFFCC","#CCCCCC","#CCCC00"];
  		var algortihm_names = ["LinearRegression","SVR","BayesianRidge","PassiveAggressiveRegressor"];
  		var color = ["#333","#111"];
  		var modelattr =['Rain','Rain1','STT','STT1','STT2','STT3','Temperature','Temperature1','Wind','Wind1']
  		this.corrattr =['Rain','Temperature']
  		this.corrstation =['ICODUBLI2','ILEINSTE8','IDUBLINC2']
  		this.corrstation_color =['red','green','blue']
  		this.corrval =['dailyrainMM','TemperatureC']
  		this.corrresult = undefined
  		this.trafficresult = undefined
  		this.trafficclf = undefined
  		this.trafficclfdata = function(){
  			this.trafficclf = []
  			for (idx in mc.trafficresult){
  				obj = this.trafficresult[idx]
  				id = obj['_id']
  				this.trafficclf[id] = obj
  			}
  		}
  		var modelindex = -1
  		var loading_status = 0
  		var map_polylines = [[],[]];
  		var init = false;
  		var distMaxStd = 0;
  		this.quantileMaxStd = function(){
  			return parseInt($('input[name=obs_quantile_range]').val());
  		}
  		this.quantile = function(){
  			return parseInt($('input[name=obs_quantile_value]').val());
  		}
  		var distValue = {}
  		this.direction = function(){
  			return parseInt($('input[name=bound]:checked').val())+1;
  		}
  		this.distribution = function(data) {
  			for(a in data){
  				//if (parseInt(data[a]["obs_count"]) > 90000){
  					
  					std =  parseInt(data[a]["obs_std"]);
  					quant =  parseInt(data[a]["obs_quantile"][this.quantile]);
  				
	  				if (distMaxStd < std){ distMaxStd = std }
	  				//if (quantileMaxStd < quant){ quantileMaxStd = quant }
	  				distValue[data[a]["_id"]] = data[a];
	  			//}
  			}
  			
  			$("#std_range_max").html(distMaxStd);
  			console.log(this.quantile())
  			$("#quant_range_max").html(this.quantileMaxStd());
  		}
  		this.distributionItem = function(id){
  			return distValue[id]
  		}
  		
  		this.color_range = function rainbow(n) {
  			c = (n/distMaxStd)*250;
  		    n = Math.round(c);
  		    return color = 'hsl(' + (n) + ',75%,40%)';
  	    }
  		
  		this.color_range_quant = function rainbow2(n) {
  			c = (n/this.quantileMaxStd())*250;
  		    n = Math.round(c);
  		    console.log(n)
  		    return color = 'hsl(' + (n) + ',75%,40%)';
  	    }
  		
  		this.initiateAlgorithms = function() {
  		//ui-block-a // ui-grid-a
	  		if (!init){
	  		    var i = 0;
	  		  for (idx in mc.models()){
	  		    	$( "select[id=model]").append("<option value=" + modelattr[idx] + ">" 
	  		    		+ modelattr[idx] + "</option>")
	  		    }
	  		    
		  		for (idx in mc.corrattr){
	  		    	$( "select[id=correlation_select]")
	  		    	  .append("<option value=" + mc.corrval[idx] + ">" + mc.corrattr[idx] + "</option>")
	  		    }
  		    
	  			for (idx in algortihm_names){
	  				i += 1
	  				id = "id=ui-block-" + i + ""
	  				path = "span[" + id + "]";
	  				span = $(path);
	  				if(!span.length){ 
	  					$("#ui-grid").append("<span " + id + " style='display: block;'>" + algortihm_names[idx] + "</span>")
	  				}
	  					
	  				$(path).html(algortihm_names[idx]);
	  				$(path).css( "background-color", mc.modelColor(algortihm_names[idx]));
	  				$(path).css( "padding", "12px");
	  			
	  			}
	  			init = !init;
	  		}
  		};

  		this.modelColor = function(name) {
  			idx = algortihm_names.indexOf(name);
  			return algortihm_colors[idx]
  		};
  		
  		this.directionColor = function(id) {
  			idx = parseInt(id) - 1
  			return direction_color[idx]
  		};
  		
  		this.showHeatMap = function(result) {
  			idx = modelattr.indexOf(result);
  			modelindex = idx
  		};
  		
  		this.models = function() {
  			return modelattr;
  		};
  		
  		this.status = function(arg) {
  			if(arg != undefined){
  				if(arg){
  					loading_status = 1;
	  			}else{
	  				loading_status = 0;
	  			}
  			}
  			return loading_status;
  		};
  		this.name = function() {
  			return direction_name[this.direction()];
  		};
  		
  		this.setPolyline = function(poly) {
  			var direction;
  			for (obj in poly){
  				direction = parseInt(poly[obj].objects[0].direction);
  				map_polylines[direction] = poly;
  			}
  			
  		};
  		
  		this.getPolyline = function() {
  			return map_polylines[this.direction()];
  		};
  		
  		this.clearMap = function() {
  			var data = map_polylines[0];
  			for (var obj in data){
  				if (data[obj].circ){
  					data[obj].circ.setMap(null)
  				}
	  			data[obj].setMap(null)
	  		}
	  		var data = map_polylines[1];
  			for (var obj in data){
  				if (data[obj].circ){
  					data[obj].circ.setMap(null)
  				}
	  			data[obj].setMap(null)
	  		}
  			
  		};
  		
  		this.markers = []
  		
  		this.corrIndex = [];
  		this.zIndex = 0
  		this.populateMap = function() {
  			
  			var p1 = new google.maps.LatLng(-6.2 , 53.3);
  			var populationOptions = {
  			      //strokeOpacity: 0.8,
  			      strokeWeight: 0,
  			      fillColor: '#000',
  			      fillOpacity: 0.35,
  			      center: p1,
  			      radius: mc.sliderValue
  			};
  			    // Add the circle for this city to the map.
  			cityCircle = new google.maps.Circle(populationOptions);
  			this.markers[0] = cityCircle;
  			
  			var selected = $( "select[id=correlation_select]").val();
  			this.zIndex = 0
  			this.clearMap();
  			var data = map_polylines[this.direction()];
  			for (var obj in data){
  				data[obj].zIndex = ++this.zIndex;
  				if (!this.trafficclf) { this.trafficclfdata() }
  				std = 0
  				if (this.trafficclf[obj]){
  					console.log(this.trafficclf[obj])
  					clf = this.trafficclf[obj]['clf'].split('_')[0]
  					std = this.trafficclf[obj]['std']
  					
  					data[obj].strokeColor = this.modelColor(clf)
  					//data[obj].fillColor = '#CCC';
  				}
  				//if (std > 2)
  					data[obj].setMap(map);
  			}
  			for (var obj in data){
  				if (data[obj].circ){
  					if (data[obj].circ.type) {
  						if (this.corrIndex.length === 0){
  							for (var mydata in this.corrresult._index){
  								value = this.corrresult._index[mydata];
  								this.corrIndex[value] = mydata; 
  							}
  						}
  						//['ICODUBLI2','ILEINSTE8','IDUBLINC2']
  						id = obj.replace('/','_').replace('/','_')
  						value = this.corrIndex[id]
  						result = 0
  						
  						result1 = this.corrresult['IDUBLINC2_' + selected][value]
  						result2 = this.corrresult['ILEINSTE8_' + selected][value]
  						result3 = this.corrresult['IDUBLINC2_' + selected][value]
  						color = '#FFF'
  						if (Math.abs(result) < Math.abs(result1)){ 
  							result = result1; 
  							color = this.corrstation_color[0]
  						} 
  						if (Math.abs(result) < Math.abs(result2)){ 
  							result = result2; 
  							color = this.corrstation_color[1]
  						} 
  						if (Math.abs(result) < Math.abs(result3)){ 
  							result = result3; 
  							color = this.corrstation_color[2]
  						} 
  						
  						data[obj].circ.fillOpacity = 1;
  						if (result <= 0){
  							data[obj].circ.fillOpacity = 0.5;
  						}
  						data[obj].circ.zIndex = ++this.zIndex;
  						data[obj].circ.fillColor = color;
  						data[obj].circ.radius = this.sliderValue * 20 * result;
  					}else{
  						data[obj].circ.radius = this.sliderValue * data[obj].data.results[0].coef[3];
  					}
  					data[obj].circ.setMap(map)
  				}
  			}
  		};
  		
  		this.populateDetails = function(poly) {
  			var data = poly.data;
  			$( "label[id=linkName]").html(data.id);
  		};
  		
  		this.linecolor = function() {
  			return color[this.direction()];
  		};

  }
  var mc = new MapContainer();
  
  $(function() {
	  $( "button[id=heatMapOfData]" )
      .button().click(function(){
      	var result = $( "select[id=model]").val();	
      	mc.showHeatMap(result)    
      });
	  
	  
	  
	  $( "button[id=predMapOfData]" )
      .button().click(function(){
    	  if (!mc.trafficresult){
	    	  console.log("get junctions")
	    	  $.getJSON( "/api/traffic", {
			      format: "json",
			      direction : mc.direction()
			  })
			  .error()
			  .done(function(data){
				  console.log("get junctions >> result");
				  this.data = data
				  mc.clearMap();
				  $.getJSON( "/api/trafficresult", {
				      format: "json",
				      direction : mc.direction()
				  })
				  .done(function(result){
					  console.log(">>> algorithm")
					  console.log(data)
					  $.each(data, json_junction_event);
					  mc.trafficresult = result
					  index = result._index
					  for (r in index){
						  idx = index[r].replace("_", "/").replace("_", "/");
						  poly = mc.getPolyline()[idx]
						  //if (undefined != poly){
							//  addCirc(0,poly);
						  //}else{
							  //console.log(poly)
						  //}
						  //mc.setPolyline(poly)
						  
					  }
					  mc.populateMap();
				  });
			  }); 
    	  }
      });
	  
	  $( "button[id=corrMapOfData]" )
      .button().click(function(){
    	  if (!mc.corrresult){
	    	  console.log("get junctions")
	    	  $.getJSON( "/api/traffic", {
			      format: "json",
			      direction : mc.direction()
			  })
			  .error()
			  .done(function(data){
				  console.log("get junctions >> result");
				  this.data = data
				  mc.clearMap();
				  $.getJSON( "/api/weather/", {
				      format: "json",
				      direction : mc.direction()
				  })
				  .done(function(result){
					  console.log(data)
					  $.each(data, json_junction_event);
					  mc.corrresult = result;
					  console.log(result)
					  index = result._index
					  for (r in index){
						  idx = index[r].replace("_", "/").replace("_", "/");
						  poly = mc.getPolyline()[idx]
						  if (undefined != poly){
							  addCirc(0,poly);
						  }else{
							  //console.log(poly)
						  }
						  //mc.setPolyline(poly)
						  
					  }
					  mc.populateMap();
				  });
			  }); 
    	  }
      });
    //$('.selectpicker').selectpicker();
    
    $("button[id=obs_quantile]").button()
    
    $( "button[id=obs_std]" ).button()
    .click(function( event ) {
    	
    	mc.clearMap();
    	
    	$.getJSON( "/api/distribution", {
		      format: "json"
		  })
		  .done(map_event_junc);  
    })
    
    $( "button[id=obs_std_wd]" ).button()
    .click(function( event ) {
    	
    	mc.clearMap();
    	
    	$.getJSON( "/api/dist_wd", {
		      format: "json"
		  })
		  .done(map_event_quantjunc);  
    })
    $( "button[id=obs_std_weekday]" ).button()
    .click(function( event ) {
    	
    	mc.clearMap();
    	
    	$.getJSON( "/api/dist_wd", {
		      format: "json"
		  })
		  .done(map_event_junc);  
    })
    $( "button[id=obs_std_weekend]" ).button()
    .click(function( event ) {
    	
    	mc.clearMap();
    	
    	$.getJSON( "/api/dist_we", {
		      format: "json"
		  })
		  .done(map_event_junc);  
    })
    
    $( "button[id=obs_std_we]" ).button()
    .click(function( event ) {
    	
    	mc.clearMap();
    	
    	$.getJSON( "/api/dist_we", {
		      format: "json"
		  })
		  .done(map_event_quantjunc);  
    })
    
    $( "button[id=toggleButton]" )
      .button()
      .click(function( event ) {
        mc.clearMap();
        $( "label[id=directionName]").html("Loading");
        if (mc.status() === 0){
        	mc.status(true);
      		if (mc.getPolyline().length === 0){
	      		$.getJSON( flickerAPI, {
			      format: "json",
			      direction: mc.direction()
			    }).done(map_event);  
			    $( "label[id=directionName]").html(mc.name() );
		    }else{
		    	mc.populateMap();
		    	mc.status(false);
		    	$( "label[id=directionName]").html(mc.name() );
		    }
	      	
	      }else{
	        mc.status(false);
	      	$( "label[id=directionName]").html(mc.name() );	
	      }
      });
  });
  
 
  

  
  var map = undefined;
  
  $( document ).ready(function() {
	  
	  $( "button[id=twitterShow]" ).button()
	  
	  $( "button[id=twitterAnalyse]" )
      .button().click(function(){
    	  var dateVal = $("#datepicker").val();
      	  dateVal += "/" + $("#timepicker").val().split(":")[0];
    	  console.log("get twitter")
    	  $.getJSON( "/api/twitterresult", {
		      format: "json",
		      date : dateVal
		  })
		  .error()
		  .done(function(data){
			  //console.log('results');
			  
			  for(item in data['tweets']){
				  //console.log(data['tweets'][item]);
				  cluster.designmarker(data['tweets'][item]);
			  }
			  cluster.display();
			  
			  //for(item in data['traffic']){
				  //console.log(data['traffic'][item]);
				  //cluster.designmarker(data['tweets'][item]);
			  //}
			  mc.traffic = data['traffic']
			  mc.tweets = data['tweets']
			  
			  $.getJSON( "/api/traffic", {
			      format: "json",
			      direction : mc.direction()
			  })
			  .error()
			  .done(function(data){
				  console.log("get junctions >> result");
				  this.data = data
				  mc.clearMap();
				  $.getJSON( "/api/traffic", {
				      format: "json",
				      direction : mc.direction()
				  })
				  .done(function( data ) {
						polyline = {}
					    $.each(data, json_junction_event);
						$.each(polyline, polyline_click_init_events);
						console.log(mc.traffic)
						mc.trafficitem = []
						mc.setPolyline(polyline);
						for (t in mc.traffic){
							item = mc.traffic[t]
							j = item['junction'];
							if (polyline[j]){
								console.log(polyline[j])
								polyline[j].strokeColor = '#777';
								if ((item.result*1.1)  < item.actual){
									polyline[j].strokeColor = 'green';
								}
								if (item.result > (item.actual*1.1)){
									polyline[j].strokeColor = 'red';
								}
								
							}
						}
						mc.populateMap();
				  });
			  }); 
			  
		  }); 
    	  
      });
	  
	
    $( "label[id=directionName]").html(mc.name() );
    map = new google.maps.Map(document.getElementById("map_canvas"),
			{'center':uluru,'zoom': 12});
    
    
    cluster = new MarkerClusterContainer(map);
    mc.initiateAlgorithms();
    $( "#slider" ).slider({
    		  value : mc.sliderValue,
    		  change: function( event, ui ) {
    			  mc.sliderValue = Math.abs(ui.value);
    			  mc.populateMap()
    		  }
    	 });
    id = "id=std_range_-1" 
    	$("#std_range").append(
    			"<span " + id + 
    			" style=\"width:12px;display: inline-block;\">&nbsp;</span>")
        for (i = 0; i < 251; i+=25){
    			id = "id=std_range_" + (i)
    			color = 'hsl(' + (i) + ',75%,60%)';
    			$("#std_range").append(
    					"<span " + id + 
    					" style=\"width:12px;display: inline-block;background-color:" + color + 
    					"\">&nbsp;</span>")
    	}
    
    $("#quant_range").append(
			"<span " + id + 
			" style=\"width:12px;display: inline-block;\">&nbsp;</span>")
    for (i = 0; i < 251; i+=25){
			id = "id=quant_range_" + (i)
			color = 'hsl(' + (i) + ',75%,60%)';
			$("#quant_range").append(
					"<span " + id + 
					" style=\"width:12px;display: inline-block;background-color:" + color + 
					"\">&nbsp;</span>")
	}
    	 
    $(function() {
    	
    	
    	$("#datepicker").datepicker({ dateFormat: 'yy/mm/dd' });
    	$("#twitterShow").click(function(){
    	markers = [];
    	var dateVal = $("#datepicker").val();
    	dateVal += "/" + $("#timepicker").val().split(":")[0];
    	$.getJSON( twitterAPI, {
			   format: "json",
			   date: dateVal
			}).done(
				function( data ) {
					cluster.markers(data);
				}).success(function(data) { console.log(data);})
				.error(function(error) { console.log(error); });
    		 });
    	 });
    	
    	addMarker2 = function addMarker(pos,clr) {
		  var goldStar = {
				    path: 'M 0,0 -20,40 20,40 z',
				    fillColor: clr,
				    fillOpacity: 0.8,
				    scale: 1,
				    strokeColor: 'gold',
				    strokeWeight: 2
				  };
		  p = new google.maps.LatLng(pos[1] , pos[0]);
		  var marker = new google.maps.Marker({
		    position: p,
		    icon : goldStar,
		    map: map
		  });
		};
		//Artane // Blackrock // Lucan	
  		//(53.387 ,-6.210),(53.296, -6.185),(53.343, -6.440 )
		var iconBase = 'https://maps.google.com/mapfiles/kml/shapes/';
		//-6.298306819491731,53.361784314536344
		//addMarker2([-6.210,53.387],'red')
		//addMarker2([-6.185,53.296],'green')
		//addMarker2([-6.39,53.343],'blue')
		
		var res = function(x,y,o,r){
			var pos = new google.maps.LatLng(x,y);
			var populationOptions = {
				      fillColor: 'YELLOW',
				      center: pos,
				      radius: r,
				      fillOpacity: o,
				      map: map
				    };
			cityCircle = new google.maps.Circle(populationOptions);
		}
		//res(53.403,-6.37,0.50,1000);
		//res(53.403,-6.34,0.50,(1000/1.50));
		//res(53.403,-6.32,0.50,(1000/3));
		
		
		//res(53.403,-6.30,1,(1000/3));
		//res(53.403,-6.28,1,(1000/1.50));
		//res(53.403,-6.25,1,1000);
		
		
		
    	
	});

