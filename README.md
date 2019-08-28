# Wikipedia Category Tree
Extract wikipedia tree structure from an assigned root word, and visualize the tree structure.

## Generation Part
### Requirements
wikitools
### Usage
python3 categoryTree-en.py category_name depth output_file

- category_name : Category which we are looking into.This category will form the root of Category tree.
- depth : This argument decides the depth of the category tree
- default language = En, support other languages by changing the wikipedia url and encoding.


## Visualize Part
### Requirements
anytree
graphviz (used to covert .dot file to .png file)

### Usage
mkdir dots
python3 VisualizeTree-en.py category_name depth cat_tree
dot -Tpng input.dot > output.png

