#from __future__ import absolute_import
#from celery.decorators import periodic_task
#from celery.decorators import task
#from django.core.mail import send_mail
#from celery.task.schedules import crontab
from django.shortcuts import render
from django.shortcuts import render_to_response
from .models import Googlenews,Querynews
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.shortcuts import redirect
from django.http import HttpResponse
from django.template import loader
from django.conf import settings
from django.core.mail import send_mail
import operator
#from post_office import mail, PRIORITY
from .feedbuilder import *
from datetime import datetime
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage



from celery.task.schedules import crontab
from celery.decorators import periodic_task

from renewable.celery import app
from django.core.mail import send_mail



@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def send_store_feed():
    feedsend_list = []
    queries = Querynews.objects.all()
    for que in queries:
        q = que.query
        num=que.num
        my_feeds = get_google_feed(q,num)
        #print my_feeds
        for feeder in my_feeds:
          #pub = time.strftime('%a, %d %b %Y %H:%M:%S GMT', feeder.pubdate)
          pub = time.strftime('%Y-%m-%d %H:%M:%S', feeder.pubdate)
          feeder.pub = pub
          #print pub
          news = Googlenews.objects.all()
          a = 0
          for new in news:
              wholeString = feeder.originalurl
              c1, d1 = wholeString.split('=http')
              whole2 = new.original_url
              c2, d2 = whole2.split('=http')
              if d1 == d2:
                 a = 1
              '''
              if new.title == feeder.title:
                   a = 1
              else:
                  if new.pubdate == feeder.pub and new.pub_agency == feeder.pub_agency:
                     a = 1
              '''
          if a == 0 :
              Googlenews.objects.create(title = feeder.title , pubdate = pub ,original_url = feeder.originalurl , imageurl = feeder.imageurl , description = feeder.description , pub_agency = feeder.pub_agency)
              feedsend_list.append(feeder)
    for fee in feedsend_list:
        print fee.title
    if feedsend_list:
        subject = "Google News"
        to = ['singhalsimran0@gmail.com']
        from_email = 'settings.EMAIL_HOST_USER'
        message = get_template('talks/googlescrap.html').render({'feedsend_list': feedsend_list})
        msg = EmailMessage(subject, message, to=to, from_email=from_email)
        msg.content_subtype = 'html'
        msg.send()




