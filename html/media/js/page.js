window.onload = init;

var prefix = '<a href="javascript:insert(\'';
var suffix = '\')">Insert Image</a>';

function init () {
    CKEDITOR.replace( 'id_content' );
    django.jQuery('.header div').append('<span id="header_url"></span>');
    django.jQuery('#id_header').change(function() {
        updateHeaderLink();
    });
}

function updateHeaderLink() {
    var g_id = django.jQuery('#id_header').val();
    if (g_id > 0) {
        var url = '/g_path/' + g_id + '/';
        django.jQuery.get(url,function(data){
            django.jQuery('#header_url').html(prefix + data + suffix);
        });
    } else { 
        django.jQuery('#header_url').html('');
    }
}

function insert(val) {
    CKEDITOR.instances.id_content.insertHtml('<img src="' + val + '"/>');
}

function do_something() {
    updateHeaderLink();
}