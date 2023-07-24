from django.shortcuts import render
import requests    #this is external lib so need to install via pip
import datetime

def index(request):
    api_key = 'f27f8296f65fe6e63f3a312552ac8897'
    current_weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_data1, daily_forecasts1 = fetch_weather_and_forecast( api_key, current_weather_url, forecast_url,city1)

        if weather_data1=='404':
            return render(request,'weather_app/index.html',{'message':weather_data1})

        if city2:
            weather_data2, daily_forecasts2 = fetch_weather_and_forecast(city2, api_key, current_weather_url,
                                                                         forecast_url)
        else:
            weather_data2, daily_forecasts2 = None, None

        context = {
            'weather_data1': weather_data1,
            'daily_forecasts1': daily_forecasts1,
            'weather_data2': weather_data2,
            'daily_forecasts2': daily_forecasts2,
        }

        return render(request, 'weather_app/index.html', context)
    else:
        return render(request, 'weather_app/index.html')


def fetch_weather_and_forecast(api_key, current_weather_url, forecast_url,city=None):
    try:
        print(city)
        response = requests.get(current_weather_url.format(city, api_key)).json()
        print(response)
        if response['cod']=='404' and response['message']=='city not found':
            print('hehehehee')
            return response['cod'],response['message']
        
        lat, lon = response['coord']['lat'], response['coord']['lon']
        forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
        # print(forecast_response,"hi hello")

        weather_data = {
            'city': city,
            'temperature': round(response['main']['temp'] - 273.15, 2),
            'description': response['weather'][0]['description'],
            'icon': response['weather'][0]['icon'],
        }

        daily_forecasts = []
        # for daily_data in forecast_response['daily'][:5]:
        for daily_data in forecast_response['list']:

            date_time=daily_data['dt_txt'].split(" ")
            date=date_time[0]
            time=date_time[1]
            daily_forecasts.append({
                'day': datetime.datetime.fromtimestamp(daily_data['dt']).strftime('%A'),
                'min_temp': round(daily_data['main']['temp_min'] - 273.15, 2),
                'max_temp': round(daily_data['main']['temp_max']- 273.15, 2),
                'description': daily_data['weather'][0]['description'],
                'icon': daily_data['weather'][0]['icon'],
                'date':date,
                'time':time,
            })

        return weather_data, daily_forecasts
    except :
        {'message':"sorry no such city exists"}



# {
#     "src": "/static/(.*)",
#     "dest": "/static/$1"
# },

# {
#     "src": "build_files.sh",
#     "use": "@vercel/static-build",
#     "config": { "distDir": "staticfiles_build" }
# }