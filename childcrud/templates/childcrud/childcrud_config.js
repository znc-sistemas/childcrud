childcrud_config['{{ variable_name }}'] = {
  urls: {
    'new': "{{ urls.new }}",
    'edit': "{{ urls.edit }}",
    'list': "{{ urls.list }}"
  }{% if options %},
{% for k, v in options.items %}
  {{ k }}: {{ v }}{% if not forloop.last %},{% endif %}{% endfor %}  {% endif %}
}
ajax_init_config('{{ variable_name }}');