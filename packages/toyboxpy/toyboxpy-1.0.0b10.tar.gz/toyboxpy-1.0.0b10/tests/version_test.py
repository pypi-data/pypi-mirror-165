# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import unittest
import sys
import os

# -- We need to import for our parent folder here.
sys.path.append(os.path.join(sys.path[0], '..'))

from toybox.version import Version       # noqa: E402
from toybox.version import VersionIs     # noqa: E402


class TestVersion(unittest.TestCase):
    """Unit tests for the Version class."""

    def test_Version(self):
        with self.assertRaises(ValueError):
            Version('34.2')

        with self.assertRaises(ValueError):
            Version('test')

        version = Version('0.0.0')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 0)
        self.assertEqual(version.asSemVer.minor, 0)
        self.assertEqual(version.asSemVer.patch, 0)
        self.assertEqual(str(version), '0.0.0')
        self.assertEqual(version.original_version, '0.0.0')

        version = Version('5.12.4')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '5.12.4')
        self.assertEqual(version.original_version, '5.12.4')

        version = Version('v5.12.4')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '5.12.4')
        self.assertEqual(version.original_version, 'v5.12.4')

        version = Version('>5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>5.12.4')
        self.assertEqual(version.original_version, '>5.12.4')

        version = Version('>v5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>5.12.4')
        self.assertEqual(version.original_version, '>v5.12.4')

        version = Version('>=5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>=5.12.4')
        self.assertEqual(version.original_version, '>=5.12.4')

        version = Version('>=v5.12.4')
        self.assertEqual(version.operator, VersionIs.greater_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '>=5.12.4')
        self.assertEqual(version.original_version, '>=v5.12.4')

        version = Version('<5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<5.12.4')
        self.assertEqual(version.original_version, '<5.12.4')

        version = Version('<v5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<5.12.4')
        self.assertEqual(version.original_version, '<v5.12.4')

        version = Version('<=5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<=5.12.4')
        self.assertEqual(version.original_version, '<=5.12.4')

        version = Version('<=v5.12.4')
        self.assertEqual(version.operator, VersionIs.less_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 12)
        self.assertEqual(version.asSemVer.patch, 4)
        self.assertEqual(str(version), '<=5.12.4')
        self.assertEqual(version.original_version, '<=v5.12.4')

    def test_defaultVersionWith(self):
        version = Version.defaultVersionWith('3.4.2')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(str(version), '3.4.2(default)')
        self.assertEqual(version.original_version, 'default')
        self.assertTrue(version.isDefault())

        with self.assertRaises(SyntaxError):
            version = Version.defaultVersionWith('<3.4.2')

        with self.assertRaises(SyntaxError):
            version = Version.defaultVersionWith('<=3.4.2')

        with self.assertRaises(SyntaxError):
            version = Version.defaultVersionWith('>3.4.2')

        with self.assertRaises(SyntaxError):
            version = Version.defaultVersionWith('>=3.4.2')

    def test_branchVersionWith(self):
        version = Version.branchVersionWith('main')
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(str(version), 'main(branch)')
        self.assertEqual(version.original_version, 'main')
        self.assertTrue(version.isBranch())

    def test_operatorEqual(self):
        self.assertTrue(Version('5.12.4') == Version('5.12.4'))
        self.assertTrue(Version('<5.12.4') == Version('<5.12.4'))
        self.assertTrue(Version('<=5.12.4') == Version('<=5.12.4'))
        self.assertTrue(Version('>5.12.4') == Version('>5.12.4'))
        self.assertTrue(Version('>=5.12.4') == Version('>=5.12.4'))

        self.assertFalse(Version('5.12.4') == Version('5.13.4'))
        self.assertFalse(Version('>=5.12.4') == Version('<5.13.4'))
        self.assertFalse(Version('5.12.4') == Version('>5.12.4'))
        self.assertFalse(Version('>=5.12.4') == Version('5.12.4'))

        self.assertTrue(Version.defaultVersionWith('3.4.2') == Version.defaultVersionWith('3.4.2'))

    def test_versionsFrom(self):
        versions = Version.versionsFrom('3.4.2')
        self.assertEqual(len(versions), 1)
        version = versions[0]
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 3)
        self.assertEqual(version.asSemVer.minor, 4)
        self.assertEqual(version.asSemVer.patch, 2)
        self.assertEqual(str(version), '3.4.2')

        versions = Version.versionsFrom('v1.0.12')
        self.assertEqual(len(versions), 1)
        version = versions[0]
        self.assertEqual(version.operator, VersionIs.equal)
        self.assertEqual(version.asSemVer.major, 1)
        self.assertEqual(version.asSemVer.minor, 0)
        self.assertEqual(version.asSemVer.patch, 12)
        self.assertEqual(str(version), '1.0.12')

        versions = Version.versionsFrom('2')
        self.assertEqual(len(versions), 2)
        version = versions[0]
        self.assertEqual(version.operator, VersionIs.greater_than_or_equal)
        self.assertEqual(version.asSemVer.major, 2)
        self.assertEqual(version.asSemVer.minor, 0)
        self.assertEqual(version.asSemVer.patch, 0)
        self.assertEqual(str(version), '>=2.0.0')
        version = versions[1]
        self.assertEqual(version.operator, VersionIs.less_than)
        self.assertEqual(version.asSemVer.major, 3)
        self.assertEqual(version.asSemVer.minor, 0)
        self.assertEqual(version.asSemVer.patch, 0)
        self.assertEqual(str(version), '<3.0.0')

        versions = Version.versionsFrom('1.4')
        self.assertEqual(len(versions), 2)
        version = versions[0]
        self.assertEqual(version.operator, VersionIs.greater_than_or_equal)
        self.assertEqual(version.asSemVer.major, 1)
        self.assertEqual(version.asSemVer.minor, 4)
        self.assertEqual(version.asSemVer.patch, 0)
        self.assertEqual(str(version), '>=1.4.0')
        version = versions[1]
        self.assertEqual(version.operator, VersionIs.less_than)
        self.assertEqual(version.asSemVer.major, 1)
        self.assertEqual(version.asSemVer.minor, 5)
        self.assertEqual(version.asSemVer.patch, 0)
        self.assertEqual(str(version), '<1.5.0')

        versions = Version.versionsFrom('>10.2.9')
        self.assertEqual(len(versions), 1)
        version = versions[0]
        self.assertEqual(version.operator, VersionIs.greater_than)
        self.assertEqual(version.asSemVer.major, 10)
        self.assertEqual(version.asSemVer.minor, 2)
        self.assertEqual(version.asSemVer.patch, 9)
        self.assertEqual(str(version), '>10.2.9')

        versions = Version.versionsFrom('<=v5.5')
        self.assertEqual(len(versions), 1)
        version = versions[0]
        self.assertEqual(version.operator, VersionIs.less_than_or_equal)
        self.assertEqual(version.asSemVer.major, 5)
        self.assertEqual(version.asSemVer.minor, 5)
        self.assertEqual(version.asSemVer.patch, 0)
        self.assertEqual(str(version), '<=5.5.0')

        with self.assertRaises(ValueError):
            Version.versionsFrom('<3.4.2 >3 <5')

    def test_includes(self):
        with self.assertRaises(SyntaxError):
            Version('<3.4.2').includes(Version('>3.4.2'))

        self.assertTrue(Version('3.4.2').includes(Version('3.4.2')))
        self.assertFalse(Version('3.4.2').includes(Version('3.40.2')))

        self.assertTrue(Version('>3.4.2').includes(Version('3.40.2')))
        self.assertFalse(Version('>3.4.2').includes(Version('3.3.2')))

        self.assertTrue(Version('<3.4.2').includes(Version('3.3.2')))
        self.assertFalse(Version('<3.4.2').includes(Version('3.4.2')))

        self.assertTrue(Version('>=3.4.2').includes(Version('3.4.2')))
        self.assertTrue(Version('>=3.4.2').includes(Version('3.40.2')))
        self.assertFalse(Version('>=3.4.2').includes(Version('3.3.2')))

        self.assertTrue(Version('<=3.4.2').includes(Version('3.4.2')))
        self.assertTrue(Version('<=3.4.2').includes(Version('3.3.2')))
        self.assertFalse(Version('<=3.4.2').includes(Version('5.4.1')))

        self.assertTrue(Version.defaultVersionWith('5.2.1').includes(Version.defaultVersionWith('5.2.1')))
        self.assertFalse(Version.defaultVersionWith('5.2.1').includes(Version.defaultVersionWith('5.3.1')))
        self.assertFalse(Version.defaultVersionWith('5.2.1').includes(Version('5.2.1')))
        self.assertFalse(Version.defaultVersionWith('5.2.1').includes(Version('3.4.2')))

        self.assertTrue(Version.branchVersionWith('main').includes(Version.branchVersionWith('main')))
        self.assertFalse(Version.branchVersionWith('main').includes(Version.branchVersionWith('test')))
        self.assertFalse(Version.branchVersionWith('main').includes(Version('3.4.2')))

    def test_includedVersionsIn(self):
        self.assertEqual(Version('<5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('3.2.1'), Version('4.2.1')])

        self.assertEqual(Version('<3.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('<=5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('3.2.1'), Version('4.2.1'), Version('5.0.0')])

        self.assertEqual(Version('<=2.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('4.2.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('4.2.1')])

        self.assertEqual(Version('4.3.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('>4.3.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('5.0.0'), Version('5.2.1')])

        self.assertEqual(Version('>6.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        self.assertEqual(Version('>=5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [Version('5.0.0'), Version('5.2.1')])

        self.assertEqual(Version('>=5.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')]),
                         [])

        defaultVersion = Version.defaultVersionWith('5.2.1')
        self.assertEqual(defaultVersion.includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), defaultVersion]),
                         [defaultVersion])
        self.assertEqual(Version('5.2.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), defaultVersion]),
                         [Version('5.2.1')])
        self.assertEqual(Version('>=4.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), defaultVersion]),
                         [Version('5.0.0'), Version('5.2.1'), defaultVersion])
        self.assertEqual(Version('<5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), defaultVersion]),
                         [Version('3.2.1'), Version('4.2.1')])
        self.assertEqual(Version('<6.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), defaultVersion]),
                         [Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), defaultVersion])

        branchVersion = Version.branchVersionWith('develop')
        self.assertEqual(branchVersion.includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [branchVersion])
        self.assertEqual(Version('5.2.1').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('5.2.1')])
        self.assertEqual(Version('>=4.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('5.0.0'), Version('5.2.1')])
        self.assertEqual(Version('<5.0.0').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('3.2.1'), Version('4.2.1')])
        self.assertEqual(Version('<6.8.4').includedVersionsIn([Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1'), branchVersion]),
                         [Version('3.2.1'), Version('4.2.1'), Version('5.0.0'), Version('5.2.1')])


if __name__ == '__main__':
    unittest.main()
