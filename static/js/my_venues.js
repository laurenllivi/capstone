$(document).ready(function(){
    
    //hover effect for venues that need a default image
    $(function(){  
        $('.venue-pic-wrapper').stop().mouseenter(function(){
            $(this).find('.tiny-camera-icon').css('visibility', 'visible') 
        }).stop().mouseleave(function(){
            $(this).find('.tiny-camera-icon').css('visibility', 'hidden') 
        });//mouseenter 
    });
    
});

