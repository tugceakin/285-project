var isFormValid = function(){
	var strategies = $('.selectpicker').val();
	var investment = $('#investment').val();
	var isValid = true;
	if(strategies && strategies.length > 2){
		$('.strategy-error').show();
		$('.strategy-error').html('You can choose up to 2 strategies.');
		isValid = false;

	}else if(!strategies || strategies.length < 1){
		$('.strategy-error').show();
		$('.strategy-error').html('Please choose a strategy.');
		isValid = false;
	}


	if(!investment){
		$('.investment-error').show();
		$('.investment-error').html('Please enter an investment amount.');
		isValid = false;
	}

	return isValid;
}

var submitForm = function(){
	$('.error').hide();
	if(isFormValid()){
		var request = getStockData();
		$('.loader').show();
		$('#stock-form').hide();	
		$('#weekly-chart-div').hide();	  	
	  	$('#bar-chart-div').hide();	
	  	$('#pie-chart-div').hide();	 

	  	$('#suggested-stocks-div ul').html("");
	  	$('#suggested-stocks-div').hide();	 

	  	destroyCharts();  

		request
		//If the request is successful, initialize the chart
		.done(function(data) {
		  	console.log(data);
		  	$('.loader').hide();
		  	$('#stock-form').show();	
		  	$('#weekly-chart-div').show();	  	
		  	$('#bar-chart-div').show();	
		  	$('#pie-chart-div').show();	
		  	$('#suggested-stocks-div').show();	
		  	initStockNameDiv(data["stock_names"]);     	
			initWeeklyChart(data);
			initPieChart(data);
	  		initBarChart(data);
		})
		.fail(function(jqXHR, textStatus) {
		  console.log('nope');
		});
	}

}
