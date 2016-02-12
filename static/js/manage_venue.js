$(document).ready(function(){
     setTimeout(function(){
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
});

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