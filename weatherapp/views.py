from django.shortcuts import render
import requests
from bs4 import BeautifulSoup as bs
import json

def get_weather_data(city):
    city = city.replace(' ','+')
    url = f'https://www.google.com/search?q=weather+of+{city}'
    user_agent ='Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1'
    language = 'en-US,en;q=0.9'
    session = requests.Session()
    session.headers ['user-agent'] = user_agent
    session.headers [ 'accept-language'] = language
    response = session.get(url)
    soup = bs(response.text, 'html.parser')
    #extract Region
    results ={}
    results['region'] = soup. find("div", attrs = {'id':'wob_loc'}).text
    results['Day_Time'] = soup.find ( "span", attrs = {'id': 'wob_dts'} ).text
    results['Weather'] = soup.find ( "span", attrs = {'id': 'wob_dc'} ).text
    results['temp'] = soup.find ( "span", attrs = {'id': 'wob_tm'} ).text
    # print(results )
    return results
# get_weather_data('new yeark')


def weather_api(city):
    api_key = 'd650e7cbe1e083d39bf6e0ec4f2b2cad'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    data = json.loads(response.text)
    results = {}
    results['lon'] = data['coord']['lon']
    results [ 'lat' ] = data [ 'coord' ] [ 'lat' ]
    results [ 'name' ] = data [ 'name' ]
    results [ 'temp' ] = data [ 'main' ]['temp']
    results [ 'humidity' ] = data [ 'main' ] [ 'humidity' ]
    return results
# print(weather_api("london"))



# Create your views here.
def home_view(request):
    if request.method == "GET" and 'city' in request.GET:
        city = request.GET.get('city')
        results = get_weather_data(city)
        context = {'results': results}
    else:
        context = {}

    return render(request,'weatherapp/home.html', context )


def api_view (request):
    if request.method== "POST" and 'city' in request.POST:
        city = request.POST.get('city')
        results = weather_api(city)
        context = {'results': results}
    else:
        context = {}
    return render (request, 'weatherapp/api.html', context)
