from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import City
from .forms import CityForm
from django.contrib import messages


# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9{api_key_here}"
    #city = "Las Vegas"

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            form.save()
        #pass

    form = CityForm()


    cities = City.objects.all()

    weather_data = []

    for city in cities:


        r = requests.get(url.format(city)).json()
        
        print(r)

        if 'main' in r and 'weather' in r:
            city_weather = {
                'city': city.name,
                'temperature': r['main'].get('temp', 'N/A'),
                'description': r['weather'][0].get('description', 'N/A'),
                'icon': r['weather'][0].get('icon', ''),
            }
            weather_data.append(city_weather)
        else:
            print(f"Error fetching data for {city.name}: {r.get('message', 'Unknown error')}")


    print(weather_data)
    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'weather/weather.html', context)

from django.shortcuts import redirect

def delete_city(request, city_name):
    if request.method == 'POST':
        try:
            # Get the city object by name instead of ID
            city = get_object_or_404(City, name=city_name)
            city.delete()

            # Optionally, use messages to notify success or failure
            messages.success(request, f"City {city_name} deleted successfully.")
            
            # Redirect to the index page
            return redirect('index')
        except City.DoesNotExist:
            messages.error(request, f"City {city_name} not found.")
        except Exception as e:
            messages.error(request, f"Error deleting city: {str(e)}")

    # If it's not a POST request, redirect to the index page
    return redirect('index')

