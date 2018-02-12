
function python(code) {
    window.location.href = "x-python://" + code;
}

function debug(string) {
    window.location.href = "x-python://self.debug(\'" + string + "\')";
}

function linkout(url) {
    window.location.href = url;
}

function contextmenu(evt) {
	python('self.onContextMenu(____' + evt.pageX + '____, ____' + evt.pageY + '____, ____' + $(evt.target).closest('.contextmenu').attr('class') + '____, ____' + $(evt.target).closest('.contextmenu').attr('id') + '____)')
}

function reloadPublisher(b64ID) {
	$("#sidebar #" + b64ID + " .badges").hide();
	$("#sidebar #" + b64ID + " .reloadAnimation").show();
	python('self.reloadPublisher(None, ____' + b64ID + '____)');
}

function reloadSubscription(b64ID) {
	// $("#sidebar #" + b64ID + " .badges").hide();
	// $("#sidebar #" + b64ID + " .reloadAnimation").show();
	python('self.reloadSubscription(None, ____' + b64ID + '____)');
}

function finishReloadPublisher(b64ID) {
	$("#sidebar #" + b64ID + " .badges").show();
	$("#sidebar #" + b64ID + " .reloadAnimation").hide();
}

function finishReloadSubscription(b64ID) {
	// $("#sidebar #" + b64ID + " .badges").show();
	// $("#sidebar #" + b64ID + " .reloadAnimation").hide();
}

keypressFunctions = [];

function registerKeypress(key, method) {
	keypressFunctions[key] = method;
}

function unregisterKeypress(key) {
	keypressFunctions[key] = null;
}

$( document ).ready(function() {

	$(document).bind("contextmenu",function(evt){
		contextmenu(evt);
		evt.preventDefault();
    	return false;
	});

	$("#sidebar .publisher").click(function() {
		$("#sidebar .publisher").removeClass('selected');
		$(this).addClass('selected');
		python('self.setPublisherHTML(\'' + $(this).attr('id') + '\')'); 
	});


	$("#main #publisher .removePublisherButton").click(function() {
		$( this ).addClass( "hover" );
		id = $(this).closest('.publisher').attr('id');
		python('self.removePublisher(\'' + id + '\')'); 
	});


	$("#url").on('keyup', function() {
		addUrl = $(this).val();
	});



	// $("#sidebar .publisher").hover(function() {
	//     $( this ).addClass( "hover" );
	//   }, function() {
	//     $( this ).removeClass( "hover" );
	//   }
	// );

	// $("#main .font").hover(function() {
	//     $( this ).addClass( "hover" );
	//   }, function() {
	//     $( this ).removeClass( "hover" );
	//   }
	// );

	$(document).on("keyup", function( event ) {
		for(var key in keypressFunctions) {
		    if(keypressFunctions.hasOwnProperty(key)) {
		        if (event.which == key) {
			        keypressFunctions[key]();
		        }
		    }
		}
	});

});

function showAddPublisher() {
	$('#addPublisher #url').val(null);
	$('#addPublisher').slideDown();
	registerKeypress(27, function(){ hideAddPublisher(); });
	$('#addPublisher #url').focus();
}

function hideAddPublisher() {
	unregisterKeypress(27);
	$('#addPublisher').slideUp();
}

function showMain() {
	$('#welcome').slideUp();
	$('#main').slideDown();
}
function hideMain() {
	$('#welcome').slideDown();
	$('#main').slideUp();
}

function showAbout() {
	$('#about').slideDown();
	registerKeypress(27, function(){ hideAbout(); });
}

function hideAbout() {
	$('#about').slideUp();
	unregisterKeypress(27);
}

/* ///////////////////////////////////////////////////////////////////////////////////////////////////// */


// JQUERY

	$( function() {
	    $( document ).tooltip();
	  } );

