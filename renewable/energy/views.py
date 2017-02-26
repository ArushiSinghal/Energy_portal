from django.shortcuts import render
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.shortcuts import redirect
from .models import Photo ,Comment
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
from django.template import context
from .forms import  UserForm , UploadIdeaForm ,CommentForm , TextBook , Clothing , Cellphone , Ereader , Transportation , Water , Waste
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UploadIdea , Googlenews , Querynews , Like
import math
from django.http import HttpResponse
from django.contrib.auth.models import UserManager
from django.contrib.auth import login
try:
    from django.utils import simplejson as json
except ImportError:
    import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
def register(request):
        registered = False
        val = 0
        if request.method == 'POST':
                user_form = UserForm(data=request.POST)
                if user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirm']:
                        user = user_form.save(commit=False)
                        if User.objects.filter(email = user.email).count()>=1 or user.email == "":
                                val = 1
                        else:
				user.set_password(user.password)
                                user.save()
				registered = True
				
                else:
                        print user_form.errors

        else:
                user_form = UserForm()
        return render(request,'talks/signup.html',{'user_form': user_form, 'registered': registered, 'val': val,})
def user_login(request):
    if request.method == 'POST':
        if User.objects.filter(email = request.POST['email']).count() ==1:
                a = User.objects.filter(email = request.POST['email'])
                for i in a :
                        username = i.username
                password = request.POST.get('password')
                user = authenticate(username=username, password=password)
                if user:
                        if user.is_active:
                                login(request, user)
				return redirect('pressrelease_short')
                        else:
                                return HttpResponse("Your account is disabled.")
		else:
			return HttpResponse("Invalid login details supplied.")
        else:
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'talks/login.html', {})
@login_required
def restricted(request):
         return HttpResponse("Since you're logged in, you can see this text!")
def user_logout(request):
        logout(request)
        return  redirect('pressrelease_short')
def upload(request):
                uploaded = False
                if request.method == "POST":
                        form = UploadIdeaForm(request.POST, request.FILES)
                        if form.is_valid():
                                post = form.save(commit=False)
                                post.uploader = request.user
                                print 1
                                uploaded = True
                                post.save()
                                print post
                        else:
                                print form.errors
                else :
                        form = UploadIdeaForm()
                return render(request,'talks/talk_edit.html', {'form': form , 'uploaded':uploaded ,})
def home(request):
        return render(request,'talks/base.html')
def user_edit(request,pk):
                Edit = 0
                user = request.user
                if request.method == "POST":
                        user_form = UserForm(data=request.POST , instance=user)
                        if user_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['password_confirm']:
                                Edit = 1
                                user = user_form.save()
                                user.set_password(user.password)
                                user =  user.save()
                                #login(request, user)
                else:
                        user_form = UserForm(instance=user)
                return render(request, 'talks/register_edit.html', {'user_form': user_form, 'Edit':Edit})
def pressrelease_short(request):
    slider_photo= Photo.objects.all().order_by('id')[:4]
    talks = UploadIdea.objects.order_by('-date')[:4]
    return render(request, 'pressrelease/slider.html', {'slider_photo':slider_photo , 'talks':talks })

def talks_list(request):
    talks = UploadIdea.objects.order_by('-date')
    return render(request, 'talks/talks_list.html', {'talks':talks})

def talk_part(request,pk):
   talk = get_object_or_404(UploadIdea, pk=pk)
   no_of_likes = Like.objects.all().filter(like_article = talk).count()
   like = Like.objects.all().filter(like_article = talk , user = request.user).count()
   if request.method == "POST":
       form = CommentForm(request.POST)
       if form.is_valid():
            comment = form.save(commit=False)
            #added by me
            comment.author = request.user
            #my adittion ends here
            comment.post = talk
            comment.save()
            return redirect('talk_part', pk=talk.pk)
   else:
       form = CommentForm()
          
   return render(request, 'talks/talk_part.html', {'talk': talk , 'form': form , 'no_of_likes':no_of_likes , 'like':like })


