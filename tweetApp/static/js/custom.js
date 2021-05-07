$(document).ready(function () {
    // $('#textInput').keydown(delay(function(e){
    //   $('#twitter-field').html($(this).val());
    // }, 200));

    $(window).keydown(function(event){
      if(event.keyCode == 13) {
        event.preventDefault();
        return false;
      }
    });

    $('#textInput').keydown(function(e){
      if(e.keyCode == 32 || e.keyCode == 229){
        var text = $(this).val()
        $.ajax({
          url: '/',
          type: 'POST',
          // dataType: 'json',
          data: {
            'text': text,
            'csrfmiddlewaretoken': csrftoken
          },
          success: function(response){
            $(".btn.btn-suggestions").css('visibility', 'visible')
            $("#top1").html(response.top1)
            $("#top2").html(response.top2)
            $("#top3").html(response.top3)
            $('#twitter-field').val(response.tweet)
          }
        })
      }
    }),

    $('#reset-button').click(function(){
        $('#textInput').val('');
        $('#twitter-field').val('');
        $(".btn.btn-suggestions").css('visibility', 'hidden');
    });
});

// function delay(callback, ms) {
//   var timer = 0;
//   return function() {
//     var context = this, args = arguments;
//     clearTimeout(timer);
//     timer = setTimeout(function () {
//       callback.apply(context, args);
//     }, ms || 0);
//   };
// }

// THIS IS FOR THE CSRFTOKEN
function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie != '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});