from tuiapp import TuiApp
from guiapp import GuiApp
from info import Info
from client import Client

class App:
  def __init__(self, file_path: str):
    self.info = Info(file_path)
    self.info.load_info()

  def run(self):
    formats = self.info.formats
    patterns = self.info.patterns
    client = Client(formats=formats, patterns=patterns)

    # self.gui_init(client)
    self.tui_init(client)

  def tui_init(self, client):
    app = TuiApp(client)
    app.run()

  def gui_init(self, client):
    app = GuiApp(client)
    app.run()

if __name__ == "__main__":
  app = App('info3.json')

  app.run()
