from django.shortcuts import render
from django.http import HttpResponse
from .models import VideoMaker, colors
from django.core.handlers.wsgi import WSGIRequest

def index(request):
    return HttpResponse("Hello, World!")

def video_maker(request: WSGIRequest, *args):
    
    clrs = sorted(colors, key=lambda clr: clr.name)
    context = {'colors': clrs}
    
    if request.method == "POST":
        text = request.POST.get("text")
        bgClr = request.POST.get("bgClr")
        checkboxes = request.POST.getlist("checkboxes")
        italic = 'italic' in checkboxes
        bold = 'bold' in checkboxes
        txtClr = request.POST.get("txtClr")
        sec = int(request.POST.get("sec"))
        image = VideoMaker.makeImageWithText(text, txtClr, bgClr, italic, bold)
        video = VideoMaker.makeVideo(image, sec)
        context['text'] = text
        context['bgClr'] = bgClr
        context['sec'] = sec
        context['txtClr'] = txtClr
        context['italic'] = italic
        context['bold'] = bold
        context['video'] = video
    else:
        context['text'] = "Text"
        context['bgClr'] = "white"
        context['sec'] = 3
        context['txtClr'] = "black"
    test = render(request, 'video_maker.html' , context)
    return test
