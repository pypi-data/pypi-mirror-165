# SPDX-FileCopyrightText: 2022-present toybox.py Contributors
#
# SPDX-License-Identifier: MIT

import subprocess


class Git:
    """Utility methods for git repos."""

    def __init__(self, url):
        """Setup access to the git repo at url."""

        self.url = url
        self.refs = None
        self.tags = None
        self.branches = None

    def git(self, arguments, folder=None):
        commands = ['git'] + arguments.split()
        commands.append(self.url)

        if folder is not None:
            commands.append(folder)

        try:
            process = subprocess.Popen(commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode != 0:
                if str(stdout).startswith('b"usage: git'):
                    # -- git is giving us the usage info back it seems.
                    raise SyntaxError('Invalid git command line')
                else:
                    # -- Or maybe something else went wrong.
                    raise RuntimeError('Error running git: ' + str(stderr)[2:-1].split('\\n')[0])

            # -- Output is bracketed with b'' when converted from bytes.
            return str(stdout)[2:-1]
        except RuntimeError:
            raise
        except SyntaxError:
            raise
        except Exception as e:
            raise RuntimeError('Error running git: ' + str(e))

    def listRefs(self):
        if self.refs is None:
            self.refs = []
            for ref in self.git('ls-remote --refs').split('\\n'):
                refs_index = ref.find('refs/')
                if refs_index >= 0:
                    self.refs.append(ref[refs_index + 5:])

        return self.refs

    def listBranches(self):
        if self.branches is None:
            self.branches = []
            for ref in self.listRefs():
                if ref.startswith('heads/'):
                    self.branches.append(ref[6:])

        return self.branches

    def listTags(self):
        if self.tags is None:
            self.tags = []
            for ref in self.listRefs():
                if ref.startswith('tags/'):
                    tag = ref[5:]
                    if not tag.startswith('@'):
                        self.tags.append(tag)

        return self.tags

    def isABranch(self, name):
        for branch in self.listBranches():
            if branch == name:
                return True

        return False

    def isATag(self, name):
        for tag in self.listTags():
            if tag == name:
                return True

        return False

    def cloneIn(self, tag, folder):
        self.git('clone --quiet --depth 1  --branch ' + tag, folder)
