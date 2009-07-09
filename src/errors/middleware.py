#!/usr/bin/env python
# vim:set ts=2 sw=2 et:
#
# Google App Engine Internal Error Middleware
# Copyright (C) 2009 Wesley Tanaka <http://wtanaka.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import django.http

from google.appengine.api.datastore_errors import InternalError
from google.appengine.api.datastore_errors import Timeout
from google.appengine.api.datastore_errors import TransactionFailedError
from google.appengine.runtime.apiproxy_errors import CapabilityDisabledError

CATCHABLE = (
 (Timeout, 'timeout.html'),
 (InternalError, 'internal-error.html'),
 (CapabilityDisabledError, 'capability-disabled.html'),
 (TransactionFailedError, 'transaction-failed.html'),
)

def render(template, template_values):
  import django.template.loader
  t = django.template.loader.get_template(template)
  import django.template
  return t.render(django.template.Context(template_values))

class GoogleAppEngineErrorMiddleware:
  """Display a default template on internal google app engine errors"""
  def process_exception(self, request, exception):
    for e_type, template_name in CATCHABLE:
      if isinstance(exception, e_type):
        html = render(template_name, {'exception': exception})
        return django.http.HttpResponseServerError(html)
