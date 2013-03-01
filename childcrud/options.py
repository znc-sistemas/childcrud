from django.contrib.admin.options import ModelAdmin
from django.contrib.contenttypes.generic import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.forms.models import _get_foreign_key


def get_generic_fk_field(model):
    for name, field in model.__dict__.items():
        if isinstance(field, GenericForeignKey):
            return field
    return None


class ChildModelAdmin(ModelAdmin):
    """
    Options for CRUD of child models
    """
    parent_model = None
    fk_name = None
    is_generic_fk = False

    # Flag to indicate if the form (ModelForm) needs to be instantiated with parent model
    form_receives_parent = False

    def set_parent_info(self, parent_model=None, fk_name=None):
        # TODO: should use property on parent_model
        self.parent_model = parent_model
        if self.parent_model:
            if self.is_generic_fk:
                # Generic FK (GenericRelation)
                field = get_generic_fk_field(self.model)
                if field:
                    self.fk_field = field.fk_field
                    self.ct_field = field.ct_field
            else:
                # Normal FK
                fk = _get_foreign_key(self.parent_model, self.model, fk_name)
                self.fk_name = fk.name

    def get_form(self, request, obj=None, parent_model=None, fk_name=None, **kwargs):
        """Returns a Form class, excluding the appropriate fields"""

        self.set_parent_info(parent_model, fk_name)

        exclude = kwargs.get('exclude', [])
        if self.parent_model:
            # additional code to exclude parent FK and other relevant fields

            if hasattr(self.form, '_meta'):
                if self.form._meta.exclude:
                    exclude_fields = list(self.form._meta.exclude)
                else:
                    raise TypeError("add the parent to exclude (can not be blank)")
            else:
                exclude_fields = []

            if self.is_generic_fk:
                exclude_fields.extend([self.fk_field, self.ct_field])
            else:
                exclude_fields.extend([self.fk_name])

            if 'user_add' in self.model._meta.get_all_field_names():
                exclude_fields.extend(['user_add', 'data_add'])
            if 'user_upd' in self.model._meta.get_all_field_names():
                exclude_fields.extend(['user_upd', 'data_upd'])

            for e in exclude_fields:
                if e not in exclude:
                    exclude.append(e)

        if exclude:
            kwargs.update({'exclude': exclude})

        return super(ChildModelAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change, parent_obj=None):
        if parent_obj:
            if not change:
                # saves the parent FK object
                if self.is_generic_fk:
                    ct = ContentType.objects.get_for_model(parent_obj)
                    setattr(obj, self.fk_field, parent_obj.pk)
                    setattr(obj, self.ct_field, ct)
                else:
                    setattr(obj, self.fk_name, parent_obj)
            if hasattr(obj, 'user_upd_id'):
                obj.user_upd = request.user
            if not obj.pk:
                if hasattr(obj, 'user_add_id'):
                    obj.user_add = request.user

        obj.save()
        form.save_m2m()

        # can include additional actions logging here

    def delete_model(self, request, obj, parent_obj=None):
        obj.delete()

        # can include additional actions logging here
