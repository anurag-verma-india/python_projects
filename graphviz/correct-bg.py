"""
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

Give something like this to an LLM with following program 
and ask it to return a program to convert this above structure into a proper tree
"""


import graphviz

class Node:
    def __init__(self, label, children=None, shape="rectangle"):
        self.label = label
        self.children = children or []
        self.shape = shape

    def add_child(self, child):
        self.children.append(child)

    def to_graphviz(self, dot, parent_name=None):
        node_name = f"node_{id(self)}"
        dot.node(node_name, self.label, shape=self.shape)
        if parent_name:
            dot.edge(parent_name, node_name)
        for child in self.children:
            child.to_graphviz(dot, node_name)

# Construct the tree from your representation
program = Node("PROGRAM")

declaration_list = Node("DECLARATION-LIST")
program.add_child(declaration_list)

declaration1 = Node("DECLARATION")
declaration_list.add_child(declaration1)
declaration1.add_child(Node('"int"'))
declaration1.add_child(Node('"x"'))
declaration1.add_child(Node('";"'))

declaration_list2 = Node("DECLARATION-LIST")
declaration_list.add_child(declaration_list2)

declaration2 = Node("DECLARATION")
declaration_list2.add_child(declaration2)
declaration2.add_child(Node('"int"'))
declaration2.add_child(Node('"y"'))
declaration2.add_child(Node('";"'))

declaration_list3 = Node("DECLARATION-LIST", shape="rectangle")
declaration_list2.add_child(declaration_list3)
declaration_list3.add_child(Node("ε"))

statement_list = Node("STATEMENT-LIST")
program.add_child(statement_list)

statement1 = Node("STATEMENT")
statement_list.add_child(statement1)
statement1.add_child(Node('"x"'))
statement1.add_child(Node('"="'))
expression1 = Node("EXPRESSION")
statement1.add_child(expression1)
expression1.add_child(Node('"10"'))

statement_list2 = Node("STATEMENT-LIST")
statement_list.add_child(statement_list2)

statement2 = Node("STATEMENT")
statement_list2.add_child(statement2)
statement2.add_child(Node('"y"'))
statement2.add_child(Node('"="'))
expression2 = Node("EXPRESSION")
statement2.add_child(expression2)
expression2.add_child(Node('"x"'))
expression2.add_child(Node('"+"'))
expression2.add_child(Node('"5"'))

statement_list3 = Node("STATEMENT-LIST", shape="rectangle")
statement_list2.add_child(statement_list3)
statement_list3.add_child(Node("ε"))

return_statement = Node("RETURN-STATEMENT")
program.add_child(return_statement)
return_statement.add_child(Node('"return"'))
expression3 = Node("EXPRESSION")
return_statement.add_child(expression3)
expression3.add_child(Node('"y"'))
return_statement.add_child(Node('";"'))

# Generate the Graphviz graph
dot = graphviz.Digraph(comment='Syntax Tree')
dot.attr(bgcolor="#F6F3EB") # Set background color
program.to_graphviz(dot)

# Render and save the SVG
dot.render('syntax_tree_3', format='svg', cleanup=True)

print("syntax_tree_3.svg generated.")
