# geospatial-data-project

#Introduction:

This is one of the projects done during the [IronHack](https://www.ironhack.com/en) Data Analytics bootcamp. 
Given some conditions, the target of the project is to find the proper place to build the headquarters/offices for a new company. It is not necessary to fulfill the full set of conditions (It is basically impossible), but at least some of them.

#Objectives:

- The full list ofrequirements can be found in this [repo](https://github.com/antoniogarciagiron/W4-geospatial-data-project), however, in order to shorten the search, the following requirements were chosen:
    - The office needs to have a Starbucks around.
    - As 30% of the staff has kids, a school has to be close to the office.
    - Account managers travel a lot, so the office has to be near a train station.
    - Everybody in the company is between 25 and 40 and they want a place to party, so a pub has to be around. 

#Data:

- [GeoCode](https://geocode.xyz/) and [Foursquare](https://foursquare.com/) APIs were used to obtian the coordinates.  I used GeoCode instead of taking the coordinates from Google, in case someone wants to make a similar research in another city. Staring from the coordinates of the selected city, Foursquare was used to find lists of places in that city, in this case, the list of Starbucks, schools, pubs and train stations in Birmingham (UK).
- The following Python libraries were used: folium, fequests, os, json, pandas, functools, geopandas, operator, cartoframes.viz, geopy.distance.

#Hypothesis and Workflow:

The project was divided in the following tasks:
    1) To select a city. In my case I decided to open the headquarters in Birmingham (UK) because I studied in the University of Birmingham and I love the city. Birmingham is the birthplace of heavy metal and tennis, where the fist football league started and the place that inspired Tolkien to write The Lord of the Rings, but also the second largest city in the UK. Birmingham is located in a strategic position between Liverpool and London, and lots of companies are starging to move their offices from the capital to Birmingham, as London is gradually becoming more and more expensive. 
    2) Once the city was chosen, the lists of Starbucks, schools, train stations and pubs (There is a pub in every corner, so the list was limited), and their coordinates were obtained from Foursquare.
    3) With the 4 lists and their coordinates, an algorithm calculated all the possible combinations of Starbucks, school, train station and pub and saved it in a list of combinations.
    4) Given the list of all possible combinations, another algorithm calculated the distances between the 4 places and selected the combination with less distance between them.
    5) Once we have the selected Starbucks, school, train station, and pub, and their coordinates, the centroid of the 4 positions was calculated and the result is the selected place for the offices.


#Results:

The following coordinates correspond to the optimal combination of required places:
Starbucks: [52.479158, -1.89932]
School: [52.48083, -1.8973938]
Pub: [52.47917395373524, -1.8986854974151004]
Train station: [52.47775090364966, -1.899928107174874]]

The optimal location for the office is the centroid of the coordinates listed above: 
Office: [52.47922821434622, -1.8988318511474938]

![Map](https://github.com/antoniogarciagiron/geospatial-data-project/blob/main/figures/Birmingham.PNG)