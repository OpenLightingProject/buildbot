# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Helper code for the Open Lighting Project buildbot configs.

import os

def LoadConfig(config_file):
  """Load the buildbot config from a config file."""
  config = {}
  globals = {
    'Slave': SlaveConfig,
  }
  execfile(config_file, globals, config)
  return config


class SlaveConfig(object):
  def __init__(self, suffix, has_lint=False):
    self._suffix = suffix
    self._has_lint = has_lint

  @property
  def suffix(self):
    return self._suffix

  @property
  def has_lint(self):
    return self._has_lint


class BuildSlave(object):
  def __init__(self, platform, arch, suffix, has_lint):
    self._platform = platform
    self._arch = arch
    self._suffix = suffix
    self._has_lint = has_lint

  def name(self):
    """Return the name of this slave."""
    return '%s-%s-%s' % (self._platform, self._arch, self._suffix)

  def password(self):
    """Get the password for this slave."""
    path = os.path.join(os.path.dirname(__file__), "%s.pass" % self.name())
    return open(path).read().strip()

  @property
  def has_lint(self):
    return self._has_lint


def HasLintFilter(slave):
  """Filter on slaves that have lint installed."""
  return slave.has_lint

class SlaveStore(object):
  """Holds the BuildSlave objects."""
  def __init__(self, slave_config):
    self._slaves = []
    for platform, platform_spec in slave_config.iteritems():
      for arch, slave_names in platform_spec.iteritems():
        for slave in slave_names:
          self._slaves.append(BuildSlave(
            platform, arch, slave.suffix, slave.has_lint))

  def GetSlaves(self, slave_filter=None):
    """Returns all slaves matching the optional filter."""
    if slave_filter is None:
      return self._slaves[:]
    else:
      return [s for s in self._slaves if slave_filter(s)]
