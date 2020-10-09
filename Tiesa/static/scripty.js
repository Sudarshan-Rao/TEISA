$(document).on('click', '#close-preview', function(){
    $('.image-preview').popover('hide');
    // Hover befor close the preview
    $('.image-preview').hover(
        function () {
           $('.image-preview').popover('show');
        },
         function () {
           $('.image-preview').popover('hide');
        }
    );
});

$(function() {
    // Create the close button
    var closebtn = $('<button/>', {
        type:"button",
        text: 'x',
        id: 'close-preview',
        style: 'font-size: initial;',
    });
    closebtn.attr("class","close pull-right");
    // Set the popover default content
    $('.image-preview').popover({
        trigger:'manual',
        html:true,
        title: "<strong>Preview</strong>"+$(closebtn)[0].outerHTML,
        content: "There's no image",
        placement:'bottom'
    });
    // Clear event
    $('.image-preview-clear').click(function(){
        $('.image-preview').attr("data-content","").popover('hide');
        $('.image-preview-filename').val("");
        $('.image-preview-clear').hide();
        $('.image-preview-input input:file').val("");
        $(".image-preview-input-title").text("Browse");
    });
    // Create the preview image
    $(".image-preview-input input:file").change(function (){
        var img = $('<img/>', {
            id: 'dynamic',
            width:250,
            height:200
        });
        var file = this.files[0];
        var reader = new FileReader();
        // Set preview image into the popover data-content
        reader.onload = function (e) {
            $(".image-preview-input-title").text("Change");
            $(".image-preview-clear").show();
            $(".image-preview-filename").val(file.name);
            img.attr('src', e.target.result);
            $(".image-preview").attr("data-content",$(img)[0].outerHTML).popover("show");
        };
        reader.readAsDataURL(file);
    });



    $("#form").submit(function(e) {
    var formData = new FormData(document.querySelector('#form'));

    // $.post($(this).attr("action"), formData, function(data) {
    //     alert(data);
    // });
        console.log(formData);

        $.ajax({
     type: 'POST',
     url: '/extract',
     data: formData,
     processData: false,
     contentType: false ,
     // beforeSend: function()
     // {
     //     alert('Fetching....');
     // },
     success: function(data)
     {
         console.log(data.text);
         var text = data.text.split('\n').join('<br/>');

         $("#result").empty().append('<div class="container">\n' +
             '      <div class="row">\n' +
             '          <br><br><div class="col-sm-2"></div>\n' +
             '         <br><br> <div class="col-sm-8">\n' +
             '  <br><br><div class="alert alert-success" role="alert">\n' +
             '  <br><h4 class="alert-heading">Text extracted :' +
             '  </h4>\n' +
             '   \n' +
             '  <hr>\n' +
             '  <div id="playground"><p class="mb-0">' + text + '</p>\n</div>' +
             '</div>\n' +
             '          <form method="GET" action="../static/hilitor.js" onsubmit="myHilitor.apply(hilite.value); return false;">'+
             '  <p class="cc"><strong>Search</strong></p><span><input type="text" size="24" name="hilite" value="">'+
             '  <input class="btn btn-light" id="keywords" type="submit" value="Apply">' +
             '  <input class="btn btn-light" type="button" value="Remove" onclick="myHilitor.remove();"></span>'+
             '  <input class="btn btn-light" type="button" id="save-btn" value="Save"/>'+
             '  </form><br><br></div>\n' +
             '          <div class="col-sm-2"></div>\n' +
             '      </div>\n' +
             '  </div>');
         $("#save-btn").click(function downloadText(){
             var val = "data:x-application/text," + escape(data.text);
             window.open(val);
});
        

     },
     error: function(err)
     {
         alert(err);
     }
 });
    e.preventDefault();

});



});
