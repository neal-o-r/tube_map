import matplotlib.pyplot as plt
import seaborn as sns; sns.set()
import pandas as pd
import numpy as np
from scipy import sparse
from utils import *


def read_panels():
        # read data files, return panels, and alphabetised stations list
        tube_pd = pd.read_csv('data/Inter_station_database.csv')
        tube_pd['Colour'] = tube_pd.apply(lambda row: add_colour(row['Line']),axis=1)

        lats = pd.read_csv('data/stations.csv')
        lats['name']=lats['name'].str.upper()

        stations = set(np.concatenate((tube_pd['Station from'].values, tube_pd['Station to'].values)))

        stations = list(stations)

        stations.sort()

        return tube_pd, lats, stations


def distace_matrix(tube_pd, stations):
        # computes distance matrix
        # prints times, returns matrix

        adj_mat = np.zeros((len(stations), len(stations)))

        for index, row in tube_pd.iterrows():
	
                i = stations.index(row['Station from'])
                j = stations.index(row['Station to'])
                # populate adjacenct matrix
                adj_mat[i][j] = row['AM peak  Running Time']

        dist = sparse.csgraph.floyd_warshall(adj_mat, directed=False)

        avgs = np.mean(dist, axis=1)

        sort_avgs = sorted(zip(avgs, stations))

        f = open('time.txt', 'w')
        for index, result in enumerate(sort_avgs):
                
                res_str = (str(index) + ' The average travel time from '
                           + result[1] + ' to any other station is '
                           + str(result[0]) + ' minutes \n' )
                f.write(res_str)
        f.close()

        return sort_avgs, dist

def geo_plot(tube_pd, lats):
        # Plot the tube map geographically

        for index, row in tube_pd.iterrows():
		# cycle through the trips
                stat_to   = row['Station to']
                stat_from = row['Station from']	
		# collect the lats and lons to and from
                lat_to   = float(lats['latitude'][lats['name']==stat_to].values)
                lat_from = float(lats['latitude'][lats['name']==stat_from].values)
                lon_to   = float(lats['longitude'][lats['name']==stat_to].values)
                lon_from = float(lats['longitude'][lats['name']==stat_from].values)
		# scatter plot the stations, a connect the lines
                plt.plot([lon_to,lon_from], [lat_to,lat_from], '-', color=row['Colour'])	
                plt.scatter(lon_to, lat_to, alpha=0.2, color='w')	
                plt.scatter(lon_from, lat_from, alpha=0.2, color='w')

        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Geographic Tube Map')

        plt.savefig('geographic_map.eps')


def time_plot(centre, lats, tube_pd, dist, stations):
        # plot polar tube map of travel times

        centre = centre.upper() # upper case everything to match input data
        lat_c = float(lats['latitude'][lats['name'] == centre].values)
        lon_c = float(lats['longitude'][lats['name'] == centre].values)
	# get the lat lon of the centre station
	# and offset everything by this (put the centre at (0,0))
        lats['lat_off'] = lats['latitude']  - lat_c
        lats['lon_off'] = lats['longitude'] - lon_c

	# get the angle between (0,0)-(x,y) and the 'North'
        lats['angles'] = lats.apply(get_angle, axis=1)
	
        ind = stations.index(centre)
        # these are the min times to every station from this station
	times = dist[ind,:]
        angles=[]
        for station in stations:
		# collect the angles for the stations
                angles.append(float(lats['angles'][lats['name'] == station].values))

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='polar')

        for index, row in tube_pd.iterrows():
		# polar plot plot these
                # with r = travel time
		stat_to   = row['Station to']
                stat_from = row['Station from']	

                ang_to   = float(lats['angles'][lats['name']==stat_to].values)
                ang_from = float(lats['angles'][lats['name']==stat_from].values)
	
                r_to   = times[stations.index(stat_to)]
                r_from = times[stations.index(stat_from)]
        
               	plt.polar([ang_to,ang_from], [r_to,r_from], '-', color=row['Colour'])

        plt.title('Travel Time by Shortest Route from '+centre[0]+centre[1:].lower()+' (mins)')
	ax.set_xticklabels(['W', '', 'N', '', 'E', '', 'S', ''])
        plt.savefig('polar'+centre+'.eps', bbox_inches='tight')

def bar_time_plot(stations, rent_flag=False):
        # plot a bar chart of travel times
	# if rent is set to true the plot is colour-coded by average
	# rent price at each station. This is not massively helpful,
	# and I find it clutters the plot.

        fig = plt.figure()
	ax = fig.add_subplot(111)

	if rent_flag:

	        rent = pd.read_csv('data/rent.csv')
        	rent['name'] = rent['name'].str.upper()
		# put each station into a decile (quintile currently)
        	rent['decile'] = np.ceil(rent['rent']/rent['rent'].max() *10) 
        
		# the station lists don't match, so cycle through and make a label list
        	tube_pd['decile'] = 0
		label = []
        	for station in stations:
                	if (len(rent['decile'][rent['name'] == station].values != 0)):
                        	label.append(int(rent['decile'][rent['name'] == station].values[0]))
                	else: # if we have a station that doesn't appear in the rent list
			      # (there are some) then give it a 0
                        	label.append(0)
 

        barlist = plt.bar(range(len(avg_times)), [s[0] for s in avg_times])

        if rent_flag:
		# add the colouring to the bar plot	
        	palette = sns.color_palette(n_colors=11)
		for index, bar in enumerate(barlist):
                	bar.set_color(palette[label[index]])

        plt.xlim([0,271])
        plt.title('Average Minimum Travel Time to Any Other Station')
        plt.ylabel('Average Min. Time (mins)')
        plt.xticks([0, 271])
	ax.set_xticklabels(['Oxford Circus', 'Chesham'])
        plt.savefig('avg_min.png') 

if __name__ == '__main__':

        tube_pd, lats, stations = read_panels()
        avg_times, dist_mat =  distace_matrix(tube_pd, stations)

  #     geo_plot(tube_pd, lats)
        time_plot('oxford circus', lats, tube_pd, dist_mat, stations)
  #	bar_time_plot(stations)
	
