import numpy
import flexpolyline as fp
import requests
import tools_GIS
# ----------------------------------------------------------------------------------------------------------------------
folder_in = './data/ex_datasets/'
folder_out = './data/output/'
# ----------------------------------------------------------------------------------------------------------------------
# Where is the nearest McDonald's near the London Eye?
# ----------------------------------------------------------------------------------------------------------------------
# https://gemini.google.com/share/39d4ef4d2c1f
# ----------------------------------------------------------------------------------------------------------------------
# I am in Berlin and want to visit a Bauhaus place in Dessau, get me there
# I will need to charge my car, please find a charging station, compatible with my Tesla, half-way and make a stop
# Is there a restaurant in walking distance from the stop which one will be open when I’m there?
# I just drove past a nice restaurant with a terrasse on my right, please save this restaurant in my favorites
# This little village on my right looks very nice, what is it called and how much of a detour would it be to go there?
# Please give me a route to X that goes through forests and avoids highways
# The highway entrance I was planning to take towards X is closed, which route should I take now?
# How long does it take to walk from Eindhoven airport to the city center?
# What is my ETA to Chicago's Pizza. I live in the intersection of Irving and Austin, Chicago
# I need to travel to the Allstate arena from Cloud Gate. Find me a route to the nearest parking lot to the arena.
# I am in Berlin, Deutschland. Can you please route me to Warsaw, Poland? I am driving an Electric Vehicle, so please plan a stop to charge my vehicle along the route.
# Where can I eat next to Simon-Dach-Str 9 and not walk more than 5 minutes?
# Find top restaurants near Golden Gate Bridge, San Francisco, and route to one of these restaurants from Berkeley, CA
# Find me a route from Amsterdam to Berlin with a stop in the middle near a McDonalds restaurant
# I have a Tesla Model Y and want to go from Berlin to Essen. My car is charged 90%. What is the best place to recharge if I also want to eat something?
# What is the best walking route from the tribune tower to the water tower building in Chicago with a quick stop at McDonald's on the way?
# I want to drive from Berlin, Neukölln to Essen with a regular car. After about 2-3 hours, I want to have a break, so my kids can play and eat. Can you recommend something?
# I am driving from Chicago to Asheville starting at 8:00 AM. At lunch time, I plan to eat at Taco bell. Please give me the best options to eat for lunch.
# Where is the Kentucky Derby? Find me a route to a nearby hotel with a quick stop at Starbucks along the way.
# ----------------------------------------------------------------------------------------------------------------------
# where is the nearest mcdonald's near London eye?
# Find top restaurants near Golden Gate Bridge, San Francisco, and route to one of these restaurants from Berkeley
# Hi, what is the best restaurant in Budva, Montenegro?
# How many coffee shops are there in Eindhoven, Netherlands? List the closest one to the Central Station.
# I would like to visit parks near
# Show me bars near lakes in Potsdam
# find a restaurant in Berlin with a playground
# how long is the drive from Berlin to Paris?
# Find me a great coffee place within 30 minutes from Ouderkerk aan de Amstel
# Electric vehicle charging station near bijlmer
# what is the lat lng for Amsterdam
# Find me a route from Amsterdam to Berlin with a stop in the middle near a mcdonalds restaurant
# How long does it take from Eindhoven airport to the city center by walking?
# I have a Tesla Model Y and want to go from Berlin to Essen. My car is charged to 90%. What is the best place to recharge if I also want to eat something?
# I want to drive from Berlin, Neukölln to Essen with a regular car. After about 2-3 hours, I want have a break, so my kids can play and eat. Can you recommend something? 42.07 [4] [18107 → 376 (Σ 18483)] 56.0 [5] [21392 → 787 (Σ 22179)] Error 48.58 [5]
# Which is the closest parking garage to Amsterdam Centraal?
# what are the top cinemas in Berlin?
# Find top indian restaurants near bad soden am taunus frankfurt
# find me good hotels within 2 km Amrutha hospital cochin and good rating
# top 5 cinemas in Berlin
# Recommend a museum close to Nordbahnhof in Berlin
# where are the best hotels in the north side of chicago, IL and how to route to one of these from milwaukee, WI
# Please recommend me a museum for technology topics in Berlin
# What's my eta to Chicago's Pizza. I live in the intersection of Irving and Austin, Chicago
# What is the distance to the closet library to Wrigley Field in Chicago?
# what's my eta to Chicago Pizza. I live in 400N Ave, Austin
# what is the best place to get tacos in lincoln park, chicago?
# What is the location of the bean?
# How far is the tribune tower from the bean?
# What is the best walking route from the tribune tower to the water tower building in Chicago with a quick stop at mcdonald's on the way?
# Where is the space needle? Find me a walking route to the nearest starbucks from there.
# Where is the kentucky derby? Find me a route to a nearby hotel with a quick stop at startbucks along the way
# I need to travel to the all state arena from cloud gate. Find me a route to the nearest parking lot to the arena
# What are some of the best Italian restaurants near the water tower building in Chicago? Route me to one of them from the tribune tower on foot
# ell me the location of Scheumann Stadium
# Plot a route from Chicago to Muncie by car, with stops along the way at a restaurant every hour or so
# What are some of the best hotels close to the airport in Doral Florida?
# Where is the national corvette museum? Find a car route from Chicago with one stop about half way with a hotel to rest.
# how to drive an EV from HERE melbourne office to Sydney Harbour bridge
# where can i get lunch near Villa Jacobs?
# Route me to the closest McDonalds from Frohnauer Straße
# Find top restaurants near Invalidenstrasse 116, Berlin, and route to one of these restaurants from Chausseestr. 94, Berlin
# Hi HUGO, I am located in Berlin, Deutschland. Can you please route me to Warsaw, Poland? I am driving an Electic Vehicle, so please plan a stop
# to charge my vehicle along the route. Thank you.
# Find all tacobell on the route from Chicago to Asheville
# I am driving from Chicago to Asheville starting at 8:00 AM. At lunch time, I plan to eat at Taco bell. Please give me the best options to eat for lunch.
# provide all Tesla locations in Chicago
# Are you able to calculate time of car trip from Berlin to Szczecin by night?"
# Where can I eat next so Simon-Dach-Str 9 and not walk more than 5 minutes?
# ----------------------------------------------------------------------------------------------------------------------
API_ID = 'ZmAS6TOal7irdXvS2coQ'
API_KEY = 'zW_OcP6hbbwJmS5OZtU8qVWMpjSxLdPxqGiGzPRWmRE'
#'https://geocode.search.hereapi.com/v1/geocode?q=240+Washington+St.%2C+Boston&limit=4&apiKey=zW_OcP6hbbwJmS5OZtU8qVWMpjSxLdPxqGiGzPRWmRE'
# ----------------------------------------------------------------------------------------------------------------------
def get_route(origin, destination):
    url = "https://router.hereapi.com/v8/routes"
    params = {'transportMode': 'car', 'origin': f'{origin[0]},{origin[1]}', 'destination': f'{destination[0]},{destination[1]}','return': 'summary,polyline,actions,instructions', 'apiKey': API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        route_data = response.json()
        rotes = [route for route in route_data['routes']]
        for route in rotes:
            for section in route['sections']:
                polyline_decoded = numpy.array([(p[0],p[1]) for p in fp.iter_decode(section['polyline'])])

    return polyline_decoded
# ----------------------------------------------------------------------------------------------------------------------
def search_poi(query,at):
    #url = "https://discover.search.hereapi.com/v1/discover"
    #url =  "https://places.cit.api.here.com/places/v1/discover/search"
    url = "https://places.demo.api.here.com/places/v1/discover/around?at=52.521%2C13.3807&cat=hotel&apiKey=ZmAS6TOal7irdXvS2coQ"
    params = {'apiKey': API_KEY}
    #params = {'q': query,'at': f'{at[0],at[1]}','limit': 10,'apiKey': API_KEY}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        poi_data = response.json()
        res = [(item['position']['lat'],item['position']['lng']) for item in poi_data['items']]

    return res
# ----------------------------------------------------------------------------------------------------------------------
G = tools_GIS.tools_GIS()
# ----------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    #origin = (52.5200,13.4050)
    #destination = (51.8416,12.2436)
    #G.build_folium_html([get_route(origin, destination)]).save(folder_out + 'map_folium.html')
    #search_poi('McDonalds',origin)

