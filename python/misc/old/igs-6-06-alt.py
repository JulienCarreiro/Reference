#!/bin/python3

import itertools as it
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font
from PIL import ImageTk,Image
import RPi.GPIO as GPIO
import pyfirmata
import time
from datetime import datetime

print(datetime.now().strftime("%H:%M - %m/%d/%Y"))

try:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(37,GPIO.OUT)
    GPIO.output(37,GPIO.LOW)
    GPIO.setup(40,GPIO.OUT)
    GPIO.output(40,GPIO.LOW)
    GPIO.setup(38,GPIO.OUT)
    GPIO.output(38,GPIO.LOW)
except: 
   pass

reservoir_level = 2.5
flowrate = 0.0006
start = time.time()

#------------------Arduino control-------------------
try:
    board = pyfirmata.Arduino('/dev/ttyACM0')
except:
    pass

print("Connected to arduino")

try:
    pump1 = board.digital[6]
    pump2 = board.digital[7]
    pump3 = board.digital[8]
    pump4 = board.digital[9]
    pump5 = board.digital[10]

    pumps = [pump1, pump2, pump3, pump4, pump5]
except: 
    pass


class igs():
    
    def read_pumps(self):
        try:
            get_pump1 = pump1.read()
            get_pump2 = pump2.read()
            get_pump3 = pump3.read()
            get_pump4 = pump4.read()
            get_pump5 = pump5.read()
        except:
            get_pump1 = 0
            get_pump2 = 0
            get_pump3 = 0
            get_pump4 = 0
            get_pump5 = 0

        get_pumps = [get_pump1, get_pump2, get_pump3, get_pump4, get_pump5]
        
        return get_pumps


#-----Function to remember a starting time------

    def update_clock(self):
        self.current_time = datetime.now().strftime("  %H:%M  -  %m/%d/%Y")
        return self.current_time
    

#----------Get value of an arduino pin-----------

    def analog_in(self):
        #self.analog_input = board.get_pin('a:0:i')
        self.analog_input = True
        return self.analog_input


#-----------------Water level logic--------------

    #--------Get current water level------
    
    def water_level(self):
        #board.digital[9].write(0)
        self.watertime = time.time() - start
        self.reservoir_level = reservoir_level - self.watertime * flowrate
        self.reservoir_level = str("{:.6f}".format(self.reservoir_level))
        return self.reservoir_level
    
    
    #---------Update water level label-----
    
    def level_update(self):
        self.res_level.set(str(self.water_level()))
        self.toolbar_label = str('IGS GrowHUB    ::   ' + str(self.update_clock()))
        self.toolbar.config(text=self.toolbar_label)
        self.root.after(5000,self.level_update)
    

#--------------------Button logic----------------------

    def fan_toggle(self):
        self.button_fan['image'] = next(self.images_f)
        try:
            if GPIO.input(37):
                GPIO.output(37,GPIO.LOW)
            else:
                GPIO.output(37,GPIO.HIGH)
        except:
            pass

    def led_upper(self):
        self.button_up['image'] = next(self.images_u)
        try:
            if GPIO.input(40):
                GPIO.output(40,GPIO.LOW)
            else:
                GPIO.output(40,GPIO.HIGH)
        except:
            pass

    def led_lower(self):
        self.button_low['image'] = next(self.images_l)
        try:
            if GPIO.input(38):
                GPIO.output(38,GPIO.LOW)           
            else:
                GPIO.output(38,GPIO.HIGH)
        except:
            pass


