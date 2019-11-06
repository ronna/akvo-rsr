# -*- coding: utf-8 -*-

"""Akvo RSR is covered by the GNU Affero General Public License.

See more details in the license.txt file located at the root folder of the
Akvo RSR module. For additional details on the GNU license please
see < http://www.gnu.org/licenses/agpl.html >.
"""

import pdfkit
import io
import requests

from decimal import Decimal, InvalidOperation, DivisionByZero
from akvo.rsr.models import Project, IndicatorPeriodData
from akvo.rsr.docx_util import markdown_to_docx
from datetime import date
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from django.conf import settings


@login_required
def render_pdf(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related(
            'partners',
            'related_projects',
            'related_to_projects',
            'results',
            'project_updates'
        ),
        pk=project_id
    )
    html = render_to_string('reports/project.html', {'project': project})

    if request.GET.get('show-html', ''):
        response = HttpResponse(html)
    else:
        options = {
            'page-size': 'A4',
            'orientation': 'Portrait',
            'margin-left': '0.28in',
            'margin-top': '1in',
            'margin-right': '0.28in',
            'margin-bottom': '1in',
            'footer-left': 'Akvo RSR Report {}'.format(date.today().strftime('%d-%b-%Y')),
            'footer-right': '[page]',
            'footer-font-size': 8,
            'footer-font-name': 'Roboto Condensed',
            'footer-spacing': 10,
        }
        pdf = pdfkit.from_string(html, False, options=options)
        filename = 'project-report.pdf'
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="' + filename + '"'

    return response


@login_required
def render_docx(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related('project_updates'),
        pk=project_id
    )

    doc = DocxTemplate(settings.BASE_DIR + '/templates/reports/project.docx')
    context = {'title': project.title, 'updates': []}
    for update in project.project_updates.all():
        photo_url = 'https://rsr.akvo.org{}'.format(update.photo.url)\
            if update.photo\
            else None
        if photo_url:
            image_response = requests.get(photo_url, stream=True)
            image_file = io.BytesIO(image_response.content)
            image = InlineImage(doc, image_file, width=Mm(100))
        else:
            image = ''

        context['updates'].append({
            'title': update.title,
            'photo': image,
            'created_at': update.created_at.strftime('%-d %b %Y'),
            'text': markdown_to_docx(update.text, doc),
        })
    doc.render(context)

    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    filename = "generated_doc.docx"
    response = HttpResponse(
        doc_io.read(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'

    return response


def count_indicator_completion_percentage(indicator):
    values = [
        {'target': p.target_value, 'actual': p.actual_value}
        for p
        in indicator.periods.all()
    ]
    total_target = sum_attr('target', values)
    total_actual = sum_attr('actual', values)

    try:
        percentage = int(round(total_actual / total_target * 100, 0))
    except (InvalidOperation, TypeError, DivisionByZero):
        return 0

    return percentage if percentage <= 100 else 100


def sum_attr(attr, values):
    total = Decimal(0)
    for value in values:
        try:
            acc = Decimal(value[attr])
        except (InvalidOperation, TypeError):
            acc = Decimal(0)
        total = total + acc

    return total


def get_image(photo, doc):
    image = ''
    photo_url = 'https://rsr.akvo.org{}'.format(photo.url) if photo else None
    if photo_url:
        try:
            image_response = requests.get(photo_url, stream=True)
            image_file = io.BytesIO(image_response.content)
            image = InlineImage(doc, image_file, width=Mm(100))
        except (requests.RequestException, IOError):
            pass

    return image


@login_required
def render_kickstart_docx(request, project_id):
    project = get_object_or_404(
        Project.objects.prefetch_related('project_updates'),
        pk=project_id
    )

    doc = DocxTemplate(settings.BASE_DIR + '/templates/reports/project-kickstart.tpl.docx')
    context = {
        'today': date.today().strftime('%d-%B-%Y'),
        'title': project.title,
        'project_plan': markdown_to_docx(project.project_plan, doc),
        'goals_overview': markdown_to_docx(project.goals_overview, doc),
        'target_group': markdown_to_docx(project.target_group, doc),
        'project_plan_summary': markdown_to_docx(project.project_plan_summary, doc),
        'background': markdown_to_docx(project.background, doc),
        'current_status': markdown_to_docx(project.current_status, doc),
        'sustainability': markdown_to_docx(project.sustainability, doc),
        'partnerships': [
            {
                'organisation': p.organisation.name,
                'role': p.iati_organisation_role_label(),
            }
            for p
            in project.partnerships.all()
        ],
        'budget_items': [
            {
                'label': b.get_label(),
                'period_start': b.period_start.strftime('%Y-%m-%d') if b.period_start else '',
                'period_end': b.period_end.strftime('%Y-%m-%d') if b.period_end else '',
                'amount': b.amount,
                'currency': b.get_currency(),
            }
            for b
            in project.budget_items.all()
        ],
        'budget': project.budget,
        'currency': project.currency,
        'results': [
            {
                'title': r.title.strip(),
                'indicators': [
                    {
                        'title': i.title.strip(),
                        'completion': count_indicator_completion_percentage(i),
                    }
                    for i
                    in r.indicators.all()
                ]
            }
            for r
            in project.results.all()
        ],
        'narratives': [
            {
                'narrative': markdown_to_docx(d.narrative, doc),
                'period_start': d.period.period_start.strftime('%Y-%m-%d') if d.period.period_start else '',
                'period_end': d.period.period_end.strftime('%Y-%m-%d') if d.period.period_end else '',
                'indicator': d.period.indicator.title.strip()
            }
            for d
            in IndicatorPeriodData.objects.select_related(
                'period', 'period__indicator'
            ).filter(
                period__indicator__result__project=project
            ).exclude(narrative__exact='')
        ],
        'updates': []
    }

    for update in project.project_updates.all():
        photo_url = 'https://rsr.akvo.org{}'.format(update.photo.url)\
            if update.photo\
            else None
        if photo_url:
            image_response = requests.get(photo_url, stream=True)
            image_file = io.BytesIO(image_response.content)
            image = InlineImage(doc, image_file, width=Mm(100))
        else:
            image = ''

        context['updates'].append({
            'title': update.title,
            'photo': image,
            'created_at': update.created_at.strftime('%-d %b %Y'),
            'text': markdown_to_docx(update.text, doc),
        })

    doc.render(context)

    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    filename = "project_{}_kickstart.docx".format(project_id)
    response = HttpResponse(
        doc_io.read(),
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    response["Content-Disposition"] = 'attachment; filename="' + filename + '"'

    return response
