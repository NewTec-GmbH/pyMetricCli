# Examples

## Configuration File

The configuration file must have the same structure as `examples\config.json`.

## Adapter

Each project must provide an `Adapter` class with the methods `handle_jira` and `handle_polarion` to pack the data from the search results into the output dictionary.
The declaration, arguments and name of the methods must remain the same as in `examples\adapter\adapter.py`, otherwise the program will not work correctly.