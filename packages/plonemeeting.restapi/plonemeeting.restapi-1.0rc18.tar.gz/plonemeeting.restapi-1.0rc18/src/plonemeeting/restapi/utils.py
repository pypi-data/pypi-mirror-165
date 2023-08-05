# -*- coding: utf-8 -*-

from AccessControl import Unauthorized
from BeautifulSoup import BeautifulSoup
from HTMLParser import HTMLParser
from imio.helpers.content import uuidToObject
from lxml.html.clean import Cleaner
from plone import api
from plone.restapi.deserializer import boolean_value
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.interfaces import ISerializeToJsonSummary
from plonemeeting.restapi.bbb import getActiveConfigs
from plonemeeting.restapi.config import HAS_MEETING_DX
from plonemeeting.restapi.config import INDEX_CORRESPONDENCES
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import _checkPermission
from Products.CMFPlone.utils import safe_unicode
from Products.PloneMeeting.config import MEETINGMANAGERS_GROUP_SUFFIX
from Products.PloneMeeting.utils import convert2xhtml
from zExceptions import BadRequest
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest


IN_NAME_OF_CONFIG_ID_UNAUTHORIZED = 'User "%s" must be Manager/MeetingManager for ' \
    'config "%s" to use "in_name_of=%s" option!'
IN_NAME_OF_UNAUTHORIZED = 'User "%s" must be Manager/MeetingManager to use "in_name_of=%s" option!'
IN_NAME_OF_USER_NOT_FOUND = 'The in_name_of user "%s" was not found!'
UID_NOT_ACCESSIBLE_ERROR = 'Element with UID "%s" was found in config "%s" but ' \
    'user "%s" can not access it!'
UID_NOT_ACCESSIBLE_IN_NAME_OF_ERROR = 'Element with UID "%s" was found in config ' \
    '"%s" but user "%s" can not access it (using "in_name_of" original power user "%s")!'
UID_NOT_FOUND_ERROR = 'No element found with UID "%s"!'


def check_in_name_of(cfg_id, data):
    """ """
    in_name_of = data.get("in_name_of", None)
    access_cfg_ids = None
    if in_name_of is not None:
        access_cfg_ids = get_poweraccess_configs()
        # if user not a (Meeting)Manager or a cfg_id is given and user is not
        # MeetingManager for it, raise Unauthorized
        if not access_cfg_ids:
            raise Unauthorized(IN_NAME_OF_UNAUTHORIZED %
                               (api.user.get_current().getId(), in_name_of))
        elif cfg_id and cfg_id not in access_cfg_ids:
            # not MeetingManager for the given cfg_id
            raise Unauthorized(IN_NAME_OF_CONFIG_ID_UNAUTHORIZED %
                               (api.user.get_current().getId(), cfg_id, in_name_of))
        user = api.user.get(in_name_of)
        if not user:
            raise BadRequest(IN_NAME_OF_USER_NOT_FOUND % in_name_of)
    return in_name_of, access_cfg_ids


def get_serializer(obj, extra_include_name=None, serializer=None):
    """ """
    request = getRequest()
    interface = ISerializeToJsonSummary
    prefix = ''
    if extra_include_name:
        prefix = "extra_include_{0}_".format(extra_include_name)
    if use_obj_serializer(request.form, prefix=prefix):
        interface = ISerializeToJson
    serializer = queryMultiAdapter((obj, request), interface)
    if extra_include_name:
        serializer._extra_include_name = extra_include_name
    return serializer


def get_param(value, default=False, extra_include_name=None, serializer=None):
    """If current serialized element is an extra_include,
       infos in request.form are relative to extra_include,
       else information are directly available.
       For extra_include, a parameter is passed like :
       ?extra_include=extra_include_name:parameter_name:value so
       ?extra_include_category_fullobjects or ?extra_include_category_metadata_fields=acronym."""
    request = getRequest()
    # extra_include_name is stored on serializer or passed as parameter when serializer
    # still not initialized, this is the case for parameter "fullobjects" as from this
    # will depend the interface to use to get the serializer
    extra_include_name = serializer and \
        getattr(serializer, "_extra_include_name", extra_include_name)
    if extra_include_name:
        # change param value
        value = "extra_include_{0}_{1}".format(extra_include_name, value)

    param = request.form.get(value, None)

    # param was not found in request.form
    if param is None:
        param = default
    elif default in (True, False):
        param = boolean_value(param)
    # if default is a list, then make sure we return a list
    elif isinstance(default, (tuple, list)) and not isinstance(param, (tuple, list)):
        param = [param]
    return param


