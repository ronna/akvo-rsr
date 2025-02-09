# -*- coding: utf-8 -*-

# Akvo Reporting is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from datetime import date
from akvo.rsr.tests.base import BaseTestCase
from akvo.rsr.tests.utils import ProjectFixtureBuilder
from akvo.rsr.usecases import remove_project_parent as command


class ChangeProjectParentTestCase(BaseTestCase):

    def test_remove_parent(self):
        # Given
        root = ProjectFixtureBuilder()\
            .with_title('Parent project')\
            .with_disaggregations({'Foo': ['Bar']})\
            .with_results([{
                'title': 'Result #1',
                'indicators': [{
                    'title': 'Indicator #1',
                    'periods': [{
                        'period_start': date(2020, 1, 1),
                        'period_end': date(2020, 12, 31),
                    }]
                }]
            }])\
            .with_contributors([
                {'title': 'Child project'},
                {'title': 'New project'}
            ])\
            .build()
        child_project = root.get_contributor(title='Child project')
        # When
        command.remove_parent(child_project.object)
        # Then
        self.assertIsNone(child_project.object.parents_all().first())

        self.assertIsNone(
            child_project.results.get(title='Result #1').parent_result
        )
        self.assertIsNone(
            child_project.indicators.get(title='Indicator #1').parent_indicator
        )
        self.assertIsNone(
            child_project.periods.get(period_start=date(2020, 1, 1)).parent_period
        )
        self.assertIsNone(
            child_project.object.dimension_names.get(name='Foo').parent_dimension_name
        )
        self.assertIsNone(
            child_project.get_disaggregation('Foo', 'Bar').parent_dimension_value
        )
