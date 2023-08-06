# fleter
一个flet的扩展组件库，提供一些常用组件及功能。

## SwichThemeButton
用于快速切换窗口主题的图标按钮组件。

### 常规
![](SwichThemeButton.gif)
```python
import flet
import fleter

def main(page: flet.Page):
    swich_theme_button = fleter.SwichThemeButton(page)
    page.add(
        swich_theme_button
    )
    page.update()

flet.app(target=main)
```

### 无系统主题选项
![](SwichThemeButton-None-System.gif)
```python
import flet
import fleter

def main(page: flet.Page):
    swich_theme_button = fleter.SwichThemeButton(page, has_system=False)
    page.add(
        swich_theme_button
    )
    page.update()

flet.app(target=main)
```