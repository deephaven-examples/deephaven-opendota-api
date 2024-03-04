# deephaven-opendota-api

This is the repository for the Deephaven OpenDOTA API integration.  It contains functionalities for:

- The top live/most recently played matches
- Constants:
  - Heroes
  - Items
  - Game modes
  - Chatwheel
- Match details

## Usage

Several classes and methods are instantiated upon startup.  The scripts that run on startup can be found in the directory `/data/app.d`.  There is a script in `/data/notebooks` for pulling the top live/recent matches played.

### Constants

Five scripts are run in app mode that create a class containing Dota 2 constants.  These scripts will pull from the OpenDOTA API if no local data is available.  If the data is pulled from the API, it will be written to parquet files in `/data/parquet`.  From then on, as long as these files exist, the constant data will be pulled from those files rather than the API itself.  Note that this constant data tends to change when a new patch for the game is released, so consider occasionally removing all Parquet files from `/data/parquet` to make sure the constant data is up to date.

The class created by these app mode scripts is called `Dota2`.  It has the following attributes:

- `Heroes`
- `GameModes`
- `Items`
- `Chatwheel`

Each of these attributes is a class in and of itself, and has three attributes of its own:

- `json`
  - A list of dicts containing the relevant data
- `dataframe`
  - A Pandas DataFrame containing the relevant data
- `table`
  - A Deephaven table containing the relevant data

If constant data is pulled from the API, it will be created in the order `json` -> `dataframe` -> `table`.  If the data is pulled from local Parquet, it is created in the opposite order.

### Live matches

To get the top live/most recent matches played and many of their attributes, run the `Get_Live_Matches.py` script in `/data/notebooks`.  This creates two tables:

- `live_dota2_matches`
- `live_match_data`

The script will pull live/recent match data once per minute for one hour.  The duration can be changed by updating the `num_pulls` variable in the script.  The `live_match_data` table gets the latest data per Match ID in the table, so it will have the most recent information.

### Match details

The last script run via app mode defines the classes and functions that pull match data for a given match id.  To get match data, run the function `get_dota2_match`.  Here's an example function call:

```python
SomeMatch = get_dota2_match(match_id)
```

The Match ID is an integer.  If the Match ID is invalid, the function will return None instead of a Match class.  If the Match ID is valid, the match class will have the following attributes:

- id
  - The integer match ID.
- Players
  - A class with a very large amount of data in JSON/list format.  For a list of all class attributes, type `vars(SomeMatch.Players)`.
- draft
  - A Deephaven table with draft timing and information.  If the draft has yet to happen, this will be None.
- chat
  - A Deephaven table of chat logs with time stamps.  If there is no chat, this will be None.
- teamfights
  - The teamfight data for the match in JSON format.
- Details
  - A class with match detail information.  For all attributes, type `vars(SomeMatch.Details)`.

The OpenDOTA API is weird about match details for matches in progress.  It is often missing data for certain fields/details of a match.  I've tried to write the code such that this is accounted for, but likely missed some.  If your attempt to pull match data via the `get_dota2_match` function returns an error, please file a ticket with the match ID and the stack trace.

## API Usage Limits

This repository doesn't contain any code or utilities for securely storing an API key.  Usage limits without an API key are as follows:

- 60 requests/min
- 50,000 requests/month

API key support will be added in a future update.  With an API key, the usage limits for free use don't change, but the following limits and pricing to requests beyond free usage (as of June 2022):

- 1200 requests/min
- Unlimited/month
- $.0001/request over the free usage limit, rounded up to the nearest cent

## Note

The code in this repository is built for Deephaven Community Core v0.13.0. No guarantee of forward or backward compatibility is given.

Additionally, the OpenDOTA API has changed since this code was built, and no guarantee of forward or backward compatibilty can be given.

## Disclaimer

Deephaven makes no claim to the validity or authenticity of the data provided by the OpenDOTA API.  Deephaven makes no claim of ownership of the data found on the OpenDOTA API, and will not provide any of its data in this repository.
