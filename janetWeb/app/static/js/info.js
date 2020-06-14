var contrastMode = false;

$(document).ready(function() {
    var contrastButton = document.getElementById("contrastButton");
	contrastButton.addEventListener("click", changeStyle);

    function changeStyle() { // Activar/Desactivar el modo de alto contraste
        $('body .message').toggleClass('dark-msg');
		$('.container-fluid').toggleClass('dark-mode');
		$('footer').toggleClass('dark-mode');
		$('.navbar-brand').toggleClass('dark-mode');
		$('body').toggleClass('dark-mode');
		$('#message').toggleClass('dark-mode');
		$('#submit').toggleClass('dark-mode');
		$('#recordButton').toggleClass('dark-mode');
		$('.btn-privacity').toggleClass('dark-mode');
		$('#contrastButton').toggleClass('dark-mode');
		$('body').toggleClass('white-letters');
        $('hr').toggleClass('dark-mode');

		if (contrastMode == false) {
			$('#contrastButton').attr('title', 'Activar modo de vista normal');
			contrastMode = true;
		}
		else {
			$('#contrastButton').attr('title', 'Activar modo de alto contraste');
			contrastMode = false;
		}
    }
});
