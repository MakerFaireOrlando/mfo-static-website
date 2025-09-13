console.log("isotope helper js loaded -010");


//new for Jul 2025 - switch category mechanism
//var initFilter = ':not(.combat-robots)';
var initFilter = '';


if (window.location.href.includes("categories")) {

  const pathSegments = window.location.pathname.split('/');
  const cat = pathSegments.filter(Boolean).pop();
  console.log("Category slug: ", cat);
  jQuery('.filters-select').val('.' + cat);
}
  else {
    //jQuery('.filters-select').val(':not(.combat-robots)');
  }



// quick search regex
var qsRegex;

var $container = jQuery('#exhibits');    // Container for the all post items

// init
$container.isotope({
  // options
  itemSelector: '.item',    // Individual post item selector
  masonry: {
    	gutter: 20,
      isFitWidth: true
  },
//  filter: function() {
//    return qsRegex ? jQuery(this).text().match( qsRegex ) : true;
    filter: initFilter
//  layoutMode: 'fitRows'
});

$(window).on("load", function() {
//previously used the imagesLoaded() function and it was running hundreds of times!
//$container.imagesLoaded().progress( function () {
  console.log("Calling isotope.layout");
  $container.isotope('layout');
});

 // Enable filter buttons to behave as expected
jQuery('.button-group').on( 'click', 'button', function() {
  var filterValue = jQuery(this).attr('data-filter');
  $container.isotope({ filter: filterValue });
  console.log("filter:" + filterValue);
  var textValue = "Category: ";
  textValue += jQuery(this).attr('data-text');
  jQuery('div.category-text').text(textValue);
});


// Enable shuffle button
jQuery(function() {
  jQuery('#shuffle').click (function() {
    console.log("Shuffle!");
    $container.isotope('shuffle')
  });

});

var fv = jQuery('#category').attr('class');
if (fv) {
	console.log("filter category:" + fv);
	$container.isotope({ filter: fv });


	//set select to the right item
	//document.getElementById('makers-category-select').value=fv;
}

//if url params are used...
//var cat = jQuery('#cat-param').text();
//var hashcat = "#" + cat;
//console.log("hashcat:" + hashcat);
//var fv = "." + cat;
//console.log("filter:" + fv);
//$container.isotope({ filter: fv });
//var textValue = "Category: ";
//textValue += jQuery(hashcat).attr('data-text');

//jQuery('div.category-text').text(textValue);


// use value of search field to filter
var $quicksearch = jQuery('.quicksearch').keyup( debounce( function() {
  qsRegex = new RegExp( $quicksearch.val(), 'gi' );
  $container.isotope({
    filter: function() {
    return qsRegex ? jQuery(this).text().match( qsRegex ) : true;
  }});


}, 200 ) );

// debounce so filtering doesn't happen every millisecond
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

// filter functions (need the outer function and leaving the inner as examples)
var filterFns = {
  // show if number is greater than 50
  numberGreaterThan50: function() {
    var number = $(this).find('.number').text();
    return parseInt( number, 10 ) > 50;
  },
  // show if name ends with -ium
  ium: function() {
    var name = $(this).find('.name').text();
    return name.match( /ium$/ );
  }
};



// /makers /exhibits /categories pages - bind filter on select change
jQuery('.filters-select').on( 'change', function() {
  // get filter value from option value
  var filterValue = this.value;
  // use filterFn if matches value
  filterValue = filterFns[ filterValue ] || filterValue;

  jQuery('.quicksearch').val('');

  if (filterValue =="*") {
    console.log("redirecting to: /exhibits")
	  window.location = "/exhibits/";
	}
  else {
    url = "/exhibits/categories/" + filterValue.substring(1) + "/"
    console.log("redirecting to: " + url )
    window.location = url;
	}

//  if ( filterValue.includes("battlebot") || filterValue.includes("combat-robot")) window.location.reload();
//  else {
  $container.isotope({ filter: filterValue });
 	console.log("filterValue:" + filterValue);
//	}//end if filtervalue.includes
});



// Schedule Code
var scheduleFilter = ""
var scheduleFilterDay = ""

jQuery('.schedule-filters-select').on( 'change', function() {
  // get filter value from option value
  var filterValue = this.value;
  // use filterFn if matches value
  filterValue = filterFns[ filterValue ] || filterValue;

  jQuery('.quicksearch').val('');

  if (filterValue =="*") {
	  window.history.pushState("object or string", "Title", "/schedule/");
	} else {
    window.history.pushState("object or string", "Title", "/schedule/?category=" + filterValue.substring(1));
	}

  scheduleFilter = filterValue;
  updateSchedule();
});

jQuery('.schedule-filters-select-day').on( 'change', function() {
  // get filter value from option value
  var filterValue = this.value;
  // use filterFn if matches value
  filterValue = filterFns[ filterValue ] || filterValue;

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
