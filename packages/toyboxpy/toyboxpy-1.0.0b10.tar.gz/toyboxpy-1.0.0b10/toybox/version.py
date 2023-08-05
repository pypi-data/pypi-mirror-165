# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import enum

from semver import VersionInfo


class VersionIs(enum.Enum):
    """The possible outcomes of a comparison."""

    equal = 1
    less_than = 2
    less_than_or_equal = 3
    greater_than = 4
    greater_than_or_equal = 5


class Version:
    """A helper class to compare dependency versions."""

    def __init__(self, version_as_string):
        """Create a version number from a string."""
        """Format can be simply a full semver version number (i.e. 3.2.5) to point to an exact version,"""
        """or a partial one (i.e. 3 or 3.2) to require any given major or minor version."""
        """It can also have a comparison operator as a prefix (i.e. '>3.0,2' or '<=3.4')."""

        self.original_version = version_as_string

        if version_as_string.startswith('>'):
            if version_as_string.startswith('>='):
                self.operator = VersionIs.greater_than_or_equal
                version_as_string = version_as_string[2:]
            else:
                self.operator = VersionIs.greater_than
                version_as_string = version_as_string[1:]
        elif version_as_string.startswith('<'):
            if version_as_string.startswith('<='):
                self.operator = VersionIs.less_than_or_equal
                version_as_string = version_as_string[2:]
            else:
                self.operator = VersionIs.less_than
                version_as_string = version_as_string[1:]
        else:
            self.operator = VersionIs.equal

        if version_as_string.startswith('v'):
            version_as_string = version_as_string[1:]

        self.asSemVer = VersionInfo.parse(version_as_string)

    def __eq__(self, other):
        if self.asSemVer != other.asSemVer:
            return False

        if self.operator != other.operator:
            return False

        self_is_default = self.isDefault()
        other_is_default = other.isDefault()
        return self_is_default == other_is_default

    def __lt__(a, b):
        return a.asSemVer < b.asSemVer

    def __gt__(a, b):
        return a.asSemVer < b.asSemVer

    def __str__(self):
        switch = {
            VersionIs.equal: '',
            VersionIs.less_than: '<',
            VersionIs.less_than_or_equal: '<=',
            VersionIs.greater_than: '>',
            VersionIs.greater_than_or_equal: '>='
        }

        if self.isBranch():
            version_string = self.original_version + '(branch)'
        else:
            version_string = switch.get(self.operator) + str(self.asSemVer)

        if self.isDefault():
            version_string += '(default)'

        return version_string

    def isDefault(self):
        return self.original_version == 'default'

    def isBranch(self):
        return self.asSemVer is None

    def includes(self, other):
        if other.operator != VersionIs.equal:
            raise SyntaxError('Right hand operand must be an exact version number, not a range.')

        if self.operator is VersionIs.equal:
            self_is_branch = self.isBranch()
            other_is_branch = other.isBranch()
            if self_is_branch or other_is_branch:
                return self_is_branch == other_is_branch and self.original_version == other.original_version

            return self.isDefault() == other.isDefault() and other.asSemVer == self.asSemVer
        elif self.operator is VersionIs.less_than:
            return other.isBranch() is False and other.asSemVer < self.asSemVer
        elif self.operator is VersionIs.less_than_or_equal:
            return other.isBranch() is False and other.asSemVer <= self.asSemVer
        elif self.operator is VersionIs.greater_than:
            return other.isBranch() is False and other.asSemVer > self.asSemVer
        else:
            return other.isBranch() is False and other.asSemVer >= self.asSemVer

    def includedVersionsIn(self, list):
        result = []

        for version in list:
            if self.includes(version):
                result.append(version)

        return result

    @classmethod
    def defaultVersionWith(cls, version_as_string):
        new_version = Version(version_as_string)

        if new_version.operator != VersionIs.equal:
            raise SyntaxError('Can\'t make a default version with operator ' + str(new_version.operator) + '.')

        new_version.original_version = 'default'

        return new_version

    @classmethod
    def branchVersionWith(cls, branch_as_string):
        new_version = Version('1.0.0')

        new_version.original_version = branch_as_string
        new_version.asSemVer = None

        return new_version

    @classmethod
    def versionsFrom(cls, version_as_string):
        versions = []

        components = version_as_string.split('.')
        nb_of_components = len(components)
        if nb_of_components > 3:
            raise SyntaxError('Malformed version \'' + version_as_string + '\' (too many components).')

        nb_of_components_added = 0

        for i in range(nb_of_components, 3):
            # -- If we're missing any minor or patch numbers, we set them as 0.
            version_as_string += '.0'
            nb_of_components_added += 1

        if version_as_string.startswith('>') or version_as_string.startswith('<'):
            nb_of_components_added = 0

        if nb_of_components_added != 0:
            version_as_string = '>=' + version_as_string

        new_version = Version(version_as_string)
        versions.append(new_version)

        if nb_of_components_added == 1:
            top_bracket = new_version.asSemVer.bump_minor()
            top_bracket_as_string = '<' + str(top_bracket)
            versions.append(Version(top_bracket_as_string))
        elif nb_of_components_added == 2:
            top_bracket = new_version.asSemVer.bump_major()
            top_bracket_as_string = '<' + str(top_bracket)
            versions.append(Version(top_bracket_as_string))

        return versions
