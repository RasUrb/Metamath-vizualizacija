$c 0 1 2 + = ( ) term wff ⊢ → $.
$v t r s P Q A B $.

tt $f term t $.
tr $f term r $.
ts $f term s $.
ta $f term A $.
tb $f term B $.
wp $f wff P $.
wq $f wff Q $.

tze $a term 0 $.
tpl $a term ( t + r ) $.
weq $a wff t = r $.
wim $a wff ( P → Q ) $.

def1 $a ⊢ 1 = ( 0 + 1 ) $.
def2 $a ⊢ 2 = ( 1 + 1 ) $.

${
  min $e ⊢ 2 = ( 1 + 1 ) $.
  maj $e ⊢ ( 2 = ( 1 + 1 ) → ( 1 + 1 ) = 2 ) $.
  mp $a ⊢ ( 1 + 1 ) = 2 $.
$}

step1 $p ⊢ ( 1 + 1 ) = 2 $=
  def2
  maj
  mp
$. 