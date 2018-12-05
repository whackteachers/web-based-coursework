

$( function() {
var dateFormat = "dd/mm/yy",
checkIn = ["18/12/2018","23/12/2018", "1/1/2019"],
checkOut = ["21/12/2018","30/12/2018","10/1/2019"],
bookedDates = []

for (var i=0; i<checkIn.length;i++){
	var start = $.datepicker.parseDate(dateFormat,checkIn[i]);
	var end = $.datepicker.parseDate(dateFormat,checkOut[i]);
	
	while (start <= end) {
    bookedDates.push(new Date(start));
	console.log(bookedDates[i]);
    start.setDate(start.getDate() + 1);
	}
}


//choosing the check in date
  from = $( "#from" )
	.datepicker({
	  minDate: 0,
	  defaultDate: "+1w",
	  changeMonth: true,
	  numberOfMonths: 1,
	  beforeShowDay: function(date){
			for (var i = 0; i < checkIn.length; i++){
				var s = jQuery.datepicker.formatDate(dateFormat, date);
				var booked = bookedDates.indexOf(s) != -1 ;
				if(booked){
					return [false , "reserved","booking"]
				}else{
					return [true , '']
				}
			}
		},
	  onSelect:function(date){
		  var nextDay = $( "#from" ).datepicker('getDate');
		  nextDay.setDate(nextDay.getDate() + 1);
		  $("#to").datepicker( "option", "minDate", nextDay );
	  },
	  // onChangeMonthYear : function(date){
		  // for (var i = 0; i < checkIn.length; i++){
				// var s = jQuery.datepicker.formatDate(dateFormat, date);
				// var booked = checkIn.indexOf(s) != -1 ;
				// if(booked){
					// return [false , "reserved","booking"]
				// }else{
					// return [true , '']
				// }
			// }
	  // }
	})
	.on( "change", function() {
	  to.datepicker( "option", "minDate", getDate( this ) );
	}),
	//choose check out date
  to = $( "#to" ).datepicker({
	minDate: 0,
	firstDay: '1',
	defaultDate: "+1w",
	changeMonth: true,
	numberOfMonths: 1,
	beforeShowDay: function(date){
			for (var i = 0; i < checkOut.length; i++){
				var s = jQuery.datepicker.formatDate(dateFormat, date);
				var booked = checkOut.indexOf(s) != -1 ;
				if(booked){
					return [false , "reserved","booking"]
				}else{
					return [true , '']
				}
				
				}
	},
	onSelect: function dayDiff(){
	var startDay = $( "#from" ).datepicker('getDate');
	var endDay = $( "#to" ).datepicker('getDate');

	var duration = (endDay - startDay)/(1000 * 60 * 60 * 24);
	$('.dur').html(duration + " night(s)");
	$('.dur').show();
	console.log(duration);
	console.log();
	return Math.floor(duration)
	}
  })
  .on( "change", function() {
	from.datepicker( "option", "minDate", startDay );
  });
  
  
} );

function getDate( element ) {
  var date;
  try {
	date = $.datepicker.parseDate( dateFormat, element.value );
  } catch( error ) {
	date = null;
  }

  return date;
}
