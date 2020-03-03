var mapCount = 0;

//Se desactiva el text to speech por defecto
var speech = false;

$(document).ready(function() {
	$('form').on('submit', function(event) {
		//Elimina todas las tildes antes de enviar. Puede que tambien se quiera eliminar otros caracteres.
		
		sendDataToJanet($('#message').val());

		event.preventDefault();
		
	});









	//PONGO AQUI LA LICENCIA DE ESTE CODIGO
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
      
        let AudioContext = window.AudioContext ||  window.webkitAudioContext;
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

      		onComplete: function(recorder, blob) {
		    	console.log("MISSION COMPLETE");

		    	//We can't send a binary directly though AJAX, so we will have to create a FormData with it
		    	var fd = new FormData();
				fd.append('audio', blob, 'audio');

		    	$.ajax({
		    		
					data : fd,
					type : 'POST',
					url : '/processAudio',
					processData: false,
    				contentType: false
				})
				.done(function(data){
					if (data != '') {
						console.log("DATA " + data)
						sendDataToJanet(data);
					}
					console.log("Done");
				});
			},
			onError: (recorder, err) => {
		    	console.error(err);
			},
			onEncoderLoaded: function(recorder, encoding) {
				console.log("LO HEMOS CARGADO");
			}
      	});

		var recordButton = document.getElementById("recordButton");
		recordButton.addEventListener("click", toggleRecording);

		function toggleRecording() {
			if (recorder)
			{
				if (recorder.isRecording()) {
			   		recordButton.innerHTML = "<img src=\"../static/img/mic.svg\" alt=\"grabar\">";
			        recorder.finishRecording();
			        console.log(recorder.recordingTime());
			    } else {
		        	recordButton.innerHTML = "<img src=\"../static/img/stop.svg\" alt=\"parar\">";
		            recorder.startRecording();
			    }
		    }    
		}
      }, function () {
      	//PONER AQUI LO QUE PASA SI NO SE DA PERMISO DE MICRO O SI NO FUNCIONA POR ALGUNA RAZON
      	console.log("NO TENEMOS MICRO SEÑORES")
      });
    

	
/*
	recorder.onComplete = function(recorder, blob) {
		var url = URL.createObjectURL(blob);
	    var preview = document.createElement('audio');
	    preview.controls = true;
        preview.src = url;
        document.body.appendChild(preview);
	};

	var recordButton = document.getElementById("recordButton");
	recordButton.addEventListener("click", toggleRecording);

	function toggleRecording() {
		if (recorder)
		{
			if (recorder.isRecording()) {
		   		recordButton.innerHTML = "Record";
		        recorder.finishRecording();
		    } else {
	        	recordButton.innerHTML = "Stop";
	            recorder.startRecording();
		    }
	    }    
	}
*/
	//---------------------------------------------------------------------------------------------------------------------------------------------------------------


});

function sendDataToJanet(mes)
{
	$('#submit').attr("disabled", true)
	$('#messages').append("<div class='row justify-content-end'><div class='col-9 col-md-5 message outMessage'><p>" + mes + "<p></div></div>")
	mes = mes.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
	$.ajax({
		data : {
			message : mes
		},
		type : 'POST',
		url : '/process'
	})
	.done(function(data){
		oldData = data;
		data = JSON.parse(data);
		if (data.errorno == 0){
			//Genera la respuesta por voz
			if (speech){
				//Voz temporal
				var msg = new SpeechSynthesisUtterance(data.response);
				speechSynthesis.getVoices().forEach(voice => {
				    console.log(voice.name, voice.lang)
				  })
				msg.lang = 'es';
				window.speechSynthesis.speak(msg);
			}

			$('#messages').append("<div class='row'><div class='col-9 col-md-5 message inMessage'><p>" + data.response + "</p></div></div>");

			switch(data["content-type"]){
				case "list-books":
					$('#messages').append();
					data.books.forEach(function(element) {
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

				default:
					break;
			}

		}
		else {
			$('#messages').append("<div class='row'><div class='col-9 col-md-5 message inMessage'><p>" + "No he podido realizar la consulta." + "</p></div></div>");
			//De momento no hace textToSpeech en este mensaje, si se va a quedar habría que refactorizar eso
		}
		newMessageScroll();
		$('#submit').attr("disabled", false)
		$('#message').val("")

	});
}


function addMap(lat, long, location){
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
function getBookHTML(title, author, url = undefined)
{
	if (typeof url !== 'undefined')
		return "<a target='_blank' href='" + url + "'><h3>" + title + "</h3></a><h4>" + author + "</h4>";
	else
		return "<h3>" + title + "</h3><h4>" + author + "</h4>";
}

//Hace scroll hasta el final del documento
function newMessageScroll()
{
	$("html, body").animate({ scrollTop: document.body.scrollHeight }, "slow");
}

