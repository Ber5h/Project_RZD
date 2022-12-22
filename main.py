import openpyxl
import math
class Station:
    name = ''
    longitude = 0 #East-West
    width = 0 #North-South
    hub = False
    history = None
    year = None
    isRing = False
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
    #def angle_vector(self):
        #угол между y = 0 и вектором
     #   return math.atan((self.list_station[-1].width-self.list_station[0].width)/(self.list_station[-1].longitude-self.list_station[0].longitude))
    def output(self):
        print (self.list_station[0].name, '-', self.list_station[-1].name)
    def num_history(self):
        n = 0
        for x in self.list_station:
            if x.history!=None:
                n+=1
        if self.list_station[0].history!=None:
            n-=1
        return n

class Ring:
    list_vectors = []
    def __init__(self, list_vectors):
        self.list_vectors = list_vectors.copy()
    def output(self):
        for x in self.list_vectors:
            for y in x.list_station:
                if y.hub == True or y.history!=None:
                    y.output()
                else:
                    print (y.name)

def angle_vector(longitude1, width1, longitude2, width2):
    try:
        tan = (width1-width2)/(longitude1-longitude2)
    except:
        tan = (width1-width2)/(longitude1-longitude2+1)
    isTanPos = tan>=0
    isCosPos = longitude1>=longitude2
    if (isTanPos and isCosPos): #I четверть
        return math.atan(tan)
    elif isTanPos and not isCosPos: #III четверть
        return math.atan(tan)+math.pi
    elif not isTanPos and isCosPos: #IV четверть
        return math.atan(tan)+2*math.pi
    else: #II четверть
        return math.atan(tan)+math.pi

def find_next_station_of_vector(list_piece, init_station_python_shit):
    r_min = 5
    station_temp = Station('', 0, 0, None, None, None)
    for x in list_piece:
        r_temp = math.sqrt((init_station_python_shit.width-x.width)**2+(init_station_python_shit.longitude-x.longitude)**2)
        if r_temp<r_min and (init_station_python_shit.width!=x.width or init_station_python_shit.longitude!=x.longitude):
            #print (x.name, init_station_python_shit.name)
            r_min = r_temp
            station_temp = Station(x.name, x.longitude, x.width, x.hub, x.history, x.year)
    return station_temp

def isAngleInInterval(angle_vector_x, angle_temp):
    coef_const = 6
    if angle_vector_x+math.pi/coef_const>2*math.pi:
        if angle_temp<angle_vector_x-(2*coef_const-1)*math.pi/coef_const:
            return True
    if angle_vector_x-math.pi/coef_const<0:
        if angle_vector_x+(2*coef_const-1)*math.pi/coef_const<angle_temp:
            return True
    return angle_vector_x-math.pi/coef_const<angle_temp and angle_temp<angle_vector_x+math.pi/coef_const

def list_split(list_piece, angle_vector_x, init_station, isNorth, isEast):
    list_result = []
    angle_temp = 0
    crutch = True
    for x in list_piece:
        if ((isEast and x.longitude-init_station.longitude>-0.05)or (not isEast and x.longitude-init_station.longitude<0.05)) and init_station.name!=x.name:
            crutch = True
        else:
            crutch = False
        #print (crutch)
        #if x.width>init_station.width and x.longitude>init_station.longitude:
          #  print (x.name)
          #  print (isNorth)
           # print (isEast)
        #crutch = init_station!=x
        angle_temp = angle_vector(x.longitude, x.width, init_station.longitude, init_station.width)
        #if x.name == 'КАРАБАНОВО':
            #print (angle_temp)
        if isAngleInInterval(angle_vector_x, angle_temp):
            #print (x.name)
            list_result.append(x)
    return list_result