#---------------------Pump toggles------------------------
    
    
    #-----------------Pump 1-------------------
    
    def pump_toggle1(self):
        if self.pump_switch1['bg'] == 'GREY':
            self.pump_switch1['bg'] = 'RED'
            try:
                pumps[0].write(1)
            except:
                pass
            self.pump_status[0] = 1
        else:
            self.pump_switch1['bg'] = 'GREY'
            try:
                pumps[0].write(0)
            except:
                pass
            self.pump_status[0] = 0

    #-----------------Pump 2-------------------
    
    def pump_toggle2(self):
        if self.pump_switch2['bg'] == 'GREY':
            self.pump_switch2['bg'] = 'RED'
            try:
                pumps[1].write(1)
            except:
                pass
            self.pump_status[1] = 1
        else:
            self.pump_switch2['bg'] = 'GREY'
            try:
                pumps[1].write(0)
            except:
                pass
            self.pump_status[1] = 0
        
    #-----------------Pump 3-------------------
    
    def pump_toggle3(self):
        if self.pump_switch3['bg'] == 'GREY':
            self.pump_switch3['bg'] = 'RED'
            try:
                pumps[2].write(1)
            except:
                pass
            self.pump_status[2] = 1
        else:
            self.pump_switch3['bg'] = 'GREY'
            try:
                pumps[2].write(0)
            except:
                pass
            self.pump_status[2] = 0
        
    #-----------------Pump 4-------------------
    
    def pump_toggle4(self):
        if self.pump_switch4['bg'] == 'GREY':
            self.pump_switch4['bg'] = 'RED'
            try:
                pumps[3].write(1)
            except:
                pass
            self.pump_status[3] = 1
        else:
            self.pump_switch4['bg'] = 'GREY'
            try:
                pumps[3].write(0)
            except:
                pass
            self.pump_status[3] = 0

    #-----------------Pump 5-------------------
    
    def pump_toggle5(self):
        if self.pump_switch5['bg'] == 'GREY':
            self.pump_switch5['bg'] = 'RED'
            try:
                pumps[4].write(1)
            except:
                pass
            self.pump_status[4] = 1
        else:
            self.pump_switch5['bg'] = 'GREY'
            try:
                pumps[4].write(0)
            except:
                pass
            self.pump_status[4] = 0

        
    def pump_bg_calc(self):
       
        self.pump_status = self.read_pumps()
        self.pump_switch = []
        
        for i in range(5):
            if self.pump_status[i] == 1:
                self.pump_switch.append('RED')
            else:
                self.pump_switch.append('GREY')
        
        return self.pump_switch
        

    def schedule_submit_button(self):
        #for z in range(0,5):
            #pump[z].write(0)
        self.pump_times = [
            [[self.pump1_hour.get(), self.pump1_min.get(), self.pump1_am.get()], [self.pump1_hour_end.get(), self.pump1_min_end.get(), self.pump1_am_end.get()]],
            [[self.pump2_hour.get(), self.pump2_min.get(), self.pump2_am.get()], [self.pump2_hour_end.get(), self.pump2_min_end.get(), self.pump2_am_end.get()]]
        ]


        self.pump_info = "start: " + self.pump_times[0][0][0] + ":" + self.pump_times[0][0][1] + " " + self.pump_times[0][0][2] + " end: " + self.pump_times[0][1][0] + ":" + self.pump_times[0][1][1] + " " + self.pump_times[0][1][2]

        messagebox.showinfo("Pump Schedules", self.pump_info)
        print(self.pump_info)


#---------------------Pump logic------------------------

    #-------------Pump timer--------------
    
    def pump_timer(self):
        pass
    
#--------------------Pump 1-----------------------
    
    #-----User input and dialog boxes-----
    
    def pump_submit(self):
        try:
            self.p_in = float(self.usr_in_label.get())
            self.p_in = str("{:.2f}".format(self.p_in))
            print(str(self.p_in))
            
            #Ask user to confirm. First string is title, second is the message 
            messagebox.askyesno('Confirm','Set pump to run in ' + str(self.p_in) + ' minutes?')
        except:
            #Error message popup
            messagebox.showerror("Error","EPIC FAIL!!!!!!")
        finally:
            #Clear the input box
            self.pump_input.delete('0','end')
            self.toolbar.focus()


#--------------------Pump 2-----------------------

    #-----User input and dialog boxes-----
    
    def pump_submit2(self):
        try:
            self.p_in2 = float(self.usr_in_label2.get())
            self.p_in2 = str("{:.2f}".format(self.p_in2))
            print(str(self.p_in2))
            
            #Ask user to confirm. First string is title, second is the message 
            messagebox.askyesno('Confirm','Set pump to run in ' + str(self.p_in2) + ' minutes?')
        except:
            #Error message popup
            messagebox.showerror("Error","EPIC FAIL!!!!!!")
        finally:
            #Clear the input box
            self.pump_input2.delete('0','end')
            self.toolbar.focus()


#--------------------Pump 3-----------------------

    #-----User input and dialog boxes-----
    
    def pump_submit3(self):
        try:
            self.p_in3 = float(self.usr_in_label3.get())
            self.p_in3 = str("{:.2f}".format(self.p_in3))
            print(str(self.p_in3))
            
            #Ask user to confirm. First string is title, second is the message 
            messagebox.askyesno('Confirm','Set pump to run in ' + str(self.p_in3) + ' minutes?')
        except:
            #Error message popup
            messagebox.showerror("Error","EPIC FAIL!!!!!!")
        finally:
            #Clear the input box
            self.pump_input3.delete('0','end')
            self.toolbar.focus()


#--------------------Pump 3-----------------------

    #-----User input and dialog boxes-----
    
    def pump_submit4(self):
        try:
            self.p_in4 = float(self.usr_in_label4.get())
            self.p_in4 = str("{:.2f}".format(self.p_in4))
            print(str(self.p_in4))
            
            #Ask user to confirm. First string is title, second is the message 
            messagebox.askyesno('Confirm','Set pump to run in ' + str(self.p_in4) + ' minutes?')
        except:
            #Error message popup
            messagebox.showerror("Error","EPIC FAIL!!!!!!")
        finally:
            #Clear the input box
            self.pump_input4.delete('0','end')
            self.toolbar.focus()
            

#--------------------Pump 5-----------------------

    #-----User input and dialog boxes-----
    
    def pump_submit5(self):
        try:
            self.p_in5 = float(self.usr_in_label5.get())
            self.p_in5 = str("{:.2f}".format(self.p_in5))
            print(str(self.p_in5))
            
            #Ask user to confirm. First string is title, second is the message 
            messagebox.askyesno('Confirm','Set pump to run in ' + str(self.p_in5) + ' minutes?')
        except:
            #Error message popup
            messagebox.showerror("Error","EPIC FAIL! luser!!!!!")
        finally:
            #Clear the input box
            self.pump_input5.delete('0','end')
            self.toolbar.focus()


