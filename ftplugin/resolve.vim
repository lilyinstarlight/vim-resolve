" Vim filetype plugin file
" Language: RESOLVE
" Maintainer: Foster McLane and Mackenzie Binns
" Last Change: 2016-04-04

" guard against multiple ftplugins
if exists('b:did_ftplugin')
  finish
endif
let b:did_ftplugin=1

" save cpoptions
let s:cpoptions_save=&cpoptions
set cpoptions&vim

" tabbing settings
setlocal tabstop=4
setlocal softtabstop=4
setlocal shiftwidth=4
setlocal expandtab

" comment information
setlocal comments=sO:*\ -,mO:*\ \ ,exO:*),s1:(*,mb:*,ex:*),:--
setlocal commentstring=--%s

" formatting options
setlocal formatoptions-=t
setlocal formatoptions+=croql

" restore cpoptions
let &cpoptions=s:cpoptions_save
unlet s:cpoptions_save
