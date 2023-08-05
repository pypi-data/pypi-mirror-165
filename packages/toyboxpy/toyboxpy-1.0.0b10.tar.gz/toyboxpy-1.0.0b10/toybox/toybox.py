# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import getopt
import os
import shutil

from pathlib import Path
from toybox.__about__ import __version__
from toybox.boxfile import Boxfile
from toybox.exceptions import ArgumentError


class Toybox:
    """A Lua and C dependency management system for the Playdate SDK."""

    def __init__(self, args):
        """Initialise toybox based on user configuration."""

        self.dependencies = []
        self.only_update = None

        try:
            # -- Gather the arguments
            opts, other_arguments = getopt.getopt(args, '')

            if len(other_arguments) == 0:
                raise SyntaxError('Expected a command!  Maybe start with `toybox help`?')

            number_of_arguments = len(other_arguments)

            self.argument = None

            i = 0
            self.command = other_arguments[i]
            i += 1

            if i != number_of_arguments:
                self.argument = other_arguments[i]
                i += 1

            if i != number_of_arguments:
                raise SyntaxError('Too many commands on command line.')

        except getopt.GetoptError:
            raise ArgumentError('Error reading arguments.')

    def main(self):
        switch = {
            'help': Toybox.printUsage,
            'version': Toybox.printVersion,
            'info': self.printInfo,
            'add': self.addDependency,
            'remove': self.removeDependency,
            'update': self.update
        }

        if self.command is None:
            print('No command found.\n')
            self.printUsage()
            return

        if self.command not in switch:
            raise ArgumentError('Unknow command \'' + self.command + '\'.')

        switch.get(self.command)()

    def printInfo(self, folder=None):
        if folder is None:
            folder = Toybox.boxfileFolder()
            print('Resolving dependencies...')

        box_file = Boxfile(folder)
        if len(box_file.dependencies) == 0:
            if folder is None:
                print('Boxfile is empty.')
        else:
            for dep in box_file.dependencies:
                info_string = '       - ' + str(dep) + ' -> ' + str(dep.resolveVersion())

                dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
                folder_exists = os.path.exists(dep_folder)

                if not folder_exists:
                    info_string += ' (not installed)'

                print(info_string)

                if folder_exists:
                    self.printInfo(dep_folder)

    def addDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'add\' command.')

        version = 'default'

        box_file = Boxfile(Toybox.boxfileFolder())
        box_file.addDependency(self.argument, version)
        box_file.save()

        print('Added a dependency for \'' + self.argument + '\' at \'' + version + '\'.')

    def removeDependency(self):
        if self.argument is None:
            raise SyntaxError('Expected an argument to \'remove\' command.')

        box_file = Boxfile(Toybox.boxfileFolder())
        box_file.removeDependency(self.argument)
        box_file.save()

        print('Removed a dependency for \'' + self.argument + '\'.')

    def installDependency(self, dep, no_copying=False):
        dependency_is_new = True

        for dependency in self.dependencies:
            if dependency.url == dep.url:
                for version in dep.versions:
                    dependency.versions.append(version)

                dep = dependency
                dependency_is_new = False

        should_copy = (self.only_update is not None) and (self.only_update != dep.repo_name) and Toybox.dependencyExistsInBackup(dep)

        if (no_copying is False) and should_copy:
            print('Copying \'' + str(dep) + '.')
            self.copyDependencyFromBackup(dep)
        else:
            version = dep.installIn(Toybox.toyboxesFolder())

            if version is not None:
                info_string = 'Installed \'' + str(dep) + ' -> ' + str(version) + '\''

                if should_copy and no_copying:
                    info_string += ' (force-installed by another dependency)'

                print(info_string + '.')

            no_copying = True

        dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
        box_file = Boxfile(dep_folder)
        for child_dep in box_file.dependencies:
            self.installDependency(child_dep, no_copying)

        if dependency_is_new:
            self.dependencies.append(dep)

    def generateLuaIncludeFile(self):
        lua_includes = []

        for dep in self.dependencies:
            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
            lua_include_path = Toybox.findLuaIncludeFileIn(dep_folder, dep.repo_name)
            if lua_include_path is not None:
                lua_includes.append(os.path.join(dep.subFolder(), lua_include_path))

        if len(lua_includes) == 0:
            return

        with open(os.path.join(Toybox.toyboxesFolder(), 'toyboxes.lua'), 'w') as out_file:
            out_file.write('--\n')
            out_file.write('--  toyboxes.lua - include file auto-generated by toybox.py (https://toyboxpy.io).\n')
            out_file.write('--\n')
            out_file.write('\n')

            for lua_include in lua_includes:
                out_file.write('import \'' + lua_include + '.lua\'\n')

            out_file.close()

    def generateMakefile(self):
        makefiles = []

        for dep in self.dependencies:
            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
            makefile_path = Toybox.findMakefileIn(dep_folder, dep.repo_name)
            if makefile_path is not None:
                makefiles.append([os.path.join(dep.subFolder(), makefile_path), dep.repo_name.upper()])

        if len(makefiles) == 0:
            return

        with open(os.path.join(Toybox.toyboxesFolder(), 'toyboxes.mk'), 'w') as out_file:
            out_file.write('#\n')
            out_file.write('#  toyboxes.mk - include file auto-generated by toybox.py (https://toyboxpy.io).\n')
            out_file.write('#\n')
            out_file.write('\n')
            out_file.write('_RELATIVE_FILE_PATH := $(lastword $(MAKEFILE_LIST))\n')
            out_file.write('_RELATIVE_DIR := $(subst /$(notdir $(_RELATIVE_FILE_PATH)),,$(_RELATIVE_FILE_PATH))\n')
            out_file.write('\n')
            out_file.write('uniq = $(if $1,$(firstword $1) $(call uniq,$(filter-out $(firstword $1),$1)))\n')
            out_file.write('UINCDIR := $(call uniq, $(UINCDIR) $(_RELATIVE_DIR))\n')
            out_file.write('\n')

            for makefile in makefiles:
                out_file.write(makefile[1] + '_MAKEFILE := $(_RELATIVE_DIR)/' + makefile[0] + '\n')

            out_file.write('\n')

            for makefile in makefiles:
                out_file.write('include $(' + makefile[1] + '_MAKEFILE)\n')

            out_file.close()

    def generateIncludeFile(self):
        include_files = []

        for dep in self.dependencies:
            dep_folder = os.path.join(Toybox.toyboxesFolder(), dep.subFolder())
            include_file_path = Toybox.findIncludeFileIn(dep_folder, dep.repo_name)
            if include_file_path is not None:
                include_files.append([os.path.join(dep.subFolder(), include_file_path), dep.repo_name])

        if len(include_files) == 0:
            return

        with open(os.path.join(Toybox.toyboxesFolder(), 'toyboxes.h'), 'w') as out_file:
            out_file.write('//\n')
            out_file.write('//  toyboxes.h - include file auto-generated by toybox.py (https://toyboxpy.io).\n')
            out_file.write('//\n')
            out_file.write('\n')

            for include in include_files:
                out_file.write('#include "' + include[0] + '"\n')

            out_file.write('\n')

            prefix = ''
            out_file.write('#define REGISTER_TOYBOXES(pd)')
            for include in include_files:
                out_file.write(prefix + '   register_' + include[1] + '(pd);')
                prefix = ' \\\n                             '

            out_file.write('\n')

            out_file.close()

    def update(self):
        if self.argument is not None:
            self.only_update = self.argument

        Toybox.backupToyboxes()

        try:
            box_file = Boxfile(Toybox.boxfileFolder())
            for dep in box_file.dependencies:
                self.installDependency(dep)

            if os.path.exists(Toybox.toyboxesFolder()):
                Toybox.generateReadMeFile()
                self.generateLuaIncludeFile()
                self.generateMakefile()
                self.generateIncludeFile()

        except Exception:
            Toybox.restoreToyboxesBackup()
            raise

        Toybox.deleteToyboxesBackup()

        print('Finished.')

    @classmethod
    def printVersion(cls):
        print('🧸 toybox.py v' + __version__)

    @classmethod
    def printUsage(cls):
        Toybox.printVersion()
        print('Usage:')
        print('    toybox help                      - Show a help message.')
        print('    toybox version                   - Get the Toybox version.')
        print('    toybox info                      - Describe your dependency set.')
        print('    toybox add <dependency>          - Add a new dependency.')
        print('    toybox remove <dependency>       - Remove a dependency.')
        print('    toybox update                    - Update all the dependencies.')
        print('    toybox update <dependency>       - Update a single dependency.')

    @classmethod
    def boxfileFolder(cls):
        return os.getcwd()

    @classmethod
    def toyboxesFolder(cls):
        return os.path.join(Toybox.boxfileFolder(), 'toyboxes')

    @classmethod
    def toyboxesBackupFolder(cls):
        return Toybox.toyboxesFolder() + '.backup'

    @classmethod
    def backupToyboxes(cls):
        toyboxes_folder = Toybox.toyboxesFolder()
        toyboxes_backup_folder = Toybox.toyboxesBackupFolder()
        if os.path.exists(toyboxes_folder):
            shutil.move(toyboxes_folder, toyboxes_backup_folder)

    @classmethod
    def restoreToyboxesBackup(cls):
        toyboxes_folder = Toybox.toyboxesFolder()
        if os.path.exists(toyboxes_folder):
            shutil.rmtree(toyboxes_folder)

        toyboxes_backup_folder = Toybox.toyboxesBackupFolder()
        if os.path.exists(toyboxes_backup_folder):
            shutil.move(toyboxes_backup_folder, toyboxes_folder)

    @classmethod
    def dependencyExistsInBackup(cls, dep):
        return os.path.exists(os.path.join(Toybox.toyboxesBackupFolder(), dep.subFolder()))

    @classmethod
    def copyDependencyFromBackup(cls, dep):
        source_path = os.path.join(Toybox.toyboxesBackupFolder(), dep.subFolder())
        if not os.path.exists(source_path):
            raise RuntimeError('Backup from ' + dep.subFolder() + ' cannot be found.')

        shutil.copytree(source_path, os.path.join(Toybox.toyboxesFolder(), dep.subFolder()))

    @classmethod
    def deleteToyboxesBackup(cls):
        toyboxes_backup_folder = Toybox.toyboxesBackupFolder()
        if os.path.exists(toyboxes_backup_folder):
            shutil.rmtree(toyboxes_backup_folder)

    @classmethod
    def findLuaIncludeFileIn(cls, folder, repo_name):
        paths_found = []
        looking_in = Path(folder)
        # -- We use this first pass here instead of just simply os.path.exists()
        # -- because we want the test to be case-sensitive on all platforms,
        # -- so we list what the match are and let glob give us the paths.
        for p in looking_in.glob('**/import.lua'):
            as_string = str(p)
            if len(as_string) > 4:
                paths_found.append(as_string[:-4])
        for p in looking_in.glob('**/' + repo_name + '.lua'):
            as_string = str(p)
            if len(as_string) > 4:
                paths_found.append(as_string[:-4])

        correct_names = [repo_name,
                         'import',
                         os.path.join('Source', repo_name),
                         os.path.join('Source', 'import'),
                         os.path.join('source', repo_name),
                         os.path.join('source', 'import')]
        for path_found in paths_found:
            path_found = path_found[len(folder) + 1:]
            for correct_name in correct_names:
                if path_found == correct_name:
                    return path_found

        return None

    @classmethod
    def findMakefileIn(cls, folder, repo_name):
        potential_names = [repo_name + '.mk',
                           'Makefile',
                           'Makefile.mk']
        for name in potential_names:
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return name

        return None

    @classmethod
    def findIncludeFileIn(cls, folder, repo_name):
        potential_names = [os.path.join(repo_name, repo_name + '.h'),
                           os.path.join(repo_name, 'include.h')]
        for name in potential_names:
            path = os.path.join(folder, name)
            if os.path.exists(path):
                return name

        return None

    @classmethod
    def generateReadMeFile(cls):
        with open(os.path.join(Toybox.toyboxesFolder(), 'README.md'), 'w') as out_file:
            out_file.write('# toyboxes\n')
            out_file.write('\n')
            out_file.write('This folder contains files auto-generated and managed by [**toybox.py**](https://toyboxpy.io).\n')
            out_file.write('\n')
            out_file.write('**!!! DO NOT MODIFY OR PLACE ANYTHING IN THIS FOLDER !!!**\n')
            out_file.write('\n')
            out_file.write('Please [install](https://github.com/toyboxpy/toybox.py#installing) **toybox.py** in order to modify or update the content of this folder.\n')
