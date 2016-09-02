# Tube Map

It's always kinda bugged me that the Tube map has no scale. It warps your sense of geography when places that are East-West (or North-South) of one another are reversed on the Tube map, or when places that are very close together seem far apart. When I first moved to the city I decided to look at some Tube data to better orient myself.

# Centre of London

People often say that London has no centre, but that doesn't seem right to me. Looking at the Tube travel times between pairs of adjacent stations (taking data from TfL and using the Floyd-Warshall algorithm to compute the full distance/time matrix) I got the average minimum travel times from any station to any other on the network, below

![alt tag](https://github.com/neal-o-r/tube_map/blob/master/avg_min.png)

According to this analysis, the 3 stations with the average minimum (un-impeded) travel time to any other station are Oxford Circus, Green Park, and Bond St; all at around 17 minutes. The top 10 stations all surround this three. Seems like the centre of London is somewhere in that triangle. Incidentally this is a decent stretch away from the traditional centre of London, the statue of Charles I at Charring Cross.

# Maps

I also tried to make slight variations on the classic map. First I made a geographically accurate map, below

![alt tag](https://github.com/neal-o-r/tube_map/blob/master/geographic_map.png)

Next I made polar tube plots. Each plot has a given station at its centre, with all other stations retaining their position angles relative to that station (and sort of relative to one another), and their radial distance being the travel time in minutes to the central station. Here's Oxford Circus, the centre of the tube network

![alt tag](https://github.com/neal-o-r/tube_map/blob/master/polarOXFORD%20CIRCUSxkcd.png)

And here's Chesham, statistically the worst place to live

![alt tag](https://github.com/neal-o-r/tube_map/blob/master/polarCHESHAM.png)
