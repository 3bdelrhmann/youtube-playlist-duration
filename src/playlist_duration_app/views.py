from django.shortcuts import render
import urllib.request
from bs4 import BeautifulSoup
import sys,os
import random
from .forms import linkForm
# Create your views here.
def index(request):
	duration = None
	form = linkForm()		

	if request.method == 'POST': 
		form = linkForm(request.POST)  
		if form.is_valid():
			link = form.cleaned_data['link'] ## get our link from form
			url  = link 
			## Check if link is a valid url
			try:
				page = urllib.request.urlopen(url) ## open url 
				soup = BeautifulSoup(page,'html')

				orig_stdout = sys.stdout
				randNum = random.randrange(9999) 
				fileName = 'out'+str(randNum)+'.html'
				f = open(fileName, 'w')
				sys.stdout = f

				print(soup.html.parent.encode("utf-8"))
				sys.stdout = orig_stdout
				## after this code we now having creat a new file containing a html webpage
				f.close()

					## now we will open this file
				with open(fileName,'r') as f:
					   contents = f.read()
					   htmlFileSoup = BeautifulSoup(contents,'html.parser')
					   mainDurationList = []
					   ## check if our url is a youtube playlist url
					   if htmlFileSoup.select('.pl-video-time .more-menu-wrapper .timestamp span'):
					  	   ## get duration of all videeos in playlist
						   for item in htmlFileSoup.select('.pl-video-time .more-menu-wrapper .timestamp span'):

						    ## and now we will clean our duration 
						    ## <span>\n         10:03\n        <span>
						       r = item.text
						       removeSlash = r.replace('\\n','')
						       removeSpaces = removeSlash.replace(' ','')
						       Change = removeSpaces.split(':')
						       convertStrForInt = [ int(z) for z in Change ]
						       if len(convertStrForInt) < 3:
						           convertStrForInt.insert(0,0)
						           mainDurationList.append(convertStrForInt)
						       else:
						           mainDurationList.append(convertStrForInt)
						   a = [sum(x) for x in zip(*mainDurationList)]
						  
						   if a[1] < 60:
						       mins = a[1] / 60
						       PlaylistDuration = str(a[0]) + ' Hours ' + str(a[1]) + ' Mins'
						   else:
						       PlaylistDuration = str(a[0]) + ' Hours ' + str(a[1]) + ' Mins'
						   duration = PlaylistDuration

					   else:
						   duration = 'Please enter valid playlist url'
				os.remove(fileName)
			except Exception as e:
				duration = e


	else:
		form = linkForm()		

	context = {
		'form' : form,
		'duration' : duration,
		
	}

	return render(request,'playlist_duration_app/index.html',context)