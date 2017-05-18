var submitForm = function(){
	var request = getStockData();
	$('.loader').show();
	$('#weekly-chart-div').hide();	  	
  	$('#bar-chart-div').hide();	
  	$('#pie-chart-div').hide();	   

	request
	//If the request is successful, initialize the chart
	.done(function(data) {
	  	console.log(data);
	  	$('.loader').hide();
	  	$('#weekly-chart-div').show();	  	
	  	$('#bar-chart-div').show();	
	  	$('#pie-chart-div').show();	    	
		initWeeklyChart(data);
		initPieChart(data);
  		initBarChart(data);
	})
	.fail(function(jqXHR, textStatus) {
	  console.log('nope');
	});
}
