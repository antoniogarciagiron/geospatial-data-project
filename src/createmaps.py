import folium
from folium import Choropleth, Circle, Marker, Icon, Map
from folium.plugins import HeatMap, MarkerCluster

def get_the_map(closer_places, the_place, tags):

    final_map = Map(location=the_place,zoom_start=15)
    counter = 0
    for coordinates in closer_places:
        loc = coordinates
        icon = Icon(color = "green",
                    prefix = "fa",
                    icon ="flag",
                    icon_color ="black",
                    tooltip = tags[counter]
                    )
        counter += 1
        marker = Marker(location = loc, icon = icon)
        marker.add_to(final_map)
    loc = the_place
    icon_2 = Icon(color = "red",
                prefix = "fa",
                icon ="space-shuttle",
                icon_color ="black",
                tooltip = "The place"
                )
    marker = Marker(location = loc, icon = icon_2)
    marker.add_to(final_map)
    return final_map