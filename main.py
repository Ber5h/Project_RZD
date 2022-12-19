import openpyxl
import math
class Station:
    name = ''
    longitude = 0 #East-West
    width = 0 #North-South
    hub = False
    history = None
    year = None
    def __init__(self, name, longitude, width, hub, history, year ):
        self.name = name
        self.longitude = float(longitude)
        self.width = float(width)
        if hub!= None and hub!=False:
            self.hub = True
        self.history = history
        if self.history!=None:
            self.year = year
    def output (self):
        result = self.name+' '+str(self.longitude)+' '+str(self.width)+' '
        if self.hub:
            result+= 'узловая'
        if self.history!=None:
            result+=' '+self.history
        print (result)
    def isEqual(self, obj2):
        return (self.name == obj2.name and self.longitude == obj2.longitude and self.width == obj2.width and self.hub == obj2.hub)

class Vector:
    list_station = []
    isEast = None
    isNorth = None
    def __init__(self, list_station):
        self.list_station = list_station.copy()
        isEast = list_station[-1].longitude>list_station[0].longitude
        isNorth = list_station[-1].width>list_station[0].width
    def angle_vector(self):
        #угол между y = 0 и вектором
        return math.atan((self.list_station[-1].width-self.list_station[0].width)/(self.list_station[-1].longitude-self.list_station[0].longitude))
    def output(self):
        print (self.list_station[0].name, '-', self.list_station[-1].name)

def find_next_station_of_vector(list_piece, init_station):
    r_min = 5
    station_temp = Station('', 0, 0, None, None, None)
    for x in list_piece:
        r_temp = math.sqrt((init_station.width-x.width)**2+(init_station.longitude-x.longitude)**2)
        if r_temp<r_min:
            r_min = r_temp
            station_temp = Station(x.name, x.longitude, x.width, x.hub, x.history, x.year)
    return station_temp

def list_split(list_piece, angle_vector, init_station, isNorth, isEast):
    list_result = []
    angle_temp = 0
    crutch = True
    for x in list_piece:
        if ((isNorth and x.width>init_station.width) or (not isNorth and x.width<= init_station.width))and ((isEast and x.longitude>init_station.longitude)or (not isEast and x.width<=init_station.longitude)):
            crutch = True
        else:
            crutch = False
        #print (crutch)
        #if x.width>init_station.width and x.longitude>init_station.longitude:
          #  print (x.name)
          #  print (isNorth)
           # print (isEast)
        try:
            angle_temp = math.atan((x.width-init_station.width)/(x.longitude-init_station.longitude))
        except:
            angle_temp = math.atan((x.width - init_station.width) / (x.longitude - init_station.longitude+1))
        if angle_vector-math.pi/5<angle_temp and angle_temp<angle_vector+math.pi/5 and crutch:
            #print (x.name)
            list_result.append(x)
    return list_result

def create_vector(list_piece, isEast, isNorth, init_station): #задается направление (одно из четырех), в квадрате проходимся по ближайшим точкам
    list_temp = []
    vector_list = []
    if isEast and isNorth:
        for x in list_piece:
            if x.width>init_station.width and x.longitude>init_station.longitude:
                list_temp.append(x) #по идее сортированы по долготе
    elif isEast and not isNorth:
        for x in list_piece:
            if x.width<init_station.width and x.longitude>init_station.longitude:
                list_temp.append(x)
    elif not isEast and isNorth:
        for x in list_piece:
            if x.width>init_station.width and x.longitude<init_station.longitude:
                list_temp.append(x)
    else:
        for x in list_piece:
            if x.width<init_station.width and x.longitude<init_station.longitude:
                list_temp.append(x)
    print (len(list_temp))
    station_temp = find_next_station_of_vector(list_temp, init_station)
    #print (station_temp.name)
    vector_list.append(init_station)
    #не оптимизируем пока
    while station_temp.hub == False:
        vector_list.append(station_temp)
        try:
            angle_temp = math.atan((vector_list[-1].width-vector_list[-2].width)/(vector_list[-1].longitude-vector_list[-2].longitude))
        except:
            angle_temp = math.atan((vector_list[-1].width-vector_list[-2].width)/(vector_list[-1].longitude-vector_list[-2].longitude+1))
        list_temp = list_split(list_piece, angle_temp, vector_list[-1], isNorth, isEast)
        #print (len(list_temp))
        station_temp = find_next_station_of_vector(list_temp, vector_list[-1])
        print (station_temp.name)
    vector_list.append(station_temp)
    result = Vector(vector_list)
    return result

if __name__ == '__main__':
    excel_file = openpyxl.load_workbook('finally_ready_station_file.xlsx')
    excel_file = excel_file['Sheet']
    list_station = []
    for row in excel_file:
        if row[0].value!= 'name' and row[0].value!=None:
            list_station.append(Station(row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value))
    create_vector(list_station, True, True, Station('МОС-ПАС-ЯРОС', 37.6575, 55.7777, True, None, None)).output()