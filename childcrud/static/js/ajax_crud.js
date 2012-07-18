var childcrud_config = new Array();
    
function ajax_show_form(name, id, cb, form_load_cb){
    var form_url;
    if(id == null){
        form_url = childcrud_config[name].urls['new'];
    } else {
        form_url = childcrud_config[name].urls.edit.replace('/0/', '/'+id+'/');
        childcrud_config[name]['is_editing'] = true;
        var pos = jQuery("#" + name + "-form").offset();
        window.scrollTo(pos.left, pos.top);
    }
	
    if(childcrud_config[name].dialog == 'form'){
        jQuery("#" + name + "-dialog").dialog('open');
    } else {
	   jQuery("#" + name + "-bt").hide();
	   jQuery("#" + name + "-wait").show();	
	}
	
	if(form_load_cb == null && childcrud_config[name].form_load_cb){
		form_load_cb = childcrud_config[name].form_load_cb;
	}

    if(cb == null && childcrud_config[name].form_cb){
        cb = childcrud_config[name].form_cb;
    }
    	
    jQuery("#" + name + "-form").load(form_url, '', function(){
        jQuery(this).fadeIn('slow');
		jQuery("#" + name + "-wait").hide();
        jQuery(this).attr('action', form_url);
        jQuery("#"+ name + "-form").ajaxForm({
			 target:"#" + name + "-form", 
			 success:function(responseText, statusText){         
                jQuery("#" + name + "-wait").hide();
                jQuery(".dateselector").datepicker();
				if(form_load_cb != null){
                    form_load_cb();
                }
                
                if (jQuery(responseText).filter("div.info").length){
					jQuery("#" + name + "-wait").show();

					var params = "";
					if(childcrud_config[name].list_querystring_data_cb)
						params = '?' + jQuery.param(childcrud_config[name].list_querystring_data_cb());

                    jQuery("#" + name + "-list").load(childcrud_config[name].urls.list + params, '', function(){
						jQuery("#" + name + "-wait").hide();
                        if(childcrud_config[name].list_cb) {
                            childcrud_config[name].list_cb();
                        }						
					});
					if(childcrud_config[name].sticky_form){
						jQuery("#" + name + "-form").attr('action', childcrud_config[name].urls['new']);
					} else {
	                    jQuery(this).delay(3000).fadeOut("slow");
						jQuery("#" + name + "-bt").show();						
					}
					if(childcrud_config[name].dialog == 'form'){
                        jQuery("#" + name + "-dialog").dialog('close');
                    }
                    if(cb != null){
                        cb();
                    }
                    
                    childcrud_config[name]['is_editing'] = false;
                    
                }  else {
                    if(childcrud_config[name].dialog == 'form') {
                        jQuery("#" + name + "-dialog").scrollTop(0);
                    }
                }
				
            },
			beforeSubmit: function(){
				jQuery("#" + name + "-wait").show();
			}
        });
        
        jQuery(".dateselector").datepicker();
        if(form_load_cb != null){
            form_load_cb();
        }		
    });
}

function ajax_delete(name, id, cb){
    if(childcrud_config[name]['is_editing']){
        alert('Durante a edição, não é possível excluir um item!');
    } else {
        if(confirm("Tem certeza que deseja excluir este item?")){
        	var params = '';
			if(childcrud_config[name].list_querystring_data_cb)
				params = '?' + jQuery.param(childcrud_config[name].list_querystring_data_cb());
        	
           jQuery("#" + name + "-list").load(childcrud_config[name].urls.list + params, {'del': id}, function(responseText, statusText){
                jQuery(this).find("div.info").delay(3000).fadeOut("slow");
                if(childcrud_config[name].list_cb) {
                    childcrud_config[name].list_cb();
                }                       
               
           });  
           if(cb == null && childcrud_config[name].delete_cb){
               cb = childcrud_config[name].delete_cb;
           }       
           if(cb != null){
               cb();
           }       
        }        
    }
}

var gen_ajax_dialogs = new Array();
function ajax_init_config(name){
    var w = 600, h = 350;
	
	if(childcrud_config[name].width) 
	   w = childcrud_config[name].width;

    if(childcrud_config[name].height)
       h = childcrud_config[name].height;
	 
	
	if(childcrud_config[name].dialog){
		if(!gen_ajax_dialogs[name]){
	        jQuery("#" + name + "-dialog").dialog({
	                 bgiframe: true,
	                 width: w,
	                 height: h,
	                 modal: true,
	                 autoOpen: false,
	                 closeOnEscape: false,
	                 close: childcrud_config[name].close_cb
	        });     
            gen_ajax_dialogs[name] = true;			
		}
	}
	
	if(childcrud_config[name].sticky_form){
		jQuery("#" + name + "-bt").hide();
	}	
	
	jQuery("#" + name + "-bt").click(function(){
	    ajax_show_form(name);
    });	
	
	jQuery("#" + name + "-bt").after('<span class="wait" id="' + name + '-wait" style="display:none;">Aguarde...</span>');
	
	if(childcrud_config[name].dialog == 'form' || childcrud_config[name].dialog == null) {
		ajax_init_list(name);
	}
	
}

function ajax_init_list(name, skipformreload){
	if(childcrud_config[name].sticky_form){
		
		if(!skipformreload) 
			ajax_show_form(name);
	} else {
		jQuery("#" + name + "-form").hide();
	}
	jQuery("#" + name + "-wait").show();
	
	var params = "";
	if(childcrud_config[name].list_querystring_data_cb)
		params = '?' + jQuery.param(childcrud_config[name].list_querystring_data_cb());
		
    jQuery("#" + name + "-list").load(childcrud_config[name].urls.list + params, '', function(){
		jQuery("#" + name + "-wait").hide();
        if(childcrud_config[name].list_cb) {
            childcrud_config[name].list_cb();
        }                       
	});
}

function ajax_cancel_form(name){
	jQuery("#" + name + "-form").fadeOut();
	jQuery("#" + name + "-bt").show();
	if(childcrud_config[name].dialog == 'form'){
		jQuery("#" + name + "-dialog").dialog('close');
	}
	
	childcrud_config[name]['is_editing'] = false;
}

function ajax_show_dialog(name, url_new, url_list){
	childcrud_config[name].urls.list = url_list;
	childcrud_config[name].urls['new'] = url_new;
	childcrud_config[name].urls.edit = url_new.replace('/new/', '/0/');
	jQuery("#" + name + "-bt").show();
	jQuery('#' + name + '-dialog').dialog('open');
	ajax_init_list(name);
}
