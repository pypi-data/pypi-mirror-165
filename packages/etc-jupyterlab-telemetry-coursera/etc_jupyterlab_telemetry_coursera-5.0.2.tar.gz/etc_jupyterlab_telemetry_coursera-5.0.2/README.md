# ETC JupyterLab Telemetry Coursera

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/educational-technology-collective/etc_jupyterlab_telemetry_coursera/main?urlpath=lab)

A JupyterLab telemetry extension that logs telemetry events to a AWS S3 Bucket.

## Requirements

* JupyterLab >= 3.0

## Dependencies

### ETC JupyterLab Telemetry Library (`etc-jupyterlab-telemetry-library`)

This extension requires the ETC JupyterLab Telemetry Library. The ETC JupyterLab Telemetry Library provides the JupyterLab events that are consumed by this extension.

### ETC JupyterLab Notebook State Provider (`etc-jupyterlab-notebook-state-provider`)

This extension will use the ETC JupyterLab Notebook State Provider in order to produce diffs of the Notebooks that it receives from the ETC JupyterLab Telemetry Library.  This extension will log the diffs of the Notebooks, as opposed the entire Notebook.

Each message contains an *incremental* representation of the Notebook.  A Notebook cell will contain just the cell ID if the cell input and output haven't changed since the last event; otherwise, if the cell has changed since the last logged event, the entire contents of the cell will be logged. By providing incremental representations of the Notebook each message will requires less storage.  

This incremental logging approach allows for messages to be reconstructed by using the cell contents contained in previously logged messages i.e., the cell IDs are used in order to obtain the contents of the cell from a previously logged cell.

Please note that in order to reconstruct messages all *enabled* events must be logged.  Please see the Configuration section of the "ETC JupyterLab Telemetry Library" for details on how to toggle events.

## Configuration

The AWS endpoint that is used for storing telemetry data is configurable.  The configuration file must be named `jupyter_etc_jupyterlab_telemetry_coursera_config.py`.  The configuration file must be placed in one of the config directories given by `jupyter --paths` e.g., `/etc/jupyter`.

This is an example of a valid configuration file:

```py
#  This file should be saved into one of the config directories provided by `jupyter lab --path`.

#  The url of the S3 bucket, which will comprise the first component of the bucket_url.
c.ETCJupyterLabTelemetryCourseraApp.url = "https://telemetry.mentoracademy.org"

#  bucket will be appended to the bucket_url after the url.
c.ETCJupyterLabTelemetryCourseraApp.bucket = "telemetry-edtech-labs-si-umich-edu"

# path will be appended to the bucket_url after the bucket.
c.ETCJupyterLabTelemetryCourseraApp.path = "dev/test-telemetry"

#  The values of env_path_segment_names will be appended to the bucket_url after the path.
c.ETCJupyterLabTelemetryCourseraApp.env_path_segment_names = ['COURSE_ID']

#  If a .telemetry file is present in the Lab home directory its contents will
#  be appended to the bucket_url after the env_path_segment_names.  The .telemetry
#  file should contain a relative path e.g., "segment1/segment2".

#  Telemetry can be turned on by either setting telemetry to True or by touching the .telemetry file in the Lab home directory.
# c.ETCJupyterLabTelemetryCourseraApp.telemetry = True

```

## Install

To install the extension:

```bash
pip install etc-jupyterlab-telemetry-coursera
```

## Uninstall

To remove the extension, execute:

```bash
pip uninstall etc-jupyterlab-telemetry-coursera
```

## Troubleshoot

If you are seeing the frontend extension, but it is not working, check
that the server extension is enabled:

```bash
jupyter server extension list
```

If the server extension is installed and enabled, but you are not seeing
the frontend extension, check the frontend extension is installed:

```bash
jupyter labextension list
```
## Contributing

### Development install

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the etc_jupyterlab_telemetry_coursera directory
# Install package in development mode
pip install -e .
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Server extension must be manually installed in develop mode
jupyter server extension enable etc_jupyterlab_telemetry_coursera
# Rebuild extension Typescript source after making changes
jlpm run build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm run watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm run build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
# Server extension must be manually disabled in develop mode
jupyter server extension disable etc_jupyterlab_telemetry_coursera
pip uninstall etc_jupyterlab_telemetry_coursera
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `@educational-technology-collective/etc_jupyterlab_telemetry_coursera` within that folder.
