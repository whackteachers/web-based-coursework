$( function() {
	var ukFormat = "dd/mm/yy",
	tet = [03/12/2018,04/12/2018]
	
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
				return [ tet.indexOf(string) == -1 ]
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
