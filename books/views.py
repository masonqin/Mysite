from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Template, Context

import os
import json
import thread 

from models import DouBanBook

from django.conf import settings

BASE_DIR = settings.BASE_DIR  
PICS = os.listdir(os.path.join(BASE_DIR, 'static/pics'))

# Create your views here.
from books.models import Book
from bookCralwer import Spider_Model
from books.forms import AddForm

def display_meta(request):
	values = request.META.items()
	values.sort()
	html = []
	for k, v in values:
		html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
	return HttpResponse('<table>%s</table>' % '\n'.join(html))

def search(request):
    error = False

    myModel = Spider_Model()    
    thread.start_new_thread(myModel.Start,())
    #thread.start_new_thread(myModel.GetPage,(9,))

    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search_result.html',
                {'books': books, 'query': q})
    return render_to_response('search_form.html',
        {'error': error})

def ajax(request):
    if request.method == 'POST':
        form = AddForm(request.POST) 
         
        if form.is_valid():
            a = form.cleaned_data['a']
            b = form.cleaned_data['b']
            return render_to_response('ajaxTest.html', {'form': form, 'result':str(int(a) + int(b))})
     
    else:
        form = AddForm()
    return render(request, 'ajaxTest.html', {'form': form})

def add(request):
    a = request.GET['a']
    b = request.GET['b']
    a = int(a)
    b = int(b)
    return HttpResponse(str(a+b))
 
def ajax_list(request):
    a = range(100)
    return HttpResponse(json.dumps(a), content_type='application/json')
    #return JsonResponse(a, safe=False)
 
def ajax_dict(request):
    
    myModel = Spider_Model()    
    thread.start_new_thread(myModel.Start,())

    name_dict = []
    for i in range(1,250):
        p = DouBanBook.objects.get(topNum=i)
        name_dict.append({'titleMain': p.titleMain, 'publisher': p.publisher})

    #print name_dict

    return HttpResponse(json.dumps(name_dict), content_type='application/json')
    #return JsonResponse(name_dict)

def get_pic(request):
    color = request.GET.get('color')
    number = request.GET.get('number')
    name = '{}_{}'.format(color, number)

    result_list = filter(lambda x: x.startswith(name), PICS)

    print 'result_list', result_list

    return HttpResponse(
        json.dumps(result_list),
        content_type='application/json')