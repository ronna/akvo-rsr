# -*- coding: utf-8 -*-

"""Akvo RSR is covered by the GNU Affero General Public License.

See more details in the license.txt file located at the root folder of the
Akvo RSR module. For additional details on the GNU license please
see < http://www.gnu.org/licenses/agpl.html >.
"""

from akvo.rsr.models import IndicatorPeriod, ProjectHierarchy, Result
from akvo.rsr.models.result.utils import PERCENTAGE_MEASURE
from akvo.rsr.decorators import with_download_indicator
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404
from pyexcelerate import Workbook, Style, Font, Color, Fill, Alignment
from pyexcelerate.Borders import Borders
from pyexcelerate.Border import Border

from . import utils


def build_view_object(organisation, result_id):
    project_ids = organisation.all_projects()\
        .annotate(results_count=Count('results'))\
        .filter(results_count__gt=0)\
        .values_list('pk', flat=True)

    filter_q = dict(indicator__result__project__in=project_ids)
    if result_id is not None:
        results = Result.objects.get(id=result_id).descendants()
        filter_q['indicator__result__in'] = results

    periods = IndicatorPeriod.objects\
        .select_related('indicator', 'indicator__result', 'indicator__result__project')\
        .filter(**filter_q)\
        .exclude(indicator__result__type__iexact='')\
        .order_by('indicator__result__project__iati_activity_id')

    return utils.make_project_proxies(periods)


