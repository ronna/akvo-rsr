# -*- coding: utf-8 -*-
"""Akvo RSR is covered by the GNU Affero General Public License.

See more details in the license.txt file located at the root folder of the Akvo RSR module.
For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.
"""

from . import views

from django.conf.urls import url, include
from rest_framework import routers

# Wire up our API using automatic URL routing.
router = routers.DefaultRouter()

# NOTE: any url template tags targeting API endpoints need to include the version as the first
# parameter. Example: {% url 'project_extra-detail' 'v1' project.id 'json' %}

router.register(r'(?P<version>(v1))/administrative_location', views.AdministrativeLocationViewSet)
router.register(r'(?P<version>(v1))/benchmark', views.BenchmarkViewSet)
router.register(r'(?P<version>(v1))/benchmark_name', views.BenchmarknameViewSet)
router.register(r'(?P<version>(v1))/budget_item', views.BudgetItemViewSet)
router.register(r'(?P<version>(v1))/budget_item_label', views.BudgetItemLabelViewSet)
router.register(r'(?P<version>(v1))/category', views.CategoryViewSet)
router.register(r'(?P<version>(v1))/country', views.CountryViewSet)
router.register(r'(?P<version>(v1))/country_budget_item', views.CountryBudgetItemViewSet)
router.register(r'(?P<version>(v1))/crs_add', views.CrsAddViewSet)
router.register(r'(?P<version>(v1))/crs_add_other_flag', views.CrsAddOtherFlagViewSet)
router.register(r'(?P<version>(v1))/default_period', views.DefaultPeriodViewSet)
router.register(r'(?P<version>(v1))/employment', views.EmploymentViewSet)
router.register(r'(?P<version>(v1))/focus_area', views.FocusAreaViewSet)
router.register(r'(?P<version>(v1))/fss', views.FssViewSet)
router.register(r'(?P<version>(v1))/fss_forecast', views.FssForecastViewSet)
router.register(r'(?P<version>(v1))/goal', views.GoalViewSet)
router.register(r'(?P<version>(v1))/humanitarian_scope', views.HumanitarianScopeViewSet)
router.register(r'(?P<version>(v1))/iati_activity_export', views.IatiActivityExportViewSet)
router.register(r'(?P<version>(v1))/iati_check', views.IatiCheckViewSet)
router.register(r'(?P<version>(v1))/iati_export', views.IatiExportViewSet)
router.register(r'(?P<version>(v1))/indicator', views.IndicatorViewSet)
router.register(r'(?P<version>(v1))/dimension_name', views.IndicatorDimensionNameViewSet)
router.register(r'(?P<version>(v1))/dimension_value', views.IndicatorDimensionValueViewSet)
router.register(r'(?P<version>(v1))/indicator_custom_field', views.IndicatorCustomFieldViewSet)
router.register(r'(?P<version>(v1))/indicator_custom_value', views.IndicatorCustomValueViewSet)
router.register(r'(?P<version>(v1))/indicator_framework', views.IndicatorFrameworkViewSet)
router.register(r'(?P<version>(v1))/indicator_label', views.IndicatorLabelViewSet)
router.register(r'(?P<version>(v1))/indicator_period', views.IndicatorPeriodViewSet)
router.register(r'(?P<version>(v1))/indicator_period_framework', views.IndicatorPeriodFrameworkViewSet)
router.register(r'(?P<version>(v1))/indicator_period_actual_location', views.IndicatorPeriodActualLocationViewSet)
router.register(r'(?P<version>(v1))/indicator_period_data', views.IndicatorPeriodDataViewSet)
router.register(r'(?P<version>(v1))/indicator_period_data_framework', views.IndicatorPeriodDataFrameworkViewSet)
router.register(r'(?P<version>(v1))/indicator_period_data_comment', views.IndicatorPeriodDataCommentViewSet)
router.register(r'(?P<version>(v1))/indicator_period_disaggregation', views.IndicatorPeriodDisaggregationViewSet)
router.register(r'(?P<version>(v1))/disaggregation', views.DisaggregationViewSet)
router.register(r'(?P<version>(v1))/disaggregation_target', views.DisaggregationTargetViewSet)
router.register(r'(?P<version>(v1))/indicator_disaggregation_target', views.IndicatorDisaggregationTargetViewSet)
router.register(r'(?P<version>(v1))/indicator_period_target_location', views.IndicatorPeriodTargetLocationViewSet)
router.register(r'(?P<version>(v1))/indicator_reference', views.IndicatorReferenceViewSet)
router.register(r'(?P<version>(v1))/indicator_period_label', views.IndicatorPeriodLabelViewSet)
router.register(r'(?P<version>(v1))/internal_organisation_id',
                views.InternalOrganisationIDViewSet)
