# -*- encoding: utf-8 -*-
import re
from enum import Enum

from lxml import etree


class Country(Enum):
    NOT_DETERMENATED = 0
    BELARUS = 1
    GEORGIA = 2
    KAZAKHSTAN = 3
    LITHUANIA = 4
    PORTUGAL = 5
    RUSSIA = 6
    USA = 7
    UKRAINE = 8

    @classmethod
    def get_country_value_by_name(cls, name):
        name = name.decode('utf-8').lower()

        if u'беларусь' == name:
            return cls.BELARUS.value
        elif u'грузия' == name:
            return cls.GEORGIA.value
        elif u'казахстан' == name:
            return cls.KAZAKHSTAN.value
        elif u'литва' == name:
            return cls.LITHUANIA.value
        elif u'португалия' == name:
            return cls.PORTUGAL.value
        elif u'россия' == name:
            return cls.RUSSIA.value
        elif u'сша' == name:
            return cls.USA.value
        elif u'украина' == name:
            return cls.UKRAINE.value
        else:
            return cls.NOT_DETERMENATED.value


class OwnershipType(Enum):
    NOT_DETERMENATED = 0
    INDIVIDUAL = 1
    TOTAL = 2
    PARTIAL = 3

    @classmethod
    def get_ownership_value_by_name(cls, name):
        if 'индивидуальная' in name:
            return cls.INDIVIDUAL.value
        elif 'совместная' in name:
            return cls.INDIVIDUAL.value
        elif 'долевая' in name:
            return cls.PARTIAL.value
        else:
            return cls.NOT_DETERMENATED.value


class ObjectType(Enum):
    NOT_DETERMENATED = 0
    GARDEN = 1
    NOT_LIVING_HOUSE = 2
    PARTIAL_BUILDING_HOUSE = 3
    CAR_PLACE = 4
    ROOMS = 5
    ROOM = 6
    FLAT = 7
    DIFFERENT_REAL_RSTATE = 8
    GROUNG_PLACE = 9
    LIVING_HOUSE = 10
    LIVING_STROENIE = 11
    LIVING_PLACE = 12
    HOUSE = 13
    HOUSE_DACHA = 14
    PLACE_DACHA = 15
    DACHA = 16
    GARAGE = 17

    @classmethod
    def get_value_by_name(cls, name):
        name = name.decode('utf-8').lower()

        if u'садовый участок' in name:
            return cls.GARDEN.value
        elif u'нежилой дом' in name:
            return cls.NOT_LIVING_HOUSE.value
        elif u'недостроенный дом' in name:
            return cls.PARTIAL_BUILDING_HOUSE.value
        elif u'машино-место' in name:
            return cls.CAR_PLACE.value
        elif u'комнаты' in name:
            return cls.ROOMS.value
        elif u'комната' in name:
            return cls.ROOM.value
        elif u'квартира' in name:
            return cls.FLAT.value
        elif u'иное недвижимое имущество':
            return cls.DIFFERENT_REAL_RSTATE.value
        elif u'земельный участок' in name:
            return cls.GROUNG_PLACE.value
        elif u'жилой дом' in name:
            return cls.LIVING_HOUSE.value
        elif u'жилое строение' in name:
            return cls.LIVING_STROENIE.value
        elif u'жилое помещение' in name:
            return cls.LIVING_PLACE.value
        elif u'дачный дом' in name:
            return cls.HOUSE_DACHA.value
        elif u'дом' in name:
            return cls.HOUSE.value
        elif u'дачное строение' in name:
            return cls.PLACE_DACHA.value
        elif u'дача' in name:
            return cls.DACHA.value
        elif u'гараж' in name:
            return cls.GARAGE.value
        else:
            return cls.NOT_DETERMENATED.value



class RelationType(Enum):
    NOT_DETERMENATED = 0
    HUSBAND = 1
    WIFE = 2
    CHILD = 3

    @classmethod
    def get_value_by_name(cls, name):
        if u'супруга' in name:
            return cls.WIFE.value
        elif u'супруг' in name:
            return cls.HUSBAND.value
        elif u'ребенок' in name:
            return cls.CHILD.value
        else:
            return None
            # cls.NOT_DETERMENATED.value


