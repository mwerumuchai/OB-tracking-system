/*
  **********************************************************
  * OPAQUE NAVBAR SCRIPT
  **********************************************************
  */

  //  Toggle tranparent navbar when the user scrolls the page

  $(window).scroll(function() {
    if($(this).scrollTop() > 50)  /*height in pixels when the navbar becomes non opaque*/
    {
        $('.opaque-navbar').addClass('opaque');
    } else {
        $('.opaque-navbar').removeClass('opaque');
    }
});

// when .modal-wide opened, set content-body height based on browser height; 200 is appx height of modal padding, modal title and button bar

$(".modal-wide").on("show.bs.modal", function() {
  var height = $(window).height() - 200;
  $(this).find(".modal-body").css("max-height", height);
});

// tabs
(function($) {

	var tabs =  $(".tabs li a");

	tabs.click(function() {
		var terms = this.hash.replace('/','');
		tabs.removeClass("active");
		$(this).addClass("active");
    $("#terms").find('p').hide();
    $(terms).fadeIn(200);
	});

})(jQuery);
