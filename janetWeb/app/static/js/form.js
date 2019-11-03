var mapCount = 0;

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
			oldData = data;
			data = JSON.parse(data);
			if (data.errorno == 0){
				//Voz temporal
				var msg = new SpeechSynthesisUtterance(data.response);
				speechSynthesis.getVoices().forEach(voice => {
				    console.log(voice.name, voice.lang)
				  })
				msg.lang = 'es';
				window.speechSynthesis.speak(msg);

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
				newMessageScroll();
			}
			else {
				$('#messages').append("<div class='row'><div class='col-9 col-md-5 message inMessage'><p>" + "No he podido realizar la consulta." + "</p></div></div>");
			}
			$('#submit').attr("disabled", false)


		});
		$('#messages').append("<div class='row justify-content-end'><div class='col-9 col-md-5 message outMessage'><p>" + $('#message').val() + "<p></div></div>")
		newMessageScroll();
		$('#submit').attr("disabled", true)
		$('#message').val("")
		event.preventDefault();
	});
});



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

	//Añadimos el marcador en nuestra ubicacion
	var marker = L.marker([lat, long]).addTo(mymap);
	mapCount++;
}

function getBookHTML(title, author, url = undefined)
{
	if (typeof url !== 'undefined')
		return "<a target='_blank' href='" + url + "'><h3>" + title + "</h3></a><h4>" + author + "</h4>";
	else
		return "<h3>" + title + "</h3><h4>" + author + "</h4>";
}

function newMessageScroll()
{
	$("html, body").animate({ scrollTop: document.body.scrollHeight }, "slow");
}
