# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import unittest
import sys
import os

# -- We need to import for our parent folder here.
sys.path.append(os.path.join(sys.path[0], '..'))

from toybox.dependency import Dependency       # noqa: E402
from toybox.dependency import DependencyError  # noqa: E402


class MockGit:
    """Mock of a Git class for the purpose of testing the Dependency class."""

    def __init__(self, tags, branches=[]):
        """Setup access to the git repo at url."""
        self.tags = tags
        self.branches = branches

    def listTags(self):
        return self.tags

    def listBranches(self):
        return self.branches

    def isATag(self, name):
        return name in self.tags

    def isABranch(self, name):
        return name in self.branches


class TestDependency(unittest.TestCase):
    """Unit tests for the Dependency class."""

    def test_addVersions(self):
        dependency = TestDependency.dependencyObject()
        dependency.addVersions('develop')
        self.assertEqual(len(dependency.versions), 1)
        self.assertTrue(dependency.versions[0].isBranch())
        self.assertEqual(dependency.versions[0].original_version, 'develop')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>1.0 <3')
        self.assertEqual(len(dependency.versions), 2)
        self.assertEqual(dependency.versions[0].original_version, '>1.0.0')
        self.assertEqual(dependency.versions[1].original_version, '<3.0.0')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>1 default')
        self.assertEqual(len(dependency.versions), 2)
        self.assertEqual(dependency.versions[0].original_version, '>1.0.0')
        self.assertTrue(dependency.versions[1].isDefault())
        self.assertEqual(dependency.versions[1].original_version, 'default')

        dependency = TestDependency.dependencyObject()
        with self.assertRaises(SyntaxError):
            dependency.addVersions('>1 <=4.5 =4')

    def test_resolveVersion(self):
        dependency = TestDependency.dependencyObject()
        dependency.addVersions('default')
        self.assertEqual(dependency.resolveVersion().original_version, 'default')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>v1.2.3')
        self.assertEqual(dependency.resolveVersion().original_version, 'v3.2.3')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>v1.2.3 default')
        self.assertEqual(dependency.resolveVersion().original_version, 'default')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('3')
        self.assertEqual(dependency.resolveVersion().original_version, 'v3.2.3')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('<2.0.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v1.0.2')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('1.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v1.0.2')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>v1.0.0 <2.0.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v1.0.2')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>v1.0.0 <=2.0.0')
        self.assertEqual(dependency.resolveVersion().original_version, 'v2.0.0')

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('>2.0.0')
        dependency.addVersions('default')
        self.assertEqual(dependency.resolveVersion().original_version, 'default')

        dependency = TestDependency.dependencyObject()
        with self.assertRaises(DependencyError):
            dependency.resolveVersion()

        dependency = TestDependency.dependencyObject()
        dependency.addVersions('3.0.0')
        dependency.addVersions('default')
        with self.assertRaises(DependencyError):
            dependency.resolveVersion()

        dependency = TestDependency.dependencyObject()
        dependency.git = MockGit([])
        dependency.addVersions('>1.0.0')
        dependency.addVersions('default')
        with self.assertRaises(DependencyError):
            dependency.resolveVersion()

        dependency = TestDependency.dependencyObject()
        dependency.addBranch('main')
        self.assertEqual(dependency.resolveVersion().original_version, 'main')

        dependency = TestDependency.dependencyObject()
        dependency.addBranch('test')
        with self.assertRaises(DependencyError):
            dependency.resolveVersion()

    @classmethod
    def dependencyObject(cls):
        dependency = Dependency('toyboxpy.io/DidierMalenfant/MyProject.py')
        dependency.git = MockGit(['v1.0.0', 'v1.0.2', 'v2.0.0', 'v2.1.0', 'v3.0.0', 'v3.2.3'], ['main', 'develop'])
        return dependency


if __name__ == '__main__':
    unittest.main()
