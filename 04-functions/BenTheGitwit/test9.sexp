( sequence ( declare a ( function ( parameters ) ( sequence ( assign ( varloc b ) ( lookup a ) ) ( print ( lookup b ) ) ) ) ) ( declare b ( function ( parameters ) ( sequence ( declare b 1 ) ( call ( lookup a ) ( arguments ) ) ( print ( lookup b ) ) ) ) ) ( call ( lookup b ) ( arguments ) ) ( call ( lookup b ) ( arguments ) ) )