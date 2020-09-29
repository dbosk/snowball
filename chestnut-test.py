from pprint import pprint
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
sch = SemanticScholar(config['s2_api_url'], config['s2_api_key'], timeout=60)

# Load 'base' collection, declare arrays for storing results
base_papers = zot.collection_items(config['zot_base_collection'])
references = []
failed_base_papers = []
orphaned_items = {}

# Retrieve all items in the base collection, and check their type
for base_paper in base_papers:
	item_type = base_paper['data']['itemType']

	if item_type == 'journalArticle' or item_type == 'conferencePaper':
		base_paper_doi = base_paper['data']['DOI'];
	elif item_type == 'document':
		base_paper_doi = base_paper['data']['url'].strip('https://doi.org/');
	# Skip the item if it is none of the accepted types
	else: continue

	# For a valid item in the base collection, try to retrieve it from S2
	try: base_paper_s2 = sch.paper(base_paper_doi)
	except:
		failed_base_papers.append(base_paper)
		continue

	print('{}:'.format(base_paper['data']['title']))
	references.clear()

	# Get references from S2
	for reference in base_paper_s2['references']:

		# If the DOI field is missing, skip this entry
		if not reference['doi']: continue
		paper = sch.paper(reference['doi'])
		print(' ''{}'' -> {}'.format(len(references), paper['title']))

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

	# Create items in Zotero, and assign to the references collection
	response = zot.create_items(references)
	if response['failed']:
		print('WARNING: The following references were not created in Zotero:')
		pprint(response['failed'])

	for created in response['successful']:
		for attempt in range(3):
			added = zot.addto_collection(config['zot_ref_collection'], response['successful'][created])
			if added: break
		if not added: orphaned_items[created] = response['success'][created]

	if orphaned_items:
		print('WARNING: The following references were not added to the collection:')
		pprint(orphaned_items)

if failed_base_papers:
	print('WARNING: The following base papers failed to be retreived:')
	pprint(orphaned_items)
