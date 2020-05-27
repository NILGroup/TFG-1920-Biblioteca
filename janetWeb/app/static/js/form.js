var mapCount = 0;

//Se desactiva el text to speech por defecto
var speech = false;

$(document).ready(function () {
	$('form').on('submit', function (event) {
		//Elimina todas las tildes antes de enviar. Puede que tambien se quiera eliminar otros caracteres.

		sendDataToJanet($('#message').val());

		event.preventDefault();

	});

	/*
	License
	Ogg Vorbis encoder part of the library uses JavaScript-converted code of libogg and libvorbis. They are released under Xiph's BSD-like license. Ogg Vorbis encoder part of this library follows the same license (see link below).

	http://www.xiph.org/licenses/bsd/

	MP3 encoder part of this library uses JavaScript-converted code of LAME. LAME is licensed under the LGPL. MP3 encoder part of this library follows the same license (see link below).

	http://lame.sourceforge.net/about.php

	All other parts are released under MIT license (see LICENSE.txt).
	*/

	let options = { audio: true, video: false };

	// the built-in method for capturing audio/video from the user's device
	// pass in the media capture options object and ask for permission to access the microphone
	navigator.mediaDevices.getUserMedia(options)
		.then(stream => {
			console.log("IN")
			currentlyRecording = true;

			let AudioContext = window.AudioContext || window.webkitAudioContext;
			let audioContext = new AudioContext();
			// an audio node that we can feed to a new WebAudioRecorder so we can record/encode the audio data
			let source = audioContext.createMediaStreamSource(stream);
			// the creation of the recorder with its settings:
			let recorder = new WebAudioRecorder(source, {
				// workerDir: the directory where the WebAudioRecorder.js file lives
				workerDir: 'static/js/audioRecorder/',
				// encoding: type of encoding for our recording ('mp3', 'ogg', or 'wav')
				encoding: 'wav',
				options: {
					// encodeAfterRecord: our recording won't be usable unless we set this to true
					encodeAfterRecord: true
				},

				onComplete: function (recorder, blob) {
					console.log("MISSION COMPLETE");

					//We can't send a binary directly though AJAX, so we will have to create a FormData with it
					var fd = new FormData();
					fd.append('audio', blob, 'audio');

					$.ajax({

						data: fd,
						type: 'POST',
						url: $SCRIPT_ROOT + '/processAudio',
						processData: false,
						contentType: false
					})
						.done(function (data) {
							if (data != '') {
								console.log("DATA " + data)
								sendDataToJanet(data);
								$('#loadingMessageMic').remove();
							}
							else {
								$('#loadingMessageMic').remove();
								$('#messages').append("<div class='row'><div class='col-9 col-md-5 message infoMicMessage'><p>" + "No se ha escuchado el mensaje correctamente. Por favor, intentelo de nuevo." + "</p></div></div>");
								$('#notiSound')[0].play();
							}
							console.log("Done");
						});
				},
				onError: (recorder, err) => {
					console.error(err);
				},
				onEncoderLoaded: function (recorder, encoding) {
					console.log("LO HEMOS CARGADO");
				}
			});

			var recordButton = document.getElementById("recordButton");
			recordButton.addEventListener("click", toggleRecording);

			function toggleRecording() {
				if (recorder) {
					recordButton.classList.toggle('grabando');
					if (recorder.isRecording()) {
						var mic_img = $('body').data('mic-img');
						recordButton.innerHTML = '<img src="' + mic_img + '" alt=\"grabar\">';
						recorder.finishRecording();
						console.log(recorder.recordingTime());
					} else {
						var stop_img = $('body').data('stop-img');
						recordButton.innerHTML = '<img src="' + stop_img + '" alt=\"parar\">';
						$('#messages').append("<div id='loadingMessageMic' class='row justify-content-end'><div class='col-9 col-md-5 message outMessage'><span id='loadingMicData'>.</span></div></div>");

						let x = 0;
						setInterval(function () {
							currentDate = Date.now();
							var dots = ".";
							x++;
							for (var y = 0; y < x % 3; y++) {
								dots += ".";
							}
							$("#loadingMicData").text(dots);
						}, 200)
						recorder.startRecording();
					}
				}
			}
		}, function () {
			console.log("No se ha obtenido micrófono"); //TODO
		});

	var voiceButton = document.getElementById("voiceButton");
	voiceButton.addEventListener("click", toggleVoice);

	function toggleVoice() {
		if (speech) {
			speech = false;
			var mute_img = $('body').data('mute-img');
			voiceButton.innerHTML = '<img src="' + mute_img + '" alt=\"Activar Voz\">';
			$('#voiceButton').prop('title', 'Activar lector por Voz');
		}
		else {
			speech = true;
			var vol_img = $('body').data('vol-img');
			voiceButton.innerHTML = '<img src="' + vol_img + '" alt=\"Desactivar Voz\">';
			$('#voiceButton').prop('title', 'Desactivar lector por Voz');
		}
	}

});


