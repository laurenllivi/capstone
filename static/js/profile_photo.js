//hover effect for deleting images from the manage venue page
$(function(){  
    $('.hover-delete').stop().mouseenter(function(){
        $(this).find('.hide-x-until-hover').css('visibility', 'visible') 
    }).stop().mouseleave(function(){
        $(this).find('.hide-x-until-hover').css('visibility', 'hidden') 
    });//mouseenter 
});