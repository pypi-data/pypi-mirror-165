# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['prefixmaps',
 'prefixmaps.data',
 'prefixmaps.datamodel',
 'prefixmaps.ingest',
 'prefixmaps.io']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['slurp-prefixmaps = prefixmaps.ingest.etl_runner:cli']}

setup_kwargs = {
    'name': 'prefixmaps',
    'version': '0.1.2',
    'description': '',
    'long_description': '# prefixmaps\n\nA python library for retrieving semantic prefix maps\n\nA semantic prefix map will map a a prefix (e.g. `skos`) to a namespace (e.g `http://www.w3.org/2004/02/skos/core#`)\n\nThis library is designed to satisfy the following requirements\n\n- coverage of prefixes from multiple different domains\n- no single authoritative source of either prefixes or prefix-namespace mappings (clash-resilient)\n- preferred semantic namespace is prioritized over web URLs\n- authority preferred prefix is prioritized where possible\n- each individual prefixmap is case-insenstive bijective\n- prefixmap composition and custom ordering of prefixmaps\n- lightweight / low footprint\n- fast (TODO)\n- network-independence / versioned prefix maps\n- optional ability to retrieve latest from external authority on network\n\n## Installation\n\n```\npip install prefixmaps\n```\n\n## Usage\n\nto use in combination with [curies](https://github.com/cthoyt/curies) library:\n\n```python\nfrom prefixmaps.io.parser import load_context, load_multi_context\nfrom curies import Converter\n\nctxt = load_multi_context(["obo", "bioregistry.upper", "linked_data", "prefixcc"])\nconverter = Converter.from_prefix_map(ctxt.as_dict())\n\n>>> converter.expand("CHEBI:1")\n\'http://purl.obolibrary.org/obo/CHEBI_1\'\n>>> converter.expand("GEO:1")\n\'http://purl.obolibrary.org/obo/GEO_1\'\n>>> converter.expand("owl:Class")\n\'http://www.w3.org/2002/07/owl#Class\'\n>>> converter.expand("FlyBase:FBgn123")\n\'http://identifiers.org/fb/FBgn123\'\n```\n\n### Alternate orderings / clash resilience\n\n- prefix.cc uses the prefix `geo` for geosparql `http://www.opengis.net/ont/geosparql#`\n- OBO uses prefix `GEO` for the geographic ontology `http://purl.obolibrary.org/obo/GEO_`\n- bioprefix uses the prefix `geo` for NCBI GEO, and "re-mints" a GEOGEO prefix for the OBO ontology\n\nIf we prioritize prefix.cc the OBO prefix is ignored:\n\n```python\n>>> ctxt = load_multi_context(["prefixcc", "obo"])\n>>> converter = Converter.from_prefix_map(ctxt.as_dict())\n>>> converter.expand("GEO:1")\n>>> converter.expand("geo:1")\n\'http://www.opengis.net/ont/geosparql#1\'\n```\n\nEven though prefix expansion is case sensitive, we intentionally block conflicts that differ only in case.\n\nIf we push bioregistry at the start of the list then GEOGEO can be used as the prefix for the OBO ontology\n\n```python\n>>> ctxt = load_multi_context(["bioregistry", "prefixcc", "obo"])\n>>> converter = Converter.from_prefix_map(ctxt.as_dict())\n>>> converter.expand("geo:1")\n\'http://identifiers.org/geo/1\'\n>>> converter.expand("GEO:1")\n>>> converter.expand("GEOGEO:1")\n\'http://purl.obolibrary.org/obo/GEO_1\'\n```\n\nNote that from the OBO perspective, GEOGEO is non-canonical\n\nWe get similar results using the upper-normalized variant of bioregistry:\n\n```python\n>>> ctxt = load_multi_context(["bioregistry.upper", "prefixcc", "obo"])\n>>> converter = Converter.from_prefix_map(ctxt.as_dict())\n>>> converter = Converter.from_prefix_map(ctxt.as_dict())\n>>> converter = Converter.from_prefix_map(ctxt.as_dict())\n>>> converter.expand("GEO:1")\n\'http://identifiers.org/geo/1\'\n>>> converter.expand("geo:1")\n>>> converter.expand("GEOGEO:1")\n\'http://purl.obolibrary.org/obo/GEO_1\'\n```\n\nUsers of OBO ontologies will want to place OBO at the start of the list:\n\n```python\n>>> ctxt = load_multi_context(["obo", "bioregistry.upper", "prefixcc"])\n>>> converter = Converter.from_prefix_map(ctxt.as_dict())\n>>> converter.expand("geo:1")\n>>> converter.expand("GEO:1")\n\'http://purl.obolibrary.org/obo/GEO_1\'\n>>> converter.expand("GEOGEO:1")\n```\n\nNote under this ordering there is no prefix for NCBI GEO. This is not\na major limitation as there is no canonical semantic rendering of NCBI\nGEO. This could be added in future with a unique OBO prefix.\n\nYou can use the ready-made "merged" prefix set, which prioritizes OBO:\n\n```python\n>>> ctxt = load_context("merged")\n>>> converter = Converter.from_prefix_map(ctxt.as_dict())\n>>> converter.expand("GEOGEO:1")\n>>> converter.expand("GEO:1")\n\'http://purl.obolibrary.org/obo/GEO_1\'\n>>> converter.expand("geo:1")\n```\n\n### Network independence and requesting latest versions\n\nBy default this will make use of metadata distributed alongside the package. This has certain advantages in terms\nof reproducibility, but it means if a new ontology or prefix is added to an upstream source you won\'t see this.\n\nTo refresh and use the latest upstream:\n\n```python\nctxt = load_context("obo", refresh=True)\n```\n\nThis will perform a fetch from http://obofoundry.org/registry/obo_prefixes.ttl\n\n## Context Metadata\n\nSee [contexts.curated.yaml](src/prefixmaps/data/contexts.curated.yaml)\n\nSee the description fields\n\n## Code organization\n\nData files containing pre-build prefix maps using sources like OBO and BioRegistry are distributed alongside the python\n\nLocation:\n\n * [src/prefixmaps/data](src/prefixmaps/data/)\n\nThese can be regenerated using:\n\n```\nmake etl\n```\n\nTODO: make a github action that auto-released new versions\n\n## Requesting new prefixes\n\nThis repo is NOT a prefix registry. Its job is simply to aggregate\ndifferent prefix maps. Request changes upstream.\n',
    'author': 'cmungall',
    'author_email': 'cjm@berkeleybop.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
