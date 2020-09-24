from pyzotero import zotero
import semanticscholar as sch
from pprint import pprint
from nameparser import HumanName

library_id = 6526634
library_type = 'user'
api_key = 'h1CPDrvbTRNBjzpJNAN7ZFkd'

zot = zotero.Zotero(library_id, library_type, api_key)

doi =  '10.1109/SCCC.2014.21'

paper = sch.paper(doi)
paper.keys()

pprint(paper)

# pprint.pprint(zot.item_types())

template = zot.item_template('journalArticle')
pprint(template)
template['title'] = paper['title']
template['DOI'] = paper['doi']
template['URL'] = paper['url']
template['libraryCatalog'] = 'Semantic Scholar'
template['abstractNote'] = paper['abstract']
template['publicationTitle'] = paper['venue']
template['date'] = paper['year']

template['creators'].clear()
for author in paper['authors']:
	name = HumanName(author['name'])
	template['creators'].append({'creatorType':'author','firstName':name.first,'lastName':name.last})

# pprint(template)

resp = zot.create_items([template])
