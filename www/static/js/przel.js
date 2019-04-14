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

    $('[data-toggle="tooltip"]').tooltip();
});

function toggle_row_action(table) {
    if (!detectmob()) {
        var active_rows = $(table).find('tbody').find('tr.active');
        var nonactive_rows = $(table).find('tbody').find('tr:not(.active)');
        nonactive_rows.find('.prod-value-input, .btn-save').hide();
        nonactive_rows.find('.prod-value-text, .btn-edit').show();
        active_rows.find('.prod-value-text, .btn-edit').hide();
        active_rows.find('.btn-save').show();
        active_rows.find('.prod-value-input').fadeIn();
    }
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

function detectmob() {
    return window.innerWidth <= 1024;
}

function reload() {
    location.reload();
}

function save_product_row(caller) {
    var caller_row = $(caller).closest('tr');
    var product_slug = caller_row.data('prod-slug');
    var product_data = {};
    caller_row.find('input[name]').each(function (i, input) {
        var name = $(input).attr('name');
        if (name) {
            product_data[name] = $(input).val();
        }
    });
    var url = PRODUCT_UPDATE_URL.replace('XXX', product_slug);
    var on_success = function () {
        caller_row.removeClass('active');
        toggle_row_action(caller.closest('table'));
        location.reload();
    };
    product_data['basic'] = true;
    send_ajax(null, url, product_data, on_success)
}

function send_ajax(caller, url, data, on_success, type, on_error) {
    if (type) {
        type = type.toUpperCase();
    }
    if (!type || type !== 'GET' && type !== 'POST') {
        type = 'POST';
    }
    if (!data && caller) {
        data = $(caller).data();
    }
    if (!data) {
        data = {};
    }
    if (!url) {
        url = data.href;
    }
    if (!url) {
        console.error('send_ajax: href unspecified');
        return -1;
    }
    else {
        blockui();
        $.ajax({
            type: type,
            url: url,
            dataType: 'json',
            data: data,
            success: function (data) {
                if (on_success) {
                    on_success(data);
                } else {
                    location.reload();
                }
            },
            error: function (response, status, error) {
                if (on_error) {
                    on_error(response);
                } else {
                    console.error(response, status, error);
                    unblockui();
                    alert('Unexpected error. Please try again later.');
                }
            }
        });
    }
}

function question_delete(prod_slug, prod_name) {
    $('#update-product-modal').modal('hide');
    var modal = $('#delete-product-modal');
    modal.find('.prod-name').text(prod_name);
    modal.find('.btn-delete').data('href', PRODUCT_DELETE_URL.replace('XXX', prod_slug));
    modal.modal('show');
}

function edit_product_popup(prod_slug, prod_name) {
    var modal = $('#update-product-modal');
    var container = $('#product-form');
    var url = null;
    var action = null;
    if(prod_slug) {
        url = PRODUCT_UPDATE_URL + '/form';
        url = url.replace('XXX', prod_slug);
        modal.find('.btn-delete').attr('onclick', "question_delete('" + prod_slug + "', '" + prod_name + "');");
        modal.find('.btn-delete').show();
        modal.find('.action').text('Edit');
        action = 'updated';
    } else {
        url = PRODUCT_CREATE_URL + '/form';
        modal.find('.btn-delete').attr('onclick', '');
        modal.find('.btn-delete').hide();
        modal.find('.action').text('Create');
        action = 'created';
    }

    modal.find('.btn-submit').attr('onclick', "submit_product('" + url + "', '" + action + "');");
    modal.find('.modal-error').hide();
    var on_success = function (data) {
        container.html(data.form);
        modal.modal('show').on('shown.bs.modal', unblockui);
    };
    send_ajax(null, url, null, on_success, 'GET');
}

function submit_product(url, action) {
    var modal = $('#update-product-modal');
    var success_modal = $('#success-msg-modal');
    var container = $('#product-form');
    var data = container.serializeArray();
    var on_success = function (data) {
        modal.modal('hide').on('hidden.bs.modal', function () {
            success_modal.find('.action').text(action);
            success_modal.modal('show').on('hidden.bs.modal', function () {
                blockui();
                reload();
            });
            unblockui();
        });
    };
    var on_error = function (data) {
        var form = data.responseJSON.form;
        modal.find('.modal-error').show();
        container.html(form);
        unblockui();
        container.find('.is-invalid').first().focus().select();
    };
    send_ajax(null, url, data, on_success, 'POST', on_error);
}