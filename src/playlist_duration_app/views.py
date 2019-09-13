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

				print(soup.encode("utf-8"))
				sys.stdout = orig_stdout
				## after this code we now having creat a new file containing a html webpage
				f.close()

					## now we will open this file
				with open(fileName,'r') as f:
					   contents = f.read()
					   htmlFileSoup = BeautifulSoup(contents,'html.parser')
					   sum = 0
					   videoDuration = []
					   ## check if our url is a youtube playlist url
					   if htmlFileSoup.select('.pl-video-time .more-menu-wrapper .timestamp span'):
					  	   ## get duration of all videeos in playlist
						   for item in htmlFileSoup.select('.pl-video-time .more-menu-wrapper .timestamp span'):

						    ## and now we will clean our duration 
						    ## <span>\n         10:03\n        <span>
						       r = item.text
						       removeSlash = r.replace('\\n','')
						       removeSpaces = removeSlash.replace(' ','')
						       Change = removeSpaces.replace(':','.')
						       s = float(Change)
						       videoDuration.append(s)
						   for time in videoDuration:
						       sum = sum+time
						   duration = (sum / 60)
						   covertToStr = str(duration) 
						   duration = covertToStr[:4]
					   else:
						   duration = 'Please enter valid url'
				os.remove(fileName)	
			except:
				duration = 'Please enter valid url'

	else:
		form = linkForm()		

	context = {
		'form' : form,
		'duration' : duration,
		
	}

	return render(request,'playlist_duration_app/index.html',context)