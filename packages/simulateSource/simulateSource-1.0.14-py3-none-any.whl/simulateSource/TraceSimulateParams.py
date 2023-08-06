from simulateSource.SimulateParams import SimulateParams



class TraceSimulateParams(SimulateParams):
    def __init__(self):
        self.__longitude = 0.0
        self.__latitude = 0.0
        self.altitude = 0
        self.simulateDisplaySpeed = None
        self.traceGain = None
        self.simulateTime = None
        self.fileName = None

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, lon):
        # print(lon)
        if isinstance(lon, float) and lon <= 180:
            self.__longitude = lon
        else:
            raise ValueError

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, lat):
        if isinstance(lat, float) and lat <= 90:
            self.__latitude = lat
        else:
            raise ValueError

