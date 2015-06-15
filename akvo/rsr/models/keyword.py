# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from akvo.utils import rsr_image_path

from django.db import models
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail.fields import ImageField

from ..fields import ValidXMLCharField


def logo_path(instance, file_name):
    return rsr_image_path(instance, file_name, 'db/keyword/%(instance_pk)s/%(file_name)s')


class Keyword(models.Model):
    label = ValidXMLCharField(_(u'label'), max_length=30, unique=True, db_index=True)
    logo = ImageField(
        _('logo'), blank=True, upload_to=logo_path,
        help_text=_(u'Add your keyword logo here. You can only add one logo. '
                    u'The logo will be shown on the project page, but not on Akvo Pages.<br/>'
                    u'The logo should be about 1 MB in size, and should preferably be in '
                    u'JPG format.'),
    )

    def __unicode__(self):
        return self.label

    class Meta:
        app_label = 'rsr'
        ordering = ('label',)
        verbose_name = _(u'keyword')
        verbose_name_plural = _(u'keywords')
