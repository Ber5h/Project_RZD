import openpyxl
import psycopg2
import math

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

class Point:
    def __init__(self, x, y, history):
        self.x = float(x)
        self.y = float(y)
        self.isHub = False
        self.isDeadEnd = False
        self.history = history
        self.isInVector = False
        self.isMatched = False
    def output(self, string_temp):
        print (self.x, self.y, string_temp)

class LineString:
    def __init__(self, init_point, finish_point, history):
        self.init_station = init_point
        self.finish_station = finish_point
        self.list_stations = []
        self.direction = init_point.x<finish_point.x
        self.history = history
        if self.history!=None:
            self.init_station.history = history
            self.finish_station.history = history
        self.isInVector = False
    def length(self):
        return distance(self.init_station, self.finish_station)
    def output(self, string_temp):
        print(self.init_station.x, self.init_station.y, self.finish_station.x, self.finish_station.y, string_temp)

class Vector:
    def __init__(self, list_linestrings, init_station, finish_station, id):
        self.list_linestrings = list_linestrings
        self.init_station = init_station
        self.finish_station = finish_station
        self.id=id
        self.isUsed = False
        self.isDeadEnd = False
    def init_subject(self):
        return find_subject(self.list_linestrings[0])
    def finish_subject(self):
        return find_subject(self.list_linestrings[-1])
    def angle(self, direct_vector, general_direct):
        #general_direct: 1 - East, 2 - South, 3 - West, 4 - North
        if general_direct == 1:
            ideal_angle = 0
        elif general_direct == 2:
            ideal_angle = math.pi*1.5
        elif general_direct == 3:
            ideal_angle = math.pi
        else:
            ideal_angle = math.pi/2
        if direct_vector:
            temp = angle_vector(self.list_linestrings[-1], self.list_linestrings[0])
        else:
            temp = angle_vector(self.list_linestrings[0], self.list_linestrings[-1])
        return abs(temp - ideal_angle)
    def history(self):
        list_history = []
        for x in self.list_linestrings:
            if x.history!=None and not x.history in list_history:
                list_history.append(x.history)
        return len(list_history)
    def isDirect(self, station1):
        return self.init_station == station1
    def reverse(self):
        self.list_linestrings.reverse()
        temp = self.init_station
        self.init_station = self.finish_station
        self.finish_station = temp
    def isNormalVector(self):
        return self.init_station != self.finish_station
    def output(self):
        print (self.init_station+' - '+self.finish_station)
    def length(self):
        return distance(self.list_linestrings[0], self.list_linestrings[-1])
    def x(self):
        return self.list_linestrings[-1].x-self.list_linestrings[0].x
    def y(self):
        return self.list_linestrings[-1].y-self.list_linestrings[0].y

class Subject:
    def __init__(self, north_border, south_border, west_border, east_border, name, saturation, weight, id):
        self.north_border = north_border
        self.south_border = south_border
        self.west_border = west_border
        self.east_border = east_border
        self.centre = Point((west_border+east_border)/2, (north_border+south_border)/2, None)
        self.name = name
        self.saturation = saturation
        self.weight = weight
        self.id = id
    def isinSubject(self, point1):
        return point1.x>=self.west_border and point1.x<=self.east_border and point1.y>self.south_border and point1.y<self.north_border

class Ring:
    def __init__(self, list_of_vectors, capital_name, subject_name, capital_point):
        self.list_of_vectors = list_of_vectors
        self.capital_name = capital_name
        self.subject_name = subject_name.split(' ')[0]
        self.capital_point = capital_point
    def history(self):
        result = 0
        for x in self.list_of_vectors:
            result+=x.history()
        return result
    def distance_to_edge(self):
        r_max = 0
        for x in self.list_of_vectors:
            for y in x.list_linestrings:
                temp = distance(y, self.capital_point)
                if temp>r_max:
                    r_max = temp
        return r_max
    def isNormal(self):
        temp_distance_edge = self.distance_to_edge()
        temp_history = self.history()
        print (self.capital_name, temp_distance_edge, temp_history, 'ring arguments')
        return temp_distance_edge>1.5 and temp_history>3

