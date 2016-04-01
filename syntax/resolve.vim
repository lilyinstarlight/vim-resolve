" Match language specific keyword
syntax keyword resolveKeywords 
    \ Array
    \ Concept
    \ Facility
    \ Family
    \ If
    \ Main
    \ Operation
    \ Procedure
    \ Realization
    \ Type
    \ Var
    \ While
    \ alters
    \ and
    \ by
    \ clears
    \ constraint
    \ convention
    \ correspondence
    \ decreasing
    \ do
    \ else
    \ end
    \ ensures
    \ evaluates
    \ exemplar
    \ for
    \ initialization
    \ is
    \ maintaining
    \ mod
    \ modeled
    \ not
    \ or
    \ powerset
    \ preserves
    \ replaces
    \ represented
    \ requires
    \ restores
    \ str
    \ then
    \ type
    \ updates
    \ uses
    \ constraints

syntax keyword resolveStringOperations
    \ Reverse
    \ Prt_Btwn
    \ DeString
    \ o
    \ Char_Str_for
    \ Merger
    \ Length

syntax keyword resolveMathTypes
" Math Types
    \ Character
    \ Integer
    \ Boolean
    \ Char_Str
    \ Z
    \ B

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
    \ Divide
    \ Mod
    \ Rem
    \ Quotient
    \ Div
    \ Is_Zero
    \ Is_Not_Zero
    \ Increment
    \ Decrement
    \ Sum
    \ Negative
    \ Difference
    \ Product
    \ Power

syntax keyword resolveCharacterOperations
    \ Char_to_Int
    \ Less
    \ Less_Or_Equal
    \ Greater_Or_Equal
    \ Greater

syntax keyword resolveBooleanOperations
    \ True
    \ False
    \ And
    \ Or
    \ Not

syntax keyword resolveGeneralOperations
    \ Are_Equal
    \ Are_Not_Equal
    \ Replica
    \ Read
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