@login_required
@with_download_indicator
def render_report(request, program_id, result_id=None):
    project_hierarchy = get_object_or_404(ProjectHierarchy, root_project=program_id)
    organisation = project_hierarchy.organisation
    projects = build_view_object(organisation, result_id=result_id)

    wb = Workbook()
    ws = wb.new_sheet('ProjectList')
    ws.set_col_style(1, Style(size=81.5))
    ws.set_col_style(2, Style(size=33.5))
    ws.set_col_style(3, Style(size=7.67))
    ws.set_col_style(4, Style(size=21.17))
    ws.set_col_style(5, Style(size=20.67))
    ws.set_col_style(6, Style(size=19))
    ws.set_col_style(7, Style(size=18.17))
    ws.set_col_style(8, Style(size=33.5))
    ws.set_col_style(9, Style(size=21))
    ws.set_col_style(10, Style(size=14.83))
    ws.set_col_style(11, Style(size=33.5))
    ws.set_col_style(12, Style(size=23.17))
    ws.set_col_style(13, Style(size=10.5))
    ws.set_col_style(14, Style(size=14))
    ws.set_col_style(15, Style(size=16.67))
    ws.set_col_style(16, Style(size=19.5))
    ws.set_col_style(17, Style(size=34.33))
    ws.set_col_style(18, Style(size=15.67))
    ws.set_col_style(19, Style(size=15.67))
    ws.set_col_style(20, Style(size=22.33))
    ws.set_col_style(21, Style(size=25))
    ws.set_col_style(22, Style(size=17.5))
    ws.set_col_style(23, Style(size=20.83))
    ws.set_col_style(24, Style(size=9.67))
    ws.set_col_style(25, Style(size=12.5))
    ws.set_col_style(26, Style(size=26.67))
    ws.set_col_style(27, Style(size=16.33))
    ws.set_col_style(28, Style(size=16.33))
    ws.set_col_style(29, Style(size=16.33))
    ws.set_col_style(30, Style(size=16.33))

    # r1
    ws.set_cell_style(1, 1, Style(
        font=Font(bold=True, size=18, color=Color(255, 255, 255)),
        fill=Fill(background=Color(32, 56, 100))
    ))
    ws.set_cell_value(1, 1, 'Organisation Results and Indicators simple table report')

    # r3
    for col in range(1, 31):
        ws.set_cell_style(3, col, Style(
            font=Font(bold=True, size=14),
            fill=Fill(background=Color(255, 192, 0)),
            alignment=Alignment(horizontal='center'),
            borders=Borders(bottom=Border(color=Color(0, 0, 0)))
        ))
    ws.set_cell_value(3, 1, 'Project name')
    ws.set_cell_value(3, 2, 'Subtitle')
    ws.set_cell_value(3, 3, 'IATI id')
    ws.set_cell_value(3, 4, 'Date start planned')
    ws.set_cell_value(3, 5, 'Date end planned')
    ws.set_cell_value(3, 6, 'Date start actual')
    ws.set_cell_value(3, 7, 'Date end actual')
    ws.set_cell_value(3, 8, 'Result title')
    ws.set_cell_value(3, 9, 'Result description')
    ws.set_cell_value(3, 10, 'Aggregation')
    ws.set_cell_value(3, 11, 'Indicator title')
    ws.set_cell_value(3, 12, 'Indicator description')
    ws.set_cell_value(3, 13, 'Measure')
    ws.set_cell_value(3, 14, 'Ascending')
    ws.set_cell_value(3, 15, 'Baseline year')
    ws.set_cell_value(3, 16, 'Baseline value')
    ws.set_cell_value(3, 17, 'Baseline comment')
    ws.set_cell_value(3, 18, 'Period start')
    ws.set_cell_value(3, 19, 'Period end')
    ws.set_cell_value(3, 20, 'Target value')
    ws.set_cell_value(3, 21, 'Target comment')
    ws.set_cell_value(3, 22, 'Actual value')
    ws.set_cell_value(3, 23, 'Actual comment')
    ws.set_cell_value(3, 24, 'Country')
    ws.set_cell_value(3, 25, 'Type')
    ws.set_cell_value(3, 26, 'Related partners')
    ws.set_cell_value(3, 27, 'Project id')
    ws.set_cell_value(3, 28, 'Result id')
    ws.set_cell_value(3, 29, 'Indicator id')
    ws.set_cell_value(3, 30, 'Period id')

    wrap_text = [2, 8, 9, 11, 12, 17, 21, 23]
    row = 4
    for project in projects:
        highlight = True
        for result in project.results:
            for indicator in result.indicators:
                for period in indicator.periods:
                    for col in range(1, 31):
                        ws.set_cell_style(row, col, Style(
                            alignment=Alignment(wrap_text=True) if col in wrap_text else None,
                            fill=Fill(background=Color(223, 231, 244)) if highlight else None
                        ))
                    # The empty strings are sort of a hack because the style formatting
                    # are not applied on a cell with empty content.
                    ws.set_cell_value(row, 1, project.title or ' ')
                    ws.set_cell_value(row, 2, project.subtitle or ' ')
                    ws.set_cell_value(row, 3, project.iati_activity_id or ' ')
                    ws.set_cell_value(row, 4, project.date_start_planned or ' ')
                    ws.set_cell_value(row, 5, project.date_end_planned or ' ')
                    ws.set_cell_value(row, 6, project.date_start_actual or ' ')
                    ws.set_cell_value(row, 7, project.date_end_planned or ' ')
                    ws.set_cell_value(row, 8, result.title or ' ')
                    ws.set_cell_value(row, 9, result.description or ' ')
                    ws.set_cell_value(row, 10, 'Yes' if result.aggregation_status else 'No')
                    ws.set_cell_value(row, 11, indicator.title or ' ')
                    ws.set_cell_value(row, 12, indicator.description or ' ')
                    ws.set_cell_value(row, 13, 'Percentage' if indicator.measure == PERCENTAGE_MEASURE else 'Unit')
                    ws.set_cell_value(row, 14, 'Yes' if indicator.ascending else 'No')
                    ws.set_cell_value(row, 15, indicator.baseline_year or ' ')
                    ws.set_cell_value(row, 16, indicator.baseline_value or ' ')
                    ws.set_cell_value(row, 17, indicator.baseline_comment or ' ')
                    ws.set_cell_value(row, 18, utils.get_period_start(period, project.in_eutf_hierarchy) or ' ')
                    ws.set_cell_value(row, 19, utils.get_period_end(period, project.in_eutf_hierarchy) or ' ')
                    ws.set_cell_value(row, 20, period.target_value or ' ')
                    ws.set_cell_value(row, 21, period.target_comment or ' ')
                    ws.set_cell_value(row, 22, period.actual_value or ' ')
                    ws.set_cell_value(row, 23, period.actual_comment or ' ')
                    ws.set_cell_value(row, 24, project.country_codes or ' ')
                    ws.set_cell_value(row, 25, result.iati_type_name or ' ')
                    ws.set_cell_value(row, 26, project.partner_names or ' ')
                    ws.set_cell_value(row, 27, project.id)
                    ws.set_cell_value(row, 28, result.id)
                    ws.set_cell_value(row, 29, indicator.id)
                    ws.set_cell_value(row, 30, period.id)
                    row += 1
                    highlight = False

    filename = '{}-{}-eutf-results-and-indicators-simple-table.xlsx'.format(
        datetime.now().strftime('%Y%m%d'), organisation.id)

    return utils.make_excel_response(wb, filename)
