# -*- encoding: utf-8 -*-


autos = [
            'Toyota',
            'Nissan',
            'Hyundai',
            'Honda',
            'Acura',
            'Alfa',
            'Alpina',
            'Asia',
            'Aston Martin',
            'Audi',
            'BMW',
            'BYD',
            'Bentley',
            'Brilliance',
            'Bugatti',
            'Buick',
            'Cadillac',
            'Changan',
            'Chery',
            'Chevrolet',
            'Chrysler',
            'Citroen',
            'DW Hower',
            'Dacia',
            'Daewoo',
            'Daihatsu',
            'Daimler',
            'Datsun',
            'DeLorean',
            'Derways',
            'Dodge',
            'Dongfeng',
            'Eagle',
            'FAW',
            'Ferrari',
            'Fiat',
            'Fisker',
            'Ford',
            'Foton',
            'GAC',
            'GMC',
            'Geely',
            'Genesis',
            'Geo',
            'Great Wall',
            'Hafei',
            'Haima',
            'Haval',
            'Hawtai',
            'Honda',
            'Hummer',
            'Hyundai',
            'Infiniti',
            'Iran Khodro',
            'Isuzu',
            'JAC',
            'Jaguar',
            'Jeep',
            'Kia',
            'Koenigsegg',
            'Lamborghini',
            'Lancia',
            'Land Rover',
            'Lexus',
            'Lifan',
            'Lincoln',
            'Lotus',
            'Luxgen',
            'Marussia',
            'Maserati',
            'Maybach',
            'Mazda',
            'McLaren',
            'Mercedes',
            'Mercury',
            'Mini',
            'Mitsubishi',
            'Mitsuoka',
            'Nissan',
            'Oldsmobile',
            'Opel',
            'Pagani',
            'Peugeot',
            'Plymouth',
            'Pontiac',
            'Porsche',
            'Proton',
            'Ravon',
            'Renault',
            'Renault',
            'Rolls',
            'Rover',
            'SEAT',
            'Saab',
            'Saturn',
            'Scion',
            'Skoda',
            'Smart',
            'SsangYong',
            'Subaru',
            'Suzuki',
            'Tesla',
            'Tianye',
            'Toyota',
            'Volkswagen',
            'Volvo',
            'Vortex',
            'Wiesmann',
            'Xin',
            'ZX',
            'Zotye',
            'Аурус',
            'ВАЗ',
            'ГАЗ',
            'ЗАЗ',
            'ИЖ',
            'Лада',
            'ЛуАЗ',
            'Москвич',
            'ТагАЗ',
            'УАЗ',
        ]


class Auto(object):
    @staticmethod
    def is_auto(brand):
        for auto in autos:
            if auto.lower() in brand.lower():
                return True

        return False
