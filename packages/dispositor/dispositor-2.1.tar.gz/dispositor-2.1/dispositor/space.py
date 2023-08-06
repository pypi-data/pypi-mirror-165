import dispositor.planet as planet
from dispositor.segment import Segment
from dispositor.db.db import DispositorDB


class Space:
    """
    Класс пространства.
    Для создания необходима дата и сегменты (деление пространства)
    Обязанность: Создание сегментов и планет.
    """
    def __init__(self, segmentData, date=None, db: DispositorDB = None):
        self.segmentData = segmentData
        self.deg_count = 360
        self.segments = self.createSegments()
        self.planets = self.createPlanets()
        self.date = date
        self.db = db
        if db is not None:
            db.init(self.planets, self.segments)

    def setDate(self, date):
        self.date = date
        return self

    def createPlanets(self):
        """
        Уникальные значения планет из списка сегментов
        """
        planets = []
        for owner_planet in [segment.owner_planet for segment in self.segments]:
            if owner_planet.__name__ not in [planet_class.__class__.__name__ for planet_class in planets]:
                planets.append(owner_planet(self))
        return planets

    def createSegments(self):
        """
        Фабрика сегментов
        """
        segments = []
        for i, segment_data in enumerate(self.segmentData):
            deg_in_segment = self.getDegCount() / self.getSegmentCount()
            deg_from = i * deg_in_segment
            deg_to = deg_from + deg_in_segment
            segments.append(Segment(
                i+1,
                segment_data['id'],
                segment_data['name'],
                segment_data['rus_name'],
                segment_data['owner_planet'],
                deg_from, deg_to
            ))
        return segments

    def getSegmentCount(self):
        """
        Получить количество сегментов
        """
        return len(self.segmentData)

    def getDegCount(self):
        """
        Получить количество градусов в окружности (пространстве)
        """
        return self.deg_count

    def getPlanets(self):
        """
        Получить список планет
        """
        return self.planets

    def getSegments(self):
        """
        Получить список сегментов
        """
        return self.segments

    def save(self):
        if self.db is not None:
            self.db.fillingDayTable(self.planets, self.date)


def classicSegmentData():
    """
    Классическое расположение сегментов и планет
    """
    return [
        {'id': 1, 'name': 'Aries', 'rus_name': 'Овен', 'owner_planet': planet.Mars},
        {'id': 2, 'name': 'Taurus', 'rus_name': 'Телец', 'owner_planet': planet.Venus},
        {'id': 3, 'name': 'Gemini', 'rus_name': 'Близнецы', 'owner_planet': planet.Mercury},
        {'id': 4, 'name': 'Cancer', 'rus_name': 'Рак', 'owner_planet': planet.Moon},
        {'id': 5, 'name': 'Leo', 'rus_name': 'Лев', 'owner_planet': planet.Sun},
        {'id': 6, 'name': 'Virgo', 'rus_name': 'Дева', 'owner_planet': planet.Mercury},
        {'id': 7, 'name': 'Libra', 'rus_name': 'Весы', 'owner_planet': planet.Venus},
        {'id': 8, 'name': 'Scorpio', 'rus_name': 'Скорпион', 'owner_planet': planet.Pluto},
        {'id': 9, 'name': 'Sagittarius', 'rus_name': 'Стрелец', 'owner_planet': planet.Jupiter},
        {'id': 10, 'name': 'Capricorn', 'rus_name': 'Козерог', 'owner_planet': planet.Saturn},
        {'id': 11, 'name': 'Aquarius', 'rus_name': 'Водолей', 'owner_planet': planet.Uranus},
        {'id': 12, 'name': 'Pisces', 'rus_name': 'Рыбы', 'owner_planet': planet.Neptune},
    ]


