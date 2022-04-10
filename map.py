from pprint import pprint
import gmplot, googlemaps
API_KEY = 'AIzaSyDJvLmeQoalVvo8h9lDP7c7j7n-9sneYhQ'

map_client = googlemaps.Client(API_KEY)
# og = 'Jasper, AB'
# dest = 'Edmonton, AB'

# response = map_client.directions(og, dest)
# pprint(response)
# print(response[0]['legs'][0]['distance']['text'])

# geocode1 = map_client.geocode(dests[0])
# lat1 = geocode1[0]['geometry']['location']['lat']
# lng1 = geocode1[0]['geometry']['location']['lng']
def mappyboi(dests):
    coord_start = gmplot.GoogleMapPlotter.geocode(dests[0].dest, apikey=API_KEY)
    coord_end = gmplot.GoogleMapPlotter.geocode(dests[-1].dest, apikey=API_KEY)
    coord_center = gmplot.GoogleMapPlotter.geocode(dests[int(len(dests)/2)].dest, apikey=API_KEY)
    waypoints=[]

    gmap = gmplot.GoogleMapPlotter(coord_center[0], coord_center[1], 15, apikey=API_KEY)
    count = 0
    for dest in dests:
        coord = gmplot.GoogleMapPlotter.geocode(dest.dest, apikey=API_KEY)
        waypoints.append(coord)
        # if (dest.index > 0) and (dest.index < (len(dests) - 1)):
        count = count+1
        gmap.marker(coord[0], coord[1], title=dest.dest, label=str(count), color="cyan")

    gmap.directions(coord_start, coord_end, waypoints=waypoints)
    gmap.draw('templates/map.html')

def distance(dest, end):
    response = map_client.directions(dest, end)
    dist = response[0]['legs'][0]['distance']['text']
    return dist



if __name__ == '__main__':
    mappyboi(['Jasper, AB', 'Edmonton, AB', 'Vegreville, AB'])