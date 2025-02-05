# Unified profile management in pyMetricCli

## Current state

### Notion of "profile" in pyJiraCli

Jira login data (server/token/cert) can be stored as profile, being a directory with .data JSON file and .cert file. **No support for user/password storage, not even unencrypted.**

### Server/token and user/password config in pyMetricCli(adapter)

pyMetricCli requires an adapter (project-specific ingested python config/handler), which contains Jira and/or Polarion configuration.

This includes the server URL and the token (update documentation of pyPolarionCli for the latter), but doesn't allow for cert. Currently pyMetricCli authenticates at Jira only with token (although pyJiraCli would support user/password).

See [example adapter](https://github.com/NewTec-GmbH/pyMetricCli/blob/30be6a2e8777e0c7bf99063efef30ef4097a488c/examples/adapter/adapter.py).

## Work items proposal

* Introduce "profile" notion in pyMetricCli:
  * Add cmd_profile (similar to current pyJiraCli profile capability), to create profiles with a type (Jira or Polarion) and corresponding data attributes.
  * Reference profiles through their name (check type) in the adapter config.
  * Decide what to do with server/token (jira_config) and username/password/server/token (polarion_config) in the adapter file:
    * Alternative 1: Remove it (breaking change), i.e. make profiles mandatory.
    * Alternative 2: Keep server/token (jira_config) and username/password/server/token (polarion_config) config in the adapter file and allow for profile references in addition.
* Allow persistence of user/password in data file and encrypt it (at the two).
* Remove all profile support in pyJiraCli (breaking change)?

## Open points

* Decide between alternative 1 and 2, i.e. make profiles mandatory in pyMetricCli (removing other authentication config settings) or additional?
* Keep the possibility to use profiles directly in pyJiraCli?
  * If yes, to avoid duplication, should be the same code and structure as in pyMetricCli.
* Resolve some discrepancies along the way:
  * pyJiraCli supports user/password authentication through CLI options, but the adapter file only supports token for Jira. So the "new profiles" should allow for user/password with Jira as well.
  * Update pyPolarionCli documentation and example adapter for token support.
