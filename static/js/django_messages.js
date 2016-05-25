//javascript used in the django_messages app

$(function(){
    //highlight the message preview that is currently selected
    $('.message-preview').on('click', function(){
        $('.message-preview').removeClass('message-preview-selected');
        $(this).addClass('message-preview-selected');
    });    
});//function

$(function(){
    //limit the length of the message preview
   $('.message-preview').each(function(){
       var body = $(this).find('.message_body');
       var subject = $(this).find('.message_subject');
       body.text(function(index, currentText){
           return currentText.substr(0,100)+ "...";
       });
       subject.text(function(index, currentText){
           return currentText.substr(0,40)+"..."
       });
   });
});

//test search function using info here: http://stackoverflow.com/questions/18744533/how-do-i-jquery-ajax-live-search-for-the-models-in-django
$(function() {

    $('#search-message').keyup(function() {

        $.ajax({
            type: "GET",
            url: "/django_messages/search/",
            data: {
                'search_text' : $('#search-message').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR)
{
    $('#search-results').html(data)
    console.log($('#search-results').html(data))
}


// //search function
// $(function(){
//
//     //the search filter for the products
//     $("#search-message").keyup(function(){
//
//             // Retrieve the input field text and reset the count to zero
//             var messageSearchTerms = $(this).val();
//
//             // Loop through the products
//             $(".message-preview").each(function(){
//                 var senderelem = $(this).find('.message_sender');
//                 var sentelem = $(this).find('.message_sent_at');
//                 var subjectelem = $(this).find('.message_subject');
//                 var bodyelem = $(this).find('.message_body');
//
//                 // If the list item does not contain the text phrase fade it out
//                 if (senderelem.text().search(new RegExp(messageSearchTerms, "i")) < 0 && sentelem.text().search(new RegExp(messageSearchTerms, "i")) < 0 && subjectelem.text().search(new RegExp(messageSearchTerms, "i")) < 0 && bodyelem.text().search(new RegExp(messageSearchTerms, "i")) < 0){
//                     $(this).fadeOut();
//                 } else {
//                     $(this).show();
//                 } //else
//         });//thumbnail loop
//     }); //keyup
// });

//select the first message in the list by default
$(document).ready(function(){
    var firstSelectedMessage = document.getElementsByClassName('message-preview')[0];
    $(firstSelectedMessage).addClass('message-preview-selected');
    message_id= $(firstSelectedMessage).attr('id')
    if(message_id){
        viewMessage(message_id)
    }
});//ready

// use ajax to update the content on the right
// according to which message was selected
function viewMessage(id)
{
   $.ajax({

     type: "GET",
     url: '/django_messages/view/' + id,
     success: function(data) {
           // pass the data to the right div on the page
          $('.messages-ajax-content').html(data);
     }
   });
}

var messagePreview = $('.message-preview');
var previewSelected;
//allow keying between the message previews
$(document).keydown(function(e) {
    switch(e.which) {
        case 38: // up
            if(previewSelected){
                previewSelected.removeClass('message-preview-selected');
                next = previewSelected.prev();
                if(next.length > 0){
                    previewSelected = next.addClass('message-preview-selected');
                }else{
                    previewSelected = messagePreview.last().addClass('message-preview-selected');
                }
            }else{
                previewSelected = messagePreview.last().addClass('message-preview-selected');
            }
            break;
        case 40: // down
            if(previewSelected){
                previewSelected.removeClass('message-preview-selected');
                next = previewSelected.next();
                if(next.length > 0){
                    previewSelected = next.addClass('message-preview-selected');
                }else{
                    previewSelected = messagePreview.eq(0).addClass('message-preview-selected');
                }
            }else{
                previewSelected = messagePreview.eq(0).addClass('message-preview-selected');
            }
            break;
        default: return; // exit this handler for other keys
    }
    e.preventDefault(); // prevent the default action (scroll / move caret)
});

