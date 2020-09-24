from pyzotero import zotero
import semanticscholar as sch
import pprint

library_id = 6526634
library_type = 'user'
api_key = 'h1CPDrvbTRNBjzpJNAN7ZFkd'

zot = zotero.Zotero(library_id, library_type, api_key)
items = zot.top(limit=5)
# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
# pprint.pprint(items)
    # print('Item: %s | Author: %s' % (item['data']['itemType'], item['data']['key']))

doi = (items[0])['data']['DOI']

# pprint.pprint(doi)

paper = sch.paper(doi)
paper.keys()

paper['title']
for author in paper['authors']:
	print(author['name'])
	print(author['authorId'])

paper['title']
for reference in paper['references']:
	print(reference['title'])