function sendDataToJanet(mes) {
	$('#messages').append("<div class='row justify-content-end'><div class='col-9 col-md-5 message outMessage'><p>" + mes + "<p></div></div>")
	mes = mes.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
	$('#messages').append("<div id='loadingmessage' class='row'><div class='col-9 col-md-5 message inMessage'><span id='loading'>.</span></div></div>");

	let x = 0;
	setInterval(function () {
		currentDate = Date.now();
		var dots = ".";
		x++;
		for (var y = 0; y < x % 3; y++) {
			dots += ".";
		}
		$("#loading").text(dots);
	}, 200)

	let valor = Math.random() * (1200 - 700) + 700;
	console.log(valor);
	setTimeout(function () {
		$('#submit').attr("disabled", true)

		$.ajax({
			data: {
				message: mes
			},
			type: 'POST',
			url: $SCRIPT_ROOT + '/process'
		})
			.done(function (data) {
				oldData = data;
				data = JSON.parse(data);
				if (data.errorno == 0) {
					//Genera la respuesta por voz
					if (speech) {
						//Voz temporal
						var msg = new SpeechSynthesisUtterance(data.response);
						speechSynthesis.getVoices().forEach(voice => {
							console.log(voice.name, voice.lang)
						})
						msg.lang = 'es';
						window.speechSynthesis.speak(msg);
					}

					$('#loadingmessage').remove();
					$('#messages').append("<div class='row'><div class='col-9 col-md-5 message inMessage'><p>" + data.response + "</p></div></div>");
					$('#notiSound')[0].play();

					switch (data["content-type"]) {
						case "list-books":
							$('#messages').append();
							data.books.forEach(function (element) {
								var htmlToApend = "<div class='row'><div class='col-9 col-md-5 message inMessage'>";
								htmlToApend += getBookHTML(element.title, element.author);
								$('#messages').append(htmlToApend + "</div></div>");
							});
							break;

						case "single-book":
							var htmlToApend = "<div class='row'><div class='col-9 col-md-5 message inMessage'>";
							htmlToApend += getBookHTML(data.title, data.author, data.url);
							$('#messages').append(htmlToApend + "</div></div>");
							break;

						case "location":
							addMap(data.lat, data.long, data.location)
							break;

						case "phone":
							$('#messages').append("<div class='row'><div class='col-9 col-md-5 message inMessage'><h4>" + data.library + ": " + data.phone + "</h4></div></div>");
							break;

						case "email":
							$('#messages').append("<div class='row'><div class='col-9 col-md-5 message inMessage'><h4>" + data.library + ": " + "<a href='mailto:" + data.email + "'>" + data.email + "</h4></div></div>");
							break;

						default:
							break;
					}

				}
				else {

					$('#loadingmessage').remove();
					$('#messages').append("<div class='row'><div class='col-9 col-md-5 message inMessage'><p>" + "No he podido realizar la consulta." + "</p></div></div>");
					$('#notiSound')[0].play();

					//De momento no hace textToSpeech en este mensaje, si se va a quedar habría que refactorizar eso
				}
				newMessageScroll();
				$('#submit').attr("disabled", false)
				$('#message').val("")

			});
	}, valor);

}


function addMap(lat, long, location) {
	var mapid = 'map' + mapCount;
	mapCount++; //Los mapas necesitan diferentes ids cada uno
	$('#messages').append("<div class='row'><div class='message inMessage'><h4>" + location + "</h4>" +
		"<div class='map' id='" + mapid + "'></div></div></div>");

	var mymap = L.map(mapid).setView([lat, long], 13); //Crea el mapa con un zoom de 13

	//Esto utiliza mapbox para cargar los tiles del mapa y que se vea
	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		maxZoom: 18,
		id: 'mapbox.streets',
		accessToken: 'pk.eyJ1IjoibWlndWVsYWNtIiwiYSI6ImNrMXFteDU1bjA0ajQzY3N4MnJzaTVoc3IifQ.1cLFOA_mizoP0DnpA0S37w'
	}).addTo(mymap);

	//Aniadimos el marcador en nuestra ubicacion
	var marker = L.marker([lat, long]).addTo(mymap);
	mapCount++;
}

//Aniade un libro con su formato html ya dado
function getBookHTML(title, author, url = undefined) {
	if (typeof url !== 'undefined')
		return "<a target='_blank' href='" + url + "'><h3>" + title + "</h3></a><h4>" + author + "</h4>";
	else
		return "<h3>" + title + "</h3><h4>" + author + "</h4>";
}

//Hace scroll hasta el final del documento
function newMessageScroll() {
	$("html, body").animate({ scrollTop: document.body.scrollHeight }, "slow");
}
