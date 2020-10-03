" ============================================================================
" File:        Marks.vim
" Description:
" Author:      Yggdroot <archofortune@gmail.com>
" Website:     https://github.com/Yggdroot
" Note:
" License:     Apache License, Version 2.0
" ============================================================================

if leaderf#versionCheck() == 0
    finish
endif

exec g:Lf_py "import vim, sys, os.path"
exec g:Lf_py "cwd = vim.eval('expand(\"<sfile>:p:h\")')"
exec g:Lf_py "sys.path.insert(0, os.path.join(cwd, 'python'))"
exec g:Lf_py "from projects import *"

function! leaderf#Projects#Maps()
    nmapclear <buffer>
    nnoremap <buffer> <silent> <CR>          :exec g:Lf_py "projectManager.accept()"<CR>
    nnoremap <buffer> <silent> a             :exec g:Lf_py "projectManager.addProject()"<CR>
    nnoremap <buffer> <silent> d             :exec g:Lf_py "projectManager.deleteProject()"<CR>
    nnoremap <buffer> <silent> q             :exec g:Lf_py "projectManager.quit()"<CR>
    nnoremap <buffer> <silent> i             :exec g:Lf_py "projectManager.input()"<CR>
    nnoremap <buffer> <silent> <F1>          :exec g:Lf_py "projectManager.toggleHelp()"<CR>
    if has_key(g:Lf_NormalMap, "Projects")
        for i in g:Lf_NormalMap["Projects"]
            exec 'nnoremap <buffer> <silent> '.i[0].' '.i[1]
        endfor
    endif
endfunction

function! leaderf#Projects#managerId()
    " pyxeval() has bug
    if g:Lf_PythonVersion == 2
        return pyeval("id(projectManager)")
    else
        return py3eval("id(projectManager)")
    endif
endfunction

function! leaderf#Projects#ChDir(dir)
    let dir    = fnameescape(a:dir)
    let curtab = tabpagenr()
    let curwin = winnr()

    silent! exe "cd " . dir
    "
    " for t in range(1, tabpagenr("$"))
    "     silent! exe "noautocmd tabnext " . t
    "
    "     for w in range(1, winnr("$"))
    "         silent! exe "noautocmd " . w . "wincmd w"
    "
    "         if haslocaldir()
    "             silent! exe "lcd " . dir
    "         endif
    "     endfor
    " endfor
    "
    silent! exe "noautocmd tabnext " . curtab
    silent! exe "noautocmd " . curwin . "wincmd w"
endfunction