def add_comment_to_post(request, pk):
    post = get_object_or_404(UploadIdea, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
	    #added by me
	    comment.author = request.user
	    #my adittion ends here
            comment.post = post
            comment.save()
            return redirect('talk_part', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'talks/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('talk_part', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('talk_part', pk=post_pk)
  
def like(request , pk):
   
    talk = get_object_or_404(UploadIdea, pk=pk)
    like = Like.objects.all().filter(like_article = talk , user = request.user).count()
    no_of_likes = Like.objects.all().filter(like_article = talk).count()
    form = CommentForm()
    if request.method == "POST":
    	no_of_likes = no_of_likes + 1
    	create_like = Like(like_article = talk , user = request.user)
    	create_like.save()
    	like = 1
    return render(request, 'talks/talk_part.html', {'talk': talk , 'form': form , 'no_of_likes':no_of_likes,'like':like })


def dislike(request , pk):
	talk = get_object_or_404(UploadIdea, pk=pk)
    	like = Like.objects.all().filter(like_article = talk , user = request.user).count()
    	no_of_likes = Like.objects.all().filter(like_article = talk).count()
    	form = CommentForm()
        if request.method == "POST":
		no_of_likes = no_of_likes - 1
       		a = get_object_or_404(Like , like_article = talk , user = request.user)
        	a.delete()
       		like = 0
       	return render(request, 'talks/talk_part.html', {'talk': talk , 'form': form , 'no_of_likes':no_of_likes,'like':like  })

def news(request):
    feedsend_list = Googlenews.objects.all()
    return render(request, 'talks/googlescrap.html',{'feedsend_list': feedsend_list})  
def books(request):
	carbon_year = 0
        carbon_day  = 0
        val = 0
        if request.method == 'POST':
                book_form = TextBook(data=request.POST)
                if book_form.is_valid():
                        #book = book_form.save(commit=False)	
			softcover = book_form.cleaned_data['softcover']
			hardcover = book_form.cleaned_data['hardcover']
			carbon_year = ((softcover*5)+(hardcover*10.2))*3
			carbon_day = (((softcover*5)+(hardcover*10.2))*3)/231  
			c = ((softcover*5))*3
			c1 = ((hardcover*10.2))*3
			val  = 1  
			cloth_form = Clothing()
                	reader_form = Ereader()
			phone_form = Cellphone()
                	transport_form = Transportation()
                	water_form =  Water()
                	waste_form =  Waste()
			return render(request,'talks/calculator.html',{'book_form': book_form,'val': val,'carbon_year': carbon_year,'carbon_day': carbon_day,'softcover':softcover,'hardcover':hardcover,'cloth_form': cloth_form,'reader_form': reader_form,'waste_form' : waste_form , 'water_form' : water_form , 'transport_form' : transport_form , 'phone_form' : phone_form ,'c':c,'c1':c1,})

                else:
                        print book_form.errors

        else:
                book_form = TextBook()
		cloth_form = Clothing()
		reader_form = Ereader()
		phone_form = Cellphone()
                transport_form = Transportation()
                water_form =  Water()
                waste_form =  Waste()
        return render(request,'talks/calculator.html',{'book_form': book_form,'val': val,'cloth_form': cloth_form,'reader_form': reader_form,'waste_form' : waste_form , 'water_form' : water_form , 'transport_form' : transport_form , 'phone_form' : phone_form ,})
def clothing(request):
        val1 = 0
        if request.method == 'POST':
                cloth_form = Clothing(data=request.POST)
		if cloth_form.is_valid():
                        #book = cloth_form.save(commit=False)
			clothing = cloth_form.cleaned_data['clothing']
                        carbon_year = ((clothing*0.2756*6.5*33)/4)
                        carbon_day = ((clothing*0.2756*6.5*33)/28)
                        val1  = 1
			book_form = TextBook()
                	reader_form = Ereader()
			phone_form = Cellphone()
                	transport_form = Transportation()
                	water_form =  Water()
                	waste_form =  Waste()
			return render(request,'talks/calculator.html',{'cloth_form': cloth_form,'val1': val1,'carbon_year': carbon_year,'carbon_day': carbon_day,'clothing':clothing,'book_form': book_form,'reader_form': reader_form,'waste_form' : waste_form , 'water_form' : water_form , 'transport_form' : transport_form , 'phone_form' : phone_form ,})

                else:
                        print cloth_form.errors

        else:
                cloth_form = Clothing()
		book_form = TextBook()
                reader_form = Ereader()
		phone_form = Cellphone()
                transport_form = Transportation()
                water_form =  Water()
                waste_form =  Waste()
        return render(request,'talks/calculator.html',{'cloth_form': cloth_form,'waste_form' : waste_form , 'water_form' : water_form , 'transport_form' : transport_form , 'phone_form' : phone_form ,'val1': val1,'book_form': book_form,'reader_form': reader_form,})
def ereader(request):
        val2 = 0
        if request.method == 'POST':
                reader_form = Ereader(data=request.POST)
                if reader_form.is_valid():
			e_reader_duration = reader_form.cleaned_data['e_reader_duration']
			readertype = reader_form.cleaned_data['readertype']
                        carbon_year = 65 + ((e_reader_duration*65.0)/132)
                        carbon_day = 65 + ((e_reader_duration*65.0)/(132*7))
			carbon_year1 = 84 + ((e_reader_duration*84.0)/132)
                        carbon_day1 = 84 + ((e_reader_duration*84.0)/(132*7))
			print carbon_year
			print carbon_day
			print carbon_year1
			print carbon_day1
			val2 = 1
			cloth_form = Clothing()
                	book_form = TextBook()
			phone_form = Cellphone()
                	transport_form = Transportation()
                	water_form =  Water()
                	waste_form =  Waste()
			return render(request,'talks/calculator1.html',{'reader_form': reader_form,'waste_form' : waste_form , 'water_form' : water_form , 'transport_form' : transport_form , 'phone_form' : phone_form ,'cloth_form': cloth_form,'val2': val2,'carbon_year': carbon_year,'carbon_day': carbon_day,'carbon_year1': carbon_year1,'carbon_day1': carbon_day1,'e_reader_duration': e_reader_duration, 'readertype': readertype,'book_form': book_form,})			
                else:
                        print reader_form.errors

        else:
		cloth_form = Clothing()
                book_form = TextBook()
                reader_form = Ereader()
		phone_form = Cellphone()
		transport_form = Transportation()
		water_form =  Water()
		waste_form =  Waste()
        return render(request,'talks/calculator.html',{'reader_form': reader_form,'val2': val2,'book_form': book_form,'cloth_form': cloth_form,'waste_form' : waste_form , 'water_form' : water_form , 'transport_form' : transport_form , 'phone_form' : phone_form ,})
