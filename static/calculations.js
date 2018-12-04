var stay = dayDiff($('#from').val(),$('#to').val());
$('.dur').html(stay + " night(s)");
$('.dur').show();
console.log(stay);

function getDate( element ) {
  var date;
  try {
	date = $.datepicker.parseDate( dateFormat, element.value );
  } catch( error ) {
	date = null;
  }

  return date;
}
function dayDiff(start,end){
	var startDay = new Date($('#from').val());
	var endDay = new Date($('#to').val());

	var duration = (endDay.getTime() - startDay.getTime())/(1000 * 60 * 60 * 24);
	
	return Math.floor(duration)
}
function calculateCost(days){
	var totalPrice = days * price;
	return totalPrice
}