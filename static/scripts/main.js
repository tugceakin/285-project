$(document).ready(function(){

	//Init investing strategy dropdown
	$('.selectpicker').selectpicker({
		size: 6
  	});

	//On button click, submit user input to get stock data.
  	$( "#submit-form" ).click(submitForm);
  	//submitForm();
});

 