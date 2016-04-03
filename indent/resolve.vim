" Vim indent file
" Language: RESOLVE
" Maintainer: Foster McLane and Mackenzie Binns
" Last Change: 2016-04-03

" guard against multiple indents
if exists("b:did_indent")
  finish
endif
let b:did_indent=1

" set indent settings
setlocal indentexpr=GetResolveIndent()
setlocal indentkeys+=0=do,0=else,0=end
setlocal indentkeys-=0{,0},0),:,0#,e
setlocal nosmartindent

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

	" if previous line contained a special set of keywords
	if pline =~ '\v\c^\s*<%(Concept|Convention|Correspondance|Facility|If|Initialization|Procedure|Realization|Type|While)>'
		" increase the indent
		let ind+=&sw
	endif
	" if the current line contains a special set of keywords
	if line =~ '\v\c^\s*<%(Operation|do|else|end)>'
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
