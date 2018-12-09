$( function() {
//declare the datepicker to display UK date format
var dateFormat = "dd/mm/yy",
//initalize all the check in and check out dates to arrays
arrive = document.getElementsByClassName("checkin"),
leave = document.getElementsByClassName("checkout"),
checkIn = [],
checkOut = [];
for (var i=0; i<arrive.length; i++){
	checkIn.push(arrive[i].innerHTML);
	checkOut.push(leave[i].innerHTML);
}

//choosing the check in date
  from = $( "#from" ).datepicker({
	  minDate: 0,
	  defaultDate: "+1w",
	  changeMonth: true,
	  numberOfMonths: 1,
	  //disable all checkIn dates
	  beforeShowDay: function(date){
			for (var i = 0; i < checkIn.length; i++){
				var s = jQuery.datepicker.formatDate(dateFormat, date);
				var booked = checkIn.indexOf(s) != -1 ;
				console.log(s);
				console.log(checkIn);
				if(booked){
					return [false , "reserved","booking"]
				}else{
					return [true , '']
				}
			}
		},
	  //limit the date choice of check out day to 1 day after the check in day
	  onSelect:function(date){
		  var nextDay = $( "#from" ).datepicker('getDate');
		  nextDay.setDate(nextDay.getDate() + 1);
		  $("#to").datepicker( "option", "minDate", nextDay );
	  }
	})
	.on( "change", function() {
	  to.datepicker( "option", "minDate", getDate( this ) );
	})
//choose check out date
  to = $( "#to" ).datepicker({
	minDate: 0,
	defaultDate: "+1w",
	changeMonth: true,
	numberOfMonths: 1,
	 //disable all checkout dates
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
	}
  })
  .on( "change", function() {
	from.datepicker( "option", "minDate", getDate( this ) );
  })
})

function getDate( element ) {
  var date;
  try {
	date = $.datepicker.parseDate( dateFormat, element.value );
  } catch( error ) {
	date = null;
  }

  return date;
}