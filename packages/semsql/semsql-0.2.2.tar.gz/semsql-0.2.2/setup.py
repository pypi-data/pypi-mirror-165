# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['semsql',
 'semsql.builder',
 'semsql.linkml',
 'semsql.ontlib',
 'semsql.sqla',
 'semsql.sqlutils',
 'semsql.utils']

package_data = \
{'': ['*'], 'semsql.builder': ['indexes/*', 'prefixes/*', 'sql_schema/*']}

install_requires = \
['SQLAlchemy-Utils>=0.38.2,<0.39.0',
 'click>=8.1.3,<9.0.0',
 'linkml-runtime>=1.2.15,<2.0.0']

entry_points = \
{'console_scripts': ['gen-semsql-views = semsql.sqlutils.viewgen:cli',
                     'semsql = semsql.builder.cli:main']}

setup_kwargs = {
    'name': 'semsql',
    'version': '0.2.2',
    'description': '',
    'long_description': '# SemSQL: standard SQL views for RDF/OWL ontologies\n\n[![PyPI version](https://badge.fury.io/py/semsql.svg)](https://badge.fury.io/py/semsql)\n![](https://github.com/incatools/semantic-sql/workflows/Build/badge.svg)\n\n\nThis project provides a standard collection of SQL tables/views for ontologies, such that you can make queries like this,\nto find all terms starting with `Abnormality` in [HPO](https://obofoundry.org/ontology/hp).\n\n```sql\n$ sqlite db/hp.db\nsqlite> SELECT * FROM rdfs_label_statement WHERE value LIKE \'Abnormality of %\';\n```\n\n|stanza|subject|predicate|object|value|datatype|language|\n|---|---|---|---|---|---|---|\n|HP:0000002|HP:0000002|rdfs:label||Abnormality of body height|xsd:string||\n|HP:0000014|HP:0000014|rdfs:label||Abnormality of the bladder|xsd:string||\n|HP:0000022|HP:0000022|rdfs:label||Abnormality of male internal genitalia|xsd:string||\n|HP:0000032|HP:0000032|rdfs:label||Abnormality of male external genitalia|xsd:string||\n\n\nReady-made SQLite3 builds can also be downloaded for any ontology in [OBO](http://obofoundry.org), using URLs such as https://s3.amazonaws.com/bbop-sqlite/hp.db\n\n[relation-graph](https://github.com/balhoff/relation-graph/) is used to pre-generate tables of [entailed edges](https://incatools.github.io/semantic-sql/EntailedEdge/). For example,\nall is-a and part-of ancestors of [finger](http://purl.obolibrary.org/obo/UBERON_0002389) in Uberon:\n\n```sql\n$ sqlite db/uberon.db\nsqlite> SELECT * FROM entailed_edge WHERE subject=\'UBERON:0002389\' and predicate IN (\'rdfs:subClassOf\', \'BFO:0000050\');\n```\n\n|subject, predicate, object|\n|---|\n|UBERON:0002389, BFO:0000050, UBERON:0015212|\n|UBERON:0002389, BFO:0000050, UBERON:5002389|\n|UBERON:0002389, BFO:0000050, UBERON:5002544|\n|UBERON:0002389, rdfs:subClassOf, UBERON:0000061|\n|UBERON:0002389, rdfs:subClassOf, UBERON:0000465|\n|UBERON:0002389, rdfs:subClassOf, UBERON:0000475|\n\nSQLite provides many advantages\n\n- files can be downloaded and subsequently queried without network latency\n- compared to querying a static rdf, owl, or obo file, there is no startup/parse delay\n- robust and performant\n- excellent support in many languages\n\nAlthough the focus is on SQLite, this library can also be used for other DBMSs like PostgreSQL, MySQL, Oracle, etc\n\n## Tutorials\n\n- SemSQL: [notebooks/SemanticSQL-Tutorial.ipynb](https://github.com/INCATools/semantic-sql/blob/main/notebooks/SemanticSQL-Tutorial.ipynb)\n- Using OAK: [part 7 of OAK tutorial](https://incatools.github.io/ontology-access-kit/intro/tutorial07.html)\n\n## Installation\n\nSemSQL comes with a helper Python library. Use of this is optional. To install:\n\n```bash\npip install semsql\n```\n\n## Download ready-made SQLite databases\n\nPre-generated SQLite database are created weekly for all OBO ontologies and a selection of others.\n\nTo download:\n\n```bash\nsemsql download obi -o obi.db\n```\n\nOr simply download using URL of the form:\n\n- https://s3.amazonaws.com/bbop-sqlite/hp.db\n\n## Creating a SQLite database from an OWL file\n\nThere are two protocols for doing this:\n\n1. install build dependencies\n2. use Docker\n\nIn either case:\n\n- The input MUST be in RDF/XML serialization and have the suffix `.owl`:\n- use robot to convert if format is different\n\nWe are planning to simplify this process in future.\n\n### 1. Build a SQLite database directly\n\nThis requires some basic technical knowledge about how to install things on your machine\nand how to put things in your PATH. It does not require Docker.\n\nRequirements:\n\n- [rdftab.rs](https://github.com/ontodev/rdftab.rs)\n- [relation-graph](https://github.com/balhoff/relation-graph)\n\nAfter installing these and putting both `relation-graph` and `rdftab.rs` in your path:\n\n```bash\nsemsql make foo.db\n```\n\nThis assumes `foo.owl` is in the same folder\n\n### 2. Use Docker\n\nThere are two docker images that can be used:\n\n- ODK\n- [semantic-sql](https://hub.docker.com/repository/docker/linkml/semantic-sql)\n\nThe ODK image may lag behind\n\n```bash\ndocker run  -v $PWD:/work -w /work -ti linkml/semantic-sql semsql make foo.db\n```\n\n## Schema\n\nSee [Schema Documentation](https://incatools.github.io/semantic-sql/)\n\nThe [source schema](https://github.com/INCATools/semantic-sql/tree/main/src/semsql/linkml) is in [LinkML](https://linkml.io) - this is then compiled down to SQL Tables and Views\n\nThe basic idea is as follows:\n\nThere are a small number of "base tables":\n\n* [statements](https://incatools.github.io/semantic-sql/Statements/)\n* [prefix](https://incatools.github.io/semantic-sql/Prefix/)\n* [entailed_edge](https://incatools.github.io/semantic-sql/EntailedEdge/) - populated by relation-graph\n\nAll other tables are actually views (derived tables), and are provided for convenience.\n\n## ORM Layer\n\nA SemSQL relational database can be accessed in exactly the same way as any other SQLdb\n\nFor convenience, we provide a Python Object-Relational Mapping (ORM) layer using SQL Alchemy.\nThis allows for code uchlike the following, which joins [RdfsSubclassOfStatement](https://incatools.github.io/semantic-sql/RdfsSubclassOfStatement) and [existential restrictions](https://incatools.github.io/semantic-sql/OwlSomeValuesFrom):\n\n```python\nengine = create_engine(f"sqlite:////path/to/go.db")\nSessionClass = sessionmaker(bind=engine)\nsession = SessionClass()\nq = session.query(RdfsSubclassOfStatement)\nq = q.add_entity(OwlSomeValuesFrom)\nq = q.join(OwlSomeValuesFrom, RdfsSubclassOfStatement.object == OwlSomeValuesFrom.id)\n\nlines = []\nfor ax, ex in q.all():\n    line = f\'{ax.subject} subClassOf {ex.on_property} SOME {ex.filler}\'\n    logging.info(line)\n    lines.append(line)\n```    \n\n(this example is just for illustration - to do the same thing there is a simpler Edge relation)\n\n## Applications\n\nThe semsql python library is intentionally low level - we recommend using the [ontology-access-kit](https://github.com/INCATools/ontology-access-kit)\n\nFor example:\n\n```bash\nrunoak -i db/envo.db search t~biome\n```\n\nYou can also pass in an OWL file and have the sqlite be made on the fly\n\n```bash\nrunoak -i sqlite:envo.owl search t~biome\n```\n\nEven if using OAK, it can be useful to access SQL tables directly to do complex multi-join queries in a performant way.\n\n',
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