def septenerSegmentData():
    """
    Расположение сегментов и планет
    """
    return [
        {'id': 1, 'name': 'Aries', 'rus_name': 'Овен', 'owner_planet': planet.Mars},
        {'id': 2, 'name': 'Taurus', 'rus_name': 'Телец', 'owner_planet': planet.Venus},
        {'id': 3, 'name': 'Gemini', 'rus_name': 'Близнецы', 'owner_planet': planet.Mercury},
        {'id': 4, 'name': 'Cancer', 'rus_name': 'Рак', 'owner_planet': planet.Moon},
        {'id': 5, 'name': 'Leo', 'rus_name': 'Лев', 'owner_planet': planet.Sun},
        {'id': 6, 'name': 'Virgo', 'rus_name': 'Дева', 'owner_planet': planet.Mercury},
        {'id': 7, 'name': 'Libra', 'rus_name': 'Весы', 'owner_planet': planet.Venus},
        {'id': 8, 'name': 'Scorpio', 'rus_name': 'Скорпион', 'owner_planet': planet.Mars},
        {'id': 9, 'name': 'Sagittarius', 'rus_name': 'Стрелец', 'owner_planet': planet.Jupiter},
        {'id': 10, 'name': 'Capricorn', 'rus_name': 'Козерог', 'owner_planet': planet.Saturn},
        {'id': 11, 'name': 'Aquarius', 'rus_name': 'Водолей', 'owner_planet': planet.Saturn},
        {'id': 12, 'name': 'Pisces', 'rus_name': 'Рыбы', 'owner_planet': planet.Jupiter},
    ]

def thirtySixSegmentsData():
    """
    36 сегментов
    """
    return [
        {'id': 1, 'name': 'Segment1', 'rus_name': 'Овен', 'owner_planet': planet.Sun},
        {'id': 2, 'name': 'Segment2', 'rus_name': 'Телец', 'owner_planet': planet.Sun},
        {'id': 3, 'name': 'Segment3', 'rus_name': 'Близнецы', 'owner_planet': planet.Sun},
        {'id': 4, 'name': 'Segment4', 'rus_name': 'Рак', 'owner_planet': planet.Sun},
        {'id': 5, 'name': 'Segment5', 'rus_name': 'Лев', 'owner_planet': planet.Sun},
        {'id': 6, 'name': 'Segment6', 'rus_name': 'Дева', 'owner_planet': planet.Sun},
        {'id': 7, 'name': 'Segment7', 'rus_name': 'Весы', 'owner_planet': planet.Sun},
        {'id': 8, 'name': 'Segment8', 'rus_name': 'Скорпион', 'owner_planet': planet.Sun},
        {'id': 9, 'name': 'Segment9', 'rus_name': 'Стрелец', 'owner_planet': planet.Sun},
        {'id': 10, 'name': 'Segment10', 'rus_name': 'Козерог', 'owner_planet': planet.Sun},
        {'id': 11, 'name': 'Segment11', 'rus_name': 'Водолей', 'owner_planet': planet.Sun},
        {'id': 12, 'name': 'Segment12', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 13, 'name': 'Segment13', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 14, 'name': 'Segment14', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 15, 'name': 'Segment15', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 16, 'name': 'Segment16', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 17, 'name': 'Segment17', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 18, 'name': 'Segment18', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 19, 'name': 'Segment19', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 20, 'name': 'Segment20', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 21, 'name': 'Segment21', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 22, 'name': 'Segment22', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 23, 'name': 'Segment23', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 24, 'name': 'Segment24', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 25, 'name': 'Segment25', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 26, 'name': 'Segment26', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 27, 'name': 'Segment27', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 28, 'name': 'Segment28', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 29, 'name': 'Segment29', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 30, 'name': 'Segment30', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 31, 'name': 'Segment31', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 32, 'name': 'Segment32', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 33, 'name': 'Segment33', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 34, 'name': 'Segment34', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 35, 'name': 'Segment35', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
        {'id': 36, 'name': 'Segment36', 'rus_name': 'Рыбы', 'owner_planet': planet.Sun},
    ]