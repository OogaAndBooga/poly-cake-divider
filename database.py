import pymongo
    
class DataBase():
    isconnected = False
    def __init__(self, port = 27017):
        self.port = port

    def if_not_connected_connect(self):
        if not self.isconnected:
            self.connect(self.port)

    def connect(self, port):
        self.client = pymongo.MongoClient(f'mongodb://localhost:{port}/')
        self.isconnected = True
        self.database = self.client['polygons']
        self.collection = self.database['polygons']

    def load_polygons(self):
        self.if_not_connected_connect()
        data = self.collection.find()
        return list(data)

    def save_poly(self, name, poly_points):
        self.if_not_connected_connect()
        data = {'name' : name, 'points' : poly_points}
        # print(data)
        self.collection.insert_one(data)

    