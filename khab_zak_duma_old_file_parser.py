# -*- encoding: utf-8 -*-
import pprint
import re

import docx
import nltk
import pymorphy2

from deklarator import DeklaratorXML
from main import Depute

def replace_text(text):
    if 'земельным участком' in text:
        text = text.replace('земельным участком', 'земельный участок')
    elif 'водным транспортом' in text:
        text = text.replace('водным транспортом', 'водный транспорт')
    elif 'нежилым помещением' in text:
        text = text.replace('нежилым помещением', 'нежилое помещение')
    elif 'стояночным местом' in text:
        text = text.replace('стояночным местом', 'стояночное место')
    elif 'квартирой' in text:
        text = text.replace('квартирой', 'квартира')
    elif 'грузовым автомобилем' in text:
        text = text.replace('грузовым автомобилем', 'грузовой автомобиль')
    elif 'легковыми автомобилями' in text:
        text = text.replace('легковыми автомобилями', 'легковой автомобиль')
    elif 'легковым автомобилем' in text:
        text = text.replace('легковым автомобилем', 'легковой автомобиль')
    elif 'помещением' in text:
        text = text.replace('помещением', 'помещение')
    elif 'гаражом' in text:
        text = text.replace('гаражом', 'гараж')
    elif 'жилым домом' in text:
        text = text.replace('жилым домом', 'жилой дом')
    elif 'дачей' in text:
        text = text.replace('дачей', 'дача')
    elif 'парковочным местом' in text:
        text = text.replace('парковочным местом', 'парковочное место')
    elif 'строением' in text:
        text = text.replace('строением', 'строение')
    return text
    
if __name__ == '__main__':
    filename = '2010_Deputaty.docx'
    filename = '2010_Sotrudniki_apparata.docx'
    output_filename = '%s.xml' % filename.split('.')[0].lower()
    doc = docx.Document(filename)

    deputes = []
    depute = None

    t = set()
    morph = pymorphy2.MorphAnalyzer()

    status_owner = None
    for para in doc.paragraphs[1:]:
        text = para.text.encode('utf-8')


        if text != '':
            if 'Законодательной Думы' in text:
                if depute is not None:
                    deputes.append(depute)

                depute = Depute()

                status_owner = None
                name, position = text.replace('  ', ' ').split('–')

                name = name.strip()

                if position[0] == ' ':
                    position = position[1:]

                position = position.strip()

                depute.set_name(name)
                depute.position = position
                print(name)
            elif 'упруг' in text or 'есовершен' in text:
                if depute is not None:
                    deputes.append(depute)
                depute = Depute()
                name = text.replace(':', '').strip()
                depute.set_name(name)
                # depute.position = None
                print name
            elif 'сумма дохода' in text:
                text = text.replace(' ', '').split('–')[1]
                salary = re.search(r'[0-9]+', text).group(0)
                depute.set_salary(salary)
            elif 'аходится в пользовании' in text:
                status_owner = False
            elif 'ладеет' in text.lower():
                status_owner = True
            else:
                # print(text.split(' –')[0])
                try:
                    print text
                    owner_type, value = text.split(' – ')
                except:
                    owner_type, value = text, 0.0

                t.add(text.split(' –')[0])
                if status_owner is True:
                    owner_type = replace_text(owner_type)

                    if 'грузовой автомобиль' in owner_type or 'водный транспорт' in owner_type or \
                        'легковой автомобиль' in owner_type:
                        print owner_type, "|" ,value
                        value = value.replace(',', ';').replace('\xc2\xab', '').replace('\xc2\xbb', '')
                        autos = value.split(';')

                        [depute.machines.append('%s %s' % (owner_type, auto)) for auto in autos if auto != '']
                        # print depute.machines
                    else:
                        print value
                        if not isinstance(value, float):
                            value = value.replace(' ', '').replace(' ', '').replace(',', '.')
                            try:
                                value = re.search('[0-9]+.[0-9]+', value).group()
                            except:
                                value = re.search('[0-9]+', value).group() + '.0'
                            print float(value)
                        depute.set_object_owner(owner_type, str(value), owner_type)
                        # country_name = re.search(r'\([А-Яа-я]+\)', owner_type).group(0).replace('(', '').replace(')', '')
                        # print country_name
                        # try:
                        #     pass
                        # except:
                        #     print owner_type
                elif status_owner is False:
                    if not isinstance(value, float):
                        value = value.replace(' ', '').replace(' ', '').replace(',', '.')
                        try:
                            value = re.search('[0-9]+.[0-9]+', value).group()
                        except:
                            value = re.search('[0-9]+', value).group() + '.0'
                        print float(value)
                    depute.set_object_not_owner(owner_type, str(value), owner_type)

    deklarator = DeklaratorXML()

    deklarator.add_info(deputes)

    # with open('2015_sotrudniki_apparata.xml', 'wb') as f:
    # with open('2015_deputaty.xml', 'wb') as f:
    # with open('2015_sotrudniki_apparata.xml', 'wb') as f:
    with open(output_filename, 'wb') as f:
        f.write(deklarator.get_xml())