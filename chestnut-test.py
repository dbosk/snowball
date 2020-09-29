import yaml
from pyzotero import zotero
from semanticscholar import SemanticScholar
from pprint import pprint
from nameparser import HumanName

# Load external config params
config = yaml.safe_load(open('config.yaml'))

# Configure Zotero client
zot = zotero.Zotero(config['zot_library_id'], config['zot_library_type'], config['zot_api_key'])

# Configure Semantic Scholar client
sch = SemanticScholar()

# Load 'base' collection, declare array for storing references
base_papers = zot.collection_items(config['zot_base_collection'])
references = []

# For each paper in the base collection, get all works cited from S2
for base_paper in base_papers:
	base_paper_s2 = sch.paper(base_paper['data']['DOI'], timeout=60,
		headers={'x-api-key': config['s2_api_key']})

	for reference in base_paper_s2['references']:

		# If the DOI field is missing, skip this entry
		if not reference['doi']: continue
		pprint(reference['doi'])

		paper = sch.paper(reference['doi'], timeout=60,
			headers={'x-api-key': config['s2_api_key']})

		# Use the Zotero template for Journal Articles for all publications
		template = zot.item_template('journalArticle')
		template['title'] = paper['title']
		template['DOI'] = paper['doi']
		template['URL'] = paper['url']
		template['libraryCatalog'] = 'Semantic Scholar'
		template['abstractNote'] = paper['abstract']
		template['publicationTitle'] = paper['venue']
		template['date'] = paper['year']

		# Try to parse the authors' names using the HumanName package
		template['creators'].clear()
		for author in paper['authors']:
			name = HumanName(author['name'])
			template['creators'].append({'creatorType':'author',
				'firstName':name.first,'lastName':name.last})

		# Add the entry to the references array
		references.append(template)

# When all works cited, for each publication in the base collection has been added,
#  to the array, create items in Zotero, and assign to the references bollection
resp = zot.create_items(references)
if(resp['failed']):	print(resp['failed'])
for success in resp['successful']:
	zot.addto_collection(config['zot_ref_collection'], resp['successful'][success])
