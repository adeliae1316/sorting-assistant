# SPDX-FileCopyrightText: 2024 adeliae1316 <knsak.ug487@gmail.com>
#
# SPDX-License-Identifier: MIT

import argparse
import datetime
import glob
import os
import shutil
import sys

import exif


def initialize_parser(prog: str = os.path.basename(sys.argv[0])):
    parser = argparse.ArgumentParser(
        prog=prog, description="Tool for sorting photos based on Exif."
    )
    parser.add_argument(
        "--input-directory",
        "-d",
        help="[required in cli] directory containing photos to be sorted.",
    )
    parser.add_argument(
        "--grouping-threshould",
        "-t",
        help="[optional, default: 1] threshold for the number of photos to be directory (0-99).",
        type=int,
        default=1,
    )
    parser.add_argument(
        "--cli",
        "-c",
        help="[optional, default: launch with gui] execute with CLI.",
        action="store_true",
    )
    return parser.parse_args()


def get_image_info_list(directory_path: str):
    image_info_list = []
    temp_list = [
        f
        for f in glob.glob(f"{directory_path}/*")
        if "jpg" in f or "JPG" in f or "jpeg" in f or "JPEG" in f
    ]
    for path in temp_list:
        with open(path, "rb") as image_file:
            image = exif.Image(image_file)
            if image and image.has_exif:
                image_info_list.append(
                    {
                        "path": path,
                        "datetime": image.datetime,
                        "exposure_time": image.exposure_time,
                    }
                )
    return sorted(image_info_list, key=lambda info: info["datetime"])


def get_sort_list(image_info_list: list):
    INTERVAL_THRESHOULD_SEC = 2
    EXIF_DATETIME_FORMAT = "%Y:%m:%d %H:%M:%S"
    composition_list = []
    composition_list_index = 0
    previous = None
    for info in image_info_list:
        if previous is not None:
            previous_datetime = datetime.datetime.strptime(
                previous["datetime"], EXIF_DATETIME_FORMAT
            )
            previous_timestamp = int(previous_datetime.timestamp())
            current_datetime = datetime.datetime.strptime(
                info["datetime"], EXIF_DATETIME_FORMAT
            )
            current_timestamp = int(current_datetime.timestamp())
            if (
                abs(
                    current_timestamp
                    - previous_timestamp
                    - int(previous["exposure_time"])
                )
                <= INTERVAL_THRESHOULD_SEC
            ) and 0 < len(composition_list):
                # Same composition.
                composition_list[composition_list_index].append(info["path"])
            else:
                # Other composition.
                composition_list_index = len(composition_list)
                composition_list.append([])
                composition_list[composition_list_index].append(info["path"])
        previous = info
    return composition_list


def copy(base_dir: str, sort_list: list):
    index = 0
    for index, list in enumerate(sort_list):
        dest_dir = os.path.join(base_dir, str(index).zfill(4))
        try:
            os.mkdir(dest_dir)
        except:
            return "Move or delete directories created during previous runs."
        for path in list:
            shutil.copy2(path, dest_dir)
        index = index + 1
    return ""


def execute(input_directory: str, grouping_threshould: int):
    if input_directory is None or input_directory == "":
        return "Directory Path is not set."
    elif os.path.exists(input_directory) is False:
        return "The specified directory does not exist."
    elif os.path.isdir(input_directory) is False:
        return "The specified path is not a directory."
    else:
        list = get_image_info_list(input_directory)
        sort_list = get_sort_list(list)
        filtered_sort_list = [
            sub_list for sub_list in sort_list if len(sub_list) > grouping_threshould
        ]
        return copy(input_directory, filtered_sort_list)


def cli(args=initialize_parser()):
    message = execute(args.input_directory, args.grouping_threshould)
    if message == "":
        print("Success to sort.")
    else:
        print(f"Failure to sort. {message}")

    return 0 if message == "" else 1


def gui(args=initialize_parser()):
    if __name__ == "__main__":
        if os.path.basename(sys.argv[0]) == "sorting_assistant.py":
            # Execute as script (python ./sorting_assistant.py)
            from sorting_assistant_flet import launch
        else:
            # Execute as binary (./dist/sorting-assistant)
            from sorting_assistant.sorting_assistant_flet import launch
    else:
        # Execute as module via __main__.py (python -m sorting_assistant)
        from .sorting_assistant_flet import launch

    launch(
        args.input_directory,
        args.grouping_threshould,
        lambda input_directory, grouping_threshould: execute(
            input_directory, grouping_threshould
        ),
    )


def main(args=initialize_parser()):
    result = 0

    if args.cli:
        result = cli(args)
    else:
        gui(args)

    return result


if __name__ == "__main__":
    sys.exit(main())
