$(document).ready(function () {

    $(".collapsible").collapsible();
    $(".modal").modal({dismissible:false});
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

    $("form .pageskip").on({
        click: function (event) {
            event.preventDefault();
            var data = $(this).data("action");
            $("#search").attr("action", data);
            $("#search").submit();
        }
    });
});