function changeFK(the_select){
    var id = jQuery(the_select).attr('id');
    if(jQuery(the_select).val() === ''){
        jQuery('#bt-' + id + '-editar').hide();
    } else {
        jQuery('#bt-' + id + '-editar').show();
    }
}

function fk_submit(the_form){

    var id = "#" + jQuery(the_form).attr('id').replace('-form', '-dialog');
    jQuery(the_form).ajaxSubmit({
        target: id
    });
    jQuery(the_form).find('input[type]=submit').attr('disabled', true);
    return false;
}

function fk_dialog(the_button, url, title, options) {

    var the_select = jQuery(the_button).parent().find('select');
    var id = the_select.attr('id');

    var is_upd = url.search('/0/') != -1;
    var width = 500;
    var height = 400;


    if(is_upd){
        url = url.replace('/0/', '/' + the_select.val() + '/');
    }

    url = url + '?fid=' + id;

    formload_cb = null;

    if(options) {
        if(options.width)
            width = options.width;
        if(options.height)
            height = options.height;
        if(options.formload_cb)
            formload_cb = options.formload_cb;
    }

    jQuery('#' + id + '-dialog').attr('title', title);

    jQuery('#' + id + '-dialog').dialog({
        bgiframe: true,
        width: width,
        height: height,
        modal: true,
        autoOpen: false,
        close: function(){
        }
    });

    jQuery('#' + id + '-dialog').load(url, null, formload_cb);

    jQuery('#' + id + '-dialog').dialog('open');

    return false;
}