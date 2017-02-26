from django import forms
from django.forms import extras
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from .models import UploadIdea,Comment
from .models import Googlenews,Querynews
from django.contrib.admin.widgets import AdminDateWidget
from django.utils.encoding import python_2_unicode_compatible

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	password_confirm = forms.CharField(widget=forms.PasswordInput())
   	class Meta:
        	model = User
		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','placeholder': 'User-Name'}),
	    'email': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Email-Id'}),
	    }
        	fields = ('username','email','password')
        def clean(self):
                cleaned_data = super(UserForm, self).clean()
                password = cleaned_data.get("password")
                confirm_password = cleaned_data.get("password_confirm")
                if password != confirm_password:
                        raise forms.ValidationError(
                                "password and confirm_password does not match"
                )
class UploadIdeaForm(forms.ModelForm):
        bio = forms.CharField(label='Bio of the Author', widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
	class Meta:
		model = UploadIdea
		fields = ('title','upload_image','content','link','bio',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

class TextBook(forms.Form):
	softcover = forms.IntegerField()
	hardcover = forms.IntegerField()
class Clothing(forms.Form):
	clothing = forms.IntegerField()
class Cellphone(forms.Form):
	phoneduration = forms.IntegerField()
	CHOICES=[('smart phone','smart phone'),('mobile phone','mobile phone')]
	phonetype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
class Ereader(forms.Form):
	e_reader_duration = forms.IntegerField()
	CHOICES=[('ipad','ipad'),('kindle','kindle')]
	readertype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
class Transportation(forms.Form):
	CHOICES=[('yes','yes'),('no','no')]
	drivetype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	#CHOICES1=[('small','average','SUV/truck','hybrid')]
	#cartype = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect())
	CHOICES1=[('small','small'),('average','average'),('SUV/truck','SUV/truck'),('hybrid','hybrid')]
        cartype = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect())
	milestravel = forms.DecimalField(max_digits=25, decimal_places=20)
class Water(forms.Form):
	CHOICES=[('campus resident','campus resident'),('full time commuter student','full time commuter student'),('part time commuter student or faculty + staff','part time commuter student or faculty + staff')]
	studenttype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	showers = forms.IntegerField()
	showers_week = forms.IntegerField()
	laundry_month = forms.IntegerField()
	flushes_day = forms.IntegerField()
	cup_day =  forms.IntegerField()
	CHOICES1=[('yes','yes'),('no','no')]
	refillable = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect()) 
	non_fillable = forms.IntegerField()
class Waste(forms.Form):
	CHOICES=[('campus resident','campus resident'),('full time commuter student','full time commuter student'),('part time commuter student or faculty + staff','part time commuter student or faculty + staff')]
	studenttype = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
	CHOICES1=[('below average','below average'),('average','average'),('above average','above average')]
	wastetype = forms.ChoiceField(choices=CHOICES1, widget=forms.RadioSelect())
	CHOICES2=[('less than 4lbs','less than 4lbs'),('about 4lbs','about 4lbs'),('greater than 4lbs','greater than 4lbs')]
	quantitytype = forms.ChoiceField(choices=CHOICES2, widget=forms.RadioSelect())
