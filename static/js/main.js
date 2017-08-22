$( document ).ready(function() {
	$( ".search-bar input" ).focus(function() {
		$(this).parent().addClass('search-active');
	}).blur(function(){
		$(this).parent().removeClass('search-active');
	});

});


// $('.search-input').focus(function(){
//   $(this).parent().addClass('focus');
// }).blur(function(){
//   $(this).parent().removeClass('focus');
// })