def time_to_finish(length, capital_point, that_point):
    return distance(that_point, capital_point)<2 and length>9

def find_subject(point1):
    list_result = []
    for x in subject_list:
        if x.isinSubject(point1):
            list_result.append(x)
    if len(list_result)==0:
        return find_closest_subject(point1, subject_list)
    return find_closest_subject(point1, list_result)

def angle_vector(station1, station2):
    width1 = station1.y
    width2 = station2.y
    longitude1 = station1.x
    longitude2 = station2.x
    try:
        tan = (width1-width2)/(longitude1-longitude2)
    except:
        tan = (width1-width2)/(longitude1-longitude2+1)
    isTanPos = tan>=0
    isCosPos = longitude1>=longitude2
    if (isTanPos and isCosPos): #I четверть
        return math.pi/2-math.atan(tan)
    elif isTanPos and not isCosPos: #III четверть
        return math.pi*1.5-math.atan(tan)
    elif not isTanPos and isCosPos: #IV четверть
        return math.pi/2-math.atan(tan)
    else: #II четверть
        return math.pi*1.5-math.atan(tan)

def select_list(cursor1):
    list_vector = []
    index = 0
    for row in cursor1:
        temp_id = row[0]
        init_station = row[1]
        finish_station = row[2]
        cursor_temp = conn.cursor()
        cursor_temp.execute('SELECT * FROM linestring_list WHERE id = ' + str(temp_id) + '')
        list_linestring = []
        for row_linestring in cursor_temp:
            list_linestring.append(Point(row_linestring[0], row_linestring[1], row_linestring[2]))
        list_vector.append(Vector(list_linestring, init_station, finish_station, temp_id))
        #print (init_station, finish_station)
        index+=1
    if index == 1:
        list_vector[0].isDeadEnd = True
    return list_vector

