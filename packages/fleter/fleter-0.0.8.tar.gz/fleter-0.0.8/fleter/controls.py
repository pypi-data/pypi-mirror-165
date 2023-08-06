import flet
from typing import Any, List, Optional, Union

from beartype import beartype

from flet.constrained_control import ConstrainedControl
from flet.control import (
    Control,
    CrossAxisAlignment,
    MainAxisAlignment,
    OptionalNumber,
    ScrollMode,
    TextAlign,
    InputBorder
)
from flet.focus import FocusData
from flet.form_field_control import FormFieldControl
from flet.dropdown import Option
from flet.ref import Ref
from flet.types import AnimationValue, OffsetValue, RotateValue, ScaleValue, BorderRadiusValue, PaddingValue
from fleter import buttons

__all__ = [
    "HeaderBar",
    "ComboBox"
]


class HeaderBar(flet.Row):
    def __init__(self, page: flet.Page,
                 controls: Optional[List[Control]] = None,
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
                 visible: Optional[bool] = None,
                 disabled: Optional[bool] = None,
                 data: Any = None,
                 #
                 # Row specific
                 #
                 alignment: MainAxisAlignment = None,
                 vertical_alignment: CrossAxisAlignment = None,
                 spacing: OptionalNumber = None,
                 tight: Optional[bool] = None,
                 wrap: Optional[bool] = None,
                 run_spacing: OptionalNumber = None,
                 scroll: ScrollMode = None,
                 auto_scroll: Optional[bool] = None,
                 #
                 # HeaderBar specific
                 #
                 has_close: bool = True,
                 title: str = "",
                 title_align: TextAlign = "center"
                 ):
        """

        :param page: 为被设置页面窗口
        :param has_close: 决定是否有关闭按钮
        :param title: 设置标题栏的标题
        :param title_align: 设置标题栏的标题对齐
        """
        super(HeaderBar, self).__init__(
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
            visible=visible,
            disabled=disabled,
            data=data,
            #
            # Row specific
            #
            alignment=alignment,
            vertical_alignment=vertical_alignment,
            spacing=spacing,
            tight=tight,
            wrap=wrap,
            run_spacing=run_spacing,
            scroll=scroll,
            auto_scroll=auto_scroll,
        )
        self._page = page
        self._page.window_title_bar_hidden = True
        self._page.window_title_bar_buttons_hidden = True

        self._title = title

        self._title_widget = flet.Text(title, size=18, text_align=title_align)
        self._title_area = flet.Container(self._title_widget, padding=15)
        self._darg_area = flet.WindowDragArea(self._title_area, expand=True)

        self.controls.append(
            self._darg_area,
        )

        self._has_close = has_close

        if has_close:
            self.controls.append(
                buttons.CloseButton(page)
            )

    @property
    def title_align(self):
        return self._title_widget.text_align

    @title_align.setter
    def title_align(self, align: TextAlign = "center"):
        self._title_widget.text_align = align

    @property
    def has_close(self):
        return self._has_close

    @property
    def title(self):
        return self._title_widget.value

    @title.setter
    def title(self, title: str):
        self._title_widget.value = title

    @property
    def title_widget(self):
        return self._title_widget

    @title_widget.setter
    def title_widget(self, widget):
        self._title_widget = widget

    @property
    def title_area(self):
        return self._title_area

    @property
    def darg_area(self):
        return self._darg_area


class ComboBox(flet.Dropdown):
    def __init__(self,
                 ref: Optional[Ref] = None,
                 width: OptionalNumber = None,
                 height: OptionalNumber = None,
                 expand: Union[None, bool, int] = None,
                 opacity: OptionalNumber = None,
                 tooltip: Optional[str] = None,
                 visible: Optional[bool] = None,
                 disabled: Optional[bool] = None,
                 data: Any = None,
                 #
                 # FormField specific
                 #
                 text_size: OptionalNumber = None,
                 label: Optional[str] = None,
                 icon: Optional[str] = None,
                 border: InputBorder = None,
                 color: Optional[str] = None,
                 bgcolor: Optional[str] = None,
                 border_radius: BorderRadiusValue = None,
                 border_width: OptionalNumber = None,
                 border_color: Optional[str] = None,
                 focused_color: Optional[str] = None,
                 focused_bgcolor: Optional[str] = None,
                 focused_border_width: OptionalNumber = None,
                 focused_border_color: Optional[str] = None,
                 content_padding: PaddingValue = None,
                 filled: Optional[bool] = None,
                 hint_text: Optional[str] = None,
                 helper_text: Optional[str] = None,
                 counter_text: Optional[str] = None,
                 error_text: Optional[str] = None,
                 prefix: Optional[Control] = None,
                 prefix_icon: Optional[str] = None,
                 prefix_text: Optional[str] = None,
                 suffix: Optional[Control] = None,
                 suffix_icon: Optional[str] = None,
                 suffix_text: Optional[str] = None,
                 #
                 # DropDown Specific
                 #
                 value: Optional[str] = None,
                 autofocus: Optional[bool] = None,
                 options: Optional[str] = [""],
                 on_change=None,
                 on_focus=None,
                 on_blur=None,
                 ):
        super(ComboBox, self).__init__(
            ref=ref,
            width=width,
            height=height,
            expand=expand,
            opacity=opacity,
            tooltip=tooltip,
            visible=visible,
            disabled=disabled,
            data=data,
            #
            # FormField specific
            #
            text_size=text_size,
            label=label,
            icon=icon,
            border=border,
            color=color,
            bgcolor=bgcolor,
            border_radius=border_radius,
            border_width=border_width,
            border_color=border_color,
            focused_color=focused_color,
            focused_bgcolor=focused_bgcolor,
            focused_border_width=focused_border_width,
            focused_border_color=focused_border_color,
            content_padding=content_padding,
            filled=filled,
            hint_text=hint_text,
            helper_text=helper_text,
            counter_text=counter_text,
            error_text=error_text,
            prefix=prefix,
            prefix_icon=prefix_icon,
            prefix_text=prefix_text,
            suffix=suffix,
            suffix_icon=suffix_icon,
            suffix_text=suffix_text,
            #
            # DropDown Specific
            #
            value=value,
            autofocus=autofocus,
            on_change=on_change,
            on_focus=on_focus,
            on_blur=on_blur,
        )

        self._option = []
        self._options = options

        self.option = self._options

    @property
    def option(self):
        return self._option

    @option.setter
    def option(self, list):
        self._options = list

        for item in self._options:
            self._option.append(Option(item))

        self.options = self._option