#--------------------Exit command-----------------------

    def exitProgram(self):
        #GPIO.cleanup()
        print(self.read_pumps())
        try:
            for i in pumps:
                i.write(0)
        except:
            pass
        self.root.quit()


#------------------------init----------------------------

    def __init__(self):
        
        self.root = Tk()
        self.root.title("IGS GrowHUB")
        #self.root['bg']="grey"
        self.root.attributes("-fullscreen",1)
        self.root.geometry('1280x800')
        self.root.maxsize(1280,800)
        self.root.minsize(1280,800)
        self.style = ttk.Style(self.root)
        self.style.theme_use('clam')
        

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=2)
        self.root.rowconfigure(2, weight=2)
        self.root.rowconfigure(3, weight=2)

        
        font_small = tkinter.font.Font(family='Helvetica',size=14,weight='normal')
        font_smaller = tkinter.font.Font(family='Helvetica',size=12,weight='normal')
        font_toolbar = tkinter.font.Font(size=11,weight='bold')
        font_miniscule = tkinter.font.Font(family='Helvetica',size=5,weight='normal')
        

#-------------------Toolbar---------------------------------------------------

        self.logo = tk.PhotoImage(file='/home/dietpi/Desktop/igs-logo.png')

        self.toolbar = ttk.Label(self.root,image=self.logo,text= 'IGS GrowHUB    ::   ' + str(self.update_clock()),font=font_toolbar,background="black",foreground="white",anchor=W,compound='left')
        self.toolbar.grid(column=0,row=0,columnspan=3,rowspan=1,sticky='NEW',ipady=3)


