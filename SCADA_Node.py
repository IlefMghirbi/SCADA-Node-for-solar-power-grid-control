#Author: Ilef Mghirbi

import u3
import time
import os
import Tkinter as tk
from Tkinter import *


d= u3.U3()
d.getCalibrationData()

#voltage divider ratio
ratio= 0.4952

#amplifying circuit gain
gain= 11


#create a new file called 'File_DC_Bus_Voltage' if it does not already exist
File_DC_Bus_Voltage= open( "File_DC_Bus_Voltage", "a")

#create a new file called 'File_Station_Power_Voltage' if it does not already exist

File_Station_Power_Voltage= open ("File_Station_Power_Voltage", "a")

#create a new file called 'File_Ambient_Temperature' if it does not already exist
File_Ambient_Temperature = open("File_Ambient_Temperature", "a") 



#trip and close functions 
def trip():
	DAC0Value = d.voltageToDACBits(4.95, dacNumber=0, is16Bits= False) #4.95v signal to trigger the tripping action
	d.getFeedback(u3.DAC0_8(DAC0Value))

	time.sleep(0.5) #delay to allow time for the signal to trip the breaker

	DAC0Value = d.voltageToDACBits(0.0,  dacNumber=0, is16Bits= False) #turning it back to 0v after it trips the breaker
	d.getFeedback(u3.DAC0_8(DAC0Value))
	File_trip_close_write= open ("File_trip_close_write", "a")
	File_trip_close_write.write("Breaker Tripped  " + time.ctime() + '\n') #saving the action to the file

def close():
	DAC1Value = d.voltageToDACBits(4.95, dacNumber=1, is16Bits= False) #4.95v signal to trigger the closing action
	d.getFeedback(u3.DAC1_8(DAC1Value))

	time.sleep(0.5)

	DAC1Value = d.voltageToDACBits(0.0, dacNumber=1, is16Bits= False) #turning it back to 0v after it closes the breaker
	d.getFeedback(u3.DAC1_8(DAC1Value))
	
	File_trip_close_write= open ("File_trip_close_write", "a")
	File_trip_close_write.write("Breaker Closed  " + time.ctime() + '\n') #saving the action to the file
	
#saving trip/close events with time stamps


	
def update_DC_Bus_voltage():
	
	DCbusVoltageConverted= round(d.getAIN(0),3) #measuring the circuit divider output

	Dc_Bus_Voltage= round(DCbusVoltageConverted/ ratio , 3) #converting into the real DC Bus voltage 
	text_Dc_Bus_Voltage= "DC Bus Voltage is equal to: " + str(Dc_Bus_Voltage) + "v - " + time.ctime()
	
	Label_Dc_Bus_Voltage.config(text= text_Dc_Bus_Voltage) #configuring the text inside the label to the above message
	
	#writing the DC bus voltage in a file in case it exceeds 15.5v or goes below 13v
	if Dc_Bus_Voltage > 15.5 or Dc_Bus_Voltage < 13.0 :
	
		File_DC_Bus_Voltage= open("File_DC_Bus_Voltage", "a")
		File_DC_Bus_Voltage.write( 'DC Bus Voltage=' + str(Dc_Bus_Voltage)+ 'V  '+ time.ctime()+  '\n')
	Label_Dc_Bus_Voltage.after(5000, update_DC_Bus_voltage) #function calls itself each 5 seconds
	
def update_Station_Power_voltage():
	StationVoltageConverted= round(d.getAIN(1),3) #measuring the circuit divider output

	Station_Power_Voltage= round(StationVoltageConverted/ ratio , 3)
	text_Station_Power_Voltage= "Station Power Voltage is equal to: " + str(Station_Power_Voltage) + "v - " + time.ctime()
	
	Label_Station_Power_Voltage.config(text= text_Station_Power_Voltage) #configuring the text inside the label to the above message
	Label_Station_Power_Voltage.after(5000, update_Station_Power_voltage) #function calls itself each 5 seconds
	
	#saving Station power voltage data to the file:
	File_Station_Power_Voltage= open("File_Station_Power_Voltage", "a")
	File_Station_Power_Voltage.write( 'Station Power Voltage ='+ str(Station_Power_Voltage)+ 'V  ' + time.ctime()+  '\n')
	File_Station_Power_Voltage.close()
	
