var search_location = ''
var location_markers = {};

$(document).ready(function(){

    mapSetup();

    //datepicker
      $(document).ready(function() {
          $('.datepicker').datepicker();
      });

    ///price slider
    var nonLinearSlider = document.getElementById('nonlinear');

    noUiSlider.create(nonLinearSlider, {
        connect: true,
        behaviour: 'tap',
        start: [ 0, 5000 ],
        range: {
            // Starting at 50, step the value by 10,
            // until 2500 is reached. From there, step by 100.
            'min': [ 0 ],
            '10%': [ 50, 10 ],
            '50%': [ 2500, 100 ],
            'max': [ 5000 ]
        }
    });

    // Write the CSS 'left' value to a span.
    function leftValue ( handle ) {
        return handle.parentElement.style.left;
    }

    var lowerValue = document.getElementById('lower-value'),
        lowerOffset = document.getElementById('lower-offset'),
        upperValue = document.getElementById('upper-value'),
        upperOffset = document.getElementById('upper-offset'),
        handles = nonLinearSlider.getElementsByClassName('noUi-handle');

    // Display the slider value and how far the handle moved
    // from the left edge of the slider.
    nonLinearSlider.noUiSlider.on('update', function ( values, handle ) {
        if ( !handle ) {
            lowerValue.innerHTML = parseInt(values[handle]);
        } else {
            upperValue.innerHTML = parseInt(values[handle]);
        }
    });

})//document ready

function mapSetup()
{

    Circles = [];

    //add locations from db to list
    for (var i in location_markers)
    {
        circle =
        {
            lat: location_markers[i].lat,
            lon: location_markers[i].lon
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
      alert('Geocode was not successful for the following reason: ' + status);
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
            html: '%index',
            show_infowindow : false,
            circle_options: {
                radius: 200
            },
            stroke_options: {
                strokeColor: '#00aa00',
                fillColor: '#00aa00'
            },
            visible: false //marker
        },
        show_markers: false,
    }).Load();
}

function setLocations(search_location, location_data)
{
    search_location = search_location;
    location_markers = location_data;
}
