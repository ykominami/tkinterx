from tuiapp import TuiApp
from guiapp import GuiApp
from info import Info
from client import Client
import sys

class App:
  def __init__(self, format_path = "info3.json", params_path = "params_map.json"):
    self.client = Client(format_path = format_path, params_path = params_path)

  def run(self, mode: str = "tui"):
    if self.client.patterns is not None:
      if mode and mode.lower() == "gui":
        app = GuiApp(self.client)
      else:
        app = TuiApp(self.client)

      app.run()
    else:
      print("patterns is not loaded")

if __name__ == "__main__":
  app = App('info3.json')
  # app = App(format_path = 'info.json')

  mode = sys.argv[1].lower() if len(sys.argv) > 1 else "tui"
  app.run(mode)
