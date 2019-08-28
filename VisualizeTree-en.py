from wikitools import wiki,category,api
import sys
import os
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

reload(sys)
sys.setdefaultencoding('latin1')

def wikipedia_query(query_params,lang):
  site = wiki.Wiki(url='https://'+lang+'.wikipedia.org/w/api.php')
  request = api.APIRequest(site, query_params)
  result = request.query(querycontinue=True)
  return result[query_params['action']]

def get_category_members(par_category, depth, parent_node,lang = 'en'):
    category_name = 'Category:' + par_category
    if depth < 0:
        return 0
    
    #Begin crawling articles in category
    #results = wikipedia_query({'list': 'categorymembers','cmtitle': category_name,'cmtype': 'page','cmlimit': '500','ucuser':'Example','action': 'query'},lang)  
    
    # Begin crawling subcategories
    results = wikipedia_query({'list': 'categorymembers',
                                   'cmtitle': category_name,
                                   'cmtype': 'subcat',
                                   'cmlimit': '500',
                                   'action': 'query'},lang)
    #print(results)
    subcategories = []
    if 'categorymembers' in results.keys() and len(results['categorymembers']) > 0:
        for i, category in enumerate(results['categorymembers']):
            cat_title = category['title']
            _, cat_name = cat_title.split(":",2)
            #print(cat_name)
            subcategories.append(cat_name)
    if len(subcategories) > depth * 3:
      for sc in subcategories:
        if sc != '' and sc != ' ':
          child_node = Node(sc, parent = parent_node)
          get_category_members(sc,depth-1, child_node, lang)
    #subcat= ' '.join(cat.encode('latin1', 'ignore')+',' for cat in subcategories).strip(',')
    #print(subcat)
    #if subcat !='' and subcat !=' ':
      #wp.write(str(depth)+ " " +par_category.encode('latin1', 'ignore')+' : '+subcat+'\n')
  


wikisite = "http://en.wikipedia.org/w/api.php"
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
par_category = sys.argv[1]
depth =int(sys.argv[2])
cat_tree =sys.argv[3]



root_node = Node(par_category)
get_category_members(par_category,depth, root_node,'en')
#wp =open(cat_tree,'w')
DotExporter(root_node).to_dotfile("dots/"+ par_category + '-en-' +str(depth) + ".dot")
print("Finished! Picture stored to pics folder.")