router.register(r'(?P<version>(v1))/keyword', views.KeywordViewSet)
router.register(r'(?P<version>(v1))/legacy_data', views.LegacyDataViewSet)
router.register(r'(?P<version>(v1))/link', views.LinkViewSet)
router.register(r'(?P<version>(v1))/narrative_report', views.NarrativeReportViewSet)
router.register(r'(?P<version>(v1))/organisation', views.OrganisationViewSet)
router.register(r'(?P<version>(v1))/organisation_country_budget', views.OrganisationCountryBudgetViewSet)
router.register(r'(?P<version>(v1))/organisation_country_budget_line', views.OrganisationCountryBudgetLineViewSet)
router.register(r'(?P<version>(v1))/organisation_custom_field', views.OrganisationCustomFieldViewSet)
router.register(r'(?P<version>(v1))/organisation_expense_line', views.OrganisationExpenseLineViewSet)
router.register(r'(?P<version>(v1))/organisation_indicator_label', views.OrganisationIndicatorLabelViewSet)
router.register(r'(?P<version>(v1))/organisation_location', views.OrganisationLocationViewSet)
router.register(r'(?P<version>(v1))/organisation_map_location', views.MapOrganisationLocationViewSet)
router.register(r'(?P<version>(v1))/organisation_region_budget', views.OrganisationRegionBudgetViewSet)
router.register(r'(?P<version>(v1))/organisation_region_budget_line', views.OrganisationRegionBudgetLineViewSet)
router.register(r'(?P<version>(v1))/organisation_total_budget', views.OrganisationTotalBudgetViewSet)
router.register(r'(?P<version>(v1))/organisation_total_budget_line', views.OrganisationTotalBudgetLineViewSet)
router.register(r'(?P<version>(v1))/organisation_total_expenditure', views.OrganisationTotalExpenditureViewSet)
router.register(r'(?P<version>(v1))/partner_site', views.PartnerSiteViewSet)
router.register(r'(?P<version>(v1))/partnership', views.PartnershipViewSet)
router.register(r'(?P<version>(v1))/partnership_more_link', views.PartnershipMoreLinkViewSet)
router.register(r'(?P<version>(v1))/planned_disbursement', views.PlannedDisbursementViewSet)
router.register(r'(?P<version>(v1))/policy_marker', views.PolicyMarkerViewSet)
router.register(r'(?P<version>(v1))/project', views.ProjectViewSet)
router.register(r'(?P<version>(v1))/my_projects', views.MyProjectsViewSet)
router.register(r'(?P<version>(v1))/project_iati_export', views.ProjectIatiExportViewSet,
                basename='project_iati_export')
router.register(r'(?P<version>(v1))/project_extra', views.ProjectExtraViewSet,
                basename='project_extra')
router.register(r'(?P<version>(v1))/project_extra_deep', views.ProjectExtraDeepViewSet,
                basename='project_extra_deep')
router.register(r'(?P<version>(v1))/project_up', views.ProjectUpViewSet,
                basename='project_up')
router.register(r'(?P<version>(v1))/project_condition', views.ProjectConditionViewSet)
router.register(r'(?P<version>(v1))/project_contact', views.ProjectContactViewSet)
router.register(r'(?P<version>(v1))/project_custom_field', views.ProjectCustomFieldViewSet)
router.register(r'(?P<version>(v1))/project_document', views.ProjectDocumentViewSet)
router.register(r'(?P<version>(v1))/project_document_category', views.ProjectDocumentCategoryViewSet)
router.register(r'(?P<version>(v1))/project_location', views.ProjectLocationViewSet)
router.register(r'(?P<version>(v1))/project_map_location', views.MapProjectLocationViewSet)

router.register(r'(?P<version>(v1))/project_update_extra', views.ProjectUpdateExtraViewSet,
                basename='project_update_extra')
router.register(r'(?P<version>(v1))/project_update', views.ProjectUpdateViewSet,
                basename='project_update')
router.register(r'(?P<version>(v1))/project_update_location', views.ProjectUpdateLocationViewSet)
router.register(r'(?P<version>(v1))/project_update_map_location', views.MapProjectUpdateLocationViewSet)

router.register(r'(?P<version>(v1))/project_hierarchy', views.ProjectHierarchyViewSet)
router.register(r'(?P<version>(v1))/raw_project_hierarchy', views.RawProjectHierarchyViewSet)

router.register(r'(?P<version>(v1))/publishing_status', views.PublishingStatusViewSet)
router.register(r'(?P<version>(v1))/recipient_country', views.RecipientCountryViewSet)
router.register(r'(?P<version>(v1))/recipient_organisation_budget', views.OrganisationRecipientOrgBudgetViewSet)
router.register(r'(?P<version>(v1))/recipient_organisation_budget_line',
                views.OrganisationRecipientOrgBudgetLineViewSet)
