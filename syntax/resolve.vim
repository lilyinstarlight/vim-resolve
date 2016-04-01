" Highlighting
highlight default link resolveBooleanOperations Keyword
highlight default link resolveCharacterOperations Keyword
highlight default link resolveGeneralOperations Keyword
highlight default link resolveIntegerOperations Keyword
highlight default link resolveInterpolatedString Delimiter
highlight default link resolveKeywords Keyword
highlight default link resolveMathOperators Operator
highlight default link resolveMathTypes Type
highlight default link resolveString String
highlight default link resolveStringOperations Keyword

" Match language specific keyword
syntax keyword resolveKeywords 
    \ Array
    \ Concept
    \ Convention
    \ Def
    \ Definition
    \ Facility
    \ Family
    \ If
    \ Oper
    \ Operation
    \ Proc
    \ Procedure
    \ Pty
    \ Realization
    \ Type
    \ Var
    \ Variable
    \ Variables
    \ Vars
    \ While
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
    \ do
    \ else
    \ end
    \ ensures
    \ eval
    \ evaluates
    \ exemplar
    \ for
    \ initialization
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
    
syntax keyword resolveStringOperations
    \ Char_Str_for
    \ DeString
    \ Length
    \ Merger
    \ Prt_Btwn
    \ Reverse
    \ o

syntax keyword resolveMathTypes
    \ B
    \ Boolean
    \ Char_Str
    \ Character
    \ Integer
    \ Z

syntax keyword resolveMathOperators
    \ +
    \ -
    \ *
    \ /
    \ =
    \ /=
    \ <
    \ <=
    \ >
    \ >=
    \ :=
    \ :=:
    \ **

syntax keyword resolveIntegerOperations
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

syntax keyword resolveCharacterOperations
    \ Char_to_Int
    \ Greater
    \ Greater_Or_Equal
    \ Less
    \ Less_Or_Equal

syntax keyword resolveBooleanOperations
    \ And
    \ False
    \ Not
    \ Or
    \ True

syntax keyword resolveGeneralOperations
    \ Are_Equal
    \ Are_Not_Equal
    \ Read
    \ Replica
    \ Write
    \ Write_Line

" Matching surrounded parameters
" syntax match resolveParameter "\(([^)]+)\)"
" syntax match resolveParameter "\[([^\]]+)]"
" syntax match resolveParameter "\{([^\]]+)}"
" syntax match resolveParameter "\<([^\]]+)>"

" Matching Strings
syntax region resolveString start=/"/ skip=/\\"/ end=/"/ contains=resolveInterpolatedWrapper
syntax region resolveInterpolatedWrapper start="\v\\\(\s*" end="\v\s*\)" contained containedin=resolveString contains=resolveInterpolatedString
syntax match resolveInterpolatedString "\v\w+(\(\))?" contained containedin=resolveInterpolatedWrapper

" Matching Numbers
" syntax match resolveNumber "\v<\d+>"
" syntax match resolveNumber "\v<\d+\.\d+>"
" syntax match resolveNumber "\v<\d*\.?\d+([Ee]-?)?\d+>"
" syntax match resolveNumber "\v<0x\x+([Pp]-?)?\x+>"
" syntax match resolveNumber "\v<0b[01]+>"
" syntax match resolveNumber "\v<0o\o+>"
