var selectedTab = 1;

$(document).ready(function(){

     setTimeout(function(){
         tab = document.getElementById("view"+selectedTab+"-link");
         tab.click();

         var x = $(".field_error")
            .first()
            .closest(".tab")
            .attr('id');

        linkId = x + '-link';
        link = document.getElementById(linkId);
        if(link!=null)
        {
            link.click();
        }
     },10)
      
     //hover effect for deleting images from the manage venue page
     $(function(){  
         $('.hover-delete').stop().mouseenter(function(){
             $(this).find('.hide-x-until-hover').css('visibility', 'visible') 
         }).stop().mouseleave(function(){
             $(this).find('.hide-x-until-hover').css('visibility', 'hidden') 
         });//mouseenter 
     });
     
}); //ready

function nextTab() {
   var currentTab = $(".selected").first();
   var nextTab = currentTab.next("li");

   currentTab.removeClass("selected");

   var linkId = nextTab.find("a").attr('id');
   var link = document.getElementById(linkId);

   if(link!=null)
   {
       link.click();
   }

    window.event.preventDefault();
}

function setPageVars(tab)
{
    selectedTab = tab
}

// function setAvailableDates(){
//     //get the available dates and prepopulate the calendar
//     var availableDatesField = $('#id_dates_available');
//
// }

// // event to check the altField on the calendar and update the calendar accordingly
// $(function(){
//
// });

// use ajax to update the content on the right
// according to which message was selected
// function viewVenueCalendar(id)
// {
//    $.ajax({
//
//      type: "GET",
//      url: '/venue/calendar/' + id,
//      success: function(data) {
//            // pass the data to the right div on the page
//           $('.calendar-ajax-content').html(data);
//      }
//    });
// }
