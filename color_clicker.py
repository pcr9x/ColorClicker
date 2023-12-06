from tkinter import *
from tkinter import filedialog
import tkinter.font as tk, tkinter.messagebox, random, pickle, os


class GameFunction:
    def clear_frame(self):
        for widget in window.winfo_children():
            widget.destroy()

    def close(self):
        exit()

    def save(self):
        filepath = filedialog.asksaveasfilename(
            filetypes=[("All Files", "*.*")], title="Save High Score"
        )
        try:
            if not os.path.exists(filepath):
                if filepath is None:
                    raise
                else:
                    f = open(filepath, "wb")
                    pickle.dump(highscore, f)
                    f.close()
                    tkinter.messagebox.showinfo(
                        "Notification", "High Score has been saved"
                    )
            elif os.path.exists(filepath):
                tkinter.messagebox.showerror("Error", "File already exist")
            else:
                raise
        except:
            tkinter.messagebox.showerror("Error", "File not saved")

    def load(self):
        global highscore
        file = filedialog.askopenfile(
            filetypes=[("All Files", "*.*")], title="Load High Score"
        )
        if file is None:
            tkinter.messagebox.showerror("Error", "File not loaded")
        else:
            try:
                f = open(file.name, "rb")
                load = pickle.load(f)
                f.close()
                LoadScore = int(load)
                highscore = LoadScore
                tkinter.messagebox.showinfo(
                    "Notification", "High Score has been loaded"
                )
            except:
                tkinter.messagebox.showerror("Error", "File is not a Score")


class Lobby(GameFunction):
    def __init__(self):
        self.clear_frame()
        name = Label(
            window,
            text="ColorClicker Game",
            font=tk.Font(family="Calibri", size=65, weight="bold"),
        )
        info = Label(
            window,
            text="Select circles with unique colors",
            font=tk.Font(family="Calibri", size=30, weight="bold"),
        )
        font15 = tk.Font(family="Calibri", size=15)
        font15Bold = tk.Font(family="Calibri", size=15, weight="bold")
        rule1 = Label(
            window,
            text="- The faster you answer and the higher level, the more points you get",
            font=font15,
        )
        rule2 = Label(
            window, text="- Every 10 levels, 1 more chance to answer", font=font15
        )
        rule3 = Label(window, text="- Every 25 levels, 1 more circle", font=font15)
        rule4 = Label(window, text="- Wrong answer, one less chance", font=font15)
        choices = ["Test", "Easy", "Medium", "Hard"]
        self.mode = StringVar()
        self.mode.set("Mode")
        OptMode = OptionMenu(window, self.mode, *choices)
        font20Bold = tk.Font(family="Calibri", size=20, weight="bold")
        btEnter = Button(
            window,
            text="Enter the game",
            font=font20Bold,
            command=lambda: self.enter_game(),
        )
        self.HighScore = IntVar()
        self.HighScore.set(highscore)
        lbHighscore = Label(
            window, text="High score:", font=tk.Font(family="Calibri", size=20)
        )
        lbHighscoreNum = Label(
            window, textvariable=self.HighScore, font=tk.Font(family="Calibri", size=20)
        )
        btClose = Button(
            window, text="Exit", font=font15Bold, command=lambda: self.close()
        )
        btLoad = Button(
            window, text="Load", font=font15Bold, command=lambda: self.load()
        )
        btSave = Button(
            window, text="Save", font=font15Bold, command=lambda: self.save()
        )

        name.pack(pady=30)
        info.pack(pady=30)
        rule1.pack(anchor="w", padx=230)
        rule2.pack(anchor="w", padx=230)
        rule3.pack(anchor="w", padx=230)
        rule4.pack(anchor="w", padx=230)
        OptMode.pack(pady=30)
        btEnter.pack(pady=10)
        lbHighscore.place(x=450, y=600)
        lbHighscoreNum.place(x=585, y=600)
        btClose.place(x=1026, y=670)
        btLoad.place(x=510, y=670)
        btSave.place(x=8, y=670)

    def enter_game(self):
        global gbMode
        gbMode = self.mode.get()
        if gbMode != "Mode":
            Game()
        else:
            tkinter.messagebox.showerror("Error", "Select mode")

    def clear_frame(self):
        super().clear_frame()

    def close(self):
        super().close()

    def save(self):
        super().save()

    def load(self):
        super().load()
        self.HighScore.set(highscore)


