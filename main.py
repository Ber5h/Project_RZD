import openpyxl
import math

class Station:
    def __init__(self, name, longitude, width, hub, history, year, isSubject):
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
        if isSubject != None:
            self.isSubject = True
        else: self.isSubject = False
        self.list_adjacency = []
        self.isAdjac = False
    def output (self):
        result = self.name+' '+str(self.longitude)+' '+str(self.width)+' '
        if self.hub:
            result+= 'узловая'
        if self.history!=None:
            result+=' '+self.history
        string_python_shit = ''
        for x in self.list_adjacency:
            string_python_shit = string_python_shit+' '+x.name
        print (result, ':', string_python_shit)
    def isEqual(self, obj2):
        return (self.name == obj2.name and self.longitude == obj2.longitude and self.width == obj2.width and self.hub == obj2.hub)
    def copy(self):
        return Station(self.name, self.longitude, self.width, self.hub, self.history, self.year, self.isSubject)


class Unified_Hub:
    def __init__(self, list_hubs):
        self.hub = True
        longitude = 0
        width = 0
        self.isSubject = False
        self.list_adjacency = []
        self.history = None
        for x in list_hubs:
            if x.history!=None:
                self.history = x.history
                self.year = x.year
            if x.isSubject:
                self.isSubject = True
            for y in x.list_adjacency:
                if not y in self.list_adjacency:
                    self.list_adjacency.append(y)
            longitude+=x.longitude
            width+=x.width
        if self.history!=None:
            self.name = self.history
        else:
            self.name = list_hubs[0].name
        self.longitude = longitude/len(list_hubs)
        self.width = width/len(list_hubs)
    def output(self):
        result = self.name + ' ' + str(round(self.longitude, 4)) + ' ' + str(round(self.width, 4)) + ' '
        if self.hub:
            result += 'узловая'
        if self.history != None:
            result += ' ' + self.history
        string_python_shit = ''
        for x in self.list_adjacency:
            string_python_shit = string_python_shit + ' ' + x.name
        unified_string = ''
        print('Unified_hub: ', result, ':', string_python_shit)
    def copy(self):
        list_result = []
        for x in self.list_adjacency:
            list_result.append(x)
        return Unified_Hub(list_result)

#to do: class Unified_Station_Hub - class width list of cloth hub stations, unified adjacency and history

class Vector:
    list_station = []
    isEast = None
    isNorth = None
    def __init__(self, list_station):
        self.list_station = list_station.copy()
        isEast = list_station[-1].longitude>list_station[0].longitude
        isNorth = list_station[-1].width>list_station[0].width
        if list_station[-1].hub:
            self.name = self.list_station[0].name + '-' + self.list_station[-1].name
        else:
            self.name = self.list_station[0].name + '-' + self.list_station[-2].name
    #def angle_vector(self):
        #угол между y = 0 и вектором
     #   return math.atan((self.list_station[-1].width-self.list_station[0].width)/(self.list_station[-1].longitude-self.list_station[0].longitude))
    def output(self):
        print (self.name)

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

def angle_vector(station1, station2):
    width1 = station1.width
    width2 = station2.width
    longitude1 = station1.longitude
    longitude2 = station2.longitude
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

def dif_angle_vectors(angle1, angle2):
    temp = abs(angle1-angle2)
    return abs(math.pi-temp)

