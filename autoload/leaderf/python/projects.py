#!/usr/bin/env python
# -*- coding: utf-8 -*-

import vim
import os
import os.path
import json
from leaderf.utils import *
from leaderf.explorer import *
from leaderf.manager import *
from leaderf.devicons import *


# *****************************************************
# MarksExplorer
# *****************************************************
class ProjectsExplorer(Explorer):
    def __init__(self):
        pass

    def getContent(self, *args, **kwargs):
        return self.getFreshContent()

    def supportsNameOnly(self):
        return True

    def getFreshContent(self, *args, **kwargs):
        filepath = lfEval(
            "expand(get(g:, 'Lf_ProjectFilePath', '~/.LfProjects'))")
        if not os.path.exists(filepath):
            return []

        with open(filepath) as f:
            projects = json.load(f)

        if len(projects) == 0:
            return []

        # from mruExpl.py
        _max_name_len = max(
            int(lfEval("strdisplaywidth('{}')".format(name)))
            for name in projects.keys()
        )

        lines = []
        for name, path in projects.items():
            space_num = _max_name_len - int(
                lfEval("strdisplaywidth('{}')".format(escQuote(name)))
            )
            lines.append(
                "{}{} | {}".format(
                    name,
                    " " * space_num,
                    path,
                )
            )

        self._content = lines
        return lines

    def getStlCategory(self):
        return "Projects"


def _saveProject(name, path):
    filepath = lfEval(
        "expand(get(g:, 'Lf_ProjectFilePath', '~/.LfProjects'))")

    projects = dict()
    if os.path.exists(filepath):
        with open(filepath) as f:
            projects = json.load(f)

    projects[name] = path
    with open(filepath, "w") as f:
        json.dump(projects, f)


def _removeProject(name):
    filepath = lfEval(
        "expand(get(g:, 'Lf_ProjectFilePath', '~/.LfProjects'))")
    if not os.path.exists(filepath):
        return

    with open(filepath) as f:
        projects = json.load(f)

    if len(projects) == 0:
        return

    projects.pop(name, None)
    with open(filepath, "w") as f:
        json.dump(projects, f)


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
        path = _nearestAncestor(root_markers, os.getcwd())
        projectName = lfEval("input('name for project at " + path + ": ')")
        if len(projectName) < 1:
            lfCmd("echo 'project name cannot be empty'")
            return
        _saveProject(projectName, path)
        self._getInstance().exitBuffer()

    def deleteProject(self):
        instance = self._getInstance()
        line = instance.currentLine
        projectName = line.split(None, 2)[0]
        _removeProject(projectName)
        self._getInstance().exitBuffer()

    def _acceptSelection(self, *args, **kwargs):
        if len(args) == 0:
            return
        line = args[0]
        cmd = line.split(None, 2)[2]
        # vim.chdir(cmd)
        # os.chdir(cmd)
        # lfCmd("let g:Lf_WorkingDirectory='"+cmd+"'")
        lfCmd("Leaderf file " + cmd)

    def _getDigest(self, line, mode):
        """
        specify what part in the line to be processed and highlighted
        Args:
            mode: 0, 1, 2, return the whole line
        """
        if not line:
            return ''
        if mode == 0:
            return line
        elif mode == 1:
            return line.split(None, 2)[0]
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
