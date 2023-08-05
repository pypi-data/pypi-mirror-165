# napari-allencell-annotator

[![License BSD-3](https://img.shields.io/pypi/l/napari-allencell-annotator.svg?color=green)](https://github.com/bbridge0200/napari-allencell-annotator/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-allencell-annotator.svg?color=green)](https://pypi.org/project/napari-allencell-annotator)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-allencell-annotator.svg?color=green)](https://python.org)
[![tests](https://github.com/bbridge0200/napari-allencell-annotator/workflows/tests/badge.svg)](https://github.com/bbridge0200/napari-allencell-annotator/actions)
[![codecov](https://codecov.io/gh/bbridge0200/napari-allencell-annotator/branch/main/graph/badge.svg)](https://codecov.io/gh/bbridge0200/napari-allencell-annotator)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-allencell-annotator)](https://napari-hub.org/plugins/napari-allencell-annotator)

A plugin that enables large image set annotating and writes annotations to a .csv file. 
Plugin provided by the Allen Institute for Cell Science.

The Allen Cell Image Annotator plugin for napari provides an intuitive
graphical user interface to create annotation templates, annotate large 
image sets using these templates, and save image annotations to a csv file. 
The Allen Cell Image Annotator is a Python-based open source toolkit 
developed at the Allen Institute for Cell Science for both blind, unbiased and un-blind 
microscope image annotating. This toolkit supports easy image set selection
from a file finder and creation of annotation templates (text, checkbox, drop-down, and spinbox).
With napari's multi-dimensional image viewing capabilities and AICSImageIO's
image reading and metadata conversion, the plugin seamlessly allows users to
view each image in a set and annotate according to the selected template.
Annotation templates can be written to a json file for sharing or re-using. After annotating,
both annotation template data and the annotations written for the image set 
are saved to csv file, which can be re-opened for further annotating and conveniently
stores annotations.

-   Supports the following image types:
    - `OME-TIFF`
    - `TIFF`
    - `CZI` 
    - `PNG` 
    -   `JPEG` 


----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to files up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/plugins/index.html
-->

## Installation

First install the latest version of napari. Find instructions [here](https://napari.org/stable/tutorials/fundamentals/installation.html). If you are unfamiliar with installing Python packages, follow the section titled _Install as a bundled app_.

### Option 1 (recommended):

After you installed napari, you can go to "Plugins" --> "Install/Uninstall Package(s)". Then, you will be able to see all available napari plugins and you can find us by name `napari-allencell-annotator`. Just click the "install" button to install the Annotator plugin.

### Option 2:

You can also install `napari-allencell-annotator` via [pip]:

    pip install napari-allencell-annotator

## Quick Start

In the current version, there are two parts in the plugin: **Image List** and **Annotation Editor**. 
The **Annotation Editor** allows users to create new annotation templates or upload existing annotation templates 
from a previous plugin-created csv or json file. 
Once an annotation template is chosen and approved, annotating can begin on the image set
selected in the **Image Uploader** section of the plugin. 

1. Open napari
2. Start the plugin 
   - Open napari, go to "Plugins" --> "napari-allencell-annotator".
3. Click create new annotation template or upload existing.
   - Up to 10 new annotations can be created. Each annotation must have a unique name and a type (text, number, checkbox, or dropdown).
   - If the annotation template is uploaded from a csv file, using the image set will open and allow continued editing of all annotations in the csv.
4. Click add images or add files to select images for annotating 
   - The plugin is able to support .tiff, .tif. ome.tif, .ome.tiff, .czi, .png, .jpeg, and .jpg files. 
   - Once selected, the images can be shuffled and hidden or deleted using the checkbox on the right side. 
5. Start Annotating and select or create a .csv file for writing. 
   - If the selected file already exists, it will be overwritten. 
6. Click Save and Exit at any time and all created image annotations will be written to the .csv file. 
   - If the file is opened in the plugin again, annotation will start at the first image with a blank annotation.

## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-allencell-annotator" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/bbridge0200/napari-allencell-annotator/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/
