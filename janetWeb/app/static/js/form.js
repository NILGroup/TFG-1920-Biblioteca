$(document).ready(function() {
	$('form').on('submit', function(event) {
		$.ajax({
			data : {
				message : $('#message').val()
			},
			type : 'POST',
			url : '/process' 
		})
		.done(function(data){
			console.log(data)
			$('#messages').append("<p class='message inMessage'>" + data + "</p>");
			$('#submit').attr("disabled", false)

		});
		$('#messages').append("<p class='message outMessage'>" + $('#message').val() + "</p>")
		$('#submit').attr("disabled", true)
		$('#message').val("")
		event.preventDefault();
	});
});
