# -*- encoding: utf-8 -*-
import docx

from deklarator import DeklaratorXML


class Depute(object):
    def __init__(self):
        self.name = None
        self.position = None
        self.salary = None
        self.objects_owner = []
        self.objects_not_owner = []
        self.machines = []
        self._machines_list = []

    def set_name(self, name):
        self.name = name

    def set_salary(self, salary):
        salary = self.clear_number(salary)

        if salary != '':
            self.salary = float(salary)

    def set_object_owner(self, object_type, object_size, country):
        object_list = [object_type, self.clear_number(object_size), country]
        if object_list != ['', '', ''] and object_list not in self.objects_owner:
            self.objects_owner.append(object_list)

    def set_object_not_owner(self, object_type, object_size, country):
        object_list = [object_type, self.clear_number(object_size), country]
        if object_list != ['', '', ''] and object_list not in self.objects_not_owner:
            self.objects_not_owner.append(object_list)

    def set_machine(self, machine):
        if machine != '' and machine not in self._machines_list:
            self._machines_list.append(machine)
            type_machine = ''
            for machine in machine.split(';'):
                if ':' in machine:
                    type_machine = machine.split(':')[0]

                    if 'автомобили легковые' in type_machine:
                        type_machine = 'а/м легковой'
                    elif 'автомобили грузовые' in type_machine:
                        type_machine = 'а/м грузовой'
                    elif 'моторные лодки' in type_machine:
                        type_machine = 'Моторная лодка'
                    elif 'иные транспортные средства' in type_machine:
                        type_machine = type_machine.replace('иные транспортные средства ', '')
                    machine = machine.split(':')[1]

                if machine != '':
                    self.machines.append(('%s %s' % (type_machine, machine)).strip())

    def clear_number(self, number):
        return number.replace(' ', '').replace(' ', '').replace(',', '.')

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


if __name__ == '__main__':
    doc = docx.Document('2017_Deputaty.docx')

    deputies = []

    for i, row in enumerate(doc.tables[1].rows[1:]):
        data = [cell.text.encode('utf-8').replace('\n', ' ').replace('  ', ' ').rstrip() for cell in row.cells]
        if len(deputies) > 0 and data[0] == deputies[-1].name or data[0] == '':
            depute = deputies[-1]
        else:
            depute = Depute()
            depute.set_name(data[0])
            depute.position = data[1]
            depute.set_salary(data[2])
            deputies.append(depute)

        depute.set_object_owner(data[3], data[4], data[5])
        depute.set_object_not_owner(data[6], data[7], data[8])
        depute.set_machine(data[9])

    deklarator = DeklaratorXML()

    deklarator.add_info(deputies)

    with open('2017_deputaty.xml', 'wb') as f:
        f.write(deklarator.get_xml())
