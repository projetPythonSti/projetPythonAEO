import curses

class CLIView():
    
    def __init__(self):
        pass
    
    def affichage(self, stdscr):
        curses.curs_set(0)
        stdscr.clear()
        
        letter = list("abcde")
        current = 0
        while(current < len(letter)):
            stdscr.clear()
            stdscr.addstr(0,0,f"Lettre : {letter[current]}")
            stdscr.refresh()
            
            key = stdscr.getch()
            
            if(key == curses.KEY_DOWN):
                current += 1
            
            if current >= len(letter):
                break
        
        # stdscr.getch()

if __name__ == "__main__":
    cli = CLIView()
    curses.wrapper(cli.affichage)
    