// var stay = dayDiff($('#from').val(),$('#to').val());
// $('.dur').html(stay + " night(s)");
// $('.dur').show();
// console.log(price);

$("#from").change(function processPrice(){
	//get the rates array from the table
	var ratesList = document.getElementsByClassName("rates");
	var rates = [];
	for (var i=0; i<ratesList.length; i++){
		rates.push(parseFloat(ratesList[i].innerHTML));
	}
	//get the base price
	var basePrice = parseInt($('.fprice').text);
	//get checkin date
	var arrival = $('#from').val();
	//check the month of date
	var splitDate = arrival.split("/");
	var month = splitDate[1];
	if (month == 12 || month == 1){
		applyRates = rates[0];
	}else if (month == 2){
		applyRates = rates[1];
	}else if (month == 3 || month == 4){
		applyRates = rates[2];
	}else if (month == 5 || month == 6){
		applyRates = rates[3];
	}else if (month == 7 || month == 8){
		applyRates = rates[4];
	}else if (month == 9 || month == 10 || month ==11){
		applyRates = rates[5];
	}
	//multiply by the corresponding rates
	$('.fprice').html("£" + basePrice*applyRates);
	$('.fprice').show();
});
function calculateCost(){
	//get the processed price per night
	var price = parseInt($('.fprice').text.substr(1));
	//get the stay time
	var stay = parseInt($('.dur').text.charAt(0));
	//(parse those to int)
	//multiply them together
	var totalPrice = stay*price;
	//alter the innerHTML
	$('.ttp').html("£" + totalPrice);
	$('.ttp').show();
	
	
	//total price to 0
	//get the date of checkin
	//if checkin and checkout are in same month, total price=71*rates*nights
	//else start by getting the rates on checkin date and go to next day to check rates
}
