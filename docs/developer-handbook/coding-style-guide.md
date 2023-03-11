Django Coding Style Guide
The following guide outlines the recommended coding style for writing Django applications.

### General
- Use 4 spaces for indentation.
- Use double quotes for strings.
- Use clear and descriptive names for variables, functions, and classes.
- Use comments to explain complex code or to provide context.
- Write docstrings for functions and classes.
- Follow the PEP 8 style guide for Python code.

### Models
- Use singular names for models (Person instead of Persons).
- Use `CamelCase for` model names.
- Define `__str__` method for models to provide a string representation.
- Define get_absolute_url method for models that have a unique URL.

````python
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("person_detail", args=[str(self.id)])
````

### Views
- Use function-based views unless the view requires complex logic or interactions with multiple models.
- Use `snake_case` for function names.
- Use lowercase_with_underscores for URL names.
- Define constants for URL patterns.

````python
from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def contact_us(request):
    return render(request, "contact_us.html")

app_name = "myapp"
urlpatterns = [
    path("", home, name="home"),
    path("contact-us/", contact_us, name="contact_us"),
]
````

### Templates
- Use `snake_case` for template file names.
- Use Django template language to access dynamic content and define control structures.
- Use template inheritance to avoid repetition and to provide a consistent layout across pages.


````html
<!-- base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <title>{% block title %}{% endblock %}</title>
</head>
<body>
    <header>
        {% block header %}
        <nav>
            <ul>
                <li><a href="{% url 'home' %}">Home</a></li>
                <li><a href="{% url 'contact_us' %}">Contact Us</a></li>
            </ul>
        </nav>
        {% endblock %}
    </header>
    <main>
        {% block content %}
        {% endblock %}
    </main>
    <footer>
        {% block footer %}
        <p>&copy; My Company</p>
        {% endblock %}
    </footer>
</body>
</html>

<!-- home.html -->
{% extends "base.html" %}

{% block title %}
Home Page
{% endblock %}

{% block content %}
<h1>Welcome to our website!</h1>
{% endblock %}
````

### Forms
- Use Django's built-in form classes to validate and process form data.
- Use `snake_case` for form class names.

````python
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # Send email using form data
        pass
````