def create_vector( list_piece, isEast, isNorth, init_station, history_station): #задается направление (одно из четырех), в квадрате проходимся по ближайшим точкам
    angle_temp = angle_vector(history_station.longitude, history_station.width, init_station.longitude, init_station.width)
    list_temp = list_split(list_piece, angle_temp, init_station, isNorth, isEast)
    vector_list = []
    station_temp = find_next_station_of_vector(list_temp, init_station)
    print (station_temp.name)
    vector_list.append(init_station)
    isHistory = False
    #не оптимизируем пока
    while station_temp.hub == False:
        if station_temp.name == history_station.name:
            isHistory = True
        vector_list.append(station_temp)
        angle_temp = angle_vector(history_station.longitude, history_station.width, vector_list[-1].longitude, vector_list[-1].width)
        if isHistory:
            angle_temp = angle_vector(vector_list[-1].longitude, vector_list[-1].width, vector_list[-2].longitude, vector_list[-2].width)
        list_temp = list_split(list_piece, angle_temp, vector_list[-1], isNorth, isEast)
        #print (len(list_temp))
        station_temp = find_next_station_of_vector(list_temp, vector_list[-1])
        print (station_temp.name)
    vector_list.append(station_temp)
    result = Vector(vector_list)
    #print ('helpme')
    return result

def gain_history_ring(history_list, x):
    for y in history_list:
        if x.name==y.name:
            y.isRing = True

def split_for_gird (list_station, North, South, East, West):
    list_result = []
    for x in list_station:
        if x.width<=North and x.width>=South and x.longitude<=East and x.longitude>=West:
            list_result.append(x)
    return list_result

def history_sort(list_piece, North, South):
    list_south = []
    list_north = []
    for x in list_piece:
        if x.width>=(North+South)/2 and x.history!=None:
            #print (x.name, 'чзх')
            list_north.append(x)
            #print ('чзх')
        elif x.history!=None and x.name!='КАЛУГА 1' and x.name!='ЕЛЬНЯ':
            list_south.append(x)
            #print ('south_чзх')
    for i in range (len(list_south)-1, -1, -1):
        list_north.append(list_south[i])
    return list_north

def first_not_ring(history_list):
    for x in history_list:
        if not x.isRing:
            return x

if __name__ == '__main__':
    excel_file = openpyxl.load_workbook('finally_ready_station_file.xlsx')
    excel_file = excel_file['Sheet']
    list_station = []
    for row in excel_file:
        if row[0].value!= 'name' and row[0].value!=None:
            list_station.append(Station(row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value))
    #тестим на восьмерке, потому что... я не знаю, что можно с Москвой делать
    #create_vector(list_station, True, True, Station('МОС-ПАС-ЯРОС', 37.6575, 55.7777, True, 'Москва', 1147), Station('СЕРГ.ПОСАД', 38.1368, 56.302, False, 'Сергиев Посад', 1742)).output()
    North = 55.7
    South = 53.7
    East = 37
    West = 31 #большая протяженность
    list_temp = split_for_gird(list_station, North, South, East, West)
    list_history = history_sort(list_temp, North, South)
    #desired = Ring()
    first_station = list_history[0]
    vector_list = []
    temp = 0
    isNorth = list_history[temp+1].width-list_history[temp].width>0.05
    isEast = list_history[temp+1].longitude-list_history[temp].longitude>0.05
    vector_list.append(create_vector( list_temp, isNorth, isEast, list_history[temp], list_history[temp+1]))
    desired = Ring(vector_list)
    temp = temp+desired.list_vectors[0].num_history()
    #desired.list_vectors[0].output()
    #print (temp)
    #всего: len(list_history) исторических поселений
    #за каждый вектор число пройденных исторических станций может увеличиться на сколько угодно (считается функцией)
    #temp == 0 (Смоленск)
    #temp == 1 (Вязьма-Новот)
    while desired.list_vectors[-1].list_station[-1].name!=first_station.name and temp<len(list_history)-1:
        #temp+=1
        print (temp)
        isNorth = list_history[temp+1].width - desired.list_vectors[-1].list_station[-1].width > 0.05
        isEast = list_history[temp+1].longitude - desired.list_vectors[-1].list_station[-1].longitude > 0.05
        vector_temp = create_vector(list_temp, isNorth, isEast, desired.list_vectors[-1].list_station[-1], list_history[temp+1])
        desired.list_vectors.append(vector_temp)
        print(list_history[temp + 1].name, 'helpme')
        temp = temp+vector_temp.num_history()
        #print ('helpme')
    desired.output()