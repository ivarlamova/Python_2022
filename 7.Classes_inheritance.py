# Иерархия классов для данных из таблицы.
# Классы: CarBase (базовый класс для всех типов машин), Car (легковые автомобили), Truck (грузовые автомобили) и SpecMachine (спецтехника)

import csv
import os.path


class CarBase:
    def __init__(self, brand, photo_file_name, carrying):
        try:
            if brand != '':
                self.brand = brand
            else:
                raise ValueError
        except:
            raise ValueError
        try:
            if os.path.splitext(photo_file_name)[1] in [".jpg", ".jpeg", ".png", ".gif"]:
                self.photo_file_name = photo_file_name
                #print(self.photo_file_name, os.path.splitext(photo_file_name)[1])
            else:
                raise ValueError
        except:
            raise ValueError
        try:
            self.carrying = float(carrying)
        except:
            raise ValueError
    def get_photo_file_ext(self):
        try:
            photo_extension = os.path.splitext(self.photo_file_name)
        except None:
            photo_extension = None
        return photo_extension[1]


class Car(CarBase):
    car_type='car'
    def __init__(self, brand, photo_file_name, carrying, passenger_seats_count):
        super().__init__(brand, photo_file_name, carrying)
        try:
            self.passenger_seats_count = int(passenger_seats_count)
        except:
            raise ValueError


class Truck(CarBase):
    car_type = 'truck'
    def __init__(self, brand, photo_file_name, carrying, body_whl):
        super().__init__(brand, photo_file_name, carrying)
        try:
            a = str(body_whl).split('x')
            if len(a) == 3:
                self.body_length = float(a[0])
                self.body_width = float(a[1])
                self.body_height = float(a[2])
            else:
                self.body_length = float(0)
                self.body_width = float(0)
                self.body_height = float(0)
        except ValueError:
            self.body_length = float(0)
            self.body_width = float(0)
            self.body_height = float(0)
    def get_body_volume (self):
        volume= self.body_length * self.body_width * self.body_height
        return volume



class SpecMachine(CarBase):
    car_type= 'spec_machine'
    def __init__(self, brand, photo_file_name, carrying, extra):
        super().__init__(brand, photo_file_name, carrying)
        try:
            self.extra = str(extra)
            if self.extra == '':
                raise ValueError
        except:
            raise ValueError
        pass

#p = os.path.splitext('/home/User/Desktop/file.txt')
#print(p[1])

def get_car_list(csv_filename):
    car_list = []
    with open(csv_filename) as csv_fd:
        reader = csv.reader(csv_fd, delimiter=';')  # for str type of reader
        # reader = csv.DictReader(csv_fd, delimiter=';', fieldnames=fieldnames) # for dict type of reader
        next(reader)
        for row in reader:
            try:
                if row == []:
                    continue
                elif row[0] == 'car':
                    a, b, c, d = row[1], row[3], row[5], row[2]
                    car = Car(a, b, c, d)
                    #print(car.__dict__)
                    car_list.append(car)
                elif row[0] == 'truck':
                    a, b, c, d = row[1], row[3], row[5], row[4]
                    truck = Truck(a, b, c, d)
                    #print(truck.__dict__)
                    car_list.append(truck)
                elif row[0] == 'spec_machine':
                    try:
                        a, b, c, d = row[1], row[3], row[5], row[6]
                        spec_machine = SpecMachine(a, b, c, d)
                        #print(spec_machine.__dict__)
                        #print('spec mach', a, b, c, d)
                        car_list.append(spec_machine)
                    except:
                        raise ValueError
                else:
                    raise ValueError
                    #continue
            except ValueError:
                continue
    #print(car_list)
    return car_list


