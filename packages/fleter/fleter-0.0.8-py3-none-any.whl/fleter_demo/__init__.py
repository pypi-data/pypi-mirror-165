import flet
import fleter


def run():
    def main(page: flet.Page):
        swich_theme_button = fleter.SwichThemeButton(page)
        page.add(
            swich_theme_button
        )
        page.update()

    flet.app(target=main)


if __name__ == '__main__':
    run()
