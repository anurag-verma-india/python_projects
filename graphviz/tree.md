PROGRAM
  |-- DECLARATION-LIST
  |   |-- DECLARATION
        |--"int"
        |--"x"
        |--";"
  |   |-- DECLARATION-LIST
  |       |-- DECLARATION ("int" "y" ";")
  |       |-- DECLARATION-LIST (ε)
  |-- STATEMENT-LIST
  |   |-- STATEMENT ("x" "=" EXPRESSION ";")
  |   |   |-- EXPRESSION ("10")
  |   |-- STATEMENT-LIST
  |       |-- STATEMENT ("y" "=" EXPRESSION ";")
  |       |   |-- EXPRESSION ("x" "+" "5")
  |       |   |-- STATEMENT-LIST (ε)
  |-- RETURN-STATEMENT ("return" EXPRESSION ";")
      |-- EXPRESSION ("y")
