console.log("SCHEDULE isotope helper js loaded -010");

var initFilter = '';

// quick search regex
var qsRegex;

var $container = jQuery('#events');    // Container for the all post items

// init
$container.isotope({
  // options
  itemSelector: '.item',    // Individual post item selector
  masonry: {
    	gutter: 20,
      isFitWidth: true
  },
    filter: initFilter
});

$(window).on("load", function() {
  console.log("Calling isotope.layout");
  $container.isotope('layout');
});


var fv = jQuery('#category').attr('class');
if (fv) {
	console.log("filter category:" + fv);
	$container.isotope({ filter: fv });
}


// use value of search field to filter
var $quicksearch = jQuery('.quicksearch').keyup( debounce( function() {
  //search doesn't respect the filters, need to set the controls back to "show all"
  jQuery('.schedule-filters-select').prop('selectedIndex', 0);
  jQuery('.schedule-filters-select-day').prop('selectedIndex', 0);
  qsRegex = new RegExp( $quicksearch.val(), 'gi' );
  $container.isotope({
    filter: function() {
    return qsRegex ? jQuery(this).text().match( qsRegex ) : true;
  }});


}, 200 ) );

// debounce so search filtering doesn't happen every millisecond
function debounce( fn, threshold ) {
  var timeout;
  return function debounced() {
    if ( timeout ) {
      clearTimeout( timeout );
    }
    function delayed() {
      fn();
      timeout = null;
    }
    timeout = setTimeout( delayed, threshold || 100 );
  }
}


// Schedule Code
var scheduleFilter = ""
var scheduleFilterDay = ""

jQuery('.schedule-filters-select').on( 'change', function() {
  // get filter value from option value
  var filterValue = this.value;

  jQuery('.quicksearch').val('');

  scheduleFilter = filterValue;
  updateSchedule();
});

jQuery('.schedule-filters-select-day').on( 'change', function() {
  // get filter value from option value
  var filterValue = this.value;

  jQuery('.quicksearch').val('');

  scheduleFilterDay = filterValue;
  updateSchedule();
});

function updateSchedule() {
  scheduleValue = scheduleFilter + scheduleFilterDay

  if (scheduleValue == "") {
    $container.isotope({ filter: scheduleValue });
  } else {
    $container.isotope({ filter: scheduleValue });
  }
   console.log("filterValue:" + scheduleValue);  
}
