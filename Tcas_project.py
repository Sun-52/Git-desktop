import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
from tkinter import *
from tkinter.ttk import *
from sklearn import linear_model
import pickle

#clear dataframe
name = ["Apartment floor", "Number of storeys", "Numbers of living room", "Total area(meters)", "Kitchen area(meters)", "Building type", "Facade type", "Poastal code"]
kit_name = ["Apartment floor", "Number of storeys", "Numbers of living room", "Total area(meters)", "Building type", "Facade type", "Poastal code"] 
with open('model', 'rb') as f:
  reg = pickle.load(f)
with open('kit_model', 'rb') as g:
  kit_reg = pickle.load(g)
#postal_code
postal = pd.read_csv("postal.csv")
postal_id = []
for l in range(len(postal)):
  postal_id.append(postal["Postal Code"][l])

#Ui
window = Tk()
window.geometry("1024x576")
window.title("Russia apartment predictor")

txt1 = Label(window, text = name[0])
txt1.grid(column=1, row=1)
ent1 = Entry(window, width=25)
ent1.grid(column=2,row=1)

txt2 = Label(window, text = name[1])
txt2.grid(column=4, row=1)
ent2 = Entry(window, width=25)
ent2.grid(column=5,row=1)

txt3 = Label(window, text = name[2])
txt3.grid(column=1, row=5)
comb1 = Combobox(window,width=22)
comb1["values"] = [1,2,3,4,5,6,7, "studio apartment"]
comb1.grid(column=2, row=5)

txt4 = Label(window, text = name[3])
txt4.grid(column=1, row=2)
ent3 = Entry(window, width=25)
ent3.grid(column=2, row=2)

txt5 = Label(window, text = name[4])
txt5.grid(column=4, row=2)
ent4 = Entry(window, width=25)
ent4.grid(column=5, row=2)

txt6 = Label(window, text = name[5])
txt6.grid(column=4, row=5)
comb2 = Combobox(window, width=22)
comb2_val = ["Don't know", "Other", "Panel", "Monolithic", "Brick", "Blocky", "Wooden"]
comb2["values"] = comb2_val
comb2.grid(column=5, row=5)

txt7 = Label(window, text=name[6])
txt7.grid(column=7, row=5)
comb3 = Combobox(window,width=22)
comb3_val = ["Secondary real estate market", "New building"]
comb3["values"] = comb3_val
comb3.grid(column=8,row=5)

txt8 = Label(window, text=name[7])
txt8.grid(column=1,row=4)
ent5 = Entry(window, width=25)
ent5.grid(column=2,row=4)

txt9 = Label(window, text="")
txt9.grid(column=1,row=6)

txt10 = Label(window, text="")
txt10.grid(column=1, row=8)
txt11 = Label(window, text="")
txt11.grid(column=2, row=8)

txt12 = Label(window, text="")
txt12.grid(column=1, row=9)
txt13 = Label(window, text="")
txt13.grid(column=2, row=9)

txt14 = Label(window, text="")
txt14.grid(column=1, row=10)
txt15 = Label(window, text="")
txt15.grid(column=2, row=10)

txt16 = Label(window, text="")
txt16.grid(column=1, row=11)
txt17 = Label(window, text="")
txt17.grid(column=2, row=11)