def clean_html(value):
    """ """
    if clean_html and value:
        # we need a surrounding <p></p> or the content is not generated by appy.pod
        if not value.startswith(u'<p>') or not value.endswith(u'</p>'):
            value = u'<p>%s</p>' % value
        soup = BeautifulSoup(safe_unicode(value))
        soup_contents = soup.renderContents()
        if not isinstance(soup_contents, unicode):
            soup_contents = safe_unicode(soup_contents)
        # clean HTML with HTMLParser, it will remove special entities like &#xa0;
        soup_contents = HTMLParser().unescape(soup_contents)
        # clean HTML with lxml Cleaner
        cleaner = Cleaner()
        soup_contents = cleaner.clean_html(soup_contents)
        # clean_html surrounds the cleaned HTML with <div>...</div>... removes it!
        if soup_contents.startswith(u'<div>') and soup_contents.endswith(u'</div>'):
            soup_contents = soup_contents[5:-6]
        if not soup_contents == value:
            value = soup_contents
    return value


def handle_html(obj, data):
    """ """
    return convert2xhtml(obj,
                         data,
                         image_src_to_data=True,
                         anonymize=True,
                         use_appy_pod_preprocessor=True)


def get_poweraccess_configs():
    '''
      Return the MeetingConfig ids the current user can access,
      so the active configs for which user is MeetingManager or every
      if user is Manager.
      This will be used to protect access to some config endpoints or
      functionnalities like "in_name_of".
    '''
    tool = api.portal.get_tool('portal_plonemeeting')
    if _checkPermission(ManagePortal, tool):
        cfg_ids = [cfg.id for cfg in getActiveConfigs(check_using_groups=False, check_access=False)]
    else:
        cfg_ids = [
            group_id.split('_')[0] for group_id in
            get_filtered_plone_groups_for_user(suffixes=[MEETINGMANAGERS_GROUP_SUFFIX])]
    return cfg_ids


def use_obj_serializer(form, prefix=''):
    """Methods that will determinate if regarding values in the request,
       the ISerializeToJson serializer should be used."""
    # boolean_value of "" is True
    return bool(
        boolean_value(form.get(prefix + 'fullobjects', False)) or
        [v for v in form if v.startswith(prefix + 'include_')] or
        form.get(prefix + "extra_include", []) or
        form.get(prefix + "metadata_fields", []) or
        form.get(prefix + "additional_values", []))


def rest_uuid_to_object(uid, try_restricted=True, in_name_of=None):
    """Return the object corresponding to given p_uid but manage cases when
       it was not found or is not available to current user."""
    obj = None
    if try_restricted:
        obj = uuidToObject(uid)
    if obj is None:
        # try to get it unrestricted
        obj = uuidToObject(uid, unrestricted=True)
        if obj:
            tool = api.portal.get_tool('portal_plonemeeting')
            cfg = tool.getMeetingConfig(obj)
            if in_name_of:
                msg = UID_NOT_ACCESSIBLE_IN_NAME_OF_ERROR % (
                    uid, cfg.getId(), in_name_of, api.user.get_current().getId())
            else:
                msg = UID_NOT_ACCESSIBLE_ERROR % (
                    uid, cfg.getId(), in_name_of or api.user.get_current().getId())
            raise BadRequest(msg)
        else:
            raise BadRequest(UID_NOT_FOUND_ERROR % uid)
    return obj


def build_catalog_query(serializer, extra_include_name=None):
    """ """

    # filters may be any portal_catalog index
    catalog = api.portal.get_tool('portal_catalog')
    query = {}
    for index in catalog.Indexes:
        value = serializer.get_param(
            index, None, extra_include_name=extra_include_name)
        if value is None:
            # try to get an index by it's correspondance name
            easy_index = INDEX_CORRESPONDENCES.get(index, None)
            if easy_index is not None:
                value = serializer.get_param(
                    easy_index, None, extra_include_name=extra_include_name)
        if value is not None:
            query[index] = value
    return query


def get_filtered_plone_groups_for_user(org_uids=[], user_id=None, suffixes=[], the_objects=False):
    """Copy from ToolPloneMeeting.get_filtered_plone_groups_for_user so it is available
       when using PloneMeeting 4.1.x.
       XXX to be removed when support for PloneMeeting 4.1.x will be removed."""

    tool = api.portal.get_tool('portal_plonemeeting')
    if HAS_MEETING_DX:
        user_groups = tool.get_plone_groups_for_user(
            user_id=user_id, the_objects=the_objects)
    else:
        user_groups = tool.get_plone_groups_for_user(
            userId=user_id, the_objects=the_objects)
    if the_objects:
        user_groups = [plone_group for plone_group in user_groups
                       if (not org_uids or plone_group.id.split('_')[0] in org_uids) and
                       (not suffixes or '_' in plone_group.id and plone_group.id.split('_')[1] in suffixes)]
    else:
        user_groups = [plone_group_id for plone_group_id in user_groups
                       if (not org_uids or plone_group_id.split('_')[0] in org_uids) and
                       (not suffixes or '_' in plone_group_id and plone_group_id.split('_')[1] in suffixes)]
    return sorted(user_groups)
