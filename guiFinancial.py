from tkinter import *
from tkinter.ttk import *
import Financial_Data as f_d
import Modelling_Analysis as m_a

class MainApplication(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.financialdata = f_d.FinancialData()
        self.parent = parent
        self.symbolTxt = Entry(self, width=10)
        self.symbolTxt.grid(column = 0, row = 0, sticky = N+S+E+W, padx=(50, 10), pady = (30, 10))
        self.getDatabtn = Button(self, text="Get Data", command = self.getDatabtnCommand)
        self.getDatabtn.grid(column=1, row=0, sticky = N+S+E+W, padx=(10, 10), pady = (30, 10))
        self.comboSymbols = Combobox(self)
        self.comboSymbols.grid(column=0, row=1, sticky = N+S+E+W, padx=(50, 10), pady = (10, 10))
        self.analysisSymbol = Button(self, text="Analysis", command = self.analysisSymbolCommand)
        self.analysisSymbol.grid(column=1, row=1, sticky = N+S+E+W, padx=(10, 10), pady = (10 ,10))
        style = Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=('Calibri', 11)) # Modify the font of the body
        style.configure("mystyle.Treeview.Heading", font=('Calibri', 13,'bold')) # Modify the font of the headings
        #style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})]) # Remove the borders
        #self.tv = Treeview(self, columns = 5, show="headings", style="mystyle.Treeview")
        style.configure('mystyle.Treeview', rowheight=20)
        self.tv = Treeview(self, show="headings", style="mystyle.Treeview", columns= 3)
        self.tv["columns"] = ('Date', 'Close', 'Predictions')
        self.tv.heading("Date", text="Date")
        self.tv.heading("Close", text="Close")
        self.tv.heading("Predictions", text="Predictions")
        self.tv.grid(column = 0, row = 2, columnspan = 3, sticky = N+S+E+W, padx=(50, 50), pady = (10, 30))
    
    def getDatabtnCommand(self):
        self.financialdata.updateCurrentSymbol(self.symbolTxt.get().upper())
        self.financialdata.downloadHistoricalDataSymbol()
        self.comboSymbols['values']= (sorted(self.financialdata.getAvailableSymbols()))
        print(self.comboSymbols.current())
        self.symbolTxt.delete(0, 'end')
    
    def analysisSymbolCommand(self):
        for row in self.tv.get_children():
            self.tv.delete(row)
        self.financialdata.setCurrentSymbol(self.comboSymbols.get())
        self.model_analysis = m_a.ModellingAnalysis()
        self.model_analysis.modelling(self.financialdata.readData())
        prediction = self.model_analysis.predict()
        print(prediction)
        #self.tv["columns"] = list(prediction.columns)
        self.tv["columns"] = ('Date', 'Close', 'Predictions')
        self.tv.heading(list(prediction.columns)[0], text=list(prediction.columns)[0])
        self.tv.heading(list(prediction.columns)[1], text=list(prediction.columns)[1])
        self.tv.heading(list(prediction.columns)[2], text=list(prediction.columns)[2])
        #self.tv.heading(list(prediction.columns)[3], text=list(prediction.columns)[3])
        #self.tv.heading(list(prediction.columns)[4], text=list(prediction.columns)[4])
        for index, r in prediction.iterrows():
            self.tv.insert("", "end", values = (r[list(prediction.columns)[0]],r[list(prediction.columns)[1]],r[list(prediction.columns)[2]]))      
            #self.tv.insert("", "end", values = (r[list(prediction.columns)[0]],r[list(prediction.columns)[1]],r[list(prediction.columns)[2]],r[list(prediction.columns)[3]],r[list(prediction.columns)[4]]))      
        self.tv.column("#0", width=0)
        self.tv.column(0, anchor=CENTER)
        self.tv.column(1, anchor=CENTER)
        self.tv.column(2, anchor=CENTER)
        #self.tv.column(3, anchor=CENTER)
        #self.tv.column(4, anchor=CENTER)

if __name__ == "__main__":
    root = Tk()
    root.title("Stock Market Predictor By Rand.next")
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()