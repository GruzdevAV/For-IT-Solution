from django.shortcuts import render
from django.http import HttpResponse
from .models import VideoMaker, colors
from django.core.handlers.wsgi import WSGIRequest

def index(request):
    return HttpResponse("Hello, World!")

def video_maker(request: WSGIRequest, *args):
    
    print(args)
    clrs = sorted(colors, key=lambda clr: clr.name)
    context = {'colors': clrs}
    
    if request.method == "POST":
        text = request.POST.get("text")
        bgClr = request.POST.get("bgClr")
        txtClr = request.POST.get("txtClr")
        # filename = request.POST.get("filename")
        # if len(filename)==0: filename = "file"
        image = VideoMaker.makeImageWithText(text, txtClr, bgClr, "temp")
        video = VideoMaker.makeVideo(image)
        context['video'] = video
        context['text'] = text
        context['bgClr'] = bgClr
        context['txtClr'] = txtClr
        # context['filename'] = filename
    else:
        context['text'] = ""
        context['bgClr'] = ""
        context['txtClr'] = ""
        # context['filename'] = ""
    test = render(request, 'video_maker.html' , context)
    return test
