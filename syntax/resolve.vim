" Vim syntax file
" Language: RESOLVE
" Maintainer: Foster McLane and Mackenzie Binns
" Last Change: 2016-04-03

" guard for other syntaxes
if exists('b:current_syntax')
  finish
endif
let b:current_syntax='resolve'

" comments
syn region resolveBlockComment start='(\*' end='\*)'
syn match resolveComment '\v--.*'

" common
syntax keyword resolveOperator
      \ +
      \ -
      \ *
      \ **
      \ /
      \ =
      \ /=
      \ <
      \ <=
      \ >
      \ >=

" math context
syntax keyword resolveMathConstant
      \ false
      \ true

syntax keyword resolveMathOperator
      \ o

syntax keyword resolveMathType
      \ B
      \ N
      \ Z

" strings
syntax region resolveString start=/"/ skip=/\\"/ end=/"/

" characters
syntax match resolveCharacter "\v'%(.|\\')'"

" numbers
syntax match resolveNumber '\v<\d+>'
syntax match resolveFloat '\v<\d+\.\d+>'

" general
syntax keyword resolveGeneralOperation
      \ Are_Equal
      \ Are_Not_Equal
      \ Read
      \ Replica
      \ Write
      \ Write_Line

" strings
syntax keyword resolveStringOperation
      \ Char_Str_for
      \ DeString
      \ Length
      \ Merger
      \ Prt_Btwn
      \ Reverse

" characters
syntax keyword resolveCharacterOperation
      \ Char_to_Int
      \ Greater
      \ Greater_Or_Equal
      \ Less
      \ Less_Or_Equal

" integers
syntax keyword resolveIntegerOperation
      \ Decrement
      \ Difference
      \ Div
      \ Divide
      \ Increment
      \ Is_Not_Zero
      \ Is_Zero
      \ Mod
      \ Negative
      \ Power
      \ Product
      \ Quotient
      \ Rem
      \ Sum

" booleans
syntax keyword resolveBooleanOperation
      \ And
      \ False
      \ Not
      \ Or
      \ True

" conditionals
syntax keyword resolveConditional
      \ If
      \ else
      \ elseif
      \ end

" loops
syntax keyword resolveLoop
      \ While
      \ do
      \ end

" operators
syntax keyword resolveObjectOperator
      \ =
      \ /=
      \ :=
      \ :=:

" keywords
syntax keyword resolveKeyword
      \ Array
      \ Concept
      \ Constraint
      \ Constraints
      \ Convention
      \ Correspondence
      \ Def
      \ Definition
      \ Enhancement
      \ Facility
      \ Family
      \ Oper
      \ Operation
      \ Proc
      \ Procedure
      \ Property
      \ Pty
      \ Realization
      \ Type
      \ Var
      \ Variable
      \ Variables
      \ Vars
      \ alt
      \ alters
      \ and
      \ by
      \ clears
      \ clr
      \ constraint
      \ constraints
      \ convention
      \ correspondence
      \ decreasing
      \ def
      \ definition
      \ enhanced
      \ ensures
      \ eval
      \ evaluates
      \ exemplar
      \ for
      \ finalization
      \ initialization
      \ if
      \ is
      \ maintaining
      \ mod
      \ modeled
      \ not
      \ oper
      \ operation
      \ or
      \ powerset
      \ pres
      \ preserves
      \ rea
      \ realized
      \ reassigns
      \ replaces
      \ represented
      \ requires
      \ rest
      \ restores
      \ rpl
      \ str
      \ then
      \ type
      \ upd
      \ updates
      \ uses

" types
syntax keyword resolveBuiltinType
      \ Boolean
      \ Char_Str
      \ Character
      \ Integer

" set highlights
highlight default link resolveBlockComment Comment
highlight default link resolveComment Comment

highlight default link resolveMathConstant Constant

highlight default link resolveString String

highlight default link resolveCharacter Character

highlight default link resolveNumber Number
highlight default link resolveFloat Float

highlight default link resolveBooleanOperation Identifier
highlight default link resolveCharacterOperation Identifier
highlight default link resolveGeneralOperation Identifier
highlight default link resolveIntegerOperation Identifier
highlight default link resolveStringOperation Identifier

highlight default link resolveConditional Conditional

highlight default link resolveLoop Repeat

highlight default link resolveOperator Operator
highlight default link resolveMathOperator Operator
highlight default link resolveObjectOperator Operator

highlight default link resolveKeyword Keyword

highlight default link resolveBuiltinType Type
highlight default link resolveMathType Type
