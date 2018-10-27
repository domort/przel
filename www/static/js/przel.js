var datatable = null;

$(document).ready(function () {
    var dt = $('#datatable');
    datatable = dt.DataTable();
    dt.fadeIn();
    datatable.columns.adjust();
});

$('.prod-value-text.toggleable > span').on('click', function() {
    var tr = $(this).closest('tr');
    $('.prod-value-input').hide();
    $('.prod-value-text').show();
    tr.find('.prod-value-text').hide();
    tr.find('.prod-value-input').fadeIn();
});

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