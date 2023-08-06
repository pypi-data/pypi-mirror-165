# django_search_arrayfield

## Quickstart

Install Django better admin ArrayField:

    pip install django-search-arrayfield

Add it to your \`INSTALLED\_APPS\`:

```python
INSTALLED_APPS = (
    ...
    'django_search_arrayfield',
    ...
)
```
## Usage
`django_search_arrayfield` provide dyanimic search in text boxes provides by `django_better_admin_arrayfield`,


Import it like below and use it in your model class definition.
```python
from django_search_arrayfield.models.fields import ArrayField as SearchArrayField
```
as is use to aviod any unneccary conflict with django-better-admin


Import DynamicArrayMixin like below
```python
from django_search_arrayfield.admin.mixins import DynamicArrayMixin
```

In your admin class add `DynamicArrayMixin`:
    ...
```python
class MyModelAdmin(admin.ModelAdmin, DynamicArrayMixin):
```

Inside your admin class add this line:
    ...
```python
change_form_template = 'abc.html'
```
`abc.html` is a file which will add that javascript file(`def.js`) in which function with name RouteToFunction is present
```javascript
<script src="{% static 'js/def.js' %}" ></script>
```

Inside `def.js` file  add a function with name RouteToFunction which will get the input-id of the text box selected 
```javascript
function RouteToFunction(input_id){
}
```

That's it.
