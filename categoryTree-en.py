from wikitools import wiki,category,api
import sys

reload(sys)
sys.setdefaultencoding('latin1')

def wikipedia_query(query_params,lang):
  site = wiki.Wiki(url='https://'+lang+'.wikipedia.org/w/api.php')
  request = api.APIRequest(site, query_params)
  result = request.query(querycontinue=True)
  return result[query_params['action']]

def get_category_members(par_category, depth, lang):
    category_name = 'Category:'+par_category
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
    #print(subcategories)
    subcat= ' '.join(cat.encode('latin1', 'ignore')+',' for cat in subcategories).strip(',')
    #print(subcat)
    if subcat !='' and subcat !=' ':
      wp.write(par_category.encode('latin1', 'ignore')+' : '+subcat+'\n')
    for category in subcategories:
      get_category_members(category,depth-1, lang)


wikisite = "http://en.wikipedia.org/w/api.php"
par_category = 'society'
depth = 5
cat_tree = par_category + str(depth) + '.txt'
wp =open(cat_tree,'w')

get_category_members(par_category,depth,'en')

wp.close()