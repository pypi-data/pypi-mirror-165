import flet
import flet.icons

from typing import Any, Optional, Union

from beartype import beartype

from flet.buttons import ButtonStyle
from flet.constrained_control import ConstrainedControl
from flet.control import Control, OptionalNumber
from flet.ref import Ref
from flet.types import AnimationValue, OffsetValue, RotateValue, ScaleValue


__all__ = [
    "SwichThemeButton"
]


class SwichThemeButton(flet.IconButton):

    __name__ = "fleter.SwichThemeButton"

    def __init__(self,
                 page: flet.Page,
                 ref: Optional[Ref] = None,
                 width: OptionalNumber = None,
                 height: OptionalNumber = None,
                 left: OptionalNumber = None,
                 top: OptionalNumber = None,
                 right: OptionalNumber = None,
                 bottom: OptionalNumber = None,
                 expand: Union[None, bool, int] = None,
                 opacity: OptionalNumber = None,
                 rotate: RotateValue = None,
                 scale: ScaleValue = None,
                 offset: OffsetValue = None,
                 animate_opacity: AnimationValue = None,
                 animate_size: AnimationValue = None,
                 animate_position: AnimationValue = None,
                 animate_rotation: AnimationValue = None,
                 animate_scale: AnimationValue = None,
                 animate_offset: AnimationValue = None,
                 tooltip: Optional[str] = None,
                 visible: Optional[bool] = None,
                 disabled: Optional[bool] = None,
                 data: Any = None,
                 #
                 # Specific
                 #
                 icon_size: OptionalNumber = None,
                 icon_color: Optional[str] = None,
                 selected_icon: Optional[str] = None,
                 selected_icon_color: Optional[str] = None,
                 selected: Optional[bool] = None,
                 bgcolor: Optional[str] = None,
                 style: Optional[ButtonStyle] = None,
                 content: Optional[Control] = None,
                 autofocus: Optional[bool] = None,
                 on_click=None,
                 ######
                 # Me #
                 ######
                 light_icon=flet.icons.BRIGHTNESS_7,
                 dark_icon=flet.icons.BRIGHTNESS_5,
                 system_icon=flet.icons.BRIGHTNESS_AUTO,
                 has_system: bool = True,
                 ):
        super(SwichThemeButton, self).__init__(
            ref=ref,
            width=width,
            height=height,
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            expand=expand,
            opacity=opacity,
            rotate=rotate,
            scale=scale,
            offset=offset,
            animate_opacity=animate_opacity,
            animate_size=animate_size,
            animate_position=animate_position,
            animate_rotation=animate_rotation,
            animate_scale=animate_scale,
            animate_offset=animate_offset,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            icon_size=icon_size,
            icon_color=icon_color,
            selected_icon=selected_icon,
            selected=selected,
            bgcolor=bgcolor,
            style=style,
            content=content,
            autofocus=autofocus,
            on_click=on_click,
        )

        self._page = page
        if has_system:
            self._page.theme_mode = "system"
        else:
            self._page.theme_mode = "light"
        self._light_icon = light_icon
        self._dark_icon = dark_icon
        self._system_icon = system_icon
        self._has_system = has_system

        if self._page.theme_mode == "light":
            self.icon = light_icon
        elif self._page.theme_mode == "dark":
            self.icon = dark_icon
        elif self._page.theme_mode == "system":
            self.icon = system_icon

        if on_click is None:
            self.on_click = lambda _: self.swich_theme()

    @property
    def light_icon(self):
        return self._light_icon

    @light_icon.setter
    def light_icon(self, icon):
        self._light_icon = icon

    @property
    def dark_icon(self):
        return self._dark_icon

    @dark_icon.setter
    def dark_icon(self, icon):
        self._dark_icon = icon

    @property
    def system_icon(self):
        return self._system_icon

    @system_icon.setter
    def system_icon(self, icon):
        self._system_icon = icon

    @property
    def has_system(self):
        return self._has_system

    @has_system.setter
    def has_system(self, has: bool):
        self._has_system = has

    def swich_theme(self):
        if self._has_system:
            if self._page.theme_mode == "light":
                self.icon = self._dark_icon
                self._page.theme_mode = "dark"

            elif self._page.theme_mode == "dark":
                self.icon = self._system_icon
                self._page.theme_mode = "system"

            elif self._page.theme_mode == "system":
                self.icon = self._light_icon
                self._page.theme_mode = "light"
        else:
            if self._page.theme_mode == "light":
                self.icon = self._dark_icon
                self._page.theme_mode = "dark"

            elif self._page.theme_mode == "dark":
                self.icon = self._light_icon
                self._page.theme_mode = "light"

        self._page.update()


