import datetime
import calendar
import astral
import astral.geocoder
import astral.sun


class MovingPointers:

    def __init__(self, time: datetime.datetime, city: astral.LocationInfo = None, nextDay: bool = False):
        self.time = time
        if city:
            self.city = city
        if nextDay is True or city:
            self.daylight = astral.sun.sun(
                self.city.observer, date=self.time, tzinfo=self.time.tzinfo)

    def hoursPointer(self):
        '''
            Angle in Circle for
        Hours (Small) Pointer
        '''
        return 360 * (self.time.hour*60*60 + self.time.minute*60 + self.time.second) / 86, 400

    def minutesPointer(self):
        '''
            Angle in Circle for
        Minutes (Large) Pointer
        '''
        return 360 * (self.time.minute*60 + self.time.second) / 3600

    def secondsPointer(self):
        '''
            Angle in Circle for
        Seconds (Straight) Pointer
        '''
        return 360 * self.time.second / 60

    def date_earthPosition(self):
        '''
            Angle in Circle for
        Earth.png Position that shows Date in Year
        '''
        DAYS = 366 if calendar.isleap(self.time.year) else 365
        return 360 * int(self.time.strftime('%j')) / DAYS

    def noon_hexaRotation(self):
        '''
            Rotation Angle for Hexagon
        Yellow Top pointing (Solar Noon)
        Purple Bottom (Midnight)

        --- -X° rotation to LEFT ---
        --- +X° rotation to RIGHT ---
        '''
        noon = self.daylight['noon']
        return 360 * (noon.hour*60*60 + noon.minute*60 + noon.second) / 86, 400 - 180

    def daylightPart(self):
        '''
            Area in Circle for Daylight
        Higher Left Angle for Sunrise --- > 180° ---
        Higher Right Angle for Sunset --- < 180° ---

        Lower Left Angle for Dawn --- > 180° & > Higher Left ---
        Lower Right Angle for Dusk --- < 180° & < Higher Right ---

        Upper part of Circle above 2 Higher Lines is Colored with LIGHTER colors
        Lower part of Circle above 2 Lower Lines and bellow 2 Higher Lines is Colored with DARKER colors
        Down part bellow 2 Lower Lines is GRAY colored
        '''
        sunrise = self.daylight['sunrise']
        HigherLeft = 360 * (sunrise.hour*60*60 +
                            sunrise.minute*60 + sunrise.second) / 86, 400
        sunset = self.daylight['sunset']
        HigherRight = 360 * (sunset.hour*60*60 +
                             sunset.minute*60 + sunset.second) / 86, 400

        dawn = self.daylight['dawn']
        LowerLeft = 360 * (dawn.hour*60*60 + dawn.minute *
                           60 + dawn.second) / 86, 400
        dusk = self.daylight['dusk']
        LowerRight = 360 * (dusk.hour*60*60 + dusk.minute *
                            60 + dusk.second) / 86, 400


if __name__ == '__main__':
    now = datetime.datetime.now()

    print(now.weekday())
    print(now.hour)
    print(now.minute)
    print(now.second)
    print(now.microsecond)
    print(now.astimezone().tzinfo)
    print(now.today())
    print(now.tzinfo)

    print(now.day)
    print(now.month)
    print(now.year)

    import json
    from timezonefinder import TimezoneFinder
    import time

    jsonPath = 'CLOCK/worldcities.json'
    with open(jsonPath, 'r') as file:
        WORLD: dict = json.load(file)

    start = time.time_ns()

    continent = 'Europe'
    subregion = 'Southern Europe'
    country = 'Slovenia'
    administration = 'Ptuj'
    city = 'Ptuj'

    lat = WORLD[continent][subregion][country][administration][city]['latitude']
    lng = WORLD[continent][subregion][country][administration][city]['longitude']
    timezone = WORLD[continent][subregion][country][administration][city]['timezone']

    print(timezone)
    print(f'{(time.time_ns()-start)/10**6:,.2f} ms')
    CITY = astral.LocationInfo(
        name=city,
        region=country,
        timezone=timezone,
        latitude=lat,
        longitude=lng)

    now = datetime.datetime.now(CITY.tzinfo)

    daylight = astral.sun.sun(CITY.observer, date=now, tzinfo=CITY.tzinfo)

    print(f'{(time.time_ns()-start)/10**6:,.2f} ms')

    print(daylight['dawn'])
    print(daylight['sunrise'])
    print(daylight['noon'])
    print(daylight['sunset'])
    print(daylight['dusk'])

    print(f'{(time.time_ns()-start)/10**6:,.2f} ms')