class Game(GameFunction):
    def __init__(self):
        self.clear_frame()
        self.screen_width = 1080
        self.screen_height = 720
        self.cv = Canvas(window, width=self.screen_width, height=self.screen_height)
        self.cv.pack()
        self.cv.create_rectangle(
            30, 80, self.screen_width - 30, self.screen_height - 80
        )
        self.cv.bind("<Button-1>", self.click)
        self.sec, self.level, self.chance, self.score = (
            IntVar(),
            IntVar(),
            IntVar(),
            IntVar(),
        )
        self.diff = 50
        global gbMode
        if gbMode == "Easy":
            self.sec.set(15)
            self.chance.set(3)
            self.bonus = 10
        elif gbMode == "Medium":
            self.sec.set(10)
            self.chance.set(2)
            self.diff = 45
            self.bonus = 20
        elif gbMode == "Hard":
            self.sec.set(5)
            self.chance.set(1)
            self.diff = 40
            self.bonus = 30
        else:
            self.sec, self.chance = StringVar(), StringVar()
            self.sec.set("-")
            self.chance.set("-")
        self.level.set(1)
        self.score.set(0)
        global currentlevel, currentscore
        currentlevel = self.level.get()
        currentscore = self.score.get()
        self.answer = True
        self.n = 4
        self.circle = []
        self.posx = []
        self.posy = []
        self.r = 50

        font20 = tk.Font(family="Calibri", size=20)
        lbTime = Label(window, text="Time:", font=font20)
        lbTimeNum = Label(window, textvariable=self.sec, font=font20)
        lbLevel = Label(window, text="Level:", font=font20)
        lbLevelNum = Label(window, textvariable=self.level, font=font20)
        lbChance = Label(window, text="Chance:", font=font20)
        lbChanceNum = Label(window, textvariable=self.chance, font=font20)
        lbScore = Label(window, text="Score:", font=font20)
        lbScoreNum = Label(window, textvariable=self.score, font=font20)
        font15Bold = tk.Font(family="Calibri", size=15, weight="bold")
        fnstart = lambda: [btStart.destroy(), self.countdown(), self.random_shape()]
        btStart = Button(
            window,
            text="Start",
            font=tk.Font(family="Calibri", size=20, weight="bold"),
            command=fnstart,
        )
        btHome = Button(window, text="Home", font=font15Bold, command=lambda: Lobby())
        btClose = Button(
            window, text="Exit", font=font15Bold, command=lambda: self.close()
        )
        lbMode = Label(window, text=f"Mode:  {gbMode}", font=font20)

        lbTime.place(x=40, y=17)
        lbTimeNum.place(x=120, y=17)
        lbLevel.place(x=310, y=17)
        lbLevelNum.place(x=390, y=17)
        lbChance.place(x=590, y=17)
        lbChanceNum.place(x=690, y=17)
        lbScore.place(x=900, y=17)
        lbScoreNum.place(x=980, y=17)
        btStart.place(x=495, y=555)
        btHome.place(x=8, y=670)
        btClose.place(x=1026, y=670)
        lbMode.place(x=460, y=670)

    def clear_frame(self):
        super().clear_frame()

    def close(self):
        super().close()

    def countdown(self):
        if gbMode != "Test":
            if self.sec.get() > 0 and self.answer:
                self.sec.set(self.sec.get() - 1)
                window.after(1000, self.countdown)
            elif self.answer:
                try:
                    if self.chance.get() > 1:
                        self.chance.set(self.chance.get() - 1)
                        self.cv.delete("all")
                        self.sec.set(10)
                        self.countdown()
                        self.random_shape()
                except:
                    pass
                else:
                    global reason
                    reason = "Time's up"
                    GameOver()

    def random_shape(self):
        self.circle = []
        self.posx = []
        self.posy = []
        color = random.randint(0, 0x1000000)
        colord = "{:06x}".format(color + self.diff)
        color = "{:06x}".format(color)
        self.cv.create_rectangle(
            30, 80, self.screen_width - 30, self.screen_height - 80
        )
        for i in range(self.n):
            x = random.randint(self.r + 30, self.screen_width - 30 - self.r)
            y = random.randint(self.r + 100, self.screen_height - 100 - self.r)
            # To create a non-overlapping circle.
            if i != 0:
                j = 0
                while j < i:
                    if (x - self.posx[j]) ** 2 + (y - self.posy[j]) ** 2 <= (
                        self.r * 2
                    ) ** 2:
                        x = random.randint(self.r + 30, self.screen_width - 30 - self.r)
                        y = random.randint(
                            self.r + 100, self.screen_height - 100 - self.r
                        )
                        j = 0
                    else:
                        j += 1
            if i != self.n - 1:
                self.circle.append(
                    self.cv.create_oval(
                        x - self.r, y - self.r, x + self.r, y + self.r, fill="#" + color
                    )
                )
            else:
                self.circle.append(
                    self.cv.create_oval(
                        x - self.r,
                        y - self.r,
                        x + self.r,
                        y + self.r,
                        fill="#" + colord,
                    )
                )
            self.posx.append(x)
            self.posy.append(y)

    def click(self, click_event):
        p = click_event
        click_inside_circle = False
        global currentscore, currentlevel, reason
        try:
            if gbMode != "Test":
                if gbMode == "Easy":
                    point, time, bonus = 100, 15, 10
                elif gbMode == "Medium":
                    point, time, bonus = 200, 10, 20
                else:
                    point, time, bonus = 500, 5, 30
                # Check whether mouse position when clicked is inside circle or not
                for i in range(self.n - 1):
                    if (self.posx[i] - p.x) ** 2 + (
                        self.posy[i] - p.y
                    ) ** 2 <= self.r**2:
                        click_inside_circle = True
                # When you click the right circle
                if (self.posx[self.n - 1] - p.x) ** 2 + (
                    self.posy[self.n - 1] - p.y
                ) ** 2 <= self.r**2:
                    if self.level.get() % 10 == 0:
                        self.chance.set(self.chance.get() + 1)
                    self.cv.delete("all")
                    if self.level.get() % 2 == 0:
                        self.diff -= 1
                    if self.level.get() % 25 == 0:
                        self.n += 1
                    self.score.set(
                        self.score.get()
                        + (self.sec.get() * point)
                        + (self.level.get() * 10)
                        + self.bonus
                    )
                    currentscore = self.score.get()
                    self.level.set(self.level.get() + 1)
                    currentlevel = self.level.get()
                    self.bonus += bonus
                    self.sec.set(time)
                    self.random_shape()
                # When you click the wrong circle
                elif click_inside_circle:
                    if self.chance.get() > 1:
                        self.chance.set(self.chance.get() - 1)
                        self.cv.delete("all")
                        self.sec.set(time)
                        self.random_shape()
                    else:
                        reason = "Wrong answer"
                        self.answer = False
                        GameOver()
            else:
                for i in range(self.n - 1):
                    if (self.posx[i] - p.x) ** 2 + (
                        self.posy[i] - p.y
                    ) ** 2 <= self.r**2:
                        click_inside_circle = True
                if (self.posx[self.n - 1] - p.x) ** 2 + (
                    self.posy[self.n - 1] - p.y
                ) ** 2 <= self.r**2:
                    self.cv.delete("all")
                    if self.level.get() % 2 == 0:
                        self.diff -= 1
                    if self.level.get() % 25 == 0:
                        self.n += 1
                    self.score.set(self.score.get() + 100 * self.level.get())
                    currentscore = self.score.get()
                    self.level.set(self.level.get() + 1)
                    self.random_shape()
                elif click_inside_circle:
                    self.cv.delete("all")
                    self.random_shape()
        except:
            pass


