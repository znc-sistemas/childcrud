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
    var id_target = id;
    var dialog_div = jQuery(id);
    var is_boostrap_modal = dialog_div.hasClass('modal');
    if (is_boostrap_modal) {
        id_target = id + ' .modal-body';
    }


    jQuery(the_form).ajaxSubmit({
        target: id_target
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
    var dialog_div = jQuery('#' + id + '-dialog');

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

    var is_boostrap_modal = dialog_div.hasClass('modal'); 

    if(is_boostrap_modal) {
        $('body').append(dialog_div);
        dialog_div.modal('show');

        jQuery('#' + id + '-dialog .modal-header h3').html(title);
        jQuery('#' + id + '-dialog .modal-body').load(url, null, formload_cb);
    } else {
        dialog_div.attr('title', title);
        dialog_div.dialog({
                bgiframe: true,
                width: width,
                height: height,
                modal: true,
                autoOpen: false,
                close: function(){
                }
            });        
        dialog_div.load(url, null, formload_cb);
        dialog_div.dialog('open');
    }

    return false;
}

function ajax_cancel_form(name) {
    var dialog_div = jQuery('#id_' + name + '-dialog');
    var is_boostrap_modal = dialog_div.hasClass('modal');
    
    if(is_boostrap_modal) {
        dialog_div.modal('hide');
    } else {
        dialog_div.dialog('close');
    }
}