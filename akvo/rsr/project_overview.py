# -*- coding: utf-8 -*-

"""Akvo RSR is covered by the GNU Affero General Public License.

See more details in the license.txt file located at the root folder of the
Akvo RSR module. For additional details on the GNU license please
see < http://www.gnu.org/licenses/agpl.html >.
"""

import copy
from collections import OrderedDict
from django.conf import settings
from akvo.rsr.models import IndicatorPeriod, IndicatorPeriodData
from akvo.rsr.models.result.utils import QUALITATIVE, PERCENTAGE_MEASURE, calculate_percentage
from akvo.utils import ensure_decimal, ObjectReaderProxy
from enum import Enum


def is_aggregating_targets(project):
    return project.id in settings.AGGREGATE_TARGETS


def merge_unique(l1, l2):
    out = list(l1)
    for i in l2:
        if i not in out:
            out.append(i)
    return out


def get_periods_with_contributors(root_periods, aggregate_targets=False):
    periods = get_periods_hierarchy_flatlist(root_periods)
    periods_tree = make_object_tree_from_flatlist(periods, 'parent_period')
    project = periods.first().indicator.result.project
    disaggregations = get_disaggregations(project)
    return [PeriodProxy(n['item'], n['children'], aggregate_targets, disaggregations) for n in periods_tree]


def get_disaggregations(project):
    disaggregations = OrderedDict()
    for n in project.dimension_names.all():
        disaggregations[n.name] = OrderedDict()
        for v in n.dimension_values.all():
            disaggregations[n.name][v.value] = None
    return disaggregations


def get_periods_hierarchy_flatlist(root_periods):
    family = {period.id for period in root_periods}
    while True:
        children = set(
            IndicatorPeriod.objects.filter(
                parent_period__in=family
            ).values_list(
                'id', flat=True
            ))
        if family.union(children) == family:
            break

        family = family.union(children)

    return IndicatorPeriod.objects.select_related(
        'indicator__result__project',
        'indicator__result__project__primary_location__country',
        'parent_period',
        'label',
    ).prefetch_related(
        'data',
        'data__user',
        'data__approved_by',
        'data__comments',
        'data__comments__user',
        'data__disaggregations',
        'data__disaggregations__dimension_value',
        'data__disaggregations__dimension_value__name',
        'disaggregation_targets',
        'disaggregation_targets__dimension_value',
        'disaggregation_targets__dimension_value__name'
    ).filter(pk__in=family)


def make_object_tree_from_flatlist(flatlist, parent_attr):
    tree = []
    lookup = {}
    ids = [o.id for o in flatlist]

    for obj in flatlist:
        item_id = obj.id
        if item_id not in lookup:
            lookup[item_id] = {'children': []}
        lookup[item_id]['item'] = obj
        node = lookup[item_id]

        parent_obj = getattr(obj, parent_attr)
        parent_id = parent_obj.id if parent_obj else None
        if not parent_id or parent_id not in ids:
            tree.append(node)
        else:
            if parent_id not in lookup:
                lookup[parent_id] = {'children': []}
            lookup[parent_id]['children'].append(node)

    return tree


class IndicatorType(Enum):
    UNIT = 1
    PERCENTAGE = 2
    NARRATIVE = 3

    @classmethod
    def get_type(cls, indicator):
        if indicator.type == QUALITATIVE:
            return cls.NARRATIVE
        if indicator.measure == PERCENTAGE_MEASURE:
            return cls.PERCENTAGE
        return cls.UNIT


