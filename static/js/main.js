$(function() {
  let username;
  $('#start_chat').on('click', function() {
    username = $('#username_input').val();
    $('.modal').removeClass('is-active');
  });
  $('#chat_btn').on('click', function() {
    let message = $('#chat_text').val();
    $.post('/message', {'username' : username, 'message' : message}, function() {
      $('#chat_text').val('');
    });
  });
  // Pusher.logToConsole = true;
  var pusher = new Pusher('6d0fa50e973e9e012e4b', {
    cluster: 'eu',
    encrypted: true
  });

  var channel = pusher.subscribe('chat-channel');
  channel.bind('new-message', function(data) {
      let name = data.username;
      let message = data.message;
      let message_template = `<article class="media">
                              <div class="media-content">
                                <div class="content">
                                  <p>
                                    <strong>${name}</strong>
                                    <br> ${message}
                                  </p>
                                </div>
                              </div>
                            </article>`;

      $('#content').append(message_template);
    });


});
