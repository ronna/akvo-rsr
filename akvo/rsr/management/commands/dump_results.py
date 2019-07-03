# -*- coding: utf-8 -*-

# Akvo Reporting is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

"""Dump the results framework of the specified projects

Usage:

    python manage.py dump_results <project-id1> [<project-id2> ...]


See load_results.py to load this dump

"""

from django.core.management.base import BaseCommand
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from akvo.rsr.models import Result, Project, IndicatorDimensionName


class Command(BaseCommand):
    help = u"Dump the results framework for the specified projects"

    def add_arguments(self, parser):
        parser.add_argument(
            action='store',
            dest='project_id',
            help=('Project ID whose results framework to dump.'
                  '- if dumping a results hierarchy, use ID of the parent project')
        )

    def handle(self, *args, **options):
        project_id = options['project_id']
        project = Project.objects.get(id=project_id)
        results = Result.objects.filter(project=project)
        data = self._get_related_objects(results)
        descendants = project.descendants(depth=1)
        indicator_dimension_names = IndicatorDimensionName.objects.filter(project__in=descendants)
        data = self._get_related_objects(indicator_dimension_names, data)
        path = 'results-data-{}-and-children.json'.format(project_id)
        with open(path, 'w') as f:
            f.write(DjangoJSONEncoder(indent=2).encode(data))
        children = ','.join(str(pid) for pid in project.children_all().values_list('id', flat=True))
        print('To restore the dump run the following command:')
        print('python manage.py load_results {pid} {path} {children}'.format(
            pid=project_id, path=path, children=children))

    def _get_related_objects(self, qs, data=None):
        qs_serialized = serializers.serialize("python", qs)
        if data is None:
            data = qs_serialized
        else:
            data.extend(qs_serialized)

        related_fields = qs.model._meta._get_fields(forward=False, include_hidden=True)
        related_names_models = {
            related_obj.get_accessor_name(): (related_obj.field.name, related_obj.field.model)
            for related_obj in related_fields
        }
        for _, (name, model) in related_names_models.items():
            query = {'{}__in'.format(name): qs}
            related_qs = model.objects.filter(**query)
            if related_qs.exists():
                self._get_related_objects(related_qs, data)

        return data
