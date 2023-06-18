from pywinauto.application import Application

# Start a new Notepad process
app = Application().start("notepad.exe")

# Interact with the menu
app.Notepad.menu_select("Help->About Notepad")
app.AboutNotepad.OK.click()

# Type some text
app.Notepad.Edit.type_keys("Hello, World!", with_spaces=True)
