" ============================================================================
" File:        leaderf.vim
" Description:
" Author:      Freehaha <freehaha@gmail.com>
" Website:     https://github.com/freehaha
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

" Definition of 'arguments' can be similar as
" https://github.com/Yggdroot/LeaderF/blob/master/autoload/leaderf/Any.vim#L85-L140
let s:extension = {
            \   "name": "projects",
            \   "help": "save and switch to projects",
            \   "manager_id": "leaderf#Projects#managerId",
            \   "arguments": [
            \   ]
            \ }
" In order that `Leaderf marks` is available
call g:LfRegisterPythonExtension(s:extension.name, s:extension)

command! -bar -nargs=0 LeaderfProjects Leaderf projects

" In order to be listed by :LeaderfSelf
call g:LfRegisterSelf("LeaderfProjects", "save and jump to projects")
