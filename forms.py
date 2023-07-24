from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Task, new_user, contact

class dateinput(forms.DateInput):
    input_type = 'date'

 
# ========== class-to-generate-task-from ==========
   
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task 
        fields = ['tasktitle',  
                  'taskDesc', 'developer','deadline']
        widgets ={
            'deadline':dateinput(),
            'taskDesc':forms.Textarea(attrs={'rows': 5, 'cols': 3}),
            
        }


# ========== class-to-generate-update-from ==========

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Task 
        fields = ['status']
       

# ========== class-to-generate-user-from ==========

class NewUser(UserCreationForm):
    class Meta:
        model = new_user
        fields = ['first_name', 'last_name', 'username',
                  'designation', 'profile', 'email', 'password1', 'password2']


# ========== class-to-generate-contact-from ==========

class contactform(forms.ModelForm):
    class Meta:
        model = contact
        fields = '__all__'
