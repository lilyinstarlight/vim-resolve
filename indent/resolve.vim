" Vim indent file
" Language: RESOLVE
" Maintainer: Foster McLane and Mackenzie Binns
" Last Change: 2016-04-09

" guard against multiple indents
if exists('b:did_indent')
  finish
endif
let b:did_indent=1

" set indent settings
setlocal indentexpr=GetResolveIndent()
setlocal indentkeys+=0=ensures,0=exemplar,0=finalization,0=initialization,0=requires,0=updates,0=uses,0=do,0=else,0=end
setlocal indentkeys-=0{,0},0),:,0#,e
setlocal nosmartindent

let s:declaration='\v\c^\s*<%(Concept|Convention|Correspondance|Def|Definition|Facility|Proc|Procedure|Realization|Type)>'
let s:is='\v\c<is>'
let s:modifier='\v\c^\s*<%(decreasing|enhanced|ensures|exemplar|finalization|initialization|maintaining|realized|requires|updates|uses)>'
let s:conditional='\v\c^\s*<%(do|else|end)>'

" indent function
function! GetResolveIndent()
  " get current line
  let num=v:lnum
  let line=getline(num)

  " get previous (non-blank) line
  let pnum=prevnonblank(num - 1)
  if pnum == 0
    " first line has no indent
    return 0
  endif
  let pline=getline(pnum)

  " get current indent
  let ind=indent(pnum)

  " if the previous line contains a declaration
  if pline =~ s:declaration && pline !~ s:is
    " increase the indent
    let ind+=&sw
  endif

  " if the previous line contains a modifier and this one does not
  if pline =~ s:modifier && line !~ s:modifier
    " decrease the indent
    let ind-=&sw
  endif

  " if the current line contains a modifier and the previous one did not
  if line =~ s:modifier && pline !~ s:modifier
    " increase the indent
    let ind+=&sw
  endif

  " if the current line contains part of a conditional
  if line =~ s:conditional
    " decrease the indent
    let ind-=&sw
  endif

  " special case for multi-line comments
  if pline =~ '\v^\(\*.*\*)'
    " no indent for all in one line
  elseif pline =~ '\v^\(\*'
    " increase by single indent after open parenthesis
    let ind+=1
  elseif line =~ '\v^\*\)'
    " decrease by single indent after close parenthesis
    let ind-=1
  endif

  " return calculated indent
  return ind
endfunction