class GameOver(GameFunction):
    def __init__(self):
        self.clear_frame()
        global currentscore, highscore, currentlevel
        if currentscore > highscore:
            highscore = currentscore
        lbGOV = Label(
            window,
            text="Game Over!!!",
            font=tk.Font(family="Calibri", size=65, weight="bold"),
        )
        lbReason = Label(window, text=reason, font=tk.Font(family="Calibri", size=30))
        font20 = tk.Font(family="Calibri", size=20)
        lbMode = Label(window, text=f"Mode:  {gbMode}", font=font20)
        lbScore = Label(
            window, text=f"Level:  {currentlevel}\tScore:  {currentscore}", font=font20
        )
        font25Bold = tk.Font(family="Calibri", size=25, weight="bold")
        font15Bold = tk.Font(family="Calibri", size=15, weight="bold")
        btHome = Button(window, text="Home", font=font25Bold, command=lambda: Lobby())
        btPlay = Button(
            window, text="Play again", font=font25Bold, command=lambda: Game()
        )
        btClose = Button(
            window, text="Exit", font=font15Bold, command=lambda: self.close()
        )
        btSave = Button(
            window, text="Save", font=font15Bold, command=lambda: self.save()
        )

        lbGOV.pack(pady=30)
        lbReason.pack(pady=30)
        lbMode.pack(pady=30)
        lbScore.pack(pady=30)
        btHome.place(x=380, y=520)
        btPlay.place(x=540, y=520)
        btClose.pack(side=BOTTOM, anchor="e", padx=8, pady=8)
        btSave.place(x=8, y=670)

    def clear_frame(self):
        super().clear_frame()

    def close(self):
        super().close()

    def save(self):
        super().save()


if __name__ == "__main__":
    window = Tk()
    window.title("ColorClicker Game")
    # Find position to place window in the middle
    LeftPos = (window.winfo_screenwidth() - 1080) / 2
    TopPos = (window.winfo_screenheight() - 720) / 2 - 50
    window.geometry("%dx%d+%d+%d" % (1080, 720, LeftPos, TopPos))
    # Lock the ratio of window size
    window.minsize(1080, 720)
    window.maxsize(1080, 720)
    currentlevel = 1
    currentscore = 0
    highscore = 0
    Lobby()
    window.mainloop()
