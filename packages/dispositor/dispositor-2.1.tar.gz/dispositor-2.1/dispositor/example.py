from dispositor.db.db import DispositorDB
from dispositor import space as spaceClass
import pandas as pd
from dispositor.experiments.degree_of_displacement.degree_of_displacement import DegreeOfDisplacement
from planet import Sun
import json
from os.path import exists
import threading


if __name__ == '__main__':
    db = DispositorDB({
        'host': 'localhost',
        'user': 'user',
        'password': 'password',
        'database': 'people',
        'prefix': 'wwwtest_',
        'port': 3306
    })

    # #  Пример заполнения таблицы "дни"
    # space = spaceClass.Space(spaceClass.septenerSegmentData(), None, db)
    #
    # start_date = '1900-01-01'
    # end_date = '2010-01-01'
    #
    # daterange = pd.date_range(start_date, end_date)
    #
    # for single_date in daterange:
    #     date = single_date.strftime("%Y/%m/%d")
    #     space.setDate(date)
    #     space.save()
    #     print(date)


    # Пример заполенния таблицы Центры по дням
    # space = spaceClass.Space(spaceClass.septenerSegmentData(), None, db)
    # planet = space.planets[0]
    # segment = space.segments[0]
    # degree_of_displacement = DegreeOfDisplacement(
    #     space=space,  # Пространство
    #     row_count=10000,  # Количество человек по условию
    #     conditions={'planetId': planet.id, 'segmentId': segment.id},  # Условие
    #     summary_people_threshold=50,  # Порог количества людей одной деятельности по условию
    # )
    # degree_of_displacement.fillingCenterTable()

    #  Пример создания эксперимента "По степени смещения"
    # space = spaceClass.Space(spaceClass.thirtySixSegmentsData(), None, db)
    # planet = space.planets[0]
    # segment = space.segments[0]
    # degree_of_displacement = DegreeOfDisplacement(
    #     space=space,  # Пространство
    #     row_count=10000,  # Количество человек по условию
    #     conditions={'planetId': planet.id, 'segmentId': segment.id},  # Условие/ можно передать center_planet_id
    #     summary_people_threshold=40,  # Порог количества людей одной деятельности по условию
    # )
    # degree_of_displacement = degree_of_displacement.fillingDegreeOfDisplacement(planet, segment)
    # print(degree_of_displacement)



    path = 'segmen36/data1.json'
    file_exists = exists(path)
    segment_count = len(spaceClass.septenerSegmentData())
    if file_exists is False:
        data = json.dumps([0] * segment_count)
        f = open(path, "w")
        f.write(data)
        f.close()

    f = open(path, "r")
    data = list(json.loads(f.read()))
    f.close()

    threads = []
    for i in range(500):
        for segment_number in range(segment_count):
            print('%s/%s' % (segment_number, i))
            space = spaceClass.Space(spaceClass.septenerSegmentData(), None, db)
            planet = space.planets[4]
            segment = space.segments[segment_number]
            print(segment.rus_name, planet.name)
            degree_of_displacement = DegreeOfDisplacement(
                space=space,  # Пространство
                row_count=10000,  # Количество человек по условию
                conditions={'planetId': planet.id, 'segmentId': segment.id},  # Условие/ можно передать center_planet_id
                summary_people_threshold=50,  # Порог количества людей одной деятельности по условию
            )
            degree_of_displacement = degree_of_displacement.fillingDegreeOfDisplacement(planet, segment)
            if degree_of_displacement == 0:
                print('OK')
                data[segment_number] = data[segment_number] + 1
                f = open(path, "w")
                data_for_write = json.dumps(data)
                f.write(data_for_write)
                f.close()
            print('-' * 50)


