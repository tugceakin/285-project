var portfolioChart, pieChart, myBarChart;

var destroyCharts = function(){
	if(portfolioChart) portfolioChart.destroy();
	if(pieChart) pieChart.destroy();
	if(myBarChart) myBarChart.destroy();
}

var generateWeeklyChartLabels = function(data){
	var labels = [];
	console.log(data);
	for(var i=0; i<data.length; i++){
		labels.push(data[i].date);
	}

	return labels;
}

var generatePieChartLabels = function(data){
	console.log(data);
	var labels = [];
	for (var symbol in data) {
	 labels.push(symbol);
	}
	return labels;
}

var generateClosingPrices = function(data){
	var prices = [];

	for(var i=data.length-1; i>=0; i--){
		prices.push(data[i].close);
	}

	return prices;
}

var generateDailyOverall = function(history_data, divide_data){
	var weekly_data = [0, 0, 0, 0, 0]; //Represents 5 days.

	for(var i=0; i<history_data.length; i++){ //for each stock
		for(var j=0; j<history_data[i].length; j++){ // each day
			weekly_data[j] += divide_data[history_data[i][j].symbol] * history_data[i][j].close;
		}
	}

	return weekly_data;
}


var generateWeeklyChartDataset = function(data){
	var arr = [];
	var history_data = data['history_data'];
	var divide_data = data['divide_data'];
	// debugger

		//var closing_prices = generateClosingPrices(data[i]);
	var weekly_data = generateDailyOverall(history_data, divide_data);

	arr.push(	
	   {
            //label: data[i][0].symbol + ' Closing Price',
            label: "Overall Value",
            data: [{
                x: -10,
                y: weekly_data[0]
            }, {
                x: 0,
                y: weekly_data[1]
            }, {
                x: 10,
                y: weekly_data[2]
            }, {
                x: 10,
                y: weekly_data[3]
            }, {
                x: 0,
                y: weekly_data[4]
            }],
            backgroundColor: 'rgba(75, 192, 192,0.5)',
            borderWidth: 1
        } 
    );

	return arr;
}



var generatePieChartDataset= function(data){
	var dataset = [];
	for (var symbol in data) {
	 dataset.push(data[symbol]);
	}
	return dataset;
}

var generateBarChartDataset= function(data){
	var dataset = [];
	for (var i=0; i<data.length; i++) {
	 dataset.push(data[i][0].close);
	}
	return dataset;
}


var initWeeklyChart = function(data){
	var ctx = document.getElementById("weekly-stock-chart");
	var labels = generateWeeklyChartLabels(data["history_data"][0]);


	portfolioChart = new Chart(ctx, {
	    type: 'line',
	    responsive: true,
	    height: 260,
		// Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
		maintainAspectRatio: false,
	    data: {
	        labels: labels,    
	        datasets: generateWeeklyChartDataset(data)
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

var initPieChart = function(data){
	var ctx = document.getElementById("pie-chart");


	var pieData = {
	    labels: generatePieChartLabels(data["divide_data"]),
	    datasets: [
	        {
	            data: generatePieChartDataset(data["divide_data"]),
	            backgroundColor: [
	                "#FF6384",
	                "#36A2EB",
	                "#FFCE56",
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ],
	            hoverBackgroundColor: [
	                "#FF6384",
	                "#36A2EB",
	                "#FFCE56",
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ]
	        }]
	};

	pieChart = new Chart(ctx, {
		height: 300,
	    type: 'pie',
	    data: pieData,
	    // options:{
	    // 	legend: {
	    //         display: true,
	    //         labels: {
	    //             fontSize: '20'
	    //         }
	    //     }
	    // }

	});
}

var initBarChart = function(data){
	var ctx = document.getElementById("bar-chart");

	var data = {
	    labels: generatePieChartLabels(data["divide_data"]),

	    datasets: [
	        {
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)',
	                'rgba(153, 102, 255, 0.2)',
	                'rgba(255, 159, 64, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255,99,132,1)',
	                'rgba(54, 162, 235, 1)',
	                'rgba(255, 206, 86, 1)',
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ],
	            borderWidth: 1,
	            data: generateBarChartDataset(data["history_data"]),
	        }
	    ]
	};

	myBarChart = new Chart(ctx, {
	    type: 'horizontalBar',
	    data: data,
	    options: { 
	        legend: { 
	            display: false 
	        }
        }
	});
}

var initStockNameDiv = function(names){
	var nameListHTML = "";

	for(var i=0; i<names.length; i++){
		nameListHTML += "<li>" + names[i] + "</li>";
	}

	$("#suggested-stocks-div ul").append(nameListHTML);
}
