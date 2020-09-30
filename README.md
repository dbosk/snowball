# Automatic snowballing using Semantic Scholar and Zotero web APIs
This is a script intended for `python3`, for automating the snowballing process of a systematic mapping study; i.e. retrieving the references of a list of publications. This script integrates the free and open-source reference management software Zotero with the AI-backed search engine Semantic Scholar (S2), by integrating their web APIs.

## Dependencies
To facilitate this, it depends on the package [Pyzotero](https://pypi.org/project/Pyzotero/), and includes a modified version of the package [semanticscholar](https://pypi.org/project/semanticscholar/), for details on the changes, see [this pull request](https://github.com/danielnsilva/semanticscholar/pull/15).
For this purpose, [requests](https://pypi.org/project/requests/) and [tenacity](https://pypi.org/project/tenacity/) need to be installed.
Additional dependencies include [nameparser](https://pypi.org/project/nameparser/) for parsing human names, and [PyYAML](https://pypi.org/project/PyYAML/) for reading the configuration.

To install the neccessary dependencies using `pip`, simply run
```sh
pip3 install pyzotero requests tenacity pyyaml nameparser
```

### Creating the configuration file
To configure your project, you should supply the necessary API keys and identifiers in an external configuration file, named `config.yaml`.

The following fields should be included:
```yaml
zot_library_id : <integer>
zot_library_type : <string>
zot_api_key : <string>
zot_base_collection : <string>
zot_ref_collection : <string>
s2_api_url : <string>
s2_api_key : <string>
```
In the case where you are accessing the public S2 API, you can omit the `s2_api_url` and `s2_api_url`, but you will need to remove the corresponding arguments for configuring the S2 client, on line 15 of `main.py`.

### Running the script
To execute the script, simply run
```sh
python3 main.py
```
This will begin the process of reading in items from the base collection, retrieving their references from S2, creating items for them, and adding them to the references collection in Zotero. The script should warn if any publication was unsuccessful.

### Limitations
S2 does not distinguish between the different types of publications (journal, conference, etc.), so all references that are retrieved from S2 are created as journal articles in Zotero, where the `venue` field is either the journal or name of the conference.

Additionally, since the S2 algorithm can be prone to errors, it is possible that the occasional reference will be parsed incorrectly, and thus be considered "unknown" by S2.
Such references will not be properly processed by Zotero, and will be omitted from the query.

## Acknowledgements
Finally, this work would not have been as successful without the help of the Allen Institute for AI, and their generous contribution of a private key for accessing the API at a significantly faster rate.
