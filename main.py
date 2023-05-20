import math
import openpyxl

class Station:
    def __init__(self, name, longitude, width, hub, history, year, isSubject, isBMR):
        self.unified = False
        self.name = name
        self.longitude = float(longitude)
        self.width = float(width)
        if hub != None and hub != False:
            self.hub = True
        else:
            self.hub = False
        self.history = history
        if self.history != None:
            self.year = year
        else:
            self.year = False
        if isSubject != None and isSubject!=False:
            self.isSubject = True
        else: self.isSubject = False
        self.list_adjacency = []
        self.isAdjac = False
        self.isBMR = isBMR
    def output (self):
        result = self.name+' '+str(self.longitude)+' '+str(self.width)+' '
        if self.hub:
            result+= 'узловая'
        if self.history!=None:
            result+=' '+self.history
        if self.isBMR:
            result+= ' BMR '
        string_python_shit = ''
        for x in self.list_adjacency:
            string_python_shit = string_python_shit+' '+x.name
        print (result, ':', string_python_shit)
    def isEqual(self, obj2):
        return (self.name == obj2.name and self.longitude == obj2.longitude and self.width == obj2.width and self.hub == obj2.hub)
    def copy(self):
        return Station(self.name, self.longitude, self.width, self.hub, self.history, self.year, self.isSubject, self.isBMR)

class Vector:
    def __init__(self, list_stations):
        self.list_stations = list_stations.copy()
        self.name = list_stations[0].name+'-'+list_stations[-1].name
    def output(self):
        temp_string = self.list_stations[0].name + ' - ' + self.list_stations[-1].name
        print (temp_string)
    def complete_output(self):
        temp_string = self.list_stations[0].name + ' - ' + self.list_stations[-1].name + ': '
        for i in range (1, len(self.list_stations)-1):
            temp_string += self.list_stations[i].name + ' - '
        print (temp_string)
    def longitude_dif(self):
        return self.list_stations[-1].longitude-self.list_stations[0].longitude
    def width_dif(self):
        return self.list_stations[-1].width-self.list_stations[0].width
    def length(self):
        return distance(self.list_stations[0], self.list_stations[-1])
    def isInVector(self, station):
        for x in self.list_stations:
            if x.name == station.name:
                return True
        return False
    def vector_append(self, station):
        self.list_stations.insert(1, station)

class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

class LineString:
    def __init__(self, init_point, finish_point):
        self.init_station = init_point
        self.finish_station = finish_point
        self.list_stations = []
        self.direction = init_point.x<finish_point.x
        self.list_of_station()
    def length(self):
        return distance(self.init_station, self.finish_station)
    def list_of_station(self):
        for x in main_list_station:
            if is_Station_in_Line(x, self):
                self.list_stations.insert(num_for_sort(self.list_stations, x, self.direction), x)
    def output(self):
        result = ''
        for x in self.list_stations:
            result+=x.name+' '
        return result

def is_Station_in_Line(station1,linestring1):
    temp_x = [linestring1.init_station.x, linestring1.finish_station.x]
    temp_y = [linestring1.init_station.y, linestring1.finish_station.y]
    return station1.longitude>min(temp_x) and station1.longitude<max(temp_x) and station1.width>min(temp_y) and station1.width<max(temp_y)\
           and distance_line(linestring1, Point(station1.longitude, station1.width))<0.01

def num_for_sort(station_list, temp_station, direction):
    result = 0
    for x in station_list:
        if x.longitude > temp_station.longitude and direction:
            return result
        elif x.longitude<temp_station.longitude and not direction:
            return result
        else:
            result +=1
    return result

def distance(point1, point2):
    return ((point1.x-point2.x)**2+(point1.y-point2.y)**2)**0.5

def distance_line(linestring1, point1):
    #S = h*vector1.length/2
    distance1 = linestring1.length()
    distance2 = distance(linestring1.init_station, point1)
    distance3 = distance(linestring1.finish_station, point1)
    p = (distance1+distance2+distance3)/2
    try:
        S = math.sqrt(p*(p-distance3)*(p-distance2)*(p-distance1))
    except:
        return distance2 #объективно h>0.0001
    try:
        h = 2*S/distance1
    except:
        return distance2
    return h

def count_for_point(list_temp, point_temp):
    result = 0
    for x in list_temp:
        if x.x==point_temp.x and x.y == point_temp.y:
            result +=1
    return result

if __name__ == '__main__':
    excel_file = openpyxl.load_workbook('hub_stations.xlsx')
    excel_file = excel_file['Sheet']
    main_list_station = []
    for row in excel_file:
        if row[0].value != 'name' and row[0].value != None:
            main_list_station.append(
                Station(row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value,
                        row[6].value, row[7].value))
    linestring_file = openpyxl.load_workbook('all_linestring_excel.xlsx')
    linestring_file = linestring_file['all_linestring']
    main_linestring_list = []
    point_list = []
    index = 0
    for row in linestring_file:
        if row[0].value!='x_init_station':
            point_list.append(Point(row[0].value, row[1].value))
            point_list.append(Point(row[2].value, row[3].value))
            main_linestring_list.append(LineString(Point(row[0].value, row[1].value), Point(row[2].value, row[3].value)))
            print (index)
            index+=1
    hub_list = []
    dead_end_list = []
    for x in point_list:
        if count_for_point(point_list, x)>2 and count_for_point(hub_list, x)==0:
            hub_list.append(x)
        if count_for_point(point_list, x)==1 and count_for_point(dead_end_list, x) == 0:
            dead_end_list.append(x)
    if len(dead_end_list)==len(point_list):
        print ('говно')
    wb_result = openpyxl.Workbook()
    ws_result = wb_result.active
    for x in main_linestring_list:
        print (x.output())
        ws_result.append({'A': x.init_station.x, 'B': x.init_station.y, 'C': x.finish_station.x, 'D': x.init_station.y, 'E': x.output()})
    wb_result.save('result.xlsx')