#-------------------Fan and light buttons-------------------------------------

    #-----------Toggle button images-----------
    
        self.toggle_btn_off = b'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'
        self.toggle_btn_on = b'iVBORw0KGgoAAAANSUhEUgAAAGQAAAAoCAYAAAAIeF9DAAARfUlEQVRoge1bCZRVxZn+qure+/q91zuNNNKAtKC0LYhs3R1iZHSI64iQObNkMjJk1KiJyXjc0cQzZkRwGTPOmaAmxlGcmUQnbjEGUVGC2tggGDZFBTEN3ey9vvXeWzXnr7u893oBkjOBKKlDcW9X1a137//Vv9ZfbNmyZTjSwhiDEAKGYVSYpnmOZVkzTdM8zTTNU4UQxYyxMhpzHJYupVSvUmqr67pbbNteadv2a7Ztd2SzWTiOA9d1oZQ6LGWOCJAACMuyzisqKroqGo1eYFlWxDRN3c4512OCejwWInZQpZQEQMa27WXZbHZJKpVank6nFYFzOGAOCwgR2zTNplgs9m/FxcXTioqKEABxvBL/SAsRngCwbXtNOp3+zpSLJzf3ffS5Jc8X/G0cam7DMIqKioruLy4uvjoej7NIJBICcbDnIN78cBXW71qH7d3bsTvZjoRMwpE2wIirjg0RjlbRi1wBBjcR5zFUx4ajtrQWZ46YjC+Mm4Gq0ipNJ8MwiGbTTNN8a+PyTUsSicT1jXMa0oO95oAc4k80MhqNvlBWVjYpHo9rrqD2dZ+sw9I1j6Nl/2qoGCCiDMzgYBYD49BghGh8XlEJRA5d6Z8EVFZBORJuSgEJhYahTfj7afMweczkvMcUcct7iUTikvr6+ta+0xIWAwJimmZdLBZ7uby8fGQsFtMo7zq4C/e+cg9aupphlBngcQ5OIFAVXvXA6DPZ5wkUIr4rAenfEyDBvfTulaMgHQWVVHC6HTSUN+GGP78JNUNqvCmUIiXfmkwmz6urq3s/f/oBARFC1MTj8eaKigq6ajCW/eZXuKd5EbKlGRjlBngRAzO5xxG8z0v7AAyKw2cNH180wQEmV07B2dUzcWbVFIwqHY2ySJnu68p04dOuHVi/Zx3eaF2BtXvXQkFCOYDb48LqieDGxptxwaQLw2kdx9mZSCSa6urqdgZt/QDhnBfFYjECY1JxcbEWU4+8/jAe+/DHME8wYZSIkCMKgOgLwueFKRTAJMPsmjm4YvxVGFUyyvs2LbF8iRCIL7+dLjs6d+DhdUvw7LZnoBiJMQnnoIP5p1yOK//sG+H0JL56e3ub6uvrtU4hLEKlTvrBNM37iouLJwWc8ejKH+Oxjx+FVW1BlAgtosDzCJ4PxEAgfJa5RAEnWiNw39QHcPqQCfqltdXkSCSSCWTSaUgyYcn4IZegqAiaboJjVNloLDxnMf667qu47pVvY5e7E2aVicc+ehScMVw+80r9E4ZhEK3vA/At+BiEHGIYRmNJScnblZWVjPTGyxuW4Z9Xf0+DYZQKMLM/GP2AGOy+X+cfdyElPbVsKu6f/gNURCr0uyaTSXR2duqrOsTXEO3Ky8v1lQZ1JA/i2hevwbsH10K5gL3fxh1Nd+L8My7wcFdKJZPJGePGjWt+9dVXPcHDGGOWZT1YXFysTdu2g21Y3Hy3FlPEGQVgMNYfDNa35hpyDiM+E5Wo3VTRhIdm/AjlVrn2I3bv3o329nakUin9LZyR/mQFzjCtfMY50qkU2ne362dcx0V5tAI/mfMEmqq+qEkiKgwsfvtu7DqwCwHtI5HIA3RvWZYHiBDiy0VFRdrpIz/jnlcWwy7Nap1RIKYCwvJBwAhByBG/P1h/xBXA6Oho3DvtARgQsG0HbW3tSCZT4AQAzweDhyBQG3iwSD2Akqkk2tva4WQdGNzAgxf9O0Zbo8EFQzaWweLli0KuEkI0bNu2bRbRn/viisIhWom/t2N9aNqyPjpjUK5AHhfwvHb+2QKEKYbvT1iIGI/BcST27dsL13U8MBgPweB5HOFd6W+h+7kPEFXHdbBn7x44rouoGcXds+4FyzDwIo6Wjmas274u4BKi/TWEAeecVViWdWEkYsEwBJauecLzM6LeD/VV4H3VwoT4GVgw7nZsvPgDr17k1VtOuh315gQoV/lWCXDr2O9i44Uf6HrL6Nshs7k+Kj9r+LnuWzFzFWRKes8eraKAi4ddgtPK66GURGdXpw8GL6gBR/S9Emhhf95VShddHR06vjVh+ARcMma29llEXODJtY+HksQwBGFQwTkX51qWZZmmhY7eTryzvxk8xrWfEZq2g+iM2SfMxf+c8xS+Ov5r/aj2d/Vfw09nPY1LSudoR8nXYGH/nHFzUS8nQNoyN2fQTcrvgANlq6PHIS4wr3a+Jlw6nUY2kwFjwhNPeaAInzOED4B3ZXmgsQI9Q5yTzmaQTmf03P/YcCVUGtp1WL2nGQd7OnwJwwmDc7kQ4ktBsPDNraugogCPHMKCYjnOuKvh7sMu34VnL0K9mgDpFOCBmBXD9WfeCJlU2qop4EByetN57X/oCoZJpZNRUzQSUklPeXMGoQEQ+toXGOYT3yO8yOMUkQcU1zpDcKHnpLlHVYzE5KopmkukCaza+uvwswkLAuR00u4EyLq2dV5symT9uaMAGIYrx14VNm1u3YQrHr8ctYtH4eT7R+PKn16Bzbs2hf3fGH81ZMItEE9UGsY0YHblXMBWA0ZcjlalldJU+QVNMOlKuFLqlU2rmAt/pecTXARXGuMBE4BGY3QANtyW8MAjn4XmllLhi6PO0iEWbgJrW9eGlhphwTnnY4P9jO0d27yQiBjEys5rbhjeqK879u3AxUsvxBvdr8EabsIaYWEVW4mvvHYpNrdv1mOaxjRB9voxIL88t/ZZfXP9jBvg9rr6BY9ZkcDpJRM0sRzb8QnsrWweXj1OITA05wTcQhwkhC/GvH4CQfgACh8w4iLbsbXYmnjiRB1WodXwScf2vEXITua0yxdsMu1Ot4MZrD8gff6cEJ+ImBnT98RyIs5hVAkYFYY2CMiRNCoNvHdgvR4Ti8QwMXpGASBL1z+BfT37MLRkKG4bf4dW4seqkCitiY7UxCIuITHFfTACEcR9YueLKw2CyOkW4hjBcyB4QOXaaH7y9kdVjgZ8g6U92Z7zZTgvJ0BKg4akm/ydHeruTDd4lOtKYAY6hpsMWxKbw3G1JWMLAGECeHrTU/p+7sSvoJ5P7CfSjlqRCnEjpsGAvykXiqVAmefpDtGnzauij0Um+t0TaQiUkkiJJxGUQoponuOQUp7vbarfgyKlRaXa9xho97C+4vTwftuBjwq1Omd48KMHsK93n+ag6yffqEMLx6SQESHJiJDeShV9iRuII5EHggg5RlejcHzQJ/KAIVGmuZA4Rfr7KAqFHr9SqjvYC46J2BGt0o29G5C0PWTPn3CBP3nhg/RDM6pn6PtkJon1nev7+TLEUQ+sv1/fk4IfUznmGCHihdClv2C0qBKFYGjlzVjhqmf9uSGnW3JmsAZSeFYSgd6Z6PJ+VAExEQ3fgbDgfsaEbhgeG6FZqZ9DNgBIq3d628NDS4fi2Yt/gdkVcz02lApfKpuJn037X4wuPUmP2di60RNnffZOiLNe6HwOm/d6oo1M4WNSGNCa+K1nBSnlE1uEK531UeqBWat1hfBM2wAAFoq6PCNAr36hudBVEjv2f+J9pVSojg7PTw7p5FLKj4NMiNqyWij7EB5y0MyARz58KGyuP7EeC2cuwqa/2Ko97f9oWoLThtSH/YtXLNKbWgX6KdhGEMB/fbT02AARFM6wqWOj9tBdx4Eg38E3ebnvhwiWrz9EKNY8P0XkiTkRWmnM7w84xXFtSFdhQ+t7Hi2kwpiK2vA1lFLbSGRtIkBIrk0bNU3vCWsPWYajCkS/R0iFjakNWLDilsN+681P3YgNqfUQxQIQhX3eljTDCx3PoaX1nf59R6lSWX2wWfsfru8vhA5eYLaKfEXPwvAJ83WDNnEDMISvX4QIn9W6Qy98ibe2v6mlA+WDTB05NeQQKeVm4pBfU74QPXDWqWeBpQCZUWFWRSEQuS1NmvC5jmfxV8/8JZ58p/8KX7rqCcx9ZA5+3vY0jAqh9+ALOSRHbZrrX7fQPs0xQoQpbOrdgJ09rZoOyXRa6wvB8j10plc744Gz6HEN90MnIvTchecMEucwFoou7alLhU/3/xbv7f6N53DbDGefdnb4yVLKlez111+vKCkp2V1VVWXRtu21//1NtDirYZ5ggFs8t6oHimfBQ1mlXLgJ6QUEHS/+pL3cGIco5uAxoc1g6nO6XDhdju43hxge5zAvOYD2n50OFzIrdTv1kzn9By86VCMxK/ZlXFd/k/60srIyUDg897GqMN4WEkLljcj/P9eazqTR1ekp8oW//Be8tONFzTXTKxvx0PyHPQtXqWxvb281iSxKd3wpk8lodp3f+HVNMEmiS+ZFYwfJtiP3nxPxqgxY1SYiNRYiIyzttZtDDW/r1/T0Byl2USpgDaM+s4DYBBCNNYeZ+nkCQ4f/j0bx3+2VjuXYevB9zSVdXV36Gsas8i0nFlhcOasrNy4/5sW8uTq9ubbs2oKXPvylTpuSWRfzm+aH7oLruoRBh6aIbdsPEUvZto3JtVPQVDlDp7BQrlGQ5hJi0kd0wVfMRDweF7rS6qbwMnGYDuHniTwCh/pELC9Eo/JA0Vwl9J6BflbhqFT9LiZwz/t3I5FN6D2MvXv3Qfoh+HxdEYixcKcw3BPxrClPZHGd00tz0DWZSeDOl+4AIl4q0PQTGjH91Aafrjpf64eEAfdl1/JMJkPpjhrJW8+/DVZXBE6P6+1ZBKD4Cl7JAYBRuT9C8SyPDjH/XyotCJOhTe3CXevvhO1k4Dg2drfv0fvoHkegQKfkgocMHPkhFYZUKqm3cWmOrGvju8/fhtZUq168RXYRFlx0e5gFKqVsqampeYWkFPcRUplM5ju9vb10RU1VDRacdTvsvbYX+LMLQQktr4FACcaE4AT16Orp36eS+YsIx7r0u7ij5XtIZpOwaddvzx60tbUhlUoXcgXru63LtPJub2vTz5AKIKd4wTM3oWVPi97WIF1188xbcVL1SQF3UBL2dXRPtBfz5s0LOnYqpYYahjGd9kfqauqgeoCWT1v0ytHZibxvdiILdV2/GNihPP6jpBp+5xJs5XKgLdWGVTtWYnxxHYZEh2ix09Pdg67uLmRtG45taxFPFiqB0NXdjb1796K7u0uPpbK1/QPc9PwN+KDrfe2HkfX69UlX4LKZ8zR30EKl7PgRI0Y8TOMvu+yyXF6W33ljT0/PDMoXIna8etY1Or71oy0PDZwo5yt6FQDTxwIbFJRjGGk/XNGvbnBQFIkSyP9pzbdwbsUs/E3d32J46QhIx0F3VxfCXCDi/mBF6sWp0Na1E0+2PImXt70MFkHIGQTGtRd8W4MBL3uR8nxvCF6JMGArVqwoeEXDMMJUUjKDKWHuxXd/gbtWfR92Wdbbbz8OUkmVn6erUtIz6RMSddHTMH1YI+qH1uPE0hEoiRRrEHqyPWjrbMPm3ZvQ/Onb2LhvE5ihNI3IUo3YEdwycwFmN1yaD8ZOylqsra0NU0kJi36AwE+2jsfjOtk6yGJs3d+KRS8vRPOBt3LJ1hGWE2efx2RrnVztRS5kxvOzdE1LL9ud+tzCkJK3SJneoyfTtnFYE26+cAHGVI/RRkCQbJ1IJM6rra0tSLYeFJDgOEIsFguPI9A2L7Wv+XgN/vOdn6B591tAnB0fxxECYBy/ZqUHhJsLo8Pf3yBHGRmgYUQT/qFxPhrHN2ogkFMLJKYuHTt27Kd9f4awGPDAjm8XE4pNUsr7HccJD+xMPXkqpo2dhgM9B7Dy/TfwbutabOvchvYD7eh1e+HS3uTn+cCO9I+vSe+ew0CxiKM6Xo3ailpMrpmiwyHDKqpDp88/SUXW1JLe3t7rx48fP/iBnYE4JL8QupZl0ZG2H8Tj8emUs/qnI21HVvKOtLUkk8nrxo0b9/ahHhyUQ/ILOYqZTKbZcZyGTCYzK5lMfjMajZ4fiUT0oU8vIir+dOgz79CnHz3P2rb9q0wm88NTTjll+ZHOc1gOKRjsn8Y1TZOORVOC3dmWZdUbhqGPRXPOS49TQHqUUj1SSjoWvdlxnJXZbPa1bDbbQb4K1SM6Fg3g/wC58vyvEBd3YwAAAABJRU5ErkJggg=='

        self.image_up = tk.PhotoImage(data=self.toggle_btn_on)
        self.image_down = tk.PhotoImage(data=self.toggle_btn_off)
        
        self.images_f = it.cycle([self.image_up,self.image_down]) # fan
        self.images_u = it.cycle([self.image_up,self.image_down]) # upper
        self.images_l = it.cycle([self.image_up,self.image_down]) # lower


    #---Container for all hardware controls---
        
        self.frame_controls = ttk.LabelFrame(self.root, text='Hardware Controls',borderwidth=5,padding=5)
                #relief=SUNKEN,pady=5,padx=20
        self.frame_controls.grid(column=0,row=1,rowspan=1,padx=10,pady=5,sticky=N)


        #----------------Seperators----------------
        
        self.sep1 = Label(self.frame_controls,font=font_miniscule,height=2)
        self.sep1.grid(column=0,row=5)
        self.sep2 = Label(self.frame_controls,font=font_miniscule,height=2)
        self.sep2.grid(column=0,row=8)
        self.sepbottom = Label(self.frame_controls,font=font_miniscule,height=1)
        self.sepbottom.grid(column=0, row=11)


        #-----------------Fan---------------------
        
        self.fan_btn_label = ttk.Label(self.frame_controls,text="FAN",font=font_smaller,padding=5)
        self.fan_btn_label.grid(row=3)
        
        self.button_fan = ttk.Button(self.frame_controls,image=self.image_down,command=self.fan_toggle)
        self.button_fan.grid(row=4)

        
        #--------------Upper light----------------
        
        self.upper_btn_label = ttk.Label(self.frame_controls,text="UPPER LIGHTS",font=font_smaller,padding=5)
        self.upper_btn_label.grid(row=6)
        
        self.button_up = ttk.Button(self.frame_controls,image=self.image_down,command=self.led_upper)
        self.button_up.grid(row=7)
        
        
        #--------------Lower light----------------
        
        self.lower_btn_label = ttk.Label(self.frame_controls,text="LOWER LIGHTS",font=font_smaller,padding=5)
        self.lower_btn_label.grid(row=9)
        
        self.button_low = ttk.Button(self.frame_controls,image=self.image_down,command=self.led_lower)
        self.button_low.grid(row=10)
        

