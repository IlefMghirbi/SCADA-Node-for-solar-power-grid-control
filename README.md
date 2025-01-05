# SCADA Node for a solar power grid control inside the LCSC SCL lab

I created this experimental SCADA node for the lab’s miniature power grid system. It aims to monitor conditions like voltage and ambient temperature of the power system and exert control over circuit breakers when needed via an ethernet network. To do so, I used a raspberry pi4, a Data Acquisition Unit (DAQ) from LabJack Corporation that surprised me with the detailed documentation that answered all of my questions as well as the power grid circuitry.

The project required designing and building a voltage divider circuit to provide appropriate voltage levels to the DAQ, a temperature sensing circuit to measure ambient temperature, mosfets to isolate the DAQ from the circuit breakers and avoid damage caused by excess current, as well as developing the program that reads and writes data from the DAQ and the Graphical User Interface using Python.

Check the project in action [here](https://www.youtube.com/watch?v=OH7rZSWRuKw) 
