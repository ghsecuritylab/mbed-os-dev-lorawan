"""
mbed SDK
Copyright (c) 2011-2013 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from subprocess import call


class HostTestPluginBase:
    """ Base class for all plug-ins used with host tests.
    """
    ###########################################################################
    # Interface:
    ###########################################################################

    ###########################################################################
    # Interface attributes defining plugin name, type etc.
    ###########################################################################
    name = "HostTestPluginBase" # Plugin name, can be plugin class name
    type = "BasePlugin"         # Plugin type: ResetMethod, Copymethod etc.
    capabilities = []           # Capabilities names: what plugin can achieve
                                # (e.g. reset using some external command line tool)
    stable = False              # Determine if plugin is stable and can be used

    ###########################################################################
    # Interface methods
    ###########################################################################
    def setup(self, *args, **kwargs):
        """ Configure plugin, this function should be called before plugin execute() method is used.
        """
        return False

    def execute(self, capabilitity, *args, **kwargs):
        """ Executes capability by name.
            Each capability e.g. may directly just call some command line
            program or execute building pythonic function
        """
        return False

    ###########################################################################
    # Interface helper methods - overload only if you need to have custom behaviour
    ###########################################################################
    def check_parameters(self, capabilitity, *args, **kwargs):
        """ This function should be ran each time we call execute()
            to check if none of the required parameters is missing.
        """
        for parameter in self.required_parameters:
            if parameter not in kwargs:
                print "%s::%s: Plugin parameter '%s' missing!"% (self.name, self.type, parameter)
                return False
        return True

    def run_command(self, cmd, shell=True):
        """ Runs command from command line.
        """
        result = True
        try:
            ret = call(cmd, shell=shell)
            if ret:
                print "%s::%s: [ret=%d] Command: %s"% (self.name, self.type, ret, " ".join(cmd))
        except Exception, e:
            result = False
            print "%s::%s: [ret=%d] Command: %s"% (self.name, self.type, ret, " ".join(cmd))
            print "%s::%s: " + str(e)
        return result
