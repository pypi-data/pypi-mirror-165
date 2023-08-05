from __future__ import annotations

import importlib
import inspect
import os
from typing import Any, Literal, TypedDict, cast

import yaml
from rich import box
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.rule import Rule
from rich.table import Table


def get_manim_dir() -> str:
    manimlib_module = importlib.import_module("manimlib")
    manimlib_dir = os.path.dirname(inspect.getabsfile(manimlib_module))
    return os.path.abspath(os.path.join(manimlib_dir, ".."))


def remove_empty_value(dictionary: dict[str, Any]) -> None:
    for key in list(dictionary.keys()):
        if dictionary[key] == "":
            dictionary.pop(key)
        elif isinstance(dictionary[key], dict):
            remove_empty_value(dictionary[key])


TDirectories = TypedDict(
    "TDirectories",
    {
        "mirror_module_path": Literal[False],
        "output": str,
        "raster_images": str,
        "vector_images": str,
        "sounds": str,
        "temporary_storage": str,
    },
)
TTex = TypedDict(
    "TTex",
    {
        "executable": str,
        "template_file": str,
        "intermediate_filetype": str,
        "text_to_replace": Literal["[tex_expression]"],
    },
)
TStyle = TypedDict(
    "TStyle",
    {
        "font": Literal["Consolas"],
        "background_color": str,
    },
)
TCameraResolutions = TypedDict(
    "TCameraResolutions",
    {
        "low": Literal["854x480"],
        "med": Literal["1280x720"],
        "high": Literal["1920x1080"],
        "4k": Literal["3840x2160"],
        "default_resolution": str,
    },
)
TConfiguration = TypedDict(
    "TConfiguration",
    {
        "directories": TDirectories,
        "tex": TTex,
        "universal_import_line": Literal["from manimlib import *"],
        "style": TStyle,
        "window_position": Literal["UR"],
        "window_monitor": Literal[0],
        "full_screen": Literal[False],
        "break_into_partial_movies": Literal[False],
        "camera_resolutions": TCameraResolutions,
        "fps": Literal[30],
    },
)


def init_customization() -> None:
    configuration: TConfiguration = {
        "directories": {
            "mirror_module_path": False,
            "output": "",
            "raster_images": "",
            "vector_images": "",
            "sounds": "",
            "temporary_storage": "",
        },
        "tex": {
            "executable": "",
            "template_file": "",
            "intermediate_filetype": "",
            "text_to_replace": "[tex_expression]",
        },
        "universal_import_line": "from manimlib import *",
        "style": {
            "font": "Consolas",
            "background_color": "",
        },
        "window_position": "UR",
        "window_monitor": 0,
        "full_screen": False,
        "break_into_partial_movies": False,
        "camera_resolutions": {
            "low": "854x480",
            "med": "1280x720",
            "high": "1920x1080",
            "4k": "3840x2160",
            "default_resolution": "high",
        },
        "fps": 30,
    }

    console = Console()
    console.print(Rule("[bold]Configuration Guide[/bold]"))
    # print("Initialize configuration")
    try:
        scope = Prompt.ask("  Select the scope of the configuration", choices=["global", "local"], default="local")

        console.print("[bold]Directories:[/bold]")
        dir_config = configuration["directories"]
        dir_config["output"] = Prompt.ask(
            "  Where should manim [bold]output[/bold] video and image files place [prompt.default](optional, default is none)",
            default="",
            show_default=False,
        )
        dir_config["raster_images"] = Prompt.ask(
            "  Which folder should manim find [bold]raster images[/bold] (.jpg .png .gif) in "
            "[prompt.default](optional, default is none)",
            default="",
            show_default=False,
        )
        dir_config["vector_images"] = Prompt.ask(
            "  Which folder should manim find [bold]vector images[/bold] (.svg .xdv) in "
            "[prompt.default](optional, default is none)",
            default="",
            show_default=False,
        )
        dir_config["sounds"] = Prompt.ask(
            "  Which folder should manim find [bold]sound files[/bold] (.mp3 .wav) in "
            "[prompt.default](optional, default is none)",
            default="",
            show_default=False,
        )
        dir_config["temporary_storage"] = Prompt.ask(
            "  Which folder should manim storage [bold]temporary files[/bold] "
            "[prompt.default](recommended, use system temporary folder by default)",
            default="",
            show_default=False,
        )

        console.print("[bold]LaTeX:[/bold]")
        tex_config = configuration["tex"]
        tex = Prompt.ask(
            "  Select an executable program to use to compile a LaTeX source file",
            choices=["latex", "xelatex"],
            default="latex",
        )
        if tex == "latex":
            tex_config["executable"] = "latex"
            tex_config["template_file"] = "tex_template.tex"
            tex_config["intermediate_filetype"] = "dvi"
        else:
            tex_config["executable"] = "xelatex -no-pdf"
            tex_config["template_file"] = "ctex_template.tex"
            tex_config["intermediate_filetype"] = "xdv"

        console.print("[bold]Styles:[/bold]")
        configuration["style"]["background_color"] = Prompt.ask(
            "  Which [bold]background color[/bold] do you want [italic](hex code)", default="#333333"
        )

        console.print("[bold]Camera qualities:[/bold]")
        table = Table("low", "med", "high", "4k", title="Four defined qualities", box=box.ROUNDED)
        table.add_row("480p15", "720p30", "1080p60", "2160p60")
        console.print(table)
        configuration["camera_resolutions"]["default_resolution"] = Prompt.ask(
            "  Which one to choose as the default rendering quality",
            choices=["low", "med", "high", "4k"],
            default="high",
        )

        write_to_file = Confirm.ask("\n[bold]Are you sure to write these configs to file?[/bold]", default=True)
        if not write_to_file:
            raise KeyboardInterrupt

        global_file_name = os.path.join(get_manim_dir(), "manimlib", "default_config.yml")
        if scope == "global":
            file_name = global_file_name
        else:
            if os.path.exists(global_file_name):
                remove_empty_value(cast(dict[str, Any], configuration))
            file_name = os.path.join(os.getcwd(), "custom_config.yml")
        with open(file_name, "w", encoding="utf-8") as f:
            yaml.dump(configuration, f)

        console.print(f"\n:rocket: You have successfully set up a {scope} configuration file!")
        console.print(f"You can manually modify it in: [cyan]`{file_name}`[/cyan]")

    except KeyboardInterrupt:
        console.print("\n[green]Exit configuration guide[/green]")
