from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import Template, Context


# Create your views here.
from books.models import Book
from bookCralwer import Spider_Model

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
    myModel.Start()

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