# XL Deploy Insights Integration for XL Release

[![Build Status][xlr-xld-insights-plugin-travis-image]][xlr-xld-insights-plugin-travis-url]
![GitHub release](https://img.shields.io/github/release/xebialabs-community/xlr-xld-insights-plugin.svg)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/69e1ca3ab3a14a30bb60499becbb61dc)](https://www.codacy.com/app/ndebuhr/xlr-xld-insights-plugin?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=xebialabs-community/xlr-xld-insights-plugin&amp;utm_campaign=Badge_Grade)
[![License: MIT][xlr-xld-insights-plugin-license-image]][xlr-xld-insights-plugin-license-url]
[![Github All Releases][xlr-xld-insights-plugin-downloads-image]][xlr-xld-insights-plugin-releases-url]
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-blue.svg)](https://github.com/RichardLitt/standard-readme)

> The XLD insights plugin enables the visualization of XLD package information within XL Release

## Installation

### Requirements

1. XL Release 8.0+
1. XL Deploy 8.0+

### Building the plugin
The gradle wrapper facilitates building the plugin.  Use the following command to build using [Gradle](https://gradle.org/):
```bash
./gradlew clean build
```
The built plugin, along with other files from the build, can then be found in the _build_ folder.

### Adding the plugin to XL Release

Download the latest version of the plugin from the [releases page][xlr-xld-insights-plugin-releases-url].  The plugin can then be installed through the graphical interface or the server backend.  For additional detail, please refer to [the docs.xebialabs.com documentation on XLR plugin installation](https://docs.xebialabs.com/xl-release/how-to/install-or-remove-xl-release-plugins.html)

### Configuration

The XL Deploy server can be configured at a global level, in _Shared Configuration_, or on a finer lever (e.g. at the folder level).  Please refer to [the docs.xebialabs.com documentation on configurations](https://docs.xebialabs.com/xl-release/how-to/create-custom-configuration-types.html#configuration-page).  Users may already have XL Deploy connections configured from the [bundled XLR plugin](https://docs.xebialabs.com/v.9.0/xl-release/how-to/standard-xld-plugin/) - the same server configurations are used for this plugin.

## Usage

There are no tasks associated with this plugin - only [dashboard tiles](https://docs.xebialabs.com/v.9.0/xl-release/get-started?subject=dashboards), which visually present XL Deploy package dependency information.  The dashboard tiles available with the plugin can be defined at the release, folder, and/or global scopes.  

## Contributing

Please review the contributing guidelines for _xebialabs-community_ at [http://xebialabs-community.github.io/](http://xebialabs-community.github.io/)

## License

This community plugin is licensed under the [MIT license][xlr-xld-insights-plugin-license-url].

See license in [LICENSE.md](LICENSE.md)

[xlr-xld-insights-plugin-travis-image]: https://travis-ci.org/xebialabs-community/xlr-xld-insights-plugin.svg?branch=master
[xlr-xld-insights-plugin-travis-url]: https://travis-ci.org/xebialabs-community/xlr-xld-insights-plugin
[xlr-xld-insights-plugin-license-image]: https://img.shields.io/badge/license-MIT-yellow.svg
[xlr-xld-insights-plugin-license-url]: https://opensource.org/licenses/MIT
[xlr-xld-insights-plugin-downloads-image]: https://img.shields.io/github/downloads/xebialabs-community/xlr-xld-insights-plugin/total.svg
[xlr-xld-insights-plugin-releases-url]: https://github.com/xebialabs-community/xlr-xld-insights-plugin/releases
