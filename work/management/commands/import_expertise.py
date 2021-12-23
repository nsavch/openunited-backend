# -*- coding: utf-8 -*-
import os
import json
import csv
from django.core.management import BaseCommand

from work.models import *


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def save_expertise(self, category, name, selectable, parent):
        exp = Expertise()
        exp.category = category
        exp.name = name
        exp.selectable = selectable
        exp.parent = parent
        exp.save()

        return exp

    def handle(self, *args, **options):
        # only import if we do not have any data
        if not Expertise.objects.count():
            with open('work/management/commands/data/ou-task-category-and-expertise.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                for row in csv_reader:
                    if line_count > 0:
                        cat_id = row[0]
                        cat_parent = row[1]
                        cat_name = row[4]
                        expertise = row[5]

                        if len(expertise) > 0:
                            print('Category: %s' % cat_id)

                            expertise = json.loads(expertise)
                            category = TaskCategory.objects.get(id=cat_id)

                            for key in expertise.keys():
                                print('Expertise root:', key)

                                exp = self.save_expertise(
                                    category, key, 0, None)

                                if type(expertise[key]) == list:
                                    for val in expertise[key]:
                                        print('Child:', val)
                                        child_exp = self.save_expertise(
                                            category, val, 1, exp)
                                else:
                                    print('Child: ', expertise[key])
                                    child_exp = self.save_expertise(
                                        category, expertise[key], 1, exp)

                    line_count += 1
