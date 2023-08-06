# Rally Python SDK

A collection of classes and functions for interacting with SDVI Rally APIs.

Refer to documentation found in your Rally Silo.

## v1.0.2 -- released 30 Aug 2022

### Fixes

- Titles used in some documentation have been altered in an effort to clarify documentation
- `RallyFile` `id` field is now guaranteed to be an `int`
- `RallyFile` initializer will now raise an error for invalid identifiers.
- `files.remove_inventory` now correctly marks file inventory objects as `deleted`
- Fixed a bug that prevented common error responses from returning with text and status code

---

## v1.0.1 -- released 19 July 2022

### Fixes

- Fixed a bug in `supplyChain.set_supply_chain_metadata` when attempting to set metadata on a supply chain with no
asset. This action now returns `NotFound` error.
- Fixed a bug in `asset.clear_asset_status_indicator` when attempting to use invalid indicator ids
- Fixed a parsing bug in `files.delete_file` for in files found in subfolders
- `asset.get_asset` now supports names with commas
- Fixed a bug in `supplyChain.start_new_supply_chain` that ignored `provider_filter`
- Fixed a bug in `SupplyChainStep` that ignored `provider_filter`. This action now raises an error if the supplied tag
does not exist.

---

## v1.0.0 -- released 10 May 2022

### Features

- Rally Decision Engine and SDK is now out of Beta! 💥️ 🎉 ️🎊 ️🎉 ️💥️

---

## v0.2.0 -- released 01 Apr 2022

### Features

- **Altering a different asset is no longer allowed in Decision Engine jobs.**  Allowing the alteration of another asset
could cause unpredictable behavior as multiple jobs operated on the same asset at the same time. The best practice for
altering any asset is to launch a supply chain with that asset. The following methods have had `asset_name` removed from
their kwargs:
  - `asset.add_asset_status_indicator`
  - `asset.clear_all_asset_status_indicators`
  - `supplyChain.set_scheduled_workflow`

### Fixes

- Fixed a bug in `supplyChain.get_scheduled_supply_chain` and `supplyChain.set_scheduled_supply_chain` that was
improperly converting datetimes
- Fixed an issue with `files.delete_file` that prevented deletion of files in Storage Location subdirectories
- Various documentation fixes

---

## v0.1.9 -- released 18 Jan 2022

### Features

- Added optional `remove_date` argument to `files.RallyFile.remove_location()` method, allows the actual delete to
occur at a later date
- Added `sharedDeleteAt` attribute to `RallyFile.locations`
- Added optional `timeout` argument to `files.RallyFile.presigned_url()`, `files.read_file()`, `files.read_files()`
methods
- Add `rallyUrl` to SDK context

---

## v0.1.8 -- released 09 Nov 2021

### Features

- There is a new library available! [SDVI Rally Token Auth](https://pypi.org/project/sdvi-rally-token-auth/0.1.0/)
allows users to easily access the v2 API from Decision Engine presets. Refer to preset documentation on your silo for
usage.

- Added `clientResourceId` attribute to return of `jobs.get_jobs_for_asset`, if present
- **Asset Status Indicator methods `get_asset_status_indicators`, `add_asset_status_indicator`,
`clear_asset_status_indicator`, and `clear_all_asset_status_indicators` are being promoted out of Alpha.**
They will move out of the `experimental` submodule and into the `asset` submodule.
Import statements will change accordingly.

### Fixes

- Presets can now correctly import zip packages placed in nested directories specified in
RallyConfig `Eval2Package`

---

## v0.1.7 -- released 12 Oct 2021

### Features

- A new key, `rallyUrl`, has been added to the context. This is the base URL for your silo's API.
- You can now find out the SDK version your silo is running:
    ```python
    from rally import __version__

    print(__version__)
    ```
    OR
    ```python
    import rally

    print(rally.__version__)
    ```
    Either results in "0.1.7". Note that this feature is not available in prior versions of the SDK.

### Fixes

- `SupplyChainStep` `fail_step` argument type was incorrectly listed as being either a string or a SupplyChainStep.
`fail_step` could only be the string `name` of an alternate SupplyChainStep. `fail_step` argument changed to string-type
`fail_step_name`

---

## v0.1.6 -- released 29 Sept 2021

### Features

- Add support for `forced_delete` mode to `files.RallyFile.remove_location()` method. This option removes a file
location from the asset's inventory and deletes the file even if it is referenced by another asset.
- Add support for `forced_delete` mode to `files.remove_inventory()` method. This option removes a file reference from
the asset's inventory and deletes the file locations even if they are referenced by another asset.

### Fixes

---

## v0.1.5 -- released 31 Aug 2021

### Features

- Add `set_scheduled_supply_chain` to the supplyChain submodule, allowing users to schedule a supply chain for the
  current asset
- Add `get_scheduled_supply_chain` to the supplyChain submodule, returning a dict representation of an arbitrary asset's
  scheduled supply chain

### Fixes

- Fix an issue with the SDK improperly handling missing environment variable

---

## v0.1.4 -- released 03 Aug 2021

### Features

- Add `presigned_url` method to `RallyFile`. This returns a presigned url for a file.
- Add `asset_name` and `category` arguments to `jobs.get_jobs_for_asset` method.
- Add `inputFileLabel` to dictionary returned by `jobs.get_jobs_for_asset`.
- Add `fail_step` argument to `supplyChain.SupplyChainStep` creation to specify a step to execute if the next step fails.
- Add `jobs.cancel_job` method to cancel a job given its UUID.
- `supplyChain.set_supply_chain_metadata` now overwrites existing metadata with the new value.
  This enables users to remove top-level keys.

### Fixes

- `supplyChain.SupplyChainSplit.add_split` param `async` has been renamed to `run_async`.

---

## v0.1.3 -- released 20 Jul 2021

### Features

- Add `asset_name` argument to `jobs.get_job_report` method. This allows users to retrieve QC or analyze data from
  arbitrary assets using the supplied provider type and label.

### Fixes

---

## v0.1.2 -- released 22 June 2021

### Features

- Add `files.write_files` method that offers parallel writing of files given a dict of URLs and content
- Add `files.read_files` method that offers parallel reading of files given a sequence of URLs
  **Caution should be used when reading multiple files**
- `files.list_files` now returns both files and (subdirectories) at the specified url.
- Add License-only deadline argument `step_deadline_lic_only` to `supplyChain.SupplyChainStep`
- `SupplyChainSplit` and `SupplyChainCancel` can now take a `SupplyChainSequence`

### Fixes

- `SupplyChainStep` now correctly recognizes `provider_filter` values

---

## v0.1.1 -- released 16 Mar 2021

### Features

- Initial Beta offering.
