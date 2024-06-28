# Examples

## Adapter

Each project must provide an `Adapter` class with the methods `handle_jira` and `handle_polarion` to pack the data from the search results into the output dictionary.
Additionally, the dictionaries `output`, `jira_config`, `polarion_config` and `superset_config` must also be supplied.
The declaration, arguments and name of the methods must remain the same as in `examples\adapter\adapter.py`, otherwise the program will not work correctly.
