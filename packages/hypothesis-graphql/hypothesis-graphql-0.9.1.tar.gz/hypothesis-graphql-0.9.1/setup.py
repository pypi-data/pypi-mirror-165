# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypothesis_graphql', 'hypothesis_graphql._strategies']

package_data = \
{'': ['*']}

install_requires = \
['attrs>20.3.0,<=21.4.0',
 'graphql-core>=3.1.0,<3.3.0',
 'hypothesis>=5.8.0,<7.0']

setup_kwargs = {
    'name': 'hypothesis-graphql',
    'version': '0.9.1',
    'description': 'Hypothesis strategies for GraphQL queries',
    'long_description': '# hypothesis-graphql\n\n[![Build](https://github.com/Stranger6667/hypothesis-graphql/workflows/build/badge.svg)](https://github.com/Stranger6667/hypothesis-graphql/actions)\n[![Coverage](https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master/graph/badge.svg)](https://codecov.io/gh/Stranger6667/hypothesis-graphql/branch/master)\n[![Version](https://img.shields.io/pypi/v/hypothesis-graphql.svg)](https://pypi.org/project/hypothesis-graphql/)\n[![Python versions](https://img.shields.io/pypi/pyversions/hypothesis-graphql.svg)](https://pypi.org/project/hypothesis-graphql/)\n[![Chat](https://img.shields.io/discord/938139740912369755)](https://discord.gg/VnxfdFmBUp)\n[![License](https://img.shields.io/pypi/l/hypothesis-graphql.svg)](https://opensource.org/licenses/MIT)\n\n<h4 align="center">\nGenerate queries matching your GraphQL schema, and use them to verify your backend implementation\n</h4>\n\nIt is a Python library that provides a set of [Hypothesis](https://github.com/HypothesisWorks/hypothesis/tree/master/hypothesis-python) strategies that\nlet you write tests parametrized by a source of examples.\nGenerated queries have arbitrary depth and may contain any subset of GraphQL types defined in the input schema.\nThey expose edge cases in your code that are unlikely to be found otherwise.\n\n[Schemathesis](https://github.com/schemathesis/schemathesis) provides a higher-level interface around this library and finds server crashes automatically.\n\n## Usage\n\n`hypothesis-graphql` provides the `from_schema` function, which takes a GraphQL schema and returns a Hypothesis strategy for\nGraphQL queries matching the schema:\n\n```python\nfrom hypothesis import given\nfrom hypothesis_graphql import from_schema\nimport requests\n\n# Strings and `graphql.GraphQLSchema` are supported\nSCHEMA = """\ntype Book {\n  title: String\n  author: Author\n}\n\ntype Author {\n  name: String\n  books: [Book]\n}\n\ntype Query {\n  getBooks: [Book]\n  getAuthors: [Author]\n}\n\ntype Mutation {\n  addBook(title: String!, author: String!): Book!\n  addAuthor(name: String!): Author!\n}\n"""\n\n\n@given(from_schema(SCHEMA))\ndef test_graphql(query):\n    # Will generate samples like these:\n    #\n    # {\n    #   getBooks {\n    #     title\n    #   }\n    # }\n    #\n    # mutation {\n    #   addBook(title: "H4Z\\u7869", author: "\\u00d2"){\n    #     title\n    #   }\n    # }\n    response = requests.post("http://127.0.0.1/graphql", json={"query": query})\n    assert response.status_code == 200\n    assert response.json().get("errors") is None\n```\n\nIt is also possible to generate queries or mutations separately with `hypothesis_graphql.queries` and `hypothesis_graphql.mutations`.\n\n### Customization\n\nTo restrict the set of fields in generated operations use the `fields` argument:\n\n```python\n@given(from_schema(SCHEMA, fields=["getAuthors"]))\ndef test_graphql(query):\n    # Only `getAuthors` will be generated\n    ...\n```\n\nIt is also possible to generate custom scalars. For example, `Date`:\n\n```python\nfrom hypothesis import strategies as st, given\nfrom hypothesis_graphql import from_schema, nodes\n\nSCHEMA = """\nscalar Date\n\ntype Query {\n  getByDate(created: Date!): Int\n}\n"""\n\n\n@given(\n    from_schema(\n        SCHEMA,\n        custom_scalars={\n            # Standard scalars work out of the box, for custom ones you need\n            # to pass custom strategies that generate proper AST nodes\n            "Date": st.dates().map(nodes.String)\n        },\n    )\n)\ndef test_graphql(query):\n    # Example:\n    #\n    #  { getByDate(created: "2000-01-01") }\n    #\n    ...\n```\n\nThe `hypothesis_graphql.nodes` module includes a few helpers to generate various node types:\n\n- `String` -> `graphql.StringValueNode`\n- `Float` -> `graphql.FloatValueNode`\n- `Int` -> `graphql.IntValueNode`\n- `Object` -> `graphql.ObjectValueNode`\n- `List` -> `graphql.ListValueNode`\n- `Boolean` -> `graphql.BooleanValueNode`\n- `Enum` -> `graphql.EnumValueNode`\n- `Null` -> `graphql.NullValueNode` (a constant, not a function)\n\nThey exist because classes like `graphql.StringValueNode` can\'t be directly used in `map` calls due to kwarg-only arguments.\n\n## License\n\nThe code in this project is licensed under [MIT license](https://opensource.org/licenses/MIT).\nBy contributing to `hypothesis-graphql`, you agree that your contributions will be licensed under its MIT license.\n',
    'author': 'Dmitry Dygalo',
    'author_email': 'dadygalo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Stranger6667/hypothesis-graphql',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