class PeriodProxy(ObjectReaderProxy):
    def __init__(self, period, children=[], aggregate_targets=False, project_disaggregations=None):
        super().__init__(period)
        self.type = IndicatorType.get_type(period.indicator)
        self.aggregate_targets = aggregate_targets
        self._project_disaggregations = project_disaggregations
        self._children = children
        self._project = None
        self._updates = None
        self._actual_comment = None
        self._actual_value = None
        self._actual_numerator = None
        self._actual_denominator = None
        self._target_value = None
        self._contributors = None
        self._countries = None
        self._locations = None
        self._disaggregation_targets = None
        self._disaggregation_contributions = None
        self._disaggregation_contributions_view = None
        self._indicator_target_value = None
        self._use_indicator_target = None

    @property
    def project(self):
        if self._project is None:
            self._project = self._real.indicator.result.project
        return self._project

    @property
    def updates(self):
        if self._updates is None:
            self._updates = UpdateCollection(self._real, self.type)
        return self._updates

    @property
    def contributors(self):
        if self._contributors is None:
            children = self._children if self.project.aggregate_children else []
            self._contributors = ContributorCollection(children, self.type, self._project_disaggregations)
        return self._contributors

    @property
    def target_value(self):
        if self._target_value is None:
            if self.type == IndicatorType.NARRATIVE:
                self._target_value = self._real.target_value
            elif self.aggregate_targets and self.type != IndicatorType.PERCENTAGE:
                self._target_value = _aggregate_period_targets(self._real, self._children)
            else:
                self._target_value = ensure_decimal(self._real.target_value)
        return self._target_value

    @property
    def use_indicator_target(self):
        if self._use_indicator_target is None:
            program = self.project.get_program()
            targets_at = program.targets_at if program else self.targets_at
            self._use_indicator_target = True if targets_at == 'indicator' else False
        return self._use_indicator_target

    @property
    def indicator_target_value(self):
        if self._indicator_target_value is None:
            if not self.use_indicator_target:
                self._indicator_target_value = 0
            elif self.type == IndicatorType.NARRATIVE:
                narrative = self.indicator.target_value
                self._indicator_target_value = narrative if narrative else ''
            elif self.use_indicator_target and self.type != IndicatorType.PERCENTAGE:
                self._indicator_target_value = _aggregate_indicator_targets(self._real, self._children)
            else:
                self._indicator_target_value = ensure_decimal(self.indicator.target_value)
        return self._indicator_target_value

    @property
    def actual_comment(self):
        if self._actual_comment is None:
            self._actual_comment = self._real.actual_comment.split(' | ') \
                if self._real.actual_comment \
                else False
        return self._actual_comment or None

    @property
    def actual_value(self):
        if self._actual_value is None:
            self._actual_value = calculate_percentage(self.actual_numerator, self.actual_denominator) \
                if self.type == IndicatorType.PERCENTAGE \
                else ensure_decimal(self._real.actual_value)
        return self._actual_value

    @property
    def actual_numerator(self):
        if self._actual_numerator is None and self.type == IndicatorType.PERCENTAGE:
            self._actual_numerator = self.updates.total_numerator + self.contributors.total_numerator
        return self._actual_numerator

    @property
    def actual_denominator(self):
        if self._actual_denominator is None and self.type == IndicatorType.PERCENTAGE:
            self._actual_denominator = self.updates.total_denominator + self.contributors.total_denominator
        return self._actual_denominator

    @property
    def countries(self):
        if self._countries is None:
            self._countries = self.contributors.countries
        return self._countries

    @property
    def locations(self):
        if self._locations is None:
            location = self.project.primary_location
            self._locations = merge_unique(self.contributors.locations, [location])
        return self._locations

    @property
    def disaggregation_contributions(self):
        if self._disaggregation_contributions is None:
            self._disaggregation_contributions = self.contributors.disaggregations
        return self._disaggregation_contributions

    @property
    def disaggregation_targets(self):
        if self._disaggregation_targets is None:
            disaggregations = [
                DisaggregationTarget(t)
                for t in self._real.disaggregation_targets.all()
            ]
            self._disaggregation_targets = {(d.category, d.type): d for d in disaggregations}
        return self._disaggregation_targets

    def get_disaggregation_target_of(self, category, type):
        key = (category, type)
        if key not in self.disaggregation_targets:
            return None
        return ensure_decimal(self.disaggregation_targets[key].value)

    @property
    def disaggregation_contributions_view(self):
        if self._disaggregation_contributions_view is None:
            self._disaggregation_contributions_view = copy.deepcopy(self._project_disaggregations)
            for d in self.disaggregation_contributions.values():
                category = d['category']
                type = d['type']
                value = d['value']
                numerator = d['numerator']
                denominator = d['denominator']
                if category not in self._disaggregation_contributions_view or type not in self._disaggregation_contributions_view[category]:
                    continue
                self._disaggregation_contributions_view[category][type] = {
                    'value': value,
                    'numerator': numerator,
                    'denominator': denominator,
                }

        return self._disaggregation_contributions_view

    def get_disaggregation_contribution_of(self, category, type):
        key = (category, type)
        if key not in self.disaggregation_contributions:
            return None
        return self.disaggregation_contributions[key]['value']


