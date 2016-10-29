" Vim indent file
" Language: RESOLVE
" Maintainer: Foster McLane and Mackenzie Binns
" Last Change: 2016-10-29

" guard against multiple indents
if exists('b:did_indent')
  finish
endif
let b:did_indent=1

" set indent settings
setlocal indentexpr=GetResolveIndent(v:lnum)
setlocal indentkeys+=0=ensures,0=exemplar,0=finalization,0=initialization,0=requires,0=updates,0=uses,0=do,0=else,0=end
setlocal indentkeys-=0{,0},0),:,0#,e
setlocal nosmartindent

let s:declaration='\v\c^\s*<%(Concept|Convention|Correspondance|Facility|Realization|Type)>'
let s:procedure='\v\c^\s*<%(Proc|Procedure)>'
let s:is='\v\c<is>'
let s:modifier='\v\c^\s*<%(changing|decreasing|ensures|exemplar|finalization|initialization|maintaining|requires|updates)>'
let s:conditional='\v\c^\s*<%(If|While)>'
let s:conditionalpart='\v\c^\s*<%(do|else|elseif)>'
let s:end='\v\c^\s*<%(end)>'

" comment and whitespace cleanup function
function! CleanResolve(line)
  let line = a:line

  let line = substitute(line, '--.*$', '', '')
  let line = substitute(line, '^\s*', '', '')
  let line = substitute(line, '\s*$', '', '')
  let line = substitute(line, '(\*.*\*)', '', '')

  return line
endfunction

" check if line is inside of a multiline comment
function! IsResolveComment(lnum)
  let lnum=a:lnum-1
  let line=getline(lnum)

  let c=-(getline(a:lnum) =~ '\v\*\)')

  while lnum > 0
    if line =~ '\v\(\*'
      let c+=1
    endif

    if line =~ '\v\*\)'
      let c-=1
    endif

    let lnum-=1
    let line=getline(lnum)
  endwhile

  return c > 0
endfunction

function! GetResolvePrevious(num)
  if a:num == 0
    return 0
  endif

  let pnum=a:num-1
  let pline=CleanResolve(getline(pnum))
  while pline =~ '\v^$' || pline =~ '\v\*\)$' || pline =~ '\v^\(\*' || IsResolveComment(pnum)
    if pnum == 0
      return pnum
    endif

    let pnum-=1
    let pline=CleanResolve(getline(pnum))
  endwhile

  return pnum
endfunction

" indent function
function! GetResolveIndent(lnum)
  " get current line
  let num=a:lnum
  let line=CleanResolve(getline(num))

  " get previous line
  let pnum=GetResolvePrevious(num)
  " no indent on first line
  if pnum == 0
    return 0
  endif
  let pline=CleanResolve(getline(pnum))

  " get previous previous line
  let ppnum=GetResolvePrevious(pnum)
  if ppnum == 0
    let ppline=''
  else
    let ppline=CleanResolve(getline(ppnum))
  endif

  " get current indent
  let ind=indent(pnum)

  " do not change indentation inside of comments
  if IsResolveComment(num-1)
    return indent(num-1)
  endif

  " detect beginning and end of multi-line comments
  if line =~ '\v^\s*\*'
    if getline(num-1) =~ '\v\(\*'
      let ind+=1
    elseif line =~ '\v\*\)'
      let ind-=1
    endif
  " if the previous line contains a declaration
  elseif pline =~ s:declaration && pline !~ s:is
    let ind+=&sw
  " if the previous line started a procedure
  elseif pline =~ s:procedure
    let ind+=&sw
  " if the current line contains part of a conditional
  elseif pline =~ s:conditional
    if line !~ s:conditionalpart
      let ind+=&sw
    endif
  " if line is a conditional part
  elseif line =~ s:conditionalpart
    let ind-=&sw
  " if line follows a conditional part
  elseif pline =~ s:conditionalpart
    let ind+=&sw
  " if line is an end
  elseif line =~ s:end
    let ind-=&sw
  " if the previous line contains a modifier and this one does not
  elseif pline =~ s:modifier && line !~ s:modifier
    let ind-=&sw
  " if the current line contains a modifier and the previous one did not
  elseif line =~ s:modifier && pline !~ s:modifier
    let ind+=&sw
  " if previous line did not end on a semicolon
  elseif ppline =~ '\v\c;$' && pline !~ '\v;$'
    let ind+=&sw
  " if we indented the previous line because there was not a semicolon
  elseif ppline !~ '\v;$' && pline =~ '\v\c;$' && ppline !~ s:procedure && ppline !~ s:conditional && ppline !~ s:conditionalpart
    let ind-=&sw
  endif

  " return calculated indent
  return ind
endfunction