router.register(r'(?P<version>(v1))/recipient_region', views.RecipientRegionViewSet)
router.register(r'(?P<version>(v1))/related_project', views.RelatedProjectViewSet)
router.register(r'(?P<version>(v1))/reports', views.ReportViewSet, basename='reports_api')
router.register(r'(?P<version>(v1|v2))/result', views.ResultsViewSet)
router.register(r'(?P<version>(v1))/results_framework', views.ResultsFrameworkViewSet)
router.register(r'(?P<version>(v1))/results_framework_lite', views.ResultsFrameworkLiteViewSet)
router.register(r'(?P<version>(v1))/sector', views.SectorViewSet)
router.register(r'(?P<version>(v1))/transaction', views.TransactionViewSet)
router.register(r'(?P<version>(v1))/transaction_sector', views.TransactionSectorViewSet)
router.register(r'(?P<version>(v1))/user', views.UserViewSet)


# We turn off the API root view (since it's broken with URLPathVersioning)
router.include_root_view = False
# Add API root view by version
root_url = url(r'(?P<version>(v1|v2))/$', router.get_api_root_view(), name=router.root_view_name)
router.urls.append(root_url)

# Additionally, we include URLs for non-viewsets (functional views).
# NOTE: if versions is to be added to one of the views below, the view function needs to include
# version in its parameters.

urlpatterns = (
    url(r'^', include(router.urls)),
    url(r'v1/employment/(?P<pk>[0-9]+)/set_group/(?P<group_id>[0-9]+)/$',
        views.set_group,
        name='set_group'),
    url(r'v1/user/(?P<pk>[0-9]+)/change_password/$',
        views.change_password,
        name='user_change_password'),
    url(r'v1/organisations/(?P<pk>[0-9]+)/users/$',
        views.organisation_user_roles,
        name='organisation_user_roles'),
    url(r'v1/managed-employments/$',
        views.managed_employments,
        name='managed_employments'),
    url(r'v1/organisations/(?P<org_pk>[0-9]+)/users/(?P<user_pk>[0-9]+)/$',
        views.change_user_roles,
        name='change_organisation_user_roles'),
    url(r'v1/user/(?P<pk>[0-9]+)/update_details/$',
        views.update_details,
        name='user_update_details'),
    url(r'v1/me/$',
        views.current_user,
        name='current_user'),
    url(r'v1/invite_user/$',
        views.invite_user,
        name='invite_user'),
    url(r'v1/project_iati_check/(?P<pk>[0-9]+)/$',
        views.ProjectIatiCheckView.as_view(),
        name='project_iati_check'),
    url(r'v1/project_update/(?P<update_pk>[0-9]+)/photos/$',
        views.project_update_photos,
        name='project_update_add_photos'),
    url(r'v1/project_update/(?P<update_pk>[0-9]+)/photos/(?P<photo_pk>[0-9]+)/$',
        views.project_update_photos,
        name='project_update_remove_photos'),
    url(r'v1/indicator_period_data/(?P<pk>[0-9]+)/upload_file/$',
        views.indicator_upload_file,
        name='indicator_upload_file'),
    url(r'v1/indicator_period_data/(?P<update_pk>[0-9]+)/files/$',
        views.period_update_files,
        name='period_update_add_files'),
    url(r'v1/indicator_period_data/(?P<update_pk>[0-9]+)/files/(?P<file_pk>[0-9]+)/$',
        views.period_update_files,
        name='period_update_remove_files'),
    url(r'v1/indicator_period_data/(?P<update_pk>[0-9]+)/photos/$',
        views.period_update_photos,
        name='period_update_add_photos'),
    url(r'v1/indicator_period_data/(?P<update_pk>[0-9]+)/photos/(?P<photo_pk>[0-9]+)/$',
        views.period_update_photos,
        name='period_update_remove_photos'),
    url(r'v1/set-periods-locked/(?P<project_pk>[0-9]+)/$',
        views.set_periods_locked,
        name='set_periods_locked'),
    url(r'v1/set-updates-status/(?P<project_pk>[0-9]+)/$',
        views.set_updates_status,
        name='set_updates_status'),
    url(r'v1/right_now_in_akvo/$', views.right_now_in_akvo_view, name='right_now_in_akvo'),
    url(r'v1/server_info/$', views.server_info, name='server_info'),
    url(r'v1/title-and-status/(?P<project_pk>[0-9]+)/$', views.project_title, name='project_title'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/results_framework/$',
        views.project_results_framework,
        name='project_results_framework'),
    url(r'v1/bulk-add-periods/(?P<project_pk>[0-9]+)/$',
        views.bulk_add_periods,
        name='bulk_add_periods'),
    url(r'v1/bulk-remove-periods/(?P<project_pk>[0-9]+)/$',
        views.bulk_remove_periods,
        name='bulk_remove_periods'),
)

