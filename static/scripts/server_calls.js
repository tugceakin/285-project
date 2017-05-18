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