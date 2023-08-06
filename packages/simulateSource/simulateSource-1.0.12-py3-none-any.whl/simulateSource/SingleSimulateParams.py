from simulateSource.SimulateParams import SimulateParams


class SingleSimulateParams(SimulateParams):

    def __init__(self):
        self.__longitude = 0
        self.__latitude = 0
        self.altitude = 0
        self.singleGain = None
        self.simulateTime = None
        self.simulateTimeList = [0 for _ in range(7)]

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, lon):
        if isinstance(lon, float) and lon <= 180 :
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

if __name__ == "__main__":
    sing = SingleSimulateParams()
    # sing.simulateTimetest("20210916152315")
    # t1 = time.struct_time(tm_year=2018, tm_mon=9, tm_mday=14,
    #                       tm_hour=15, tm_min=1, tm_sec=44, tm_wday=4, tm_yday=257,
    #                       tm_isdst=0)
    # print(t1)

