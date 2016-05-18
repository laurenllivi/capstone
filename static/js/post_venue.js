$(document).ready(function(){


    $('.owl-carousel').owlCarousel({
        responsiveClass:true,
        dots:false,
        nav: true,
        responsive:{
            0:{
                items:1,
            },
            600:{
                items:3,
            },
            1000:{
                items:4,
            }
        }
    });

})//document ready