# Configuration

[한국어](/CONFIG.ko.md)

You can access the Open Dccon Selector configuration by clicking the gear icon on the bottom right corner of the Open
Dccon Selector element in the "Extensions" section of the Twitch dashboard.

## 1. Dccon URL

The Dccon URL is the URL for fetching the Dccon data.

This value must be a URL of the data in a format supported by the Open Dccon Selector.

For more information, see [Supported Dccon types](#21-supported-dccon-types).

## 2. Dccon Type

Dccon Type specifies the format of the Dccon data provided by the Dccon URL.

Open Dccon Selector does not work if Dccon Type value and the Dccon data provided by the Dccon URL are different.

### 2.1. Supported Dccon types

#### 2.1.1. Open Dccon Format

Open Dccon Format is the Dccon format used by [JSAssist Open DCcon](https://github.com/rishubil/jsassist-open-dccon),
and it is also the default Dccon type of Open Dccon Selector.

Example: [https://rishubil.github.io/jsassist-open-dccon/static/dccon_list.json](https://rishubil.github.io/jsassist-open-dccon/static/dccon_list.json)

#### 2.1.2. Open Dccon Format (Relative path)

Open Dccon Format (Relative path) is basically the same as Open Dccon Format, except that the URL of the `path`
value is a relative path, not an absolute path.

#### 2.1.3. Funzinnu Dccon Format

Funzinnu Dccon Format is the Dccon format used by [Funzinnu](https://www.twitch.tv/funzinnu).

Example: [http://funzinnu.cafe24.com/stream/dccon.php](http://funzinnu.cafe24.com/stream/dccon.php)

#### 2.1.4. Telk Dccon Format

Telk Dccon Format is the Dccon format used by [Telk](https://www.twitch.tv/telk5093).

Example: [http://tv.telk.kr/?mode=json](http://tv.telk.kr/?mode=json)

## 3. Cache Dccon data to server

If this option is enabled, Dccon data is cached in the Open Dccon Selector server to use.

(Exclude Dccon image files)

You can not disable the option for all Dccon types except Open Dccon Format.

## 3.1. Why can not I disable this option for all Dccon types except Open Dccon Format?

Basically, Open Dccon Selector converts all Dccon data into Open Dccon Format through internal processing.

However, since Dccon data is not changed frequently and it is inefficient to convert it every request, so all data
except Open Dccon Format is cached data only.

# 4. Test data format

This function checks whether the entered Dccon URL and Dccon Type value are accessible to the Dccon data.

# 5. Updated cached Dccon data

This function re-caches the Dccon data.

It will not work for the unsaved setting values. If you change the setting, you must save the setting contents before
use.

It can not be used if 'Cache Dccon data to server' option is disabled.
