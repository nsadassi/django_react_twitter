from django.conf import settings

from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url

from .models import Tweet
from .forms import TweetForm

# Create your views here.

ALLOWED_HOSTS = settings.ALLOWED_HOSTS

def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)

def tweet_create_view(request, *args, **kwargs):
    form = TweetForm(request.POST or None)                                      #TweetForm class intialized with data or None
    next_url = request.POST.get("next") or None
    if(form.is_valid()):
        obj = form.save(commit=False)
        obj.save()                                                              # form is saved to the DB
        form = TweetForm() 
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
    return render(request, 'components/form.html', context={"form" : form})


def tweet_list_view(request, *args, **kwargs):
    '''
    REST API VIEW
    Return a nJSON format data 
    So that it is consumend by JavaScript in the frontend
    '''
    qs = Tweet.objects.all()
    tweets_list = [ {"id" : x.id, "content" : x.content, "likes" : 15} for x in qs ]
    data = {
        'isUser' : False,
        'response' : tweets_list,
    }
    return JsonResponse(data)


def tweet_detail_view(request,tweet_id, *args, **kwargs):
    '''
    REST API VIEW
    Return a nJSON format data 
    So that it is consumend by JavaScript in the frontend
    '''
    #if tweet-id does not exist in DB, have to return something default or so.
    data = {
        "id" : tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id=tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = 'Not found'
        status = 404

    return JsonResponse(data, status=status)