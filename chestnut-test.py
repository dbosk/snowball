from pyzotero import zotero
import semanticscholar as sch
from pprint import pprint
from nameparser import HumanName

library_id = 2569621
library_type = 'group'
api_key = 'cAjS7ISgL7i6f0XesVCS4Hfq'

zot = zotero.Zotero(library_id, library_type, api_key)

chestnut_doi =  '10.1109/SCCC.2014.21'
chestnut_paper = sch.paper(chestnut_doi)
chestnut_paper.keys()

references = []

for reference in chestnut_paper['references']:

	if not reference['doi']: continue
	pprint(reference['doi'])

	paper = sch.paper(reference['doi'])
	paper.keys()

	template = zot.item_template('journalArticle')
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

	references.append(template)

resp = zot.create_items(references)
if(resp['failed']):	print(resp['failed'])
for success in resp['successful']:
	zot.addto_collection('HXCTMQ9M', resp['successful'][success])
