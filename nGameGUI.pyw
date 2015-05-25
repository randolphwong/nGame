from combinatorics import *
import re
from Tkinter import *

class App:
    combi = None
    def __init__(self, master):
        master.title('n game')
        frame = Frame(master)
        frame.pack()
        
        txt1 = 'Type the numbers here, separated with space or comma or anything you like: '
        self.lbl1 = Label(frame, text=txt1)
        self.lbl2 = Label(frame, text='Target number to achieve: ')
        self.lbl3 = Label(frame, text='Maximum write size for random rolls (MB): ')
        self.lbl4 = Label(frame, text='Number of solutions to find before stopping (0 to find all): ')
        self.lbl_processing = Label(frame, text='')
        self.lbl1.grid(row=0, sticky=W)
        self.lbl2.grid(row=1, sticky=W)
        self.lbl3.grid(row=2, sticky=W)
        self.lbl4.grid(row=3, sticky=W)
        self.lbl_processing.grid(row=5, sticky=W)

        self.entry_val_list = StringVar()
        self.entry_val_ans = DoubleVar()
        self.entry_val_size = IntVar()
        self.entry_val_size.set('200')
        self.entry_val_max_soln = IntVar()
        self.entry_list = Entry(frame, justify=RIGHT, textvariable=self.entry_val_list)
        self.entry_ans = Entry(frame, justify=RIGHT, textvariable=self.entry_val_ans)
        self.entry_size = Entry(frame, justify=RIGHT, textvariable=self.entry_val_size)
        self.entry_max_soln = Entry(frame, justify=RIGHT, textvariable=self.entry_val_max_soln)
        self.entry_list.grid(row=0, column=1, sticky=E)
        self.entry_ans.grid(row=1, column=1, sticky=E)
        self.entry_size.grid(row=2, column=1, sticky=E)
        self.entry_max_soln.grid(row=3, column=1, sticky=E)

        self.check_random_var = IntVar()
        self.check_random = Checkbutton(frame, text='Randomised combinations', variable=self.check_random_var)
        self.check_random.grid(row=4, column=0, sticky=W)
        
        self.btn_enumerate = Button(frame, text='Find', command = self.process)
        self.btn_enumerate.grid(row=5, column=1, sticky=E)

        self.text1 = Text(frame)
        self.text1.grid(row=6, column=0, columnspan=2)

    def startProcessingLabel(self):
        self.lbl_processing['text'] = 'Processing...'

    def stopProcessing(self):
        self.lbl_processing['text'] = ''

    def emptyTextBox(self):
        self.text1.delete(0.0, END)

    def displaySolution(self):
        self.text1.insert(0.0, self.test())
        self.stopProcessing()

    def randomProcess(self):
        pass

    def process(self):
        self.emptyTextBox()
        self.startProcessingLabel()
        self.lbl_processing.after(1, self.displaySolution)

    def fixFloatToInt(self, n):
        floated = [float(i) for i in n]
        inted = [int(i) if i.is_integer() else i for i in floated]
        return inted

    def getValidList(self, l):
        numbers = re.findall(r'\d+(?:\.\d*)?', l)
        numbers = self.fixFloatToInt(numbers)
        return numbers if len(numbers) != 0 else None

    def test(self):
        n = self.getValidList(self.entry_val_list.get())
        if n is not None:
            if self.combi is not None:
                self.combi.setNewNumbers(n)
            else:
                self.combi = Combinatorics(n)
        else:
            self.text1.insert(0.0, 'Invalid input in number list.')
        ans = self.entry_val_ans.get()
        up_to = None if self.entry_val_max_soln.get() == 0 else self.entry_val_max_soln.get()
        if self.check_random_var.get():
            randomise = True
            if up_to is None:
                up_to = 1
        else:
            randomise = False
        max_write_size = self.entry_val_size.get() * 1000000
        return self.combi.evaluate(ans, up_to, randomise, max_write_size)

        

root = Tk()
app = App(root)
root.mainloop()
try:
    root.destroy()
except:
    pass
