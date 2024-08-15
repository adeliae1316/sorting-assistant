# SPDX-FileCopyrightText: 2024 adeliae1316 <knsak.ug487@gmail.com>
#
# SPDX-License-Identifier: MIT

from typing import Callable

import flet as ft

_args_input_directory: str = None
_args_grouping_threshould: int = None
_execute_func: Callable[[str, int], str] = None


def window(page: ft.Page):
    page.title = "Sorting Assistant"
    page.window.width = 640
    page.window.height = 320

    directory_path = ft.TextField(value=_args_input_directory)

    # Open directory dialog.
    def get_directory_result(e: ft.FilePickerResultEvent):
        directory_path.value = e.path if e.path else directory_path.value
        directory_path.update()

    get_directory_dialog = ft.FilePicker(on_result=get_directory_result)

    # Hide all dialogs in overlay.
    page.overlay.extend([get_directory_dialog])

    directory_path_select_button = ft.ElevatedButton(
        text="Select",
        icon=ft.icons.FOLDER_OPEN,
        on_click=lambda _: get_directory_dialog.get_directory_path(),
        disabled=page.web,
    )

    grouping_threshould = ft.Dropdown(
        options=[ft.dropdown.Option(str(index)) for index in range(0, 100)],
        value=_args_grouping_threshould,
    )

    container = ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        leading=ft.Icon(ft.icons.SETTINGS),
                        title=ft.Text("Configuration"),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text("Directory Path: ", size=16),
                                        directory_path,
                                        directory_path_select_button,
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.Text("Grouping Threshould: ", size=16),
                                        grouping_threshould,
                                    ]
                                ),
                            ]
                        ),
                        margin=ft.margin.only(20, 10, 20, 10),
                    ),
                ],
            ),
        )
    )

    def set_disabled(disabled: bool):
        directory_path.disabled = disabled
        directory_path_select_button.disabled = disabled
        grouping_threshould.disabled = disabled
        execute_button.disabled = disabled
        directory_path.update()
        directory_path_select_button.update()
        grouping_threshould.update()
        execute_button.update()

    def execute():
        set_disabled(True)

        def handle_close(e: ft.ControlEvent):
            page.close(modal)

        modal = ft.AlertDialog(
            modal=True,
            actions=[
                ft.TextButton("OK", on_click=handle_close),
            ],
        )

        message = _execute_func(directory_path.value, int(grouping_threshould.value))
        if message == "":
            modal.title = ft.Text("Success to sort.")
            modal.content = ft.Text("")
        else:
            modal.title = ft.Text("Failure to sort.")
            modal.content = ft.Text(message)

        page.open(modal)

        set_disabled(False)

    execute_button = ft.ElevatedButton(
        "Execute",
        icon=ft.icons.ROCKET_LAUNCH,
        on_click=lambda _: execute(),
        disabled=page.web,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        width=page.window.width,
        height=60,
    )

    page.add(container, execute_button)


def launch(
    args_input_directory: str,
    args_grouping_threshould: int,
    execute_func: Callable[[str, int], str],
):
    global _args_input_directory
    global _args_grouping_threshould
    global _execute_func

    _args_input_directory = args_input_directory
    _args_grouping_threshould = args_grouping_threshould
    _execute_func = execute_func

    ft.app(target=window)
