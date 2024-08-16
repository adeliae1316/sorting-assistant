# sorting-assistant

[![PyPI - Version](https://img.shields.io/pypi/v/sorting-assistant.svg)](https://pypi.org/project/sorting-assistant)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sorting-assistant.svg)](https://pypi.org/project/sorting-assistant)

---

A tool that determines sets of photos taken consecutively based on the Exif shooting date and exposure time, and creates a directory for each set.

**_[ja]_**  
Exif の撮影日時と露光時間から、連続撮影された写真のセットを判断し、セットごとにディレクトリを作成するツール。

## Table of Contents

- [Specification](#specification)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)
- [Acknowledgment](#acknowledgment)

## Specification

- Only JPEG-format photos with Exif data are acceptable.
- If the difference between the date and time of shooting in the Exif is within ±2 seconds of the exposure time,
  the camera is considered to have taken consecutive shots.
- Directories for each set are created in the directory to be sorted.
  - The directory names created will be sequentially numbered from 0000.

**_[ja]_**

- Exif が記録されている JPEG 形式の写真のみ対象です。
- Exif の撮影日時の差が、露光時間 ±2 秒以内の場合に、連続撮影されたと判断します。
- セットごとのディレクトリは、仕分け対象のディレクトリ内に作成します。
  - 作成されるディレクトリ名は 0000 からの連番となります。

## Installation

```console
pip install sorting-assistant
```

### Dependency

- Modules

  - [exif](https://pypi.org/project/exif)
  - [flet](https://pypi.org/project/flet)

- Libraries

  If you do not use the GUI, you can omit installation.

  **_[ja]_**  
  GUI を使用しない場合は、インストールを省略できます。

  ```bash
  # For Ubuntu 20.04; Mac and Windows do not require installation.
  sudo apt install libgtk-3-dev libgstreamer-plugins-base1.0-dev libmpv-dev zenity
  ```

## Usage

```bash
$ python -m sorting_assistant -h
usage: python -m sorting_assistant [-h] [--input-directory INPUT_DIRECTORY] [--grouping-threshould GROUPING_THRESHOULD] [--cli]

Sort photos based on Exif.

options:
  -h, --help            show this help message and exit
  --input-directory INPUT_DIRECTORY, -d INPUT_DIRECTORY
                        [required in cli] directory containing photos to be sorted.
  --grouping-threshould GROUPING_THRESHOULD, -t GROUPING_THRESHOULD
                        [optional, default: 1] threshold for the number of photos to be directory (0-99).
  --cli, -c             [optional, default: launch with gui] execute with CLI.
```

### CLI

```bash
# Use as module.
python -m sorting_assistant -d /path/to/image/dir -t 1 -c
# Or, use with pyproject script.
sorting-assistant-cli -d /path/to/image/dir -t 1
```

### GUI

```bash
# Use as module.
python -m sorting_assistant
python -m sorting_assistant -d /path/to/image/dir -t 1
# Or, use with pyproject script.
sorting-assistant-gui
sorting-assistant-gui -d /path/to/image/dir -t 1
```

![sorting assistant flet](https://raw.githubusercontent.com/adeliae1316/sorting-assistant/develop/sorting-assistant-flet.png)

- Set the `Directory Path` and `Grouping threshould` and press the `Execute` button to execute.
- When specifying the `Directory Path`, you can press `Select` to display the file selection dialog.
- DnD is not supported because flet does not support DnD ([flet-dev/flet#112](https://github.com/flet-dev/flet/issues/112)).

**_[ja]_**

- `Directory Path` と `Grouping threshould` を設定して、`Execute` ボタンを押すと実行されます。
- `Directory Path` を指定する際、`Select` を押すとファイルセレクションダイアログを表示できます。
- flet が DnD に対応していない ([flet-dev/flet#112](https://github.com/flet-dev/flet/issues/112)) ため、DnD は非対応です。

## License

`sorting-assistant` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

**_[ja]_**  
`sorting-assistant` は [MIT](https://spdx.org/licenses/MIT.html)ライセンス の下で配布されています。

## Acknowledgment

This tool uses the following libraries. Thank you.

**_[ja]_**  
このツールでは、以下のライブラリを使用しています。ありがとうございます。

| Library                                    | Author         | License                                                                  |
| ------------------------------------------ | -------------- | ------------------------------------------------------------------------ |
| [exif](https://gitlab.com/TNThieding/exif) | Tyler Thieding | [MIT License](https://gitlab.com/TNThieding/exif/-/blob/master/LICENSE)  |
| [flet](https://flet.dev)                   | flet-dev       | [Apache License 2.0](https://github.com/flet-dev/flet/blob/main/LICENSE) |
