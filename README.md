# fetchfox

> Because life is too short to manually install Firefox

Fetchfox is a command line tool that helps you to download and install a binary copy of [Mozilla Firefox](https://https://www.mozilla.org/en-US/firefox/) to your Linux desktop. It uses official binary builds provided and hosted by Mozilla.

## How does it work?

Fetchfox talks to Mozilla product API to determine the latest Firefox version available - it then downloads said version and extracts it in `~/.local/share/fetchfox` directory. Fetchfox then creates a `.desktop` entry in `/.local/share/applications` to make your local installation visible to your desktop environment.

Fetchfox does not change your system and does not require root privileges - all files are stored in your home directory.

You can also install a specific version of Firefox instead of using the latest one using `--pin` argument and
providing a specific version to install.

It is possible to install multiple Firefox release branches, for example, the latest stable and developer edition concurrently. However, you can only have one version of each branch at any given time.

## Installation

`sudo pip3 install fetchfox`

## Usage

`fetchfox [-h] [--locale LOCALE] [--arch ARCH] [--pin PIN] [--force] version`

### Positional arguments

#### release

Release branch to install - `stable`, `dev`, `devedition`, `esr` or `nightly`.

#### Optional arguments

`--locale LOCALE`

Locale build of Firefox to download. Defaults to `en-US`.

`--arch ARCH`

Build architecture to install. `linux` for Linux i686, `linux64` for Linux x86_64. Defaults to `linux64`.

`--pin PIN`

A specific version of Firefox to download, for example `78.0.2`. By default will determine the latest available version using Mozilla Product API.

`--force`

Force (re)install, even if there is a locally installed instance with the same version.

## External dependencies and compatibility

Fetchfox is not a package manager and does not manage external dependencies, and does not verify if your environment can run version of Firefox installed by the Fetchfox. It simply automates the download and installation steps to use a binary build already provided by Mozilla.

Fetchfox is developed and tested on Debian Stable.

## License

Licensed under terms and conditions of Apache 2.0 license.

Not affiliated to Mozilla Corporation in any way. Mozilla, Firefox - trademarks of Mozilla Corporation.
