$(document).ready(function () {

    $('.materialboxed').materialbox();
    $('select').formSelect();
    $('.collapsible').collapsible();
    $('.modal').modal();
    $('.sidenav').sidenav();

    $('form .pageskip').on({
        click: function (event) {
            event.preventDefault();
            var data = $(this).data('action');
            $('#search').attr("action", data);
            $('#search').submit();
        }
    });
});