# Project editor
urlpatterns += (
    url(r'v1/project/(?P<project_pk>[0-9]+)/copy_results/(?P<source_pk>[0-9]+)/$',
        views.project_editor_copy_results,
        name='project_editor_copy_results'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/import_results/$',
        views.project_editor_import_results,
        name='project_editor_import_results'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/import_result/(?P<parent_result_id>[0-9]+)/$',
        views.project_editor_import_result,
        name='project_editor_import_result'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/import_indicator/(?P<parent_indicator_id>[0-9]+)/$',
        views.project_editor_import_indicator,
        name='project_editor_import_indicator'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/reorder_items/$',
        views.project_editor_reorder_items,
        name='project_editor_reorder_items'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/default_periods/$',
        views.project_default_periods,
        name='project_default_periods'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/period-labels/$',
        views.project_period_labels,
        name='project_period_labels'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/indicator_custom_fields/$',
        views.project_default_periods,
        name='project_indicator_custom_fields'),
    url(r'v1/project_update/(?P<pk>[0-9]+)/upload_photo/$',
        views.upload_indicator_update_photo,
        name='upload_indicator_update_photo'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/project-roles/$',
        views.project_roles,
        name='project_roles'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/invite-user/$',
        views.project_invite_user,
        name='project_invite_user'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/enumerator-assignment-send/$',
        views.assignment_send,
        name='enumerator_assignment_send'),
)

# Directory views
urlpatterns += (
    url(r'v1/project-directory$',
        views.project_directory,
        name='project_directory'),
    url(r'v1/update_directory$',
        views.update_directory,
        name='update_directory'),
    url(r'v1/organisation_directory$',
        views.organisation_directory,
        name='organisation_directory'),
    url(r'v1/sector_codes$',
        views.sector_codes,
        name="sector_code_list"),
    url(r'v1/projects_by_id$',
        views.projects_by_id,
        name='projects_by_id'),
    url(r'v1/project_published_search$',
        views.project_published_search,
        name='project_published_search'),
    url(r'v1/demo_request$',
        views.demo_request,
        name='demo_request'),
)

# GeoJSON views
urlpatterns += (
    url(r'v1/project_location_geojson$',
        views.project_location_geojson,
        name='project_location_geojson'),
)

# Project overview
urlpatterns += (
    url(r'v1/project/(?P<pk>[0-9]+)/results/$',
        views.project_results,
        name='project_results'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/result/(?P<result_pk>[0-9]+)/$',
        views.project_result_overview,
        name='project_result_overview'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/indicator/(?P<indicator_pk>[0-9]+)/$',
        views.project_indicator_overview,
        name='project_indicator_overview'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/results_geo/$',
        views.get_program_results_geo,
        name='get_program_results_geo'),
)

# Project enumerators
urlpatterns += (
    url(r'v1/project/(?P<project_pk>[0-9]+)/enumerators/$',
        views.project_enumerators,
        name='project_enumerators'),
)

# Program
urlpatterns += (
    url(r'v1/program/(?P<program_pk>[0-9]+)/add-project/$',
        views.add_project_to_program,
        name='add_project_to_program'),
    url(r'v1/program/(?P<program_pk>[0-9]+)/countries/$',
        views.program_countries,
        name='program_countries'),
    url(r'v1/program/(?P<program_pk>[0-9]+)/updates/$',
        views.program_updates,
        name='program_updates'),
)


# Typeahead
urlpatterns += (
    url(r'v1/typeaheads/organisations$',
        views.typeahead_organisation,
        name='organisation_typeahead'),
    url(r'v1/typeaheads/projects$',
        views.typeahead_project,
        name='project_typeahead'),
    url(r'v1/typeaheads/project_updates$',
        views.typeahead_projectupdate,
        name='projectupdate_typeahead'),
    url(r'v1/organisation_reports/$',
        views.organisation_reports,
        name='organisation_reports'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/reports/$',
        views.project_reports,
        name='project_reports'),
    url(r'v1/project/(?P<project_pk>[0-9]+)/reports/period-dates/$',
        views.project_reports_period_dates,
        name='project_reports_period_dates'),
    url(r'v1/program_reports/(?P<program_pk>[0-9]+)/$',
        views.program_reports,
        name='program_reports'),
    url(r'v1/program_reports/(?P<program_pk>[0-9]+)/period-dates/$',
        views.program_reports_period_dates,
        name='program_reports_period_dates'),
    url(r'v1/program_reports/(?P<program_pk>[0-9]+)/countries/$',
        views.program_reports_countries,
        name='program_reports_countries'),
    url(r'v1/members/$',
        views.organisations_members,
        name='organisations_members'),
)

# My reports
urlpatterns += (
    url(r'v1/report_formats/$',
        views.report_formats,
        name='report_formats_api'),
)