def update_temperature():
	#reading the voltage measurment from the amplifying circuit
	Temperature_Voltage= round(d.getAIN(2),2) #measuring the input from the amplifier circuit

	time.sleep(1)

	#converting the measurement to temperature in degree celsius 
	# 100= 1000/10 as 1000 corresponds to the conversion from V to mV and 10 to the conversion from mV to Deg Celsius
	Ambient_Temperature= round(((Temperature_Voltage/gain) * 100 ), 2)
	Text_Ambient_Temperature= " The ambient temperature inside the junction box is: " + str(Ambient_Temperature) + "C - " + time.ctime()
	Label_Ambient_Temperature.config(text= Text_Ambient_Temperature) #configuring the text inside the label to the above message
	Label_Ambient_Temperature.after(5000, update_temperature) #function calls itself each 5 seconds
	
	#saving the measurements in the ambient temperature file
	File_Ambient_Temperature = open("File_Ambient_Temperature", "a") 
	File_Ambient_Temperature.write ("Ambient Temperature is: " + str(Ambient_Temperature) +"C - " + time.ctime() )
	File_Ambient_Temperature.write ("\n")

while True:
	
	#creating the root widget called window and entitled SCADA Node
	window = tk.Tk()
	window.title("SCADA Node")           
	
	#empty frame to add height to the mainn window
	empty_frame1= tk.Frame (window, height= 100)
	empty_frame1.pack() #adds the widget to the window
	
	#dc BUS
		
	Frame_Dc_Bus_Voltage= tk.Frame(window, borderwidth= 5) #creating the frame that will contain the voltages/ temperature labels
	Frame_Dc_Bus_Voltage.pack() #adds the widget to the window
	
	Label_Dc_Bus_Voltage= tk.Label (Frame_Dc_Bus_Voltage , text= "", #creating the label that will display voltages/ temperature 
	#'Frame_Dc_Bus_Voltage being its master
	width= 65, 
	height= 3, 
	bg="white" #background color
	)
	
	Label_Dc_Bus_Voltage.pack()
	update_DC_Bus_voltage()
	
	#station power
	
	Frame_Station_Power_Voltage= tk.Frame( window, borderwidth= 5)
	Frame_Station_Power_Voltage.pack()
	
	Label_Station_Power_Voltage= tk.Label(Frame_Station_Power_Voltage,
	text= "",
	width= 65, 
	height= 3, 
	bg="white")
	
	Label_Station_Power_Voltage.pack()
	update_Station_Power_voltage()
	
	
	#temperature
	Frame_Ambient_Temperature= tk.Frame (window, borderwidth= 5)
	Frame_Ambient_Temperature.pack()
	
	Label_Ambient_Temperature= tk.Label( Frame_Ambient_Temperature,
	text= "",
	width= 90,
	height= 3,
	bg= "white")
	
	Label_Ambient_Temperature.pack()
	update_temperature()
	
	
	#creating the trip and close buttons
	
	Trip_button= tk.Button(window, #tk window is the master
	 text="Trip Breaker",
	  bg="green",
	  width= 15,
	  height=3,
	  command= trip #the function to run when the button is clicked
	
	  )
	Trip_button.pack()	
	
	Close_button= tk.Button(window, #tk window is the master
	 text="Close Breaker",
	  bg="red",
	  width= 15,
	  height=3, 
	  command= close #the function to run when the button is clicked
	
	  )
	Close_button.pack()	
	
	#empty frame to add height to the mainn window
	empty_frame2= tk.Frame (window, height= 100)
	empty_frame2.pack()

	                                  

	window.mainloop() #starts running the application
