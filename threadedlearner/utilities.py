import curses

class Utilities:

    exitTriggered = False
    
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.stdscr.move(0, 0)
        self.win0 = curses.newwin(curses.LINES - 1, int((curses.COLS - 1)/ 2), 0, 0)
        self.win1 = curses.newwin(curses.LINES - 1, int((curses.COLS - 1)/ 2), 0, int((curses.COLS - 1) / 2))
        self.win0.idlok(1)
        self.win1.idlok(1)
        self.win0.scrollok(True)
        self.win1.scrollok(True)
        #self.win0.border()
        #self.win1.border()
        
        # colors
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    def print(self, msg, winid=0):
        if winid == 0:
            self.win0.addstr(msg)
            self.win0.refresh()
        elif winid == 1:
            self.win1.addstr(msg, curses.color_pair(1))
            self.win1.refresh()

    def wait(self):
        c = self.stdscr.getch()
        #if c == curses.KEY_ENTER:
            #return True
        #if c == ord('q'):
        #try: self.win0.addstr(str(c))
        #except: pass
        if c != -1: self.print(chr(c), 0)
        if c == 27:
            self.exitTriggered = True