def find_vectors_stations(list_candidates, init_station):
    #найти максимальную по модулю разницу между двумя углами
    angle_max = math.pi
    list_result = []
    station_first = Station('',0,0,False, None, None, None, None)
    station_second = Station('', 0, 0, False, None, None, None, None)
    list_hub = []
    for x in list_candidates:
        if x.hub:
            list_hub.append(x)
    r_min_x = 5
    for x in list_hub:
        r_temp = math.sqrt((x.width-init_station.width)**2+(x.longitude-init_station.longitude)**2)
        if r_min(r_temp, r_min_x, init_station, x):
            station_first = x
            r_min_x = r_temp
    if station_first.hub:
        for i in range (len(list_candidates)):
            if dif_angle_vectors(angle_vector(init_station, station_first), angle_vector(init_station, list_candidates[i]))<angle_max:
                angle_max = dif_angle_vectors(angle_vector(init_station, station_first), angle_vector(init_station, list_candidates[i]))
                station_second = list_candidates[i]
    else:
        for i in range (len(list_candidates)):
            for j in range (i+1, len(list_candidates)):
                if dif_angle_vectors(angle_vector(init_station, list_candidates[i]), angle_vector(init_station, list_candidates[j]))<angle_max:
                    angle_max = dif_angle_vectors(angle_vector(init_station, list_candidates[i]), angle_vector(init_station, list_candidates[j]))
                    station_first = list_candidates[i]
                    station_second = list_candidates[j]
    list_result.append(station_first)
    list_result.append(station_second)
    return list_result

def r_min(r_temp, r_min, init_station, x):
    return (r_temp<r_min and (init_station.width!=x.width or init_station.longitude!=x.longitude))

def find_close_station(list_piece, init_station):
    temp_r_min = 5
    temp_station = Station('', 0, 0, False, None, None, None, None)
    for x in list_piece:
        r_temp = math.sqrt((init_station.width - x.width) ** 2 + (init_station.longitude - x.longitude) ** 2)
        if r_temp<temp_r_min and r_temp!=0:
            temp_station = x
            temp_r_min = r_temp
    return temp_station


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
        elif x.history!=None:
            list_south.append(x)
            #print ('south_чзх')
    for i in range (len(list_south)-1, -1, -1):
        list_north.append(list_south[i])
    return list_north

def first_not_ring(history_list):
    for x in history_list:
        if not x.isRing:
            return x

def gain_adjac_for_stations(list_piece, North, South, West, East):
    list_temp_local = []
    for x in list_piece:
        if x.hub == False and (North-x.width<0.05 or x.width - South<0.05 or x.longitude-West<0.05 or East-x.longitude<0.05):
            x.append_list_adjacency(find_close_station(list_piece, x))
            list_temp_local.append(x)
        #elif x.hub== False:
            #list_temp_local.append(find_next_station_of_vector(list_piece, x))
        else:
            list_temp_local.append(x)
    #for x in list_temp:
      #  x.output()
    for i in range (len(list_temp_local)): #не работает, хренотень какая-то, помогите
        if list_temp_local[i].hub == False \
                and(North - list_temp_local[i].width >= 0.05 and list_temp_local[i].width - South >= 0.05 #вынести 0.05 в константу
                and list_temp_local[i].longitude - West >= 0.05 and East - list_temp_local[i].longitude >= 0.05): #если 2 станции
            for j in range (len(list_temp_local)):
                for x in list_temp_local[j].list_adjacency:
                    if x.name == list_temp_local[i].name:
                        list_temp_local[i].append_list_adjacency(list_temp_local[j])
    #for x in list_temp:
     #   x.output()
    for x in list_temp_local:
        #x.output()
        if x.hub == False and (North-x.width>=0.05 and x.width - South>=0.05 and x.longitude-West>=0.05 and East-x.longitude>=0.05):
            temporary_adjacency = []
            for y in x.list_adjacency:
                temporary_adjacency.append(list_temp_local[y.index])
            x.list_adjacency.clear()
            x.append_list_adjacency(find_close_station(temporary_adjacency, x))
         #   x.append_list_adjacency(find_close_vector_station(temporary_adjacency, x, list_piece[x.list_adjacency[0].index]))
    return list_temp_local

def gain_adjac_for_hubs(list_piece):
    #если две узловые станции очень рядом, они абсолютно точно связаны => их можно объединить
    for x in list_piece:
        if x.hub:
            for y in list_piece:
                for z in y.list_adjacency:
                    if z.name == x.name:
                        x.append_list_adjacency(y)
                        break
    return list_piece

