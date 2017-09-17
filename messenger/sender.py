#!/usr/bin/env python3

import logging
import re

from lxml import html
from messenger import utils
from messenger import xpath


class Sender(object):
    """Send Messages to an okcupid user."""

    def __init__(self, session):
        self._session = session

    def _get_authcode(self, username):
        response = self._session.okc_get('profile/{0}'.format(username))
        return get_authcode(html.fromstring(response.content))

    def message_request_parameters(self, username, message,
                                   thread_id, authcode):
        return {
            'ajax': 1,
            'sendmsg': 1,
            'r1': username,
            'body': message,
            'threadid': thread_id,
            'authcode': authcode,
            'reply': 1 if thread_id else 0,
            'from_profile': 1
        }

    def send(self, username, message, authcode=None, thread_id=None):
        authcode = authcode or self._get_authcode(username)
        params = self.message_request_parameters(
            username, message, thread_id or 0, authcode
        )
        response = self._session.okc_get('mailbox', params=params)
        response_dict = response.json()
        # logging.info(simplejson.dumps({'message_send_response': response_dict}))
        # return MessageInfo(response_dict.get('threadid'), response_dict['msgid'])


@utils.curry
def get_js_variable(html_response, variable_name):
    """
    Try to parse the profile page HTML response for something called "authcode", which will allow us to message the profile
    """
    script_elements = xpath.XPathBuilder.script.apply_(html_response)  # Here's problem - this "script" attribute seems to be currier that passes a tree to "apply_()"
    html_response = u'\n'.join(script_element.text_content()  # However, this is not working. Worst comes to worst we might have to do a plain-text regex for authcode
                               for script_element in script_elements)
    return re.search('var {0} = "(.*?)";'.format(variable_name), html_response).group(1)


get_authcode = get_js_variable(variable_name='AUTHCODE')
get_username = get_js_variable(variable_name='SCREENNAME')
get_id = get_js_variable(variable_name='CURRENTUSERID')
get_current_user_id = get_id
get_my_username = get_username
