$(document).ready(function(){
    setTimeout(function(){
       //google map
        new Maplace({
            generate_controls: false,
            locations: Circles,
            map_div: '#gmap-circles',
            start: 0,
            view_all_text: 'Points of interest',
            type: 'circle',
            shared: {
                zoom: 14,
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
    },5);

    var Circles = [
        {
            html: 'circle 1',
            lat: 40.2444,
            lon: -111.6608,
        },
        {
            html: 'circle 2',
            lat: 40.2433,
            lon: -111.6600,
        },
    ];


})//document ready

