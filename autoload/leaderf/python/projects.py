#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import os
import os.path
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.devicons import *

NO_CONTENT = "NO CONTENT"

# *****************************************************
# MarksExplorer
# *****************************************************


class ProjectsExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        return self.getFreshContent()

    def getFreshContent(self, *args, **kwargs):
        filepath = lfEval(
            "expand(get(g:, 'Lf_ProjectFilePath', '~/.LfProjects'))")
        if not os.path.exists(filepath):
            return [NO_CONTENT]

        with lfOpen(filepath) as f:
            projects = f.read().splitlines()

        if len(projects) == 0:
            return [NO_CONTENT]

        self._content = projects
        return projects

    def getStlCategory(self):
        return "Projects"


def _saveProject(path):
    filepath = lfEval(
        "expand(get(g:, 'Lf_ProjectFilePath', '~/.LfProjects'))")

    projects = []
    if os.path.exists(filepath):
        with lfOpen(filepath) as f:
            projects = f.read().splitlines()

    projects.append(path)
    with lfOpen(filepath, "w") as f:
        f.write("\n".join(sorted(set(projects))))


def _removeProject(path):
    filepath = lfEval(
        "expand(get(g:, 'Lf_ProjectFilePath', '~/.LfProjects'))")
    if not os.path.exists(filepath):
        return

    projects = []
    with lfOpen(filepath) as f:
        projects = f.read().splitlines()

    if len(projects) == 0:
        return

    if path not in projects:
        return

    projects.remove(path)
    with lfOpen(filepath, "w") as f:
        f.write("\n".join(projects))


def _nearestAncestor(markers, path):
    """
    return the nearest ancestor path(including itself) of `path` that contains
    one of files or directories in `markers`.
    `markers` is a list of file or directory names.
    """
    if os.name == 'nt':
        # e.g. C:\\
        root = os.path.splitdrive(os.path.abspath(path))[0] + os.sep
    else:
        root = '/'

    path = os.path.abspath(path)
    while path != root:
        for name in markers:
            if os.path.exists(os.path.join(path, name)):
                return path
        path = os.path.abspath(os.path.join(path, ".."))

    for name in markers:
        if os.path.exists(os.path.join(path, name)):
            return path

    return ""

# *****************************************************
# MarksExplManager
# *****************************************************


class ProjectManager(Manager):
    def __init__(self):
        super(ProjectManager, self).__init__()

    def _getExplClass(self):
        return ProjectsExplorer

    def _defineMaps(self):
        lfCmd("call leaderf#Projects#Maps()")

    def addProject(self):
        instance = self._getInstance()
        root_markers = lfEval("g:Lf_RootMarkers")
        cwd = os.getcwd()
        path = _nearestAncestor(root_markers, cwd)
        if len(path) < 1:
            path = cwd
        path = lfEval('input("add to projects: ", "'+path+'")')
        _saveProject(path)
        if not path:
            lfCmd("redraw | echo 'cancelled'")
            return
        lfCmd("redraw | echo 'added "+path+"'")
        self._getInstance().exitBuffer()

    def deleteProject(self):
        instance = self._getInstance()
        line = instance.currentLine
        confirm = lfEval(
            'confirm("remove \\"'+line+'?\\"", "&Yes\n&No\n&Cancel")')
        if confirm == "1":
            _removeProject(line)
            lfCmd("redraw | echo 'removed.'")
            self._getInstance().exitBuffer()
        else:
            lfCmd("redraw | echo 'cancelled'")

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        # vim.chdir(cmd)
        # os.chdir(cmd)
        # lfCmd("let g:Lf_WorkingDirectory='"+cmd+"'")
        lfCmd("Leaderf file " + line)

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, 1, 2, return the whole line
        """
        return line

    def _getDigestStartPos(self, line, mode):
        """
        return the start position of the digest returned by _getDigest()
        Args:
            mode: 0, 1, 2, return 1
        """
        return 0

    def _createHelp(self):
        help = []
        help.append('" <CR>/<double-click>/o : execute command under cursor')
        help.append('" a : saves current project location')
        help.append('" d : deletes the project')
        help.append('" i : switch to input mode')
        help.append('" q : quit')
        help.append('" <F1> : toggle this help')
        help.append(
            '" ---------------------------------------------------------')
        return help


# *****************************************************
# marksExplManager is a singleton
# *****************************************************
projectManager = ProjectManager()

__all__ = ['projectManager']