class ContributorCollection(object):
    def __init__(self, nodes, type=IndicatorType.UNIT, project_disaggregations=None):
        self.nodes = nodes
        self.type = type
        self._project_disaggregations = project_disaggregations
        self._contributors = None
        self._total_value = None
        self._total_numerator = None
        self._total_denominator = None
        self._countries = None
        self._locations = None
        self._disaggregations = None

    @property
    def total_value(self):
        self._build()
        return self._total_value

    @property
    def total_numerator(self):
        self._build()
        return self._total_numerator

    @property
    def total_denominator(self):
        self._build()
        return self._total_denominator

    @property
    def countries(self):
        self._build()
        return self._countries

    @property
    def locations(self):
        self._build()
        return self._locations

    @property
    def disaggregations(self):
        self._build()
        return self._disaggregations

    def __iter__(self):
        self._build()
        return iter(self._contributors)

    def __len__(self):
        self._build()
        return len(self._contributors)

    def _build(self):
        if self._contributors is not None:
            return

        self._contributors = []
        self._countries = []
        self._locations = []
        self._disaggregations = {}
        if self.type == IndicatorType.PERCENTAGE:
            self._total_numerator = 0
            self._total_denominator = 0
        else:
            self._total_value = 0

        for node in self.nodes:
            contributor = Contributor(node['item'], node['children'], self.type, self._project_disaggregations)

            if not contributor.project.aggregate_to_parent or (
                contributor.actual_value < 1 and len(contributor.updates) < 1
            ):
                continue

            self._contributors.append(contributor)
            self._countries = merge_unique(self._countries, contributor.contributing_countries)
            self._locations = merge_unique(self._locations, contributor.contributing_locations)

            # calculate values
            if self.type == IndicatorType.PERCENTAGE:
                self._total_numerator += contributor.actual_numerator
                self._total_denominator += contributor.actual_denominator
            else:
                self._total_value += contributor.actual_value

            # calculate disaggregations
            for key in contributor.contributors.disaggregations:
                if key not in self._disaggregations:
                    self._disaggregations[key] = contributor.contributors.disaggregations[key].copy()
                else:
                    self._disaggregations[key]['value'] += contributor.contributors.disaggregations[key]['value']
            for key in contributor.updates.disaggregations:
                if key not in self._disaggregations:
                    self._disaggregations[key] = contributor.updates.disaggregations[key].copy()
                else:
                    self._disaggregations[key]['value'] += contributor.updates.disaggregations[key]['value']


class Contributor(object):
    def __init__(self, period, children=[], type=IndicatorType.UNIT, project_disaggregations=None):
        self.period = period
        self.children = children
        self.type = type
        self._project_disaggregations = project_disaggregations
        self._project = None
        self._country = None
        self._actual_value = None
        self._actual_numerator = None
        self._actual_denominator = None
        self._location = None
        self._updates = None
        self._contributors = None
        self._contributing_countries = None
        self._contributing_locations = None
        self._actual_comment = None
        self._target_value = None
        self._disaggregation_targets = None
        self._disaggregations_view = None

    @property
    def project(self):
        if self._project is None:
            self._project = self.period.indicator.result.project
        return self._project

    @property
    def contributors(self):
        if self._contributors is None:
            children = self.children if self.project.aggregate_children else []
            self._contributors = ContributorCollection(children, self.type, self._project_disaggregations)
        return self._contributors

    @property
    def updates(self):
        if self._updates is None:
            self._updates = UpdateCollection(self.period, self.type)
        return self._updates

    @property
    def actual_value(self):
        if self._actual_value is None:
            self._actual_value = calculate_percentage(self.actual_numerator, self.actual_denominator) \
                if self.type == IndicatorType.PERCENTAGE \
                else ensure_decimal(self.period.actual_value)
        return self._actual_value

    @property
    def actual_numerator(self):
        if self._actual_numerator is None and self.type == IndicatorType.PERCENTAGE:
            self._actual_numerator = self.updates.total_numerator + self.contributors.total_numerator
        return self._actual_numerator

    @property
    def actual_denominator(self):
        if self._actual_denominator is None and self.type == IndicatorType.PERCENTAGE:
            self._actual_denominator = self.updates.total_denominator + self.contributors.total_denominator
        return self._actual_denominator

    @property
    def actual_comment(self):
        if self._actual_comment is None:
            self._actual_comment = self.period.actual_comment.split(' | ') \
                if self.period.actual_comment \
                else False
        return self._actual_comment or None

    @property
    def target_value(self):
        if self._target_value is None:
            self._target_value = ensure_decimal(self.period.target_value) \
                if self.type != IndicatorType.NARRATIVE \
                else self.period.target_value
        return self._target_value

    @property
    def disaggregation_targets(self):
        if self._disaggregation_targets is None:
            disaggregations = [
                DisaggregationTarget(t)
                for t in self.period.disaggregation_targets.all()
            ]
            self._disaggregation_targets = {(d.category, d.type): d for d in disaggregations}
        return self._disaggregation_targets

    def get_disaggregation_target_of(self, category, type):
        key = (category, type)
        if key not in self.disaggregation_targets:
            return None
        return ensure_decimal(self.disaggregation_targets[key].value)

    @property
    def country(self):
        if self._country is None:
            self._country = self.location.country if self.location else False
        return self._country or None

    @property
    def contributing_countries(self):
        if self._contributing_countries is None:
            self._contributing_countries = merge_unique(self.contributors.countries, [self.country])
        return self._contributing_countries

    @property
    def location(self):
        if self._location is None:
            self._location = self.project.primary_location or False
        return self._location or None

    @property
    def contributing_locations(self):
        if self._contributing_locations is None:
            self._contributing_locations = merge_unique(self.contributors.locations, [self.location])
        return self._contributing_locations

    @property
    def disaggregations_view(self):
        if self._disaggregations_view is None:
            self._disaggregations_view = copy.deepcopy(self._project_disaggregations)
            for d in self.updates.disaggregations.values():
                category = d['category']
                type = d['type']
                value = d['value']
                numerator = d['numerator']
                denominator = d['denominator']
                if category not in self._disaggregations_view or type not in self._disaggregations_view[category]:
                    continue
                self._disaggregations_view[category][type] = {
                    'value': value,
                    'numerator': numerator,
                    'denominator': denominator,
                }

        return self._disaggregations_view

    def get_disaggregation_of(self, category, type):
        key = (category, type)
        if key not in self.updates.disaggregations:
            return None
        return self.updates.disaggregations[key]['value']


