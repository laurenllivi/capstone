var imageCount = 0;
var listingDates = [];

window.addEventListener('resize', function(event){
  $('#horiz_container_outer').horizontalScroll();
});

$(document).ready(function(){

    var Circles = [
        {
            lat: 40.2404048,
            lon: -111.6465722,
        }
    ];

    //today
    var dateToday = new Date();
    var oneYear = new Date(new Date().setYear(new Date().getFullYear() + 1));

    //enabled dates
    function enableAllTheseDays(date) {
            var sdate = $.datepicker.formatDate( 'mm/dd/yy', date)
            if($.inArray(sdate, listingDates) != -1) {
                return [true];
            }
            return [false];
        }

    $('.datepicker').datepicker({
        minDate: dateToday,
        maxDate: oneYear,
        dateFormat: 'mm/dd/yy',
        beforeShowDay: enableAllTheseDays
    });

    makeMap(Circles, 40.2404048, -111.6465722)

    //photo scroller
    imageWidth = 308; //including padding
    container_width = imageWidth * imageCount;
    document.getElementById('horiz_container').style.width = container_width + "px";

    $('#horiz_container_outer').horizontalScroll();

    //star ratings
    $('.rating-cancel').remove()

})//document ready

function makeMap(Circles, centerLat, centerLon)
{
    //google map
    new Maplace({
        generate_controls: false,
        locations: Circles,
        map_div: '#gmap-circles',
        map_options: {
            set_center: [centerLat, centerLon],
            zoom: 13,
            //make map stationary
            draggable: false,
            zoomControl: false,
            scrollwheel: false,
            disableDoubleClickZoom: true
        },
        start: 0,
        type: 'circle',
        shared: {
            zoom: 13,
            show_infowindow : false,
            circle_options: {
                radius: 400
            },
            stroke_options: {
                strokeColor: '#00aa00',
                fillColor: '#00aa00'
            },
        },
        show_markers: false,
    }).Load();
}

function sizePhotoContainter(count)
{
    imageCount = count;
}

function setAvailableDates(listing_dates)
{
    listingDates = listing_dates;
}