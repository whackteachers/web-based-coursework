$( function() {
	//initalize all the check in and check out dates
	var dateFormat = "dd/mm/yy",
	/*["18/12/2018","23/12/2018", "1/1/2019"]*/
	/*["21/12/2018","30/12/2018","10/1/2019"]*/
	
	arrive = document.getElementsByClassName("checkin"),
	leave = document.getElementsByClassName("checkout"),
	checkIn = [],
	checkOut = [];
	for (var i=0; i<arrive.length; i++){
		checkIn.push(arrive[i].innerHTML);
		checkOut.push(leave[i].innerHTML);
	}
	
	console.log(checkIn);

//choosing the check in date
  from = $( "#from" ).datepicker({
	  minDate: 0,
	  defaultDate: "+1w",
	  changeMonth: true,
	  numberOfMonths: 1,
	  //disable all dates that are booked
	  beforeShowDay: function(date){
			for (var i = 0; i < checkIn.length; i++){
				//get date in uk format
				var s = jQuery.datepicker.formatDate(dateFormat, date);
				//look at the first set of checkin and checkOut dates
				var startString = checkIn[i].split("/");
				var temp = "";
				var start = temp.concat(startString[1],"/",startString[0],"/",startString[2]);
				console.log(temp);
				start = new Date(start);
				start = jQuery.datepicker.formatDate(dateFormat, start);
				
				var endString = checkOut[i].split("/");
				var temp = "";
				var end = temp.concat(endString[1],"/",endString[0],"/",endString[2]);
				end = new Date(end);
				end = jQuery.datepicker.formatDate(dateFormat, end);
				
				console.log(s+" "+start+" "+end);
				if(s.getTime <= end.getTime && s.getTime >= start.getTime){
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