#-----------------------Pump user input---------------------------------

    #Container for all the pump stuff
        
        self.frame_pump = ttk.LabelFrame(self.root,text="Pump Controls",borderwidth=1,padding=5)
        self.frame_pump.grid(column=1,row=1,rowspan=1,columnspan=1,sticky=N)
        

    #-----Manual toggle container-----
    
        self.pump_switches = ttk.Frame(self.frame_pump,borderwidth=3,relief=RIDGE,padding=2)
        self.pump_switches.grid(column=0,row=1,columnspan=1,sticky=NS)
        
        #label
        
        self.pump_switches_label = ttk.Label(self.pump_switches,text="i/o",font=font_smaller,padding=5)
        self.pump_switches_label.grid(column=0,row=0) 
        

    #------Scheduling container-------
    
        self.pump_scheduling = ttk.Frame(self.frame_pump,borderwidth=3,relief=RIDGE,padding=2)
        self.pump_scheduling.grid(column=1,row=1,columnspan=1,sticky=NS)
        
        #label
        
        self.pump_schedule_label = ttk.Label(self.pump_scheduling,text="Schedule",font=font_smaller,padding=5)
        self.pump_schedule_label.grid(column=0,row=0,columnspan=2)
        
  
    #submission button

        self.sep = ttk.Separator(self.pump_scheduling,orient=HORIZONTAL)
        self.sep.grid(row=7,columnspan=7,sticky=EW,pady=5)

        self.schedule_submit = ttk.Button(self.pump_scheduling,text='submit',command=self.schedule_submit_button)
        self.schedule_submit.grid(column=0,row=8,columnspan=7)
    
  
    #Pump toggles
        
        self.pump_bg = self.pump_bg_calc()
        
        self.sep = ttk.Separator(self.pump_switches,orient=HORIZONTAL)
        self.sep.grid(row=1,sticky=EW,pady=10)
        
        #manual pump control 1
        
        self.pump_switch1 = tk.Button(self.pump_switches,text='1',bg=self.pump_bg[0],command=self.pump_toggle1)
        self.pump_switch1.grid(row=2,pady=5)
        
        #manual pump control 2

        self.pump_switch2 = tk.Button(self.pump_switches,text='2',bg=self.pump_bg[1],command=self.pump_toggle2)
        self.pump_switch2.grid(row=3,pady=5)        

        #manual pump control 3
        
        self.pump_switch3 = tk.Button(self.pump_switches,text='3',bg=self.pump_bg[2],command=self.pump_toggle3)
        self.pump_switch3.grid(row=4,pady=5)
        
        #manual pump control 3
        
        self.pump_switch4 = tk.Button(self.pump_switches,text='4',bg=self.pump_bg[3],command=self.pump_toggle4)
        self.pump_switch4.grid(row=5,pady=5)
        
        #manual pump control 5
        
        self.pump_switch5 = tk.Button(self.pump_switches,text='5',bg=self.pump_bg[4],command=self.pump_toggle5)
        self.pump_switch5.grid(row=6,pady=5)
        
    
    #pump scheduling 
    
        self.pump_values = (12,1,2,3,4,5,6,7,8,9,10,11)

        self.pump_min_values = ('00','05','10','15','20','25','30','35','40','45','50','55')

        self.pump_scheduling_start = ttk.Label(self.pump_scheduling,text='start')
        self.pump_scheduling_start.grid(column=0,row=1)
        
        self.pump_scheduling_end = ttk.Label(self.pump_scheduling,text='end')
        self.pump_scheduling_end.grid(column=4,row=1)
    
        self.sep = ttk.Separator(self.pump_scheduling,orient=VERTICAL)
        self.sep.grid(column=3,row=0,rowspan=7,sticky=NS,padx=5)    
    
    
        #--------------------pump 1----------------------
        
        self.pump1_hour = tk.StringVar(value='12')
        self.pump_hour1 = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump1_hour,wrap=True,width=2)
        self.pump_hour1.grid(column=0,row=2,pady=10)
        #command= pump1_set
        #self.pump1_schedule.get()
    
        self.pump1_min = tk.StringVar(value='00')
        self.pump_min1 = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump1_min,wrap=True,width=2)
        self.pump_min1.grid(column=1,row=2)
        
        self.pump1_am = tk.StringVar(value='AM')
        self.pump_am1 = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump1_am,wrap=True,width=3)
        self.pump_am1.grid(column=2,row=2)    
    
        self.pump1_hour_end = tk.StringVar(value='12')
        self.pump_hour1_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump1_hour_end,wrap=True,width=2)
        self.pump_hour1_end.grid(column=4,row=2)
        #command= pump1_set
        #self.pump1_schedule.get()
    
        self.pump1_min_end = tk.StringVar(value='00')
        self.pump_min1_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump1_min_end,wrap=True,width=2)
        self.pump_min1_end.grid(column=5,row=2)
        
        self.pump1_am_end = tk.StringVar(value='AM')
        self.pump_am1_end = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump1_am_end,wrap=True,width=3)
        self.pump_am1_end.grid(column=6,row=2)
        
        self.pump1_time = [self.pump1_hour, self.pump1_min, self.pump1_am, self.pump1_hour_end, self.pump1_min_end, self.pump1_am_end]

        #--------------------pump 2----------------------
        
        self.pump2_hour = tk.StringVar(value='12')
        self.pump_hour2 = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump2_hour,wrap=True,width=2)
        self.pump_hour2.grid(column=0,row=3,pady=7)
        #command= pump2_set
        #self.pump2_schedule.get()
    
        self.pump2_min = tk.StringVar(value='00')
        self.pump_min2 = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump2_min,wrap=True,width=2)
        self.pump_min2.grid(column=1,row=3)
        
        self.pump2_am = tk.StringVar(value='AM')
        self.pump_am2 = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump2_am,wrap=True,width=3)
        self.pump_am2.grid(column=2,row=3)
    
    
        self.pump2_hour_end = tk.StringVar(value='12')
        self.pump_hour2_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump2_hour_end,wrap=True,width=2)
        self.pump_hour2_end.grid(column=4,row=3)
        #command= pump2_set
        #self.pump2_schedule.get()
    
        self.pump2_min_end = tk.StringVar(value='00')
        self.pump_min2_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump2_min_end,wrap=True,width=2)
        self.pump_min2_end.grid(column=5,row=3)
        
        self.pump2_am_end = tk.StringVar(value='AM')
        self.pump_am2_end = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump2_am_end,wrap=True,width=3)
        self.pump_am2_end.grid(column=6,row=3)
        
        
        #--------------------pump 3----------------------
        
        self.pump3_hour = tk.StringVar(value='12')
        self.pump_hour3 = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump3_hour,wrap=True,width=2)
        self.pump_hour3.grid(column=0,row=4,pady=8)
        #command= pump3_set
        #self.pump3_schedule.get()
    
        self.pump3_min = tk.StringVar(value='00')
        self.pump_min3 = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump3_min,wrap=True,width=2)
        self.pump_min3.grid(column=1,row=4)
        
        self.pump3_am = tk.StringVar(value='AM')
        self.pump_am3 = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump3_am,wrap=True,width=3)
        self.pump_am3.grid(column=2,row=4)
    
    
        self.pump3_hour_end = tk.StringVar(value='12')
        self.pump_hour3_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump3_hour_end,wrap=True,width=2)
        self.pump_hour3_end.grid(column=4,row=4)
        #command= pump3_set
        #self.pump3_schedule.get()
    
        self.pump3_min_end = tk.StringVar(value='00')
        self.pump_min3_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump3_min_end,wrap=True,width=2)
        self.pump_min3_end.grid(column=5,row=4)
        
        self.pump3_am_end = tk.StringVar(value='AM')
        self.pump_am3_end = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump3_am_end,wrap=True,width=3)
        self.pump_am3_end.grid(column=6,row=4)
        
        
        #--------------------pump 4----------------------
        
        self.pump4_hour = tk.StringVar(value='12')
        self.pump_hour4 = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump4_hour,wrap=True,width=2)
        self.pump_hour4.grid(column=0,row=5,pady=10)
        #command= pump4_set
        #self.pump4_schedule.get()
    
        self.pump4_min = tk.StringVar(value='00')
        self.pump_min4 = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump4_min,wrap=True,width=2)
        self.pump_min4.grid(column=1,row=5)
        
        self.pump4_am = tk.StringVar(value='AM')
        self.pump_am4 = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump4_am,wrap=True,width=3)
        self.pump_am4.grid(column=2,row=5)
    
    
        self.pump4_hour_end = tk.StringVar(value='12')
        self.pump_hour4_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump4_hour_end,wrap=True,width=2)
        self.pump_hour4_end.grid(column=4,row=5)
        #command= pump4_set
        #self.pump4_schedule.get()
    
        self.pump4_min_end = tk.StringVar(value='00')
        self.pump_min4_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump4_min_end,wrap=True,width=2)
        self.pump_min4_end.grid(column=5,row=5)
        
        self.pump4_am_end = tk.StringVar(value='AM')
        self.pump_am4_end = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump4_am_end,wrap=True,width=3)
        self.pump_am4_end.grid(column=6,row=5)
        
        
        #--------------------pump 5----------------------
        
        self.pump5_hour = tk.StringVar(value='12')
        self.pump_hour5 = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump5_hour,wrap=True,width=2)
        self.pump_hour5.grid(column=0,row=6,pady=8)
        #command= pump5_set
        #self.pump5_schedule.get()
    
        self.pump5_min = tk.StringVar(value='00')
        self.pump_min5 = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump5_min,wrap=True,width=2)
        self.pump_min5.grid(column=1,row=6)
        
        self.pump5_am = tk.StringVar(value='AM')
        self.pump_am5 = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump5_am,wrap=True,width=3)
        self.pump_am5.grid(column=2,row=6)
    
   
        self.pump5_hour_end = tk.StringVar(value='12')
        self.pump_hour5_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_values,textvariable=self.pump5_hour_end,wrap=True,width=2)
        self.pump_hour5_end.grid(column=4,row=6)
        #command= pump5_set
        #self.pump5_schedule.get()
    
        self.pump5_min_end = tk.StringVar(value='00')
        self.pump_min5_end = ttk.Spinbox(self.pump_scheduling,values=self.pump_min_values,textvariable=self.pump5_min_end,wrap=True,width=2)
        self.pump_min5_end.grid(column=5,row=6)
        
        self.pump5_am_end = tk.StringVar(value='AM')
        self.pump_am5_end = ttk.Spinbox(self.pump_scheduling,values=['AM','PM'],textvariable=self.pump5_am_end,wrap=True,width=3)
        self.pump_am5_end.grid(column=6,row=6)

#-------------------Reservoir level-----------------------------------

        self.frame_waterlevel = ttk.LabelFrame(self.root, text='Reservoir Water Level')
        self.frame_waterlevel.grid(column=2,row=1, rowspan=1, padx=5,pady=5,sticky=N)
        
        self.res_level = StringVar()
        #self.res_level.set(self.water_level())
        
        #Label displaying water level
        self.waterlevel = ttk.Label(self.frame_waterlevel,textvariable=self.res_level,font=font_small,padding=5)        
        self.waterlevel.grid(row=0)
        
        #Auto reload for water level (and time)
        self.level_update()

#-------------------Exit button-------------------------------------

        self.exitButton = ttk.Button(self.root,text="EXIT",command=self.exitProgram,width=4) 
        self.exitButton.grid(column=0,row=2,sticky=N)
        
        self.root.mainloop()
        

def main():
    igs()
    
main()
print('\ndude')