class DeklaratorXML(object):
    def __init__(self):
        self.result = self.create_init_element()
        self._id = None

    def create_init_element(self):
        return etree.Element('persons', attrib={
            etree.QName("http://www.w3.org/2001/XMLSchema-instance",
                        "noNamespaceSchemaLocation"): 'declarationXMLtemplate_Schema _transport_merged.xsd',
        })

    def add_info(self, persons):
        self._id = 0
        for idx, person in enumerate(persons):
            person = self._add_person(person, idx + 1)
            self.result.append(person)

    def _add_person(self, person, person_id_value):
        person_tag = etree.Element('person')

        name = self.create_tag_with_text('name', person.name)

        if person.position:
            position = self.create_tag_with_text('position', person.position)
        else:
            position = self.create_tag_with_nil('position')

        if person.salary is not None:
            income = self.create_tag_with_text('income', person.salary)
        else:
            income = self.create_tag_with_text('income', '')

        income_comment = self.create_tag_with_nil('incomeComment')

        income_source = self.create_tag_with_nil('incomeSource')

        relation_type = RelationType.get_value_by_name(name.text)
        if relation_type is None:
            relative_type = self.create_tag_with_nil('relationType')
            relative_of = self.create_tag_with_nil('relativeOf')
            self._id = person_id_value
        else:
            name = self.create_tag_with_nil('name')
            relative_type = self.create_tag_with_text('relationType', relation_type)
            relative_of = self.create_tag_with_text('relativeOf', self._id)

        person_id = self.create_tag_with_text('id', person_id_value)
        # person_id = etree.Element('id')
        # person_id.text = unicode(str(person_id_value), "utf-8")

        if person.objects_owner is [] and person.objects_not_owner is None:
            realties_tags = self.create_tag_with_nil('realties')
            # realties_tags = etree.Element('realties', attrib={
            #     etree.QName("http://www.w3.org/2001/XMLSchema-instance", "nil"): 'true',
            # })
        else:
            realties_tags = etree.Element('realties')
            self.get_realties(realties_tags, person.objects_owner, 1)
            self.get_realties(realties_tags, person.objects_not_owner, 2)

        person_tag.append(person_id)
        person_tag.append(name)
        person_tag.append(position)
        person_tag.append(income)
        person_tag.append(income_comment)
        person_tag.append(income_source)
        person_tag.append(relative_of)
        person_tag.append(relative_type)
        person_tag.append(realties_tags)

        return person_tag

    def get_realties(self, realties_tags, realties, realty_type):
        for realty in realties:
            realty_tag = etree.Element('realty')
            realty_type_tag = self.create_tag_with_text('realtyType', realty_type)
            # realty_type_tag = etree.Element('realtyType')
            # realty_type_tag.text = unicode(str(realty_type), "utf-8")

            realty_name_tag = self.create_tag_with_text('RealtyName', realty[0])
            # realty_name_tag = etree.Element('RealtyName')
            # realty_name_tag.text = unicode(str(realty[0]), "utf-8")

            if realty_type == 1:
                ownership_type = OwnershipType.get_ownership_value_by_name(realty[0])
                ownership_type_tag = self.create_tag_with_text('ownershipType', ownership_type)
                # ownership_type_tag = etree.Element('ownershipType')
                # ownership_type_tag.text = unicode(str(ownership_type), "utf-8")

                if ownership_type == OwnershipType.PARTIAL.value:
                    # ownership_part_tag = etree.Element('ownershipPart')
                    one, two = re.search(r'[0-9]+/[0-9]+$', realty[0]).group(0).split('/')
                    ownership_part = float(one) / float(two)
                    # ownership_part_tag.text = unicode(str(ownership_part), "utf-8")
                    ownership_part_tag = self.create_tag_with_text('ownershipPart', ownership_part)
                else:
                    ownership_part_tag = self.create_tag_with_nil('ownershipPart')
                    # ownership_part_tag = etree.Element('ownershipPart', attrib={
                    #     etree.QName("http://www.w3.org/2001/XMLSchema-instance", "nil"): 'true',
                    # })
                realty_tag.append(ownership_type_tag)
                realty_tag.append(ownership_part_tag)

            realty_object_tag = self.create_tag_with_text('objectType', ObjectType.get_value_by_name(realty[0]))
            # realty_object_tag = etree.Element('objectType')
            # realty_object_tag.text = unicode(str(ObjectType.get_value_by_name(realty[0])), "utf-8")

            square_tag = self.create_tag_with_text('square', realty[1])
            # square_tag = etree.Element('square')
            # square_tag.text = unicode(str(realty[1]), "utf-8")

            country_value = Country.get_country_value_by_name(realty[2])
            country_tag = self.create_tag_with_text('country', country_value)
            # country_tag = etree.Element('country')
            # country_value = Country.get_country_value_by_name(realty[2])
            # country_tag.text = unicode(str(country_value), "utf-8")

            realty_tag.append(realty_name_tag)
            realty_tag.append(realty_type_tag)
            realty_tag.append(realty_object_tag)
            realty_tag.append(square_tag)
            realty_tag.append(country_tag)

            realties_tags.append(realty_tag)
        return realties_tags

    def get_xml(self):
        return etree.tostring(self.result, pretty_print=True, xml_declaration=True, encoding='utf-8')

    def create_tag_with_text(self, name, text):
        tag = etree.Element(name)
        tag.text = unicode(str(text), "utf-8")
        return tag

    def create_tag_with_nil(self, name):
        tag = etree.Element(name, attrib={
            etree.QName("http://www.w3.org/2001/XMLSchema-instance", "nil"): 'true',
        })
        return tag

if __name__ == '__main__':
    # create XML
    # root = etree.Element('root')

    persons = etree.Element('persons', attrib={
        etree.QName("http://www.w3.org/2001/XMLSchema-instance",
                    "noNamespaceSchemaLocation"): 'declarationXMLtemplate_Schema _transport_merged.xsd',
    })

    person = etree.Element('person')

    person_id = etree.Element('id')
    person_id.text = '1'

    person_name = etree.Element('name')
    person_name.text = '1'

    person_name = etree.Element('name')
    person_name.text = '1'

    person.append(person_id)
    persons.append(person)

    s = etree.tostring(persons, pretty_print=True, xml_declaration=True, encoding='utf-8')
    print(s)
