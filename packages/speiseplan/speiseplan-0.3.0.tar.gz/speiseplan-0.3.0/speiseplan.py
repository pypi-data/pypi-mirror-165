import subprocess
import platform


FOOD_STORES = {
    "Cafe Midi": lambda: "https://cafemidi.de/lunch/",
    "Justizzentrum": lambda: "https://www.essenzzeit.de/de/essenzzeit-restaurants-in-potsdam/bistro-im-justizzentrum-_-9.html",
    "Rathaus": lambda: "https://company-catering.widynski-roick.de/menu/Stadtverwaltung%20Potsdam/Stadtverwaltung%20Potsdam",
}


def main():
    open_cmd = "open" if platform.system() == "Darwin" else "xdg-open"

    for place, method in FOOD_STORES.items():
        try:
            menu = method()
            subprocess.run([open_cmd, menu])
        except Exception:
            print(f"{name} not available today!")


if __name__ == "__main__":
    main()
