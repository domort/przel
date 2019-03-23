var datatable = null;

$(document).ready(function () {
    // ensure CSRF token is present in every ajax request
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            var csrftoken = getCookie('csrftoken') || $(":input[name='csrfmiddlewaretoken']").val();

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $('.prod-value-text.toggleable').on('click', function () {
        var tr = $(this).closest('tr');
        var table = tr.closest('table');
        table.find('tr').removeClass('active');
        tr.addClass('active');
        tr.siblings('tr.child').first().addClass('active');
        toggle_row_action(table);
    });
});

function toggle_row_action(table) {
    var active_rows = $(table).find('tbody').find('tr.active');
    var nonactive_rows = $(table).find('tbody').find('tr:not(.active)');
    nonactive_rows.find('.prod-value-input, .btn-save').hide();
    nonactive_rows.find('.prod-value-text, .btn-edit').show();
    active_rows.find('.prod-value-text, .btn-edit').hide();
    active_rows.find('.btn-save').show();
    active_rows.find('.prod-value-input').fadeIn();
}

function blockui() {
    $.blockUI({
        css: {
            border: 'none',
            padding: '15px',
            backgroundColor: '#000',
            '-webkit-border-radius': '10px',
            '-moz-border-radius': '10px',
            opacity: .5,
            color: '#fff'
        }
    });
}

function unblockui() {
    $.unblockUI();
}

function save_product_row(caller) {
    var caller_row = $(caller).closest('tr');
    caller_row.removeClass('active');
    toggle_row_action(caller.closest('table'));
}

function send_ajax(caller) {
    var data = $(caller).data();
    var href = data.href;
    if (!href) {
        console.error('send_ajax: href unspecified');
        return -1;
    }
    else {
        blockui();
        $.ajax({
            type: 'POST',
            url: href,
            dataType: 'json',
            data: data,
            success: function (data) {
                location.reload();
            },
            error: function (response, status, error) {
                console.error(response, status, error);
                unblockui();
                alert('Unexpected error. Please try again later.');
            }
        });
    }
}