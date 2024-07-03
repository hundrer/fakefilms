from tkinter import *
from sys import argv


class FilmPlayer:
    def __init__(self, root):
        self.root = root
        self.root.iconbitmap(r'Fakefilms_icon.ico')
        self.canvas = Canvas(root, width=1280, height=720, bg="black")
        self.canvas.grid()
        self.dist_obj = {"background": None}

    def set_title(self, text):
        self.canvas.delete("all")
        self.canvas.create_text(650, 50, text=text, font=("Arial", 30, "bold"), fill="white")

    def end_film(self):
        self.canvas.create_text(650, 680, text="Показ фильма завершен. Вы можете закрыть это окно.",
                                font=("Arial", 20, "bold"), fill="red")

    def process_line(self, index, content):
        if index >= len(content):
            self.end_film()
            self.root.update()
            return
        line = content[index].replace("\t", "").split()
        try:
            if line[0] == "title":
                del line[0]
                line = " ".join(line)
                self.set_title(line)
                self.dist_obj = {"background": None}

            elif line[0] == "sleep":
                self.root.after(int(float(line[1]) * 1000), self.process_line, index + 1, content)
                return

            elif line[0] == "rem":
                pass  # комментарий

            elif line[0] == "spawn":
                if line[2] == "rectangle":
                    self.dist_obj[line[1]] = [
                        self.canvas.create_rectangle(int(line[3]), int(line[4]), int(line[5]), int(line[6]),
                                                     fill=line[7].replace("\n", "")), {
                            "nickname": self.canvas.create_text(
                                int(line[3]) + (int(line[5]) / 2 - int(line[3]) / 2), int(line[4]) - 25,
                                text="", font=("Arial", 15, "bold"), fill="white"),
                            "action": self.canvas.create_text(
                                int(line[3]) + (int(line[5]) / 2 - int(line[3]) / 2), int(line[6]) + 25,
                                text="", font=("Arial", 15, "bold"), fill="white")}]
                elif line[2] == "oval":
                    self.dist_obj[line[1]] = [
                        self.canvas.create_oval(int(line[3]), int(line[4]), int(line[5]), int(line[6]),
                                                fill=line[7].replace("\n", "")), {
                            "nickname": self.canvas.create_text(
                                int(line[3]) + (int(line[5]) / 2 - int(line[3]) / 2), int(line[4]) - 25,
                                text="", font=("Arial", 15, "bold"), fill="white"),
                            "action": self.canvas.create_text(
                                int(line[3]) + (int(line[5]) / 2 - int(line[3]) / 2), int(line[6]) + 25,
                                text="", font=("Arial", 15, "bold"), fill="white")}]

            elif line[0] == "edit":
                if line[2] == "color":
                    if line[1] == "background":
                        self.canvas.config(bg=line[3].replace("\n", ""))
                    else:
                        self.canvas.itemconfig(self.dist_obj[line[1]][0], fill=line[3].replace("\n", ""))
                elif line[2] == "nickname":
                    self.canvas.itemconfig(self.dist_obj[line[1]][1]["nickname"], text=" ".join(line[3:]))
                elif line[2] == "action":
                    self.canvas.itemconfig(self.dist_obj[line[1]][1]["action"], text=" ".join(line[3:]))

            elif line[0] == "move":
                self.canvas.move(self.dist_obj[line[1]][0], int(line[2]), int(line[3]))
                if self.dist_obj[line[1]][1] is not None:
                    self.canvas.move(self.dist_obj[line[1]][1]["nickname"], int(line[2]), int(line[3]))
                    self.canvas.move(self.dist_obj[line[1]][1]["action"], int(line[2]), int(line[3]))

            elif line[0] == "delete":
                if line[1] == "background":
                    print("Warning: Cannot delete the background")
                else:
                    line[1] = line[1].replace("\n", "")
                    self.canvas.delete(self.dist_obj[line[1]][0])
                    if self.dist_obj[line[1]][1] is not None:
                        self.canvas.delete(self.dist_obj[line[1]][1]["nickname"])
                        self.canvas.delete(self.dist_obj[line[1]][1]["action"])
                    del self.dist_obj[line[1]]

            elif line[0] == "clear":
                self.set_title("")
                self.dist_obj = {"background": None}

            elif line[0] == "\n":
                pass

            else:
                print(f"Warning: Unknown function: {line[0]}")
                self.process_line(index + 1, content)

            self.root.update()
            self.root.after(400, self.process_line, index + 1, content)
        except KeyError:
            print("An error occurred, moving on...")
            self.process_line(index + 1, content)
        except IndexError:
            print("An error occurred, moving on...")
            self.process_line(index + 1, content)

if __name__ == "__main__":
    root = Tk()
    root.geometry("1280x720")

    film_player = FilmPlayer(root)

    try:
        with open(argv[1], "r", errors="ignore", encoding="utf-8") as file:
            film_player.process_line(index=0, content=file.readlines())
        root.mainloop()
    except IndexError:
        print("Укажите файл, который нужно воспроизвести.")