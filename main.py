from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import requests
import functions

fig = plt.figure(figsize = (15,14))
m = Basemap(
    projection = 'mill',
    llcrnrlat = 6,
    llcrnrlon = 67,
    urcrnrlat = 37,
    urcrnrlon = 97,
)
m.drawmapboundary(fill_color='aqua')
m.fillcontinents(color='#ddaa66',lake_color='aqua')
m.drawcoastlines()

m.drawparallels(np.arange(-90,90,5),labels=[True,False,False,False])
m.drawmeridians(np.arange(-180,180,5),labels=[0,0,0,1])

m.readshapefile('Indian_States','Indian_States')

lon,lat = 77.2,11.42
xpt,ypt = m(lon,lat)

catch = requests.get('https://api.tomtom.com/search/2/reverseGeocode/' + str(lat) + '%2C%20' + str(lon) + '.json?key=SK8FmK64sGjB471GAD4AnU26xdQH02Bv')


point, = m.plot(xpt,ypt,'bo')

annotation = plt.annotate(catch.json()['addresses'][0]['address']['localName'] + '(%5.1fE,%3.1fN)' % (lon, lat), xy=(xpt,ypt),
             xytext=(20,35), textcoords="offset points", 
             bbox={"facecolor":"w", "alpha":0.5}, 
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3"))


def onclick(event):
    try:
        ix, iy = event.xdata, event.ydata
        xpti, ypti = m(ix, iy,inverse=True)
        catch = requests.get('https://api.tomtom.com/search/2/reverseGeocode/' + str(ypti) + '%2C%20' + str(xpti) + '.json?key=SK8FmK64sGjB471GAD4AnU26xdQH02Bv')
        string = catch.json()['addresses'][0]['address']['localName'] + '(%5.1fE,%3.1fN)' % (xpti, ypti)
        annotation.xy = (ix, iy)
        point.set_data([ix], [iy])
        annotation.set_text(string)
        plt.gcf().canvas.draw_idle()
        functions.getNews(catch.json()['addresses'][0]['address']['localName'])
    except:
        print('Sorry for error')
        pass

cid = plt.gcf().canvas.mpl_connect("button_press_event", onclick)
plt.show()