$(document).ready(function(){
    setTimeout(function(){
       //google map
		function initialize() {
	        var mapCanvas = document.getElementById('map');
	        var mapOptions = {
	          center: new google.maps.LatLng(40.5403, -111.6450),
	          zoom: 9,
	          mapTypeId: google.maps.MapTypeId.ROADMAP
	        }
	        var map = new google.maps.Map(mapCanvas, mapOptions)
	      }
	      google.maps.event.addDomListener(window, 'load', initialize);

        //datepicker
          $(document).ready(function() {
              $('.datepicker').datepicker();
          });

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
                lowerValue.innerHTML = values[handle];
            } else {
                upperValue.innerHTML = values[handle];
            }
        });
    },5);

})

