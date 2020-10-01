# Automatic snowballing using Semantic Scholar and Zotero web APIs
This is a script written in Python 3, for automating the snowballing process of a systematic mapping study; i.e. retrieving the references of a list of publications. This script integrates the free and open-source reference management software Zotero with the AI-backed search engine Semantic Scholar (S2), by integrating their web APIs.

## Dependencies
To facilitate this, it depends on the package [Pyzotero](https://pypi.org/project/Pyzotero/), and includes a modified version of the package [semanticscholar](https://pypi.org/project/semanticscholar/) (for details on the changes, see [this pull request](https://github.com/danielnsilva/semanticscholar/pull/15)).
For this reason, [requests](https://pypi.org/project/requests/) and [tenacity](https://pypi.org/project/tenacity/) need to be installed.
Additional dependencies include [nameparser](https://pypi.org/project/nameparser/) for parsing human names, and [PyYAML](https://pypi.org/project/PyYAML/) for reading the configuration.

To install the necessary dependencies using [The Python Package Installer](https://pip.pypa.io/en/stable/), simply run
```sh
pip install pyzotero requests tenacity pyyaml nameparser
```

## Getting started
For the automation to be smooth, you should have a library in Zotero containing only the references you want to perform snowballing on. They should all belong to a collection, referred to in this project as the *base collection*. You should make sure the library has another (preferrably empty) collection, which will be your *reference collection*. This is where the retrieved references will end up.
The snowballing process is done in five steps, as follows.

For each publication in the base collection in Zotero:
1. The item type is checked for validity, and the DOI is read.
2. The publication is retrieved from Semantic Scholar using the DOI.
3. The references of the publication are formatted as Zotero items and added to a list.
4. When all references have been added, the list is created in the Zotero library.
5. All successfully created items are added them to the references collection.

### Creating the configuration file
To configure your project, you need to supply the necessary API keys and identifiers in an external configuration file, named `config.yaml`.
The following fields should be included:
```yaml
zot_library_type : <string>
zot_library_id : <integer>
zot_base_collection : <string>
zot_ref_collection : <string>
zot_api_key : <string>

s2_api_url : <string>
s2_api_key : <string>
```

From Zotero, you will need the following things (adapted from the [Pyzotero documentation](https://pyzotero.readthedocs.io/en/latest/#getting-started-short-version)):
* You’ll need the type of the Zotero library you are using.
  - If you are accessing your own Zotero library, set `zot_library_type` to `'user'`.
  - If you are accessing a shared group library, set `zot_library_type` to `'group'`.
* You’ll also need the ID of that library.
  - Your personal library ID is available from the [Zotero Settings](https://www.zotero.org/settings/keys), listed as "Your userID for use in API calls"
  - For group libraries, the ID can be found by opening the library in the [Zotero Web Library](https://www.zotero.org/mylibrary). The library ID is the integer in the link `https://www.zotero.org/groups/XXXXXXX/groupname`
* Then you will need the IDs of the base and reference collections
  - The collection ID can be found by opening the collection in the [Zotero Web Library](https://www.zotero.org/mylibrary). The ID is the string at the end of the link `https://www.zotero.org/groups/XXXXXXX/groupname/collections/ZZZZZZZZ`
* Finally, you will need to generate an API key from the [Zotero Settings](https://www.zotero.org/settings/keys).
  - Make sure you generate keys for the correct library, and set **Read/Write** permission.

To access the Semantic Scholar API, you will need the following things:
* You will need the URL to use for requests.
  - If you are accessing the public API, you should set `s2_api_url` to `'https://api.semanticscholar.org/v1'`
  - If you are a Semantic Scholar Data Partner, you should `s2_api_url` to `'https://partner.semanticscholar.org/v1'`
* You may also need to specify the private key
  - If you are accessing the public API, you can set `s2_api_key` to the empty string `''`. It will not be used.
  - If you are a Semantic Scholar Data Partner, you should provide your 40-character private key.

Alternatively, in the case where you are using the public S2 API, you can omit the `s2_api_url` and `s2_api_key`, but you will need to remove the corresponding arguments for configuring the S2 client, on line 14 of `main.py`.

### Running the script
To execute the script, simply run
```sh
python3 main.py
```
This will begin the process of reading in items from the base collection, retrieving their references from S2, creating items for them in Zotero, and adding them to the references collection. The script should warn if any publication was unsuccessful.

## Limitations
When reading from the base directory, only items of type `journalArticle`, `conferencepaper` or `document` are processed.
Journal articles or conference papers must have a valid DOI field for S2 to identify the publication. Items of the document-type do not have a DOI field, and so the URL field must contain the link to the correct doi.org page (or just the DOI number).

Semantic Scholar does not distinguish between the different types of publications, so all references that are retrieved from the S2 client are created as journal articles in Zotero, where the `publicationTitle` field is either the journal or name of the conference.

Additionally, since the S2 algorithm can be prone to errors, it is possible that the occasional publication will be parsed incorrectly, and thus be considered "unknown" by S2.
Such publication will not be properly processed by Zotero, and will be omitted from the results.

## Acknowledgements
Finally, this work would not have been as successful without the help of the Allen Institute for AI, and their generous contribution of a private key for accessing the API at a significantly faster rate.
