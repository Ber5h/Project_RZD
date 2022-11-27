import openpyxl
import math

class Station:
    name = ''
    longitude = 0 #East-West
    width = 0 #North-South
    hub = False
    def __init__(self, name, longitude, width, hub):
        self.name = name
        self.longitude = longitude
        self.width = width
        self.hub = hub
    def output (self):
        result = self.name+' '+str(self.longitude)+' '+str(self.width)+' '
        if self.hub:
            result+= 'узловая'
        print (result)
    def isEqual(self, obj2):
        return (self.name == obj2.name and self.longitude == obj2.longitude and self.width == obj2.width and self.hub == obj2.hub)

def sorted_width(list_station):
    min_list_width = []
    for i in range (int(math.sqrt(len(list_station)))):
        min_list_width.append(Station('', 0, 100, False))
    #for i in range (len(list_station)//10):
    #    min_list_width.append(Station('', 0, 100, False))
    for x in list_station:
        for i in range (len(min_list_width)):
            if x.width<min_list_width[i].width:
                for j in range (len(min_list_width)-1, i, -1):
                    min_list_width[j] = min_list_width[j-1]
                min_list_width[i] = x
                #x.output()
                break
    return min_list_width

def min_longitude(list_station):
    result = Station('', 100, 100, False)
    for x in list_station:
        if x.longitude<result.longitude:
            result = x
    return result

def sort_for_longitude_scatter(list_station, min_longitude, max_longitude):
    list_result = []
    for x in list_station:
        if x.longitude>=min_longitude and x.longitude<=max_longitude:
            list_result.append(x)
    return sorted_width(list_result)

if __name__ == '__main__':
    unless_format_information = openpyxl.load_workbook('for_python_code.xlsx', data_only = True)
    east_ring = unless_format_information['Станции ЖД от ПЧ по широте']
    list_station = []
    North = float(input())
    South = float(input())
    East = float(input())
    West = float(input())
    #num = 0
    for row in east_ring.values:
        if row[1]!= None and row[0]!='FID':
            name = ''
            longitude = 0 #East-West
            width = 0 #North-South
            count = 0
            hub = False
            actual_add = True
            for value in row:
                if value != None:
                    if count == 2:
                        name = value
                    elif count == 4:
                        longitude = value
                        if longitude<West or longitude>East:
                            count = 0
                            break
                    elif count == 5:
                        width = value
                        if width>North or width<South:
                            count = 0
                            break
                    elif count == 6:
                        hub = True
                    count +=1
            if count >=6:
                obj_temp = Station(name, longitude, width, hub)
                for x in list_station:
                    if x.isEqual(obj_temp):
                        actual_add = False
                if actual_add:
                    list_station.append(obj_temp)
    test_list = sorted_width(list_station)
    #for x in test_list:
    #    x.output()
    #print (len(test_list))
    min_long_width_station = min_longitude(test_list)
    #min_long_width_station.output()
    const_longitude_scatter = (East-West)/20
    const_width_scatter = (North-South)/20
    #cycle: North-East-South-West
    #min_longitude = min_long_width_station.longitude
    max_longitude = min_long_width_station.longitude+const_longitude_scatter
    test_list = sort_for_longitude_scatter(list_station, min_long_width_station.longitude, max_longitude)
    for x in test_list:
        x.output()