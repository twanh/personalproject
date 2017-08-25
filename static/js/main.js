$( document ).ready(function() {
	$( ".search-bar input" ).focus(function() {
		$(this).parent().addClass('search-active');
	}).blur(function(){
		$(this).parent().removeClass('search-active');
	});

	var slider = document.getElementById('price-slider');
	noUiSlider.create(slider, {
	 start: [10, 80],
	 connect: true,
	 step: 1,
	 orientation: 'horizontal', // 'horizontal' or 'vertical'
	 range: {
	   'min': 0,
	   'max': 100
	 }
	});

	// var slider_value = slider.noUiSlider.get()
	// console.log(slider_value)
	
	var slider_start = $('#price-start');
	var slider_end = $('#price-end')
	
	slider.noUiSlider.on('update', function(){
		var values = slider.noUiSlider.get()
		slider_start.html(('&euro; ' + values[0]).split('.')[0]);
		slider_end.html(('&euro; ' + values[1]).split('.')[0]);
	});

});


// $('.search-input').focus(function(){
//   $(this).parent().addClass('focus');
// }).blur(function(){
//   $(this).parent().removeClass('focus');
// })