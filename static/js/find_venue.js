var search_location = '';
var location_markers = {};
var price_per_hour_range = [];

function pageSetup()
{
    $('.datepicker').datepicker();
    mapSetup();
}

function mapSetup()
{

    Circles = [];

    //add locations from db to list
    for (var i in location_markers)
    {
        circle =
        {
            lat: location_markers[i].lat,
            lon: location_markers[i].lon,
            html: location_markers[i].title
        }
        Circles.push(circle);
    }

//geocoding
  var geocoder = new google.maps.Geocoder();
  var address = search_location;
  geocoder.geocode({'address': address}, function(results, status) {
    if (status === google.maps.GeocoderStatus.OK) {
        makeMap(Circles, results[0].geometry.location.lat(), results[0].geometry.location.lng());
    } else {
      //Geocode unsuccessful
    }
   });
}

function makeMap(Circles, centerLat, centerLon)
{
    //google map
    new Maplace({
        generate_controls: false,
        locations: Circles,
        map_div: '#gmap-circles',
        map_options: {
            set_center: [centerLat, centerLon],
            zoom: 12
        },
        start: 0,
        type: 'circle',
        shared: {
            zoom: 13,
//            show_infowindow : false,
            circle_options: {
                radius: 200
            },
            stroke_options: {
                strokeColor: '#00aa00',
                fillColor: '#00aa00'
            },
        },
        show_markers: false,
    }).Load();
}


function setLocations(location, location_data, price_range)
{
    search_location = location;
    location_markers = location_data;
    price_per_hour_range = price_range;
}
