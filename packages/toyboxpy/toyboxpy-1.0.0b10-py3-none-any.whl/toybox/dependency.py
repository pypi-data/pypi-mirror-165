# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import os
import shutil

from toybox.git import Git
from toybox.version import Version
from toybox.exceptions import DependencyError


class Dependency:
    """A helper class for toybox dependencies."""

    def __init__(self, url):
        """Create a dependency given a URL and a tag or branch."""

        self.url = url

        if not self.url.endswith('.git'):
            self.url = self.url + '.git'

        if not self.url.startswith('http://'):
            if not self.url.startswith('https'):
                # -- Let's make sure there is a .com,.net,etc.. before the first slash in the path.
                # -- Github usernames cannot have dots in them so testing like this should be ok.
                first_dot_index = self.url.find('.')
                first_slash_index = self.url.find('/')

                if first_dot_index < 0 or first_dot_index > first_slash_index:
                    # -- We assume a url with no server is one from Github.
                    if not self.url.startswith('/'):
                        self.url = '/' + self.url

                    self.url = 'https://github.com' + self.url
                else:
                    self.url = 'https://' + self.url

        # -- dependency_path is a simplified url without the protocol or the .git in the string.
        if self.url.startswith('http://'):
            self.dependency_path = self.url[7:-4]
        elif self.url.startswith('https://'):
            self.dependency_path = self.url[8:-4]
        else:
            raise SyntaxError('Malformed dependency URL \'' + url + '\' in Boxfile.')

        dependency_path_components = self.dependency_path.split('/')
        if len(dependency_path_components) != 3:
            raise SyntaxError('Malformed dependency URL \'' + url + '\' in Boxfile.')

        self.server = dependency_path_components[0]
        self.username = dependency_path_components[1]
        self.repo_name = dependency_path_components[2]

        self.git = Git(self.url)

        self.versions = []
        self.tag_versions = None
        self.default_version = None
        self.last_version_installed = None

    def __str__(self):
        string_version = self.dependency_path + '@'

        if len(self.versions) > 1:
            string_version += '('

        separator = ''
        for version in self.versions:
            string_version += separator + version.original_version
            separator = ' '

        if len(self.versions) > 1:
            string_version += ')'

        return string_version

    def subFolder(self):
        return os.path.join(self.server, self.username, self.repo_name)

    def resolveVersion(self):
        branch = None
        versions = None

        try:
            for version in self.versions:
                if version.isBranch():
                    if branch is not None:
                        raise DependencyError

                    if version.original_version in self.git.listBranches():
                        branch = version
                else:
                    if branch is not None:
                        raise DependencyError

                    if versions is None:
                        versions = self.listTagVersions()
                        versions.append(self.defaultVersion())

                    versions = version.includedVersionsIn(versions)

            if branch is not None:
                return branch
            elif versions is None:
                raise DependencyError
            else:
                if len(versions) > 1 and versions[-1].isDefault():
                    versions = versions[:-1]

                if len(versions) > 0:
                    return versions[-1]
                else:
                    raise DependencyError
        except DependencyError:
            raise DependencyError('Can\'t resolve version with \'' + self.versionsAsString() + '\' for \'' + self.url + '\'.')

    def addVersions(self, versions_as_string):
        separated_versions = versions_as_string.split(' ')
        if len(separated_versions) > 2:
            raise SyntaxError('Malformed version string \'' + versions_as_string + '\' (too many versions).')

        for version_as_string in separated_versions:
            if version_as_string == 'default':
                self.versions.append(self.defaultVersion())
            elif self.isABranch(version_as_string):
                self.versions.append(Version.branchVersionWith(version_as_string))
            else:
                for version in Version.versionsFrom(version_as_string):
                    self.versions.append(version)

    def addBranch(self, branch_as_string):
        self.versions.append(Version.branchVersionWith(branch_as_string))

    def isATag(self, name):
        return self.git.isATag(name)

    def isABranch(self, name):
        return self.git.isABranch(name)

    def listTagVersions(self):
        if self.tag_versions is None:
            self.tag_versions = []

            for tag in self.git.listTags():
                try:
                    self.tag_versions.append(Version(tag))
                except ValueError:
                    pass

            self.tag_versions = sorted(self.tag_versions)

        return self.tag_versions

    def defaultVersion(self):
        if self.default_version is None:
            all_versions = self.listTagVersions()

            if len(all_versions) > 0:
                highest_version = all_versions[-1]
            else:
                highest_version = Version('0.0.1')

            self.default_version = Version.defaultVersionWith(str(highest_version.asSemVer))

        return self.default_version

    def versionsAsString(self):
        versions_as_string = ''

        for version in self.versions:
            if len(versions_as_string) != 0:
                versions_as_string += ' '

            versions_as_string += version.original_version

        return versions_as_string

    def installIn(self, toyboxes_folder):
        version_resolved = self.resolveVersion()

        if version_resolved is None:
            raise DependencyError('Can\'t resolve version with \'' + self.versionsAsString() + '\' for \'' + self.url + '\'.')

        if self.last_version_installed is not None and self.last_version_installed.original_version == version_resolved.original_version:
            return

        folder = os.path.join(toyboxes_folder, self.subFolder())

        if os.path.exists(folder):
            shutil.rmtree(folder)

        os.makedirs(folder, exist_ok=True)

        self.git.cloneIn(version_resolved.original_version, folder)

        dependency_git_folder = os.path.join(folder, '.git')
        if os.path.exists(dependency_git_folder):
            shutil.rmtree(dependency_git_folder)

        self.last_version_installed = version_resolved

        return version_resolved

    def deleteFolderIn(self, toyboxes_folder):
        folder = os.path.join(toyboxes_folder, self.subFolder())

        if os.path.exists(folder):
            shutil.rmtree(folder)
