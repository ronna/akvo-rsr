# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.


from django.db import models
from django.forms.models import model_to_dict
from django.utils.translation import ugettext_lazy as _

from ..fields import ValidXMLCharField


class Employment(models.Model):
    organisation = models.ForeignKey('Organisation', verbose_name=_(u'organisation'), related_name='employees')
    user = models.ForeignKey('User', verbose_name=_(u'user'), related_name='employers')
    is_approved = models.BooleanField(
        _('approved'), default=False, help_text=_('Designates whether this employment is approved by an administrator.')
    )
    country = models.ForeignKey('Country', verbose_name=_(u'country'), null=True)
    job_title = ValidXMLCharField(_(u'job title'), max_length=50, blank=True)

    class Meta:
        app_label = 'rsr'
        verbose_name = _(u'user employment')
        verbose_name_plural = _(u'user employments')

    def __unicode__(self):
        return self.user.first_name, self.user.last_name, ":", self.organisation.name

    def to_dict(self):
        country = '' if not self.country else model_to_dict(self.country)

        return dict(
            id=self.pk,
            organisation_full=model_to_dict(self.organisation, fields=['id', 'name', 'long_name',]),
            user_full=model_to_dict(self.user, fields=['id', 'first_name', 'last_name', 'email',]),
            is_approved=self.is_approved,
            job_title=self.job_title,
            country_full=country,
        )
