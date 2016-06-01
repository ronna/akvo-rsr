# -*- coding: utf-8 -*-

# Akvo RSR is covered by the GNU Affero General Public License.
# See more details in the license.txt file located at the root folder of the Akvo RSR module.
# For additional details on the GNU license please see < http://www.gnu.org/licenses/agpl.html >.

from lxml import etree

STATUS_TO_CODE = {
    'N': '0',
    'H': '1',
    'A': '2',
    'C': '3',
    'L': '5',
    'R': '6',
}


def activity_status(project):
    """
    Generate the activity-status element.

    :param project: Project object
    :return: A list of Etree elements
    """
    if project.iati_status:
        element = etree.Element("activity-status")
        element.attrib['code'] = project.iati_status
        return [element]

    return []