def remake_hub (list_piece):
    list_result = []
    temp_list_hub = []
    for x in list_piece:
        if x.hub:
            temp_list_hub.append(x)
        else:
            list_result.append(x)
    i_x = 0
    for x in range(len(temp_list_hub)):
        x = x-i_x
        for y in range(len(temp_list_hub)):
            i = 0
            try:
                if x!=y-i and math.sqrt((temp_list_hub[x].longitude-temp_list_hub[y-i].longitude)**2+(temp_list_hub[x].width-temp_list_hub[y-i].width)**2)<0.45:
                    #print('helpme')
                    #temp_list_hub[y-i].output()
                    temp_list_hub[y-i] = Unified_Hub([temp_list_hub[x], temp_list_hub[y-i]])
                    #temp_list_hub[x].output()
                    #temp_list_hub[y-i].output()
                    #print (x, y-i)
                    del temp_list_hub[x]
                    i_x+=1
                    i+=1
            except:
                break
    for x in temp_list_hub:
        list_result.append(x)
    return list_result

def split_hub(list_piece):
    local_list_hub = []
    for x in list_piece:
        if x.hub:
            local_list_hub.append(x)
    return local_list_hub

def remove_adjac(local_station, local_adjac_station):
    for x in local_station.list_adjacency:
        if x.index == local_adjac_station.index:
            local_station.list_adjacency.remove(x)
            break

def distance(station1, station2):
    return ((station1.width-station2.width)**2+(station1.longitude-station2.longitude)**2)**0.5

def cut_list(list_temporary):
    for x in list_temporary:
        if x.isAdjac:
            del x
    return list_temporary

def isDistance(list_temporary):
    for x in list_temporary:
        if not x.hub:
            return True
    return False

def find_closest_vector_station(list_piece, init_station, vector_direction): #вот тут какая-то ошибка точно
    r_min_first = 1
    r_min_second = 0.2
    first_station = list_piece[-1].copy()
    second_station = list_piece[-1].copy()
    list_piece = cut_list(list_piece)
    is_state_hub = False
    if len(list_piece)<=3 or not isDistance(list_piece):
        return None
    if vector_direction%2==0: #find closest longitude
        for x in list_piece:
            if x.name != init_station.name and not x.isAdjac and abs(x.longitude-init_station.longitude)<r_min_second:
                if not is_state_hub:
                    r_min_second = r_min_first
                    second_station = first_station.copy()
                r_min_first = abs(x.longitude - init_station.longitude)
                first_station = x.copy()
            elif x.hub and not init_station.hub and abs(x.longitude-init_station.longitude)<r_min_second:
                is_state_hub = True
                r_min_second = abs(x.longitude-init_station.longitude)
                second_station = x.copy()
    else:
        for x in list_piece:
            if x.name!= init_station.name and not x.isAdjac and abs(x.width-init_station.width)<r_min_second:
                if not is_state_hub:
                    r_min_second = r_min_first
                    second_station = first_station.copy()
                r_min_first = abs(x.width-init_station.width)
                first_station = x.copy()
            elif x.hub and not init_station.hub and abs(x.width-init_station.width<r_min_second):
                is_state_hub = True
                r_min_second = abs(x.width - init_station.width)
                second_station = x.copy()
    list_result = []
    if distance(first_station, init_station)<distance(second_station, init_station):
        list_result.append(first_station)
        list_result.append(second_station)
    else:
        list_result.append(second_station)
        list_result.append(first_station)
    return list_result

def create_small_vector(init_station, vector_direction): #vector_direction: 0- North, 1 - East, 2 - South, 3 - West
    if vector_direction == 0:
        list_temp = split_for_gird(list_station, init_station.width+0.5, init_station.width, init_station.longitude+0.5, init_station.longitude-0.5)
    elif vector_direction == 1:
        list_temp = split_for_gird(list_station, init_station.width+0.5, init_station.width-0.5, init_station.longitude+0.5, init_station.longitude)
    elif vector_direction == 2:
        list_temp = split_for_gird(list_station, init_station.width, init_station.width-0.5, init_station.longitude+0.5, init_station.longitude-0.5)
    else:
        list_temp = split_for_gird(list_station, init_station.width+0.5, init_station.width-0.5, init_station.longitude, init_station.longitude-0.5)
    return find_closest_vector_station(list_temp, init_station, vector_direction) #выводит две станции

