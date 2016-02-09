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

function myFunction() {
   alert("askjdflkasjdf")
}