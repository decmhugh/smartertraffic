function MarkerClusterContainer(map){
	this.markerarray = [];
	this.trafficarray = [];
	this.map = map;
	var markerCluster = '';
	this.designmarker = function designmaker(item){
		var imageUrl = 'http://chart.apis.google.com/chart?cht=mm&chs=24x32&' +
        'chco=FFFFFF,008CFF,000000&ext=.png';
		var markerImage = new google.maps.MarkerImage(imageUrl,
		          new google.maps.Size(24, 32));
	    var latLng = new google.maps.LatLng(item.geo.coordinates[0], item.geo.coordinates[1]);
	    var marker = new google.maps.Marker({
	          position: latLng,
	          item: item,
	          icon:markerImage
	    });
	    google.maps.event.addListener(marker, 'click', function() {
	    	var contentString = "<span style='display: inline-block;width: 130px;'>" 
	    		+ marker.item.text 
	    		+ "</span>";
	    	var infowindow = new google.maps.InfoWindow({
	    	      content: contentString
	    	  });
	    	infowindow.open(map,marker);
	        console.log(marker.item.text);
	        
	    });
	    this.trafficarray.push(marker);
	    marker.setMap(this.map);	
	};
	this.display = function display(){
		//this.markerCluster = new MarkerClusterer(this.map, this.trafficarray);
		
	};
	this.markers = function markers(items){
		if (this.markerCluster !== ''){
			m = this.markerarray.length;
			for(i = 0; i < m; i += 1){
				console.log(this.markerarray[i].item.text);
				this.markerarray[i].setMap(null);
			}
			this.markerarray = []
		}
		for(item in items){
			this.designmarker(items[item]);
		}
		
		this.markerCluster = new MarkerClusterer(this.map, this.trafficarray);
		
	};
}
