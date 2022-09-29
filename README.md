## Description

The code monitors OLX ads and displays new ones.

## Installation

Requires only installation of the following modules:
- bs4
- unidecode
- datetime
- re
- requests
- time
- winsound

Install the modules with:
```bash
npm install $MODULE
```

## Usage

Set the following modules parameters:
- **url** - search page url with all specified filters and sorting type (see an example in the code)
- **song** - path to the alarm sound
- **n_last_offers** - number of viewed offers
- **time_window_new_offers** - time period within which new offers are displayed (in minutes)
- **time_window_all_offers** - time period within which all offers are displayed (in minutes)
- **hours_correction** - time zone correction depending on the user's location (in hours)
- **repeat_delay** - delay between page updates (without code running time) (in seconds)
```python
# ==== PARAMETERS
song = "ringtone.wav"
n_last_offers = 8
time_window_new_offers = 15
time_window_all_offers = 120
hours_correction = 2
repeat_delay = 20
# ==== PARAMETERS
```
### Just run the code and reap the harvest!

The script runs indefinitely, so to terminate it, just stop the execution.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)