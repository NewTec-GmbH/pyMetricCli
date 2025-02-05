# Unified profile management in pyMetricCli

See [ticket reference](https://github.com/NewTec-GmbH/pyMetricCli/issues/16)

## Current state

### Notion of "profile" in pyJiraCli

Jira login data (server/token/cert) can be stored as profile, being a directory with .data JSON file and .cert file. **No support for user/password storage in profile (although CLI can handle it).**

### Server/token and user/password config in pyMetricCli(adapter)

pyMetricCli requires an adapter (project-specific ingested python config/handler), which contains Jira and/or Polarion configuration.

This includes the server URL and the token (update of pyPolarionCli documentation for the latter TBD), but doesn't allow for cert. Currently pyMetricCli can authenticate at Jira only with token (although pyJiraCli would support user/password through CLI). So there are some discrepancies between the tools and the adapter config (which pyMetricCli uses).

See [example adapter](https://github.com/NewTec-GmbH/pyMetricCli/blob/30be6a2e8777e0c7bf99063efef30ef4097a488c/examples/adapter/adapter.py).

## Work items proposal

* Introduce "profile" notion in pyMetricCli:
  * Add cmd_profile (similar to current pyJiraCli profile capability), to create profiles with a type (Jira, Polarion or Superset) and corresponding data attributes.
  * Reference profiles through their name (check type) in the adapter config.
  * Decide what to do with server/token (jira_config), username/password/server/token (polarion_config) and username/password/server (superset_config) in the adapter file:
    * Alternative 1: Remove it (breaking change), i.e. make profiles on pyMetricCli level mandatory.
    * Alternative 2: Keep current jira_config/polarion_config/superset_config settings in the adapter file and allow for profile references in addition (which should have precedence).
* Allow persistence of user/password in the profile data file. There is no strict need to encrypt them as the file is locally stored in the user profile folder.
* Move profile handling (create/delete/update) to extra lib, which can be used initially by pyJiraCli (through existing cmd_profile) and pyMetricCli (adding cmd_profile).

## Open points

* Decide between alternative 1 and 2, i.e. make profiles mandatory in pyMetricCli (removing other authentication config settings) or additional?
* Resolve some discrepancies along the way:
  * pyJiraCli supports user/password authentication through CLI options, but the adapter file only supports token for Jira. The new profile management should allow for user/password with Jira as well.
  * Update pyPolarionCli documentation and example adapter for token support.