def distance(point1, point2):
    return ((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2) ** 0.5

def sort_for_capitals():
    list_result = []
    for x in main_list_station:
        if x.isSubject:
            list_result.append(x)
    return list_result

def find_closest_subject(point1, subject_list):
    r_min = 5
    temp = None
    for x in subject_list:
        temp_r = distance(x.centre, point1)
        if temp_r<r_min:
            temp = x
            r_min = temp_r
    return temp

def history_sort():
    list_result = []
    for x in main_list_station:
        if x.history:
            list_result.append(x)
    return list_result

def create_history_list():
    list_result = []
    cursor_temp = conn.cursor()
    cursor_temp.execute('SELECT history FROM linestring_list')
    for row_temp in cursor_temp:
        list_result.append(row_temp[0])
    return list_result

def correct_history_subject_list(temp_list):
    list_result = []
    for x in temp_list:
        if x in history_list:
            list_result.append(x)
    return list_result

def list_important_points(temp_history_list):
    list_result = []
    for x in temp_history_list:
        temp_vector = find_vector_for_hist(x)
        for y in temp_vector:
            list_result.append(y)
    return list_result

def find_vector_for_hist(history_name):
    temp_cursor = conn.cursor()
    id_list = []
    temp_cursor.execute('SELECT * FROM linestring_list where history like \''+history_name+'%\'')
    for temp_row in temp_cursor:
        point_temp = Point(temp_row[0], temp_row[1], temp_row[2])
        id_list.append(temp_row[3])
    if isSimilar(id_list):
        temp_cursor.execute('SELECT * FROM linestring_list where id = '+str(id_list[0]))
        count = 0
        index = 0
        point_first = None
        point_last = None
        for temp_row in temp_cursor:
            count+=1
        temp_cursor.execute('SELECT * FROM linestring_list where id = ' + str(id_list[0]))
        for temp_row in temp_cursor:
            if index == 0:
                point_first = Point(temp_row[0], temp_row[1], temp_row[2])
            if index == count-1:
                point_last = Point(temp_row[0], temp_row[1], temp_row[2])
            index+=1
        if point_first == None:
            print ('ГОВНО')
        return [point_first, point_last]
    else:
        return [point_temp]

def isSimilar(temp_list):
    temp = temp_list[0]
    for x in temp_list:
        if x!=temp:
            return False
    return True

def find_best_actual_point(point_list, capital_point):
    angle_min = 7
    temp_point = None
    for x in point_list:
        temp_angle = angle_vector(x, capital_point) #здесь норм
        if temp_angle<angle_min and not x.isMatched:
            temp_point = x
            angle_min = temp_angle
    temp_point.isMatched = True
    return temp_point

def reverse_vector(vector1, init_station_name):
    if init_station_name != vector1.init_station:
        vector1.reverse()
        return vector1
    else:
        return vector1

def isNonPriorVector(vector1, vector_temp_vector):
    for i in range(1, len(vector_temp_vector)):
        if vector1.finish_station == vector_temp_vector[i].init_station:
            print (vector1.finish_station, 'ПАРАША')
            return True
    return False

def length_ring(temp_ring):
    result = 0
    for x in temp_ring:
        result+=x.length()
    return result

def find_best_vector(init_station_name, init_point, finish_point, vector_temp_list, temp_ring):
    best_angle = 7
    cursor_temp = conn.cursor()
    cursor_temp.execute('SELECT * FROM vector_list WHERE init_station = \''+init_station_name+'\' or finish_station = \''+init_station_name+'\'')
    choice_vector = select_list(cursor_temp)
    temp_vector = None
    print (len(choice_vector), 'length')
    print (init_station_name)
    for x in choice_vector:
        x = reverse_vector(x, init_station_name)
    non_priority_vector_list = []
    try:
        capital_point = temp_ring[0].list_linestrings[0]
    except:
        capital_point = init_point
    for x in choice_vector:
        temp_angle = double_angle(x, Vector([init_point, finish_point], None, None, 0))
        #print(temp_angle, 'angle')
        #x.output()
        if temp_angle<best_angle and x.isNormalVector() and isActualVector(x, vector_temp_list):
            try:
                if isNonPriorVector(x, temp_ring) and not time_to_finish(length_ring(temp_ring), capital_point, init_point):
                    print (x.finish_station, 'ПАРАША УСЛОВИЕ')
                    non_priority_vector_list.append(x)
                else:
                    if not (finish_ring(x, temp_ring[0].init_station) and length_ring(temp_ring)<6):
                        best_angle = temp_angle
                        temp_vector = x
            except:
                try:
                    if not (finish_ring(x, temp_ring[0].init_station) and length_ring(temp_ring)<6):
                        best_angle = temp_angle
                        temp_vector = x
                except:
                    best_angle = temp_angle
                    temp_vector = x
    if temp_vector == None:
        print ('Говно')
        return non_priority_vector_list[0]
    print (length_ring(temp_ring), 'length_ring')
    return temp_vector

def isEqualPoint(point1, point2):
    return distance(point1, point2)<0.1

def finish_ring(vector1, capital_name):
    return vector1.finish_station == capital_name

def from_hist_to_hist(init_station_name, init_point, finish_point, temp_ring):
    vector_list = []
    temp_vector = find_best_vector(init_station_name, init_point, finish_point, vector_list, temp_ring)
    temp_ring.append(temp_vector)
    vector_list.append(temp_vector)
    temp_vector.output()
    while not isEqualPoint(temp_vector.list_linestrings[-1], finish_point):
        if length_ring(temp_ring)>30:
            return None
        temp_vector = find_best_vector(temp_vector.finish_station,
        Point(temp_vector.list_linestrings[-1].x, temp_vector.list_linestrings[-1].y, None), finish_point, vector_list, temp_ring)
        vector_list.append(temp_vector)
        temp_ring.append(temp_vector)
        temp_vector.output()
        if isRing(temp_ring):
            break
    return temp_ring

def isActualList(list_point):
    for x in list_point:
        if x.isMatched:
            return True
    return False

def isRing(ring_list):
    try:
        return ring_list[0].init_station == ring_list[-1].finish_station
    except:
        return False

def create_ring(capital_point, temp_important_list, capital_name, subject_name):
    temp_point = find_best_actual_point(temp_important_list, capital_point)
    ring_result = []
    temp_name = capital_name
    temp_init_point = capital_point
    while not isRing(ring_result):
        try:
            if time_to_finish(length_ring(ring_result), capital_point, ring_result[-1].list_linestrings[-1]):
                temp_point = capital_point
        except:
            print ('first_vector')
        print ('УРА')
        temp_point.output('Сосать')
        ring_result = from_hist_to_hist(temp_name, temp_init_point, temp_point, ring_result)
        if ring_result == None:
            return None
        if isRing(ring_result):
            break
        temp_point.isMatched = True
        temp_point = find_best_actual_point(temp_important_list, capital_point)
        temp_name = ring_result[-1].finish_station
        temp_init_point = ring_result[-1].list_linestrings[-1]
        print (temp_name)
    #temp_vector_list = from_hist_to_hist(temp_name, temp_init_point, capital_point)
    #for x in temp_vector_list:
    #    ring_result.append(x)
    return Ring(ring_result, capital_name, subject_name, capital_point)

def isActualVector(vector1, vector_list):
    for x in vector_list:
        if vector1.init_station == x.init_station and vector1.finish_station == x.finish_station:
            return False
    return True

def double_angle(vector1, vector2): #начинаются с одной point
    #x1*x2+y1*y2=|vector1|*|vector2|*cos(angle)
    dot_products = vector1.x()*vector2.x()+vector1.y()*vector2.y()
    try:
        cos_angle = dot_products/(vector1.length()*vector2.length())
    except:
        cos_angle = 1
    return math.acos(round(cos_angle, 4))

if __name__ == '__main__':
    used_vectors = []
    excel_file = openpyxl.load_workbook('finally_ready_station_file.xlsx')
    excel_file = excel_file['Sheet']
    main_list_station = []
    for row in excel_file:
        if row[0].value != 'name' and row[0].value != None:
            main_list_station.append(Station(row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value,
                        row[6].value, row[7].value))
    conn = psycopg2.connect(dbname='postgres', user='postgres', password='Toplova_2006', host='localhost')
    cursor = conn.cursor()
    capital_list = sort_for_capitals()
    subject_list = []
    history_list = create_history_list()
    cursor.execute('SELECT * FROM subject_rf')
    for row in cursor:
        subject_list.append(Subject(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]))
    ring_list = []
    for x in capital_list:
        temp_subject = find_subject(Point(x.longitude, x.width, None))
        temp_hist_list = []
        cursor.execute('SELECT history FROM subject_history where id = '+ str(temp_subject.id))
        for row in cursor:
            temp_hist_list.append(row[0])
        temp_hist_list = correct_history_subject_list(temp_hist_list)
        print (temp_hist_list)
        important_list = list_important_points(temp_hist_list)
        if len(temp_hist_list) > 3:
            test_ring = create_ring(Point(x.longitude, x.width, None), important_list, x.name, temp_subject.name)
            if test_ring!=None:
                if test_ring.isNormal():
                    ring_list.append(test_ring)
        print ('Х') #если ты понимаешь, о чем я
    index = 0
    for x in ring_list:
        temp_table_name = x.subject_name+'_'+str(index)
        cursor.execute('CREATE TABLE IF NOT EXISTS '+temp_table_name+'(vector_id serial not null, init_station text, finish_station text);')
        for y in x.list_of_vectors:
            cursor.execute('INSERT INTO '+ temp_table_name+ ' VALUES (%s, %s, %s)', (y.id, y.init_station, y.finish_station))
        index+=1
    cursor.close()
    conn.commit()
    conn.close()