class UpdateCollection(object):
    def __init__(self, period, type):
        self.period = period
        self.type = type
        self._updates = None
        self._total_value = None
        self._total_numerator = None
        self._total_denominator = None
        self._disaggregations = None

    @property
    def total_value(self):
        self._build()
        return self._total_value

    @property
    def total_numerator(self):
        self._build()
        return self._total_numerator

    @property
    def total_denominator(self):
        self._build()
        return self._total_denominator

    @property
    def disaggregations(self):
        self._build()
        return self._disaggregations

    def __iter__(self):
        self._build()
        return iter(self._updates)

    def __len__(self):
        self._build()
        return len(self._updates)

    def _build(self):
        if self._updates is not None:
            return

        self._updates = []
        self._total_value = 0
        if self.type == IndicatorType.PERCENTAGE:
            self._total_numerator = 0
            self._total_denominator = 0
        self._disaggregations = {}

        for update in self.period.data.all():
            self._updates.append(UpdateProxy(update))
            if update.status != IndicatorPeriodData.STATUS_APPROVED_CODE:
                continue
            if self.type == IndicatorType.PERCENTAGE:
                if update.numerator is not None and update.denominator is not None:
                    self._total_numerator += update.numerator
                    self._total_denominator += update.denominator
            elif update.value:
                self._total_value += update.value

            for d in update.disaggregations.all():
                key = (d.dimension_value.name.name, d.dimension_value.value)
                if key not in self._disaggregations:
                    self._disaggregations[key] = {
                        'category': d.dimension_value.name.name,
                        'type': d.dimension_value.value,
                        'value': 0,
                        'numerator': d.numerator,
                        'denominator': d.denominator,
                    }

                self._disaggregations[key]['value'] += ensure_decimal(d.value)

        if self.type == IndicatorType.PERCENTAGE and self._total_denominator > 0:
            self._total_value = calculate_percentage(self._total_numerator, self._total_denominator)


class UpdateProxy(ObjectReaderProxy):
    pass


class DisaggregationTarget(ObjectReaderProxy):
    def __init__(self, target):
        super().__init__(target)
        self._category = None
        self._type = None

    @property
    def category(self):
        if self._category is None:
            self._category = self.dimension_value.name.name
        return self._category

    @property
    def type(self):
        if self._type is None:
            self._type = self.dimension_value.value
        return self._type


def _aggregate_period_targets(period, children):
    aggregate = ensure_decimal(period.target_value)
    for node in children:
        aggregate += _aggregate_period_targets(node['item'], node.get('children', []))
    return aggregate


def _aggregate_indicator_targets(period, children):
    aggregate = ensure_decimal(period.indicator.target_value)
    for node in children:
        aggregate += _aggregate_indicator_targets(node['item'], node.get('children', []))
    return aggregate
