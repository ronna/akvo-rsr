# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from django.db import models
from django.utils.translation import ugettext_lazy as _

from .base_codelist import BaseCodelist


class UNSDGTargets(BaseCodelist):
    name = models.TextField(_('name'), blank=True, null=False)

    def __str__(self):
        return self.code + ' - ' + self.name.capitalize()

    class Meta:
        app_label = 'codelists'
        ordering = ('-version', 'code')
        verbose_name = _('unsdg targets')
        verbose_name_plural = _('unsdg targets')
