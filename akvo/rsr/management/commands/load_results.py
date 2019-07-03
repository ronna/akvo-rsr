# -*- coding: utf-8 -*-

# Akvo Reporting is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

"""Restore the results framework from a dump created by dump_results.py

Usage:

    python manage.py load_results <path>

"""

from collections import defaultdict
import json

from django.apps import apps
from django.core.management.base import BaseCommand

from akvo.rsr.models import Result, Project, IndicatorDimensionName, RelatedProject


class Command(BaseCommand):
    help = u"Dump the results framework for the specified projects"

    def add_arguments(self, parser):
        parser.add_argument(
            action='store',
            dest='project_id',
            help=('Project ID of the parent project whose results framework is being loaded.')
        )
        parser.add_argument(
            action='store',
            dest='path',
            help=('Path to a dump created by dump_results command')
        )
        parser.add_argument(
            action='store',
            dest='children',
            help=('Projects which are children of this project')
        )

    def handle(self, *args, **options):
        path = options['path']
        project_id = options['project_id']
        children_ids = [int(child_id) for child_id in options['children'].split(',')]
        with open(path) as f:
            data = json.load(f)

        root_project = Project.objects.get(id=project_id)
        hierarchy_projects = root_project.descendants(depth=1)
        project_children = set(root_project.children_all().values_list('id', flat=True))

        for child_id in children_ids:
            if child_id not in project_children:
                RelatedProject.objects.create(
                    project_id=child_id, related_project=root_project,
                    relation=RelatedProject.PROJECT_RELATION_PARENT)

        # Delete all the existing results framework.
        Result.objects.filter(project__in=hierarchy_projects).delete()
        # Delete all existing indicator dimension names.
        IndicatorDimensionName.objects.filter(project__in=hierarchy_projects).delete()
        # Import results on the root project
        root_project.import_results()
        for project in hierarchy_projects:
            project.import_results()

        grouped_data = self._group_by_model(data)
        project_ids = self._get_project_ids(grouped_data)
        for pid in project_ids:
            # Assert that all the projects still exist.
            Project.objects.get(id=pid)

        self.id_map = id_map = defaultdict(dict)

        for key in ('rsr.result', 'rsr.indicator', 'rsr.indicatorperiod', 'rsr.indicatorperioddata',
                    'rsr.indicatorperioddatacomment', 'rsr.indicatordimensionname', 'rsr.indicatordimensionvalue',
                    'rsr.indicator_dimension_names', 'rsr.disaggregation'):
            objects = sorted(grouped_data[key], key=lambda x: x['pk'])
            model = apps.get_model(*key.split('.'))
            print(key, len(objects))
            for old_object in objects:
                fields = old_object['fields']
                current_object = self._get_current_object(key, model, fields)
                id_map[key][old_object['pk']] = current_object.id

    def _get_current_object(self, key, model, fields):
        fields = self._replace_with_new_ids(fields)
        if key == 'rsr.result':
            current_object = model.objects.get(
                parent_result_id=fields['parent_result'], project_id=fields['project'])

        elif key == 'rsr.indicator':
            parent_indicator_id = fields.pop('parent_indicator')
            result_id = fields.pop('result')
            # FIXME: Need to do something with this...
            dimension_names = fields.pop('dimension_names')
            current_object, created = model.objects.get_or_create(
                parent_indicator_id=parent_indicator_id, result_id=result_id, defaults=fields)
            if created:
                assert parent_indicator_id is None

        elif key == 'rsr.indicatorperiod':
            parent_period_id = fields.pop('parent_period')
            indicator_id = fields.pop('indicator')
            current_object, created = model.objects.get_or_create(
                parent_period_id=parent_period_id, indicator_id=indicator_id, defaults=fields)
            if created:
                assert parent_period_id is None

        elif key == 'rsr.indicatorperioddata':
            period_id = fields.pop('period')
            user_id = fields.pop('user')
            approved_by_id = fields.pop('approved_by')
            current_object = model.objects.create(
                period_id=period_id, user_id=user_id, approved_by_id=approved_by_id, **fields)

        elif key == 'rsr.indicatorperioddatacomment':
            user_id = fields.pop('user')
            data_id = fields.pop('data')
            current_object = model.objects.create(data_id=data_id, user_id=user_id, **fields)

        elif key == 'rsr.indicatordimensionname':
            project_id = fields.pop('project')
            current_object, created = model.objects.get_or_create(
                project_id=project_id, **fields)
            if created:
                assert fields['parent_dimension_name'] is None

        elif key == 'rsr.indicatordimensionvalue':
            name_id = fields.pop('name')
            current_object, created = model.objects.get_or_create(
                name_id=name_id, **fields)
            if created:
                assert fields['parent_dimension_value'] is None

        elif key == 'rsr.indicator_dimension_names':
            indicatordimensionname_id = fields['indicatordimensionname']
            indicator_id = fields['indicator']
            current_object, _ = model.objects.get_or_create(
                indicator_id=indicator_id, indicatordimensionname_id=indicatordimensionname_id)

        elif key == 'rsr.disaggregation':
            dimension_value_id = fields.pop('dimension_value')
            update_id = fields.pop('update')
            current_object, _ = model.objects.get_or_create(
                update_id=update_id, dimension_value_id=dimension_value_id, **fields)

        return current_object

    def _replace_with_new_ids(self, fields):
        FIELDS = {
            # result
            'parent_result',
            # indicator
            'result', 'parent_indicator',
            # indicatorperiod
            'indicator', 'parent_period',
            # indicatorperioddata
            'period',
            # indicatorperioddatacomment
            'data',
            # indicatordimensionvalue
            'name',
            # indicator_dimension_names
            'indicatordimensionname',
            # disaggregation
            'update', 'dimension_value',
        }
        new_fields = dict()
        for key, value in fields.items():
            if key not in FIELDS:
                new_fields[key] = value
            else:
                name = key.split('_', 1)[-1] if key.startswith('parent_') else key
                if name == 'period':
                    name = 'indicatorperiod'
                elif name == 'data':
                    name = 'indicatorperioddata'
                elif name == 'name':
                    name = 'indicatordimensionname'
                elif name == 'update':
                    name = 'indicatorperioddata'
                elif name == 'dimension_value':
                    name = 'indicatordimensionvalue'
                model_name = 'rsr.{}'.format(name)
                new_value = self.id_map[model_name].get(value, value)
                new_fields[key] = new_value

        return new_fields

    def _group_by_model(self, data):
        grouped_by_model = defaultdict(list)
        for element in data:
            grouped_by_model[element['model']].append(element)

        return grouped_by_model

    def _get_project_ids(self, data):
        results = data['rsr.result']
        return sorted({result['fields']['project'] for result in results})
