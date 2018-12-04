$( function() {
var dateFormat = "dd/mm/yy",
tet = ["18/12/2018","19/12/2018"]

//choosing the check in date
  from = $( "#from" )
	.datepicker({
	  minDate: 0,
	  defaultDate: "+1w",
	  changeMonth: true,
	  numberOfMonths: 1,
	  beforeShowDay: function(date){
			for (var i = 0; i < tet.length; i++){
				var s = jQuery.datepicker.formatDate(dateFormat, date);
				var booked = tet.indexOf(s) != -1 ;
				if(booked){
					return [false , "reserved","booking"]
				}else{
					return [true , '']
				}
				}
			}
	})
	.on( "change", function() {
	  to.datepicker( "option", "minDate", getDate( this ) );
	}),
  to = $( "#to" ).datepicker({
	minDate: '1',
	firstDay: '1',
	defaultDate: "+1w",
	changeMonth: true,
	numberOfMonths: 1,
	beforeShowDay: function(date){
			for (var i = 0; i < tet.length; i++){
				var s = jQuery.datepicker.formatDate(dateFormat, date);
				var booked = tet.indexOf(s) != -1 ;
				if(booked){
					return [false , "reserved","booking"]
				}else{
					return [true , '']
				}
				
				}
			}
  })
  .on( "change", function() {
	from.datepicker( "option", "maxDate", getDate( this ) );
  });
  
  
} );