# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import json
import os

from toybox.dependency import Dependency


class Boxfile:
    """Read and parse a toybox config file."""

    def __init__(self, boxfile_folder):
        """Read the Boxfile for the current folder."""

        self.boxfile_path = os.path.join(boxfile_folder, 'Boxfile')
        self.dependencies = []
        self.json_content = {}

        if not os.path.exists(self.boxfile_path):
            # -- If we can't find it we may still create it later.
            return

        try:
            with open(self.boxfile_path, 'r') as file:
                self.json_content = json.load(file)
        except Exception as e:
            raise SyntaxError('Malformed JSON in Boxfile \'' + self.boxfile_path + '\'.\n' + str(e) + '.')

        for key in self.json_content.keys():
            self.addDependency(key, self.json_content[key])

    def addDependency(self, url, versions_as_string):
        new_dependency = Dependency(url)
        new_dependency.addVersions(versions_as_string)

        for dep in self.dependencies:
            if dep.url == new_dependency.url:
                raise SyntaxError('Dependency for URL \'' + dep.url + '\' already exists.')

        self.dependencies.append(new_dependency)

        self.json_content[url] = versions_as_string

    def removeDependency(self, url):
        if url not in self.json_content:
            raise SyntaxError('Couldn\'t find any dependency for URL \'' + url + '\'.')

        self.json_content.pop(url, None)

        dependency_to_remove = Dependency(url)
        dependency_to_remove.deleteFolder()

        for dep in self.dependencies:
            if dep.url == dependency_to_remove.url:
                self.dependencies.remove(dep)
                return

    def save(self):
        out_file = open(self.boxfile_path, 'w')
        json.dump(self.json_content, out_file, indent=4)

        out_file.close()
