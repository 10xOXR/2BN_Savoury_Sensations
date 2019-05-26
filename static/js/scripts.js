$(document).ready(function () {

    $('#sort_by').val(localStorage.getItem("sort_by"));
    localStorage.clear();

    $(".collapsible").collapsible();
    $('.modal').modal({
        dismissible: false,
        onCloseEnd: function () {
            $('#password').val('');
            $('#del-recipes').prop('checked', false);

        }
    });
    $(".sidenav").sidenav();
    $(".tabs").tabs();

    $(".dropdown-trigger").dropdown();
    $("select").formSelect();
    $("select[required]").css({
        display: "block",
        height: 0,
        padding: 0,
        width: 0,
        position: "absolute"
    });

    $('.carousel.carousel-slider').carousel({
        fullWidth: true,
        indicators: true
    });
    autoplay();

    function autoplay() {
        $('.carousel.carousel-slider').carousel('next');
        setTimeout(autoplay, 5000);
    }

    $(function () {
        $("#sort_by").change(function () {
            var value = $(this).val();
            localStorage.setItem("sort_by", value);
            window.location = window.location.pathname + "?" + this.value;
        });
    });

    // set the copyright year dynamically for the footer
	$("#year").html(new Date().getFullYear());
});