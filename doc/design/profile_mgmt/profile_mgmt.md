# Unified profile management (ProfileMgr component)

See also [ticket reference](https://github.com/NewTec-GmbH/pyMetricCli/issues/16) for some background.

## Current state

### Notion of "profile" in pyJiraCli

Jira login data (server/credentials/cert) can be stored as a profile, which is a directory containing .data JSON file and .cert file.
Support for user/password storage in the profile shall be added with this feature as well.

### Server/token and user/password config in pyMetricCli(adapter)

pyMetricCli requires an adapter (project-specific ingested python config/handler), which contains direct Jira, Polarion and Superset configuration.

This includes the server URL and the token (update of pyPolarionCli documentation for the latter needed), but doesn't allow for for others like cert.
Currently pyMetricCli can authenticate at Jira only with token (although pyJiraCli would support user/password through CLI).
So there are some discrepancies between the tools and the adapter config (which pyMetricCli uses).

See [example adapter](https://github.com/NewTec-GmbH/pyMetricCli/blob/30be6a2e8777e0c7bf99063efef30ef4097a488c/examples/adapter/adapter.py).

## Work items proposal

* Create pyProfileMgr component:
  * Move profile handling (create/delete/update/list) to pyProfileMgr, which shall be used by pyJiraCli (through existing cmd_profile) and pyMetricCli (read access to profile using ProfileMgr).
  * Add cmd_profile to pyProfileMgr (similar to current pyJiraCli cmd_profile), to allow create/delete/update/list
  of profiles with a type (currently Jira, Polarion or Superset) and corresponding uniform data attributes.
* Introduce "profile" notion in pyMetricCli and the adapter config:
  * Reference profiles with their name (check type) in the adapter config, having precedence before other config.
  * Decide what to do with server/token (jira_config), username/password/server/token (polarion_config) and username/password/server (superset_config) in the adapter file:
    * Alternative 1: Remove it (breaking change), i.e. make profiles on pyMetricCli level mandatory.
    * Alternative 2: Keep current jira_config/polarion_config/superset_config settings in the adapter file and allow for profile references in addition (which should have precedence).
* Allow persistence of user/password in the profile data file (mandatory for Superset). There is no strict need to encrypt them as the file is stored locally in the user profile folder.

## Open points

* Decide between alternative 1 and 2, i.e. make profiles mandatory in pyMetricCli (removing other authentication config settings) or additional?
* Resolve some discrepancies along the way:
  * pyJiraCli supports user/password authentication through CLI options, but the adapter file only supports token for Jira. The new profile management should allow for user/password with Jira as well.
  * Update pyPolarionCli documentation and example adapter for token support.
