var getStockData = function(){
	
	var dataToSend = {
		strategies: $('.selectpicker').val(), //Returns an array consisting of selected strategies
		investment: parseInt($('#investment').val())
	}


	return $.ajax({
	  url: "/stock_data",
	  type: "POST",
	  data: JSON.stringify(dataToSend),
	  contentType:"application/json"
	});
}

var generateChartLabels = function(data){
	var labels = [];

	for(var i=data.length-1; i>=0; i--){
		labels.push(data[i].Date);
	}

	return labels;
}

var generateClosingPrices = function(data){
	var prices = [];

	for(var i=data.length-1; i>=0; i--){
		prices.push(data[i].Close);
	}

	return prices;
}

var initChart = function(data){
	var ctx = document.getElementById("stock-chart");
	var labels = generateChartLabels(data);
	var closing_prices = generateClosingPrices(data);

	var myChart = new Chart(ctx, {
	    type: 'line',
	    responsive: true,

		// Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
		maintainAspectRatio: false,
	    data: {
	        labels: labels,
	        datasets: [{
	            label: data[0].Symbol + ' Closing Price',
	            data: [{
	                x: -10,
	                y: closing_prices[0]
	            }, {
	                x: 0,
	                y: closing_prices[1]
	            }, {
	                x: 10,
	                y: closing_prices[2]
	            }, {
	                x: 10,
	                y: closing_prices[3]
	            }, {
	                x: 0,
	                y: closing_prices[4]
	            }],
	            backgroundColor: 'rgba(75, 192, 192,0.5)',
	            borderWidth: 1
	        }]
	    },
	    options: {
	        scales: {
	            yAxes: [{
	                ticks: {
	                    beginAtZero:false
	                }
	            }]
	        }
	    }
	});
};

var submitForm = function(){
	var request = getStockData();
	$('.loader').show();

	request
	//If the request is successful, initialize the chart
	.done(function(data) {
	  	console.log(data);
	  	$('.loader').hide();
	  	$('#chart-div').show();
		initChart(data);
	})
	.fail(function(jqXHR, textStatus) {
	  console.log('nope');
	});
}

$(document).ready(function(){

	//Init investing strategy dropdown
	$('.selectpicker').selectpicker({
		size: 6
  	});

	//On button click, submit user input to get stock data.
  	$( "#submit-form" ).click(submitForm);
	
});

 