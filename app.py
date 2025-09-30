from tuiapp import TuiApp
from guiapp import GuiApp
from info import Info
from client import Client
import sys

class App:
  def __init__(self, file_path: str):
    self.info = Info(file_path)
    self.info.load_info()

  def run(self, mode: str = "tui"):
    formats = self.info.formats
    patterns = self.info.patterns
    client = Client(formats=formats, patterns=patterns)

    if mode and mode.lower() == "gui":
      self.gui_init(client)
    else:
      self.tui_init(client)

  def tui_init(self, client):
    app = TuiApp(client)
    app.run()

  def gui_init(self, client):
    app = GuiApp(client)
    app.run()

if __name__ == "__main__":
  app = App('info3.json')

  mode = sys.argv[1].lower() if len(sys.argv) > 1 else "tui"
  app.run(mode)
