import curses

class Utilities:
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.move(0, 0)
        self.win1 = curses.newwin(curses.LINES, int(curses.COLS / 2), 0, int(curses.LINES / 2))

    def print(self, msg, winid=0):
        if winid == 0:
            self.stdscr.addstr(msg)
            self.stdscr.refresh()
        elif winid == 1:
            self.win1.addstr(msg)
            self.win1.refresh()

    def wait(self):
        c = self.stdscr.getch()
        if c == curses.KEY_ENTER:
            return
