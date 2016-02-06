from django.conf import settings
import django.utils.translation
import base64, re, decimal, rjsmin, datetime
import django.forms
import django.forms.widgets
from django.forms.util import flatatt

class fileUploadInput(django.forms.FileInput):
    def __init__(self, *args, **kwargs):
        super(fileUploadInput, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        html = []

        html.append(super(render, self).render(name, value, attrs))
        html.append('<br/>')

        html.append('<div class="progress">')
        html.append('   <div id="progressBar" class="progress-bar progress-bar-success progress-bar-striped active" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100">')
        html.append('   <span class="sr-only">50% Complete</span>')
        html.append('   </div')
        html.append('</div>')

        html.append('<script>')
        html.append('$(function(){')
        html.append("   $('#id_upload_file').off('change.upload').on('change.upload', function(){")
        html.append("       var fd = new FormData();")
        html.append("       var file = this.files[0];")
        html.append('       fd.append("upload", file);')
        html.append("       $.ajax({")
        html.append("           url: '/homepage/upload.upload/',")
        html.append("           type: 'POST',")
        html.append("           contentType: false,")
        html.append("           processData: false,")
        html.append("           data: fd,")
        html.append("           xhr: function() {")
        html.append("               var xhr = jQuery.ajaxSettings.xhr();")
        html.append("               if (xhr.upload) {")
        html.append("                   xhr.upload.addEventListener('progress', function(evt) {")
        html.append("                       if (evt.lengthComputable) {")
        html.append("                           //update the UI")
        html.append("                           var percentComplete = (evt.loaded / evt.total)*100;")
        html.append('                           $("#progressBar").css("width", percentComplete + "%");')
        html.append("                           if (percentComplete = 100){")
        html.append('                               $("#progressBar").removeClass("progress-bar-striped");')
        html.append('                               $("#progressBar").removeClass("active");}')
        html.append("                       }//if")
        html.append("                   }, false);")
        html.append("               }//if")
        html.append("               return xhr;")
        html.append("           },//xhr")
        html.append("           success: function(data){")
        html.append("               //save the name to be uploaded with the main form")
        html.append("               $('#id_upload_fullname').val(data)")
        html.append("           },//success")
        html.append("           error: function(err){")
        html.append('               console.log("ERROR");')
        html.append("               console.log(err);")
        html.append("           },//error")
        html.append("       });//ajax")
        html.append("   })//change")
        html.append("   $('#id_upload_file').closest('form').off('submit.upload').on('submit.upload', function(){")
        html.append("       $('#id_upload_file').remove();")
        html.append("   });//submit")
        html.append("})//ready")
        html.append('</script>')

        return '\n'.join(html)
