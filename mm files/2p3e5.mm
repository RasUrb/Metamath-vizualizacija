$( Konstantų apibrėžimas $)
$c 0 1 2 3 4 5 + = ( ) ⊢ $.

$( Kintamųjų apibrėžimas $)
$v x y z $.


$( Aksiomos $)
a1 $a ⊢ 1 $.

${ $( 1 + 1 = 2 $)
  h1 $e ⊢ 1 $.
  h2 $e ⊢ 1 $.
  add1 $a ⊢ ( 1 + 1 ) = 2 $.
$}
t-1p1e2 $p ⊢ ( 1 + 1 ) = 2 $= a1 a1 add1 $.


${ $( Iš lygybės gauname reikšmę: jei ⊢ (1 + 1) = 2, tai ⊢ 2 $)
  h3 $e ⊢ ( 1 + 1 ) = 2 $.
  convert $a ⊢ 2 $.
$}
t-conv2 $p ⊢ 2 $= t-1p1e2 convert $.

${ $( 1 + 2 = 3 $)
  h4 $e ⊢ 1 $.
  h5 $e ⊢ 2 $.
  add2 $a ⊢ ( 1 + 2 ) = 3 $.
$}

t-1p2e3 $p ⊢ ( 1 + 2 ) = 3 $= a1 t-conv2 add2 $.

${ $( Iš lygybės gauname reikšmę: jei ⊢ (1 + 2) = 3, tai ⊢ 3 $)
  h6 $e ⊢ ( 1 + 2 ) = 3 $.
  convert3 $a ⊢ 3 $.
$}
t-conv3 $p ⊢ 3 $= t-1p2e3 convert3 $.

${ $( 2 + 3 = 5 $)
  h7 $e ⊢ 2 $.
  h8 $e ⊢ 3 $.
  add3 $a ⊢ ( 2 + 3 ) = 5 $.
$}

t-2p3e5 $p ⊢ ( 2 + 3 ) = 5 $= t-conv2 t-conv3 add3 $.

${ $( Iš lygybės gauname reikšmę: jei ⊢ (1 + 2) = 3, tai ⊢ 3 $)
  h9 $e ⊢ ( 2 + 3 ) = 5 $.
  convert5 $a ⊢ 5 $.
$}
t-conv5 $p ⊢ 5 $= t-2p3e5 convert5 $.