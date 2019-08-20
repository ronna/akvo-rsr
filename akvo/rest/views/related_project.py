# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType

from rest_framework.response import Response
from rest_framework import status


from akvo.rsr.models import RelatedProject
from akvo.rsr.mixins import LogProjectActionMixin
from akvo.rsr.models.related_project import ParentChangeDisallowed
from ..serializers import RelatedProjectSerializer
from ..viewsets import PublicProjectViewSet


class RelatedProjectViewSet(PublicProjectViewSet, LogProjectActionMixin):
    """
    """
    queryset = RelatedProject.objects.all()
    serializer_class = RelatedProjectSerializer

    def create(self, request, *args, **kwargs):
        response = super(RelatedProjectViewSet, self).create(request, *args, **kwargs)
        instance = RelatedProject.objects\
            .select_related('project', 'related_project')\
            .get(pk=response.data['id'])
        self.log_addition(
            request.user,
            instance.project,
            'Add related project (id:{}, relation:{})'.format(
                instance.related_project.id,
                instance.relation
            )
        )
        return response

    def update(self, request, *args, **kwargs):
        response = super(RelatedProjectViewSet, self).update(request, *args, **kwargs)
        instance = RelatedProject.objects\
            .select_related('project', 'related_project')\
            .get(pk=response.data['id'])
        self.log_changes(
            request.user,
            instance.project,
            'Change related project (id:{}, relation:{})'.format(
                instance.related_project.id,
                instance.relation
            )
        )
        return response

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            project = instance.project
            message = 'Remove related project (id:{})'.format(instance.related_project.id)
            response = super(RelatedProjectViewSet, self).destroy(request, *args, **kwargs)
            self.log_deletion(request.user, project, message)
            return response
        except ParentChangeDisallowed as e:
            return Response(str(e), status=status.HTTP_403_FORBIDDEN)