def create_vector(init_station, vector_direction):
    list_vector = []
    list_vector.append(init_station)
    temp = create_small_vector(init_station, vector_direction)
    try:
        for x in temp:
            list_vector.append(x)
    except: return None
    temp = list_vector[2].copy()
    init_station.isAdjac = True
    North_or_South = 0 #0 - North, 2 - South
    East_or_West = 1 #1 - East, 2 - West
    count_i = 0
    while (not temp.hub and not list_vector[-2].hub) or distance(init_station, temp)<0.45:
        count_i+=1
        if count_i>100:
            return None
        if list_vector[-1].width > list_vector[-3].width:
            North_or_South = 0
        else:
            North_or_South = 2
        if list_vector[-1].longitude>list_vector[-3].longitude:
            East_or_West = 1
        else:
            East_or_West = 3
        #temp.output()
        r_min = 5
        list_variaties = []
        isNone = True
        for i in range (0, 4):
            list_variaties.append(create_small_vector(temp, i)) #очень неоптимизированно, надо будет исправить
            if list_variaties[i]!=None and (i == North_or_South or i == East_or_West):
                isNone = False
                if distance(list_variaties[i][0], temp)<r_min:
                    r_min = distance(list_variaties[i][0], temp)
                    vector_direction = i
        if isNone:
            return None
        for x in list_variaties[vector_direction]:
            if not x.hub:
                x.isAdjac = True
            list_vector.append(x)
        temp = list_vector[-1].copy()
    return Vector(list_vector)

if __name__ == '__main__':
    #Создать файл .py sort_subject - проверить субъект на адекватность (4 исторические станции с 4 сторон)
    excel_file = openpyxl.load_workbook('sorted_subjects.xlsx')
    excel_file = excel_file['Sheet']
    list_station = []
    for row in excel_file:
        if row[0].value!= 'name' and row[0].value!=None:
            list_station.append(Station(row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value, row[6].value))
    #тестим на восьмерке, потому что... я не знаю, что можно с Москвой делать
    #create_vector(list_station, True, True, Station('МОС-ПАС-ЯРОС', 37.6575, 55.7777, True, 'Москва', 1147), Station('СЕРГ.ПОСАД', 38.1368, 56.302, False, 'Сергиев Посад', 1742)).output()
    North = 58.3
    South = 45.6
    East = 52
    West = 28
    list_station = split_for_gird(list_station, North, South, East, West)
    list_hub = split_hub(list_station)
    list_vectors = []
    print ('start_algorythm')
    for j in range (len(list_hub)):
        list_hub[j].output()
        for i in range (0, 4):
            temp = create_vector(list_hub[j], i)
            if temp != None:
                list_vectors.append(temp)
                temp.output()
            else:
                print (i)
        print ('I am working')
    wb = openpyxl.Workbook()
    ws_incomplete_information = wb.create_sheet("Список векторов")
    ws_incomplete_information.append({'A': 'название', 'B': 'широта init_station', 'C': 'долгота init_station', 'D': 'широта finish_station',
                                      'E': 'долгота finish_station', 'F': 'количество исторических поселений', 'G': 'номер вектора'})
    num_count = 0
    for x in list_vectors:
        ws_incomplete_information.append({'A': x.name, 'B': x.list_station[0].width, 'C': x.list_station[0].longitude,
                                          'D': x.list_station[-1].width, 'E': x.list_station[-1].longitude,
                                          'F': x.num_history(), 'G': num_count})
        ws_temp = wb.create_sheet(str(num_count))
        ws_temp.append({'A': 'название', 'B': 'history', 'C': 'широта', 'D': 'долгота'})
        for y in x.list_station:
            ws_temp.append({'A': y.name, 'B': y.history, 'C': y.width, 'D': y.longitude})
        num_count +=1
    wb.save ('all_vectors_helpme.xlsx')