detail_list = [txt10, txt11, txt12, txt13, txt14, txt15, txt16, txt17]
his_input = []
def button():
    global comb2_val
    global comb3_val
    global postal_id
    global detail_list
    comd = [float, int]
    global his_input
    input_list = []
    if ent4.get().count(".") > 0:
      run_comd =comd[0]
    if ent4.get().count(".") <=0:
      run_comd = comd[1]
    if run_comd(ent4.get()) > 0:
      print("kit activation")
      sep_act_list = [[ent1, ent2, ent3, ent4, ent5], [comb1, comb2, comb3]]
      x = [ent1, ent2, ent3, ent4, ent5]
      y = [comb1, comb2, comb3]
      act_list_step = []
      act_list = [ent1, ent2, comb1, ent3, ent4, comb2, comb3, ent5]
      for n in range(len(sep_act_list)):
        for o in sep_act_list[n]:
          act_list_step.append(act_list.index(o))
      cal_list = []
      comb2_num = [7,8,9,10,11,12,13]
      comb3_num = [1,2]
      txt9.configure(text="")
      for m in act_list:
        if m == comb1 and comb1.get() == "studio apartment":
            cal_list.append(8)
        elif m == comb2:
            index = comb2_val.index(comb2.get())
            cal_list.append(comb2_num[index])
        elif m == comb3:
            index = comb3_val.index(comb3.get())
            cal_list.append(comb3_num[index])
        else:
          for p in sep_act_list:
            if p.count(m) > 0:
              location = p.index(m)
              if p == x:
                cal_list.append(float(x[location].get()))
              if p == y:
                cal_list.append(float(y[location].get()))
        for p2 in sep_act_list:
          if p2.count(m) > 0:
            location = p2.index(m)
            if p2 == x:
              input_list.append(x[location].get())
            if p2 == y:
              input_list.append(y[location].get())
        data_ent = isinstance(m, Entry)
        data_comb = isinstance(m, Combobox)
        if data_ent == True:
          m.delete(0,END)
        if data_comb == True:
          m.set("")
      translate_type = [0,1,2,5,6]
      for q in translate_type:
        cal_list[q] = int(cal_list[q])
      print(cal_list)
      if cal_list[0] > cal_list[1] or postal_id.count(cal_list[len(cal_list)-1]) <= 0 or cal_list[4] < 0:
        txt9.configure(text="Error") 
      else:
        #for q in cal_list:
          #q = math.exp(q)
        #cal_list = np.reshape(cal_list,(1, cal_list.shape[0]))
        prediction = reg.predict([cal_list])
        if int(prediction) > 0:
          txt9.configure(text=(str(int(prediction)),"Russian ruble"))
          for r in range(len(detail_list)):
            detail_list[r].configure(text=(name[r]+": "+input_list[r]))
          txt18 = Label(window, text="Detail:")
          txt18.grid(column=1, row=7)
        if int(prediction) <= 0:
          txt9.configure(text="invalid output")
    his_input.append(input_list)      
    if ent4.get() == '0':
      print("non-kit activation")
      sep_act_list = [[ent1, ent2, ent3, ent5], [comb1, comb2, comb3]]
      x = [ent1, ent2, ent3,ent5]
      y = [comb1, comb2, comb3]
      act_list_step = []
      act_list = [ent1, ent2, comb1, ent3, ent4, comb2, comb3, ent5]
      for n in range(len(sep_act_list)):
        for o in sep_act_list[n]:
          act_list_step.append(act_list.index(o))
      cal_list = []
      comb2_num = [7,8,9,10,11,12,13]
      comb3_num = [1,2]
      txt9.configure(text="")
      for m in act_list:
          if m == comb1 and comb1.get() == "studio apartment":
              cal_list.append(8)
          elif m == comb2:
              index = comb2_val.index(comb2.get())
              cal_list.append(comb2_num[index])
          elif m == comb3:
              index = comb3_val.index(comb3.get())
              cal_list.append(comb3_num[index])
          else:
            for p in sep_act_list:
              if p.count(m) > 0:
                location = p.index(m)
                if p == x:
                  cal_list.append(float(x[location].get()))
                if p == y:
                  cal_list.append(float(y[location].get()))
          for p2 in sep_act_list:
              if p2.count(m) > 0:
                location = p2.index(m)
                if p2 == x:
                  input_list.append(x[location].get())
                if p2 == y:
                  input_list.append(y[location].get())
          data_ent = isinstance(m, Entry)
          data_comb = isinstance(m, Combobox)
          if data_ent == True:
              m.delete(0,END)
          if data_comb == True:
              m.set("")
      translate_type = [0,1,2,4,5]
      for q in translate_type:
        cal_list[q] = int(cal_list[q])
      print(cal_list)
      if cal_list[0] > cal_list[1] or postal_id.count(cal_list[len(cal_list)-1]) <=0:
        txt9.configure(text="Error") 
      else:
        #for q in cal_list:
          #q = math.exp(q)
        #cal_list = np.reshape(cal_list,(1, cal_list.shape[0]))
        prediction = kit_reg.predict([cal_list])
        if int(prediction) > 0:
          txt9.configure(text=(str(int(prediction)),"Russian ruble"))
          for r in range(len(detail_list)):
            detail_list[r].configure(text=(name[r]+": "+input_list[r]))
          txt18 = Label(window, text="Detail:")
          txt18.grid(column=1, row=7)
        if int(prediction) <= 0:
          txt9.configure(text="invalid output")
    his_input.append(input_list)
def history():
  history = Toplevel(window)
  history.title("History")

  txt18 = Label(history, text="")
  txt18.grid(column=1, row=1)

  txt19 = Label(history, text="")
  txt19.grid(column=1, row=3)

  txt20 = Label(history, text="")
  txt20.grid(column=1, row=5)

  txt21 = Label(history, text="")
  txt21.grid(column=1, row=7)

  txt22 = Label(history, text="")
  txt22.grid(column=1, row=9)

  txt_list = [txt18, txt19, txt20, txt21, txt22]
  for s in range(len(his_input)):
    if 0<=s-1<5:
      txt_list[s-1].configure(text=(str(s)+str(his_input[s-1])))
    if s-1 >5:
      txt_list[(s-1)%5].configure(text=his_input[s-1])

bt = Button(window, text="Predict", command=lambda:[button()])
bt.grid(column=7, row=1)
bt3 = Button(window, text="History", command=history)
bt3.grid(column=8, row=1)

window.mainloop()