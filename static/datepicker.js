$( function() {
	var ukFormat = "dd/mm/yy",
	tet = ["18/12/2018","19/12/2018"]
	
	//choosing the check in date
      from = $( "#from" )
		.datepicker(
			{
			defaultDate: "+1w",
			changeMonth: true,
			numberOfMonths: 1,
			minDate: 0,
			dateFormat: ukFormat,
			beforeShowDay: function(date){
				for (var i = 0; i < tet.length; i++){
					var s = jQuery.datepicker.formatDate(ukFormat, date);
					var booked = tet.indexOf(s) == -1 ;
					if(!booked){
						return [false , "reserved","booking"]
					}else{
						return [true , '']
					}
					
					}
				}
			}
		)
        .on( "change", 
			function() {
				to.datepicker( "option", "minDate", getDate( this ) );
			}
		),
	  //choosing the check in date
      to = $( "#to" )
	  .datepicker(
		{
			defaultDate: "+1w",
			changeMonth: true,
			numberOfMonths: 1,
			dateFormat: ukFormat,
		}
	  )
      .on( "change", function() 
		{
			from.datepicker( "option", "maxDate", getDate( this ) );
		}
	  );
 
      function getDate( element ) {
      var date;
      try {
        date = $.datepicker.parseDate( dateFormat, element.value );
      } catch( error ) {
        date = null;
      }
 
      return date;
	  }
	} 
);
