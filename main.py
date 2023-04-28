import openpyxl
import math
import sklearn
from sklearn import svm
from sklearn import ensemble
from sklearn import neighbors
from sklearn import linear_model
from sklearn import metrics
from sklearn import cluster

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
        self.index = index
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
        return self.list_stations[-1].width-self.list_stations[-1].width
    def length(self):
        return distance(self.list_stations[0], self.list_stations[-1])
    def isInVector(self, station):
        for x in self.list_stations:
            if x.name == station.name:
                return True
        return False

def distance_vector(vector1, station1):
    #S = h*vector1.length/2
    distance1 = vector1.length()
    distance2 = distance(vector1.list_stations[0], station1)
    distance3 = distance(vector1.list_stations[-1], station1)
    p = (distance1+distance2+distance3)/2
    S = math.sqrt(p*(p-distance3)*(p-distance2)*(p-distance1))
    h = 2*S/distance1
    return h

def distance(station1, station2):
    return ((station1.longitude-station2.longitude)**2+(station1.width-station2.width)**2)**0.5

def num_station_between(station1, station2):
    temp_list = split_for_gird(list_station, max(station1.width, station2.width), min(station1.width, station2.width),
        max(station1.longitude, station2.longitude), min(station1.longitude, station2.longitude))
    return len(temp_list)-2

class X_train:
    def __init__(self, station1, vector1):
        temp = []
        temp.append(abs(vector1.list_stations[0].longitude-station1.longitude))
        temp.append(abs(vector1.list_stations[0].width-station1.width))
        temp.append(abs(vector1.list_stations[-1].longitude-station1.longitude))
        temp.append(abs(vector1.list_stations[-1].width-station1.width))
        temp.append(distance_vector(vector1, station1))
        self.train_list = temp.copy()

def split_for_gird (list_station, North, South, East, West):
    list_result = []
    for x in list_station:
        if x.width<=North and x.width>=South and x.longitude<=East and x.longitude>=West:
            list_result.append(x)
    return list_result

def create_test_adjac(list_temp, filename):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append({'A': 'adjacency'})
    ws.append(list_name())
    for x in list_temp:
        ws.append({'A': x.name})
    wb.save(filename+ '.xlsx')

def list_name():
    list_result = []
    for x in list_station:
        list_result.append(x.name)
    return list_result

def ML_fit(vector_list, main_list):
    X_train_list = []
    Y_train_list = []
    for x in vector_list:
        for y in main_list:
            X_train_list.append(X_train(y, x).train_list)
            if x.isInVector(y):
                Y_train_list.append(1)
            else:
                Y_train_list.append(0)
    # что-то выводят: r2, randomforest и PassiveAgressive
    model = ensemble.RandomForestClassifier() #пока что лучший из работающих
    print (X_train_list)
    model.fit(X_train_list, Y_train_list)
    return model

def ML_predict(model, predict_hubs_list, predict_station_list):
    vector_list_result = []
    for x in predict_hubs_list:
        for y in predict_hubs_list:
            if x.name!=y.name:
                temp_list = []
                temp_list.append(x)
                temp_list.append(y)
                temp_vector = Vector(temp_list)
                for z in predict_station_list:
                    temp_data = X_train(x, temp_vector).train_list
                    if model.predict(temp_data)>0.5 and not temp_vector.isInVector(z):
                        temp_vector.list_stations.append(z)
                vector_list_result.append(temp_list)
    return vector_list_result

def find_adjac_station(init_station, index_last_station):
    result = []
    for i in range(len(N)):
        if N[init_station.index][i]==1 and i!= index_last_station:
            result.append(i)
    return result #list of indexes

def create_vector(init_station, next_index):
    temp_vector = []
    temp_vector.append(init_station)
    temp_vector.append(list_station[next_index])
    temp_index = init_station.index
    while not list_station[next_index].hub:
        a = next_index
        temp_list_index = find_adjac_station(list_station[next_index], temp_index)
        if len(temp_list_index)==1:
            next_index = temp_list_index[0]
        else:
            return Vector(temp_vector)
        temp_vector.append(list_station[next_index])
        temp_index = a
    return Vector(temp_vector)

def create_list_vectors(init_station):
    list_vectors = []
    n = sum(N[init_station.index])
    temp = find_adjac_station(init_station, -1)
    for x in temp:
        temp_list = create_vector(init_station, x)
        if temp_list!=None:
            list_vectors.append(temp_list)
    return list_vectors

def list_hubs_sort(temp_list_station):
    result = []
    for x in range(len(N)):
        if sum(N[x])>2:
            result.append(list_station[x])
    return result

def isVector(first_station, finish_station):
    for x in main_list_vectors:
        if x.list_stations[0].name == first_station.name and x.list_stations[-1].name == finish_station.name:
            return True
    return False

def correct_data_for_ML():
    #adjacency_matrix_for_hubs
    N_hubs = []
    new_index = 0
    for x in list_hubs:
        x.index = new_index
        new_index+=1
        temp_matrix_string = []
        for y in list_hubs:
            if isVector(x, y):
                temp_matrix_string.append(1)
            else:
                temp_matrix_string.append(0)
        N_hubs.append(temp_matrix_string)
    return N_hubs

if __name__ == '__main__':
    index = 0
    excel_file = openpyxl.load_workbook('finally_ready_station_file.xlsx')
    excel_file = excel_file['Sheet']
    main_list_station = []
    North = 52.82
    South = 51.4
    East = 40
    West = 37.1
    for row in excel_file:
        if row[0].value != 'name' and row[0].value != None:
            main_list_station.append(Station(row[0].value, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value,
                        row[6].value, row[7].value))
            if row[2].value <= North and row[2].value >= South and row[1].value <= East and row[1].value >= West:
                index+=1
    list_station = split_for_gird(main_list_station, North, South, East, West)
    excel_file = openpyxl.load_workbook('adjacency.xlsx')
    excel_file = excel_file['Sheet']
    N = []
    for row in excel_file:
        if row[0].value != 'adjacency' and row[0].value != None:
            temp = []
            i = 1
            while i<=len(list_station):
                temp.append(row[i].value)
                i += 1
            N.append(temp)
    print (N)
    list_hubs = list_hubs_sort(list_station)
    main_list_vectors = []
    for x in list_hubs:
        temp_list_vectors = create_list_vectors(x)
        for y in temp_list_vectors:
            main_list_vectors.append(y)
    #for x in main_list_vectors:
    #    x.complete_output()
    North = 54.1
    South = 52.5
    East = 40.6
    West = 37.88
    predict_data_list = split_for_gird(main_list_station, North, South, East, West)
    predict_hub_list = []
    for x in predict_data_list:
        if x.hub:
            predict_hub_list.append(x)
    N_hubs = correct_data_for_ML()
    model_hub = ML_fit(main_list_vectors, list_station)
    vector_predict_result = ML_predict(model_hub, predict_hub_list, predict_data_list)
    for x in vector_predict_result:
        x.complete_output()