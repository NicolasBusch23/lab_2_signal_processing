Pulse Transit Time PPG Dataset Version 1.0.0 README
===================================================

Name:
Pulse Transit Time PPG Dataset

Purpose:

This README file describes the Pulse Transit Time PPG Dataset Version 1.0.0

Authors:
Philip Mehrgardt (philip DOT mehrgardt AT uni DOT sydney DOT edu DOT au)
Matloob Khushi
Simon Poon
Anusha Withana

Last modified by Philip Mehrgardt, June 2021

License: Open Data Commons Open Database License v1.0

Version: 1.0.0

Title: Pulse Transit Time PPG Dataset


Abstract:
We provide an open access, high resolution and time synchronised dataset from 
multiple sensors worn at different body locations including Photoplethysmogram 
(PPG), Inertial, Pressure and ECG. The recordings are from 22 healthy subjects 
performing 3 physical activities. This dataset contains 66 waveform records from 
multi-site and multi-wavelength PPGs, sensors’ attachment pressures, sensors’ 
temperatures, inertial data from accelerometer and gyroscope, along with annotated 
ECG data for a total of 19 channels. Additionally, systolic and diastolic blood 
pressures, as well as blood oxygenation saturation levels (SpO2) numerics are 
provided.


Background:
This dataset contains 66 recordings of 19 physiologic time series for more than 
40000 heartbeats. These data were collected to conduct investigations into signal 
processing and machine learning models for applications in short distance Pulse 
Transit Time (PTT) recognition, cuffless pressure sensing and other cardiovascular 
activity modelling research.
PTT is the time that pulse waves require to travel in blood vessels between two 
sites [1]. It is an important indicator for many medical properties [2] and recent 
research focused on its potential for continuous blood pressure monitors [3, 4]. 
Three challenges make it difficult to measure it precisely: 1) PPG measurements 
are inherently noisy [5, 6], 2) the required wave phase detection accuracy for 
measurement sited in proximity (e.g., on the same finger) is in the order of 
milliseconds [7] and 3) the lack of available datasets for PPG measurements in 
proximity at the required high sample rates. This dataset is designed to address 
these challenges by providing, amongst other physiologic time series and numerics 
such as blood pressure, 2x3 unfiltered raw PPG sensor signals of multiple 
wavelengths for 2 measurement sites in a defined distance to each other.


Methods:
The data were acquired from 22 healthy subjects at The University of Sydney. 6 
participants were female and the age range was from 20 to 53 with a mean of 28.52 
years. All participants performed 3 activities in random order, namely sitting,
stationary walking and running. The data was collected from a device similar to 
commercial pulse oximeters, containing commercial sensors in a 3D-printed finger
clip. A 3-lead ECG recorded the electrical signal of the heart in parallel. The
included file device_schematic.png illustrates the used device.
The numerical records include gender, age group, weight group, systolic and 
diastolic blood pressure at the beginning and end of each activity. The heart rate 
was recorded at the beginning and end of the measurements with a commercial pulse 
oximeter and blood pressure monitor. SpO2 levels were measured at the start and 
end of each activity.

The hardware consisted of the following sensors, their locations is illustrated in 
the attached file device_schematic.png:

•	2X Maxim Integrated MAX30101 PPG configured to measure infrared 
	lambda=880+20-10nm (pleth_1 and pleth_4), red lambda = 660±10nm (pleth_2 and 
	pleth_5), green  lambda= 537+4-7nm (pleth_3 and pleth_6) at 1000Hz (multi-LED
	mode). The optimum settings for the LED current (18.8mA), pulse width of 215us
	and ADC range of 16384 were grid searched
•	2x TAL221100g miniature load cells (lc_1, lc_2) measuring the mechanical 
	attachment pressure, connected to 2x HX711 24-bit loadcell amplifier measuring 
	at 80Hz
•	1x TDK - InvenSenseMPU-9250 IMU (a_x, a_y, a_z, g_x, g_y, g_z) 
	measuring at 500Hz
•	1x AD8232 ECG amplifier (ecg) measuring at 500Hz

All sensors were connected to an ARM Cortex-M4 at 180 MHz microcontroller, reading 
all sensors within a 2ms window (500Hz).
The blood pressure was recorded with an OMRON HEM-7322 blood pressure monitor and 
blood oxygen saturation levels with an iHealth Air Wireless Pulse Oximeter.


Data Description:
The data is distributed in two formats, WFDB (WaveForm DataBase) and CSV (comma-
separated-value). The WFDB data for all participants have been placed in the root 
directory along with a corresponding RECORDS file. Each WFDB HEA header file 
contains the participants' numerics such as <weight>. ATR annotation files contain
automatically detected and manually verified R peak ECG annotations for all records.
Record, header and annotation file names incorporated subject and activity following 
this structure:

sXX_YYYY
s = subject
XX = subject number (1-22)
YYY = activity (sit, walk, run)

The data is also provided in CSV format in the \CSV folder. All CSV records include a
“time” column that was date shifted to de-indentify participants. The \CSV folder 
also contains the file subjects_info.csv, describing the participants' numerics 
such as <weight>.

Both WFDB and CSV records contain the following channels:

•	ecg: 3-lead ECG captured at 500Hz
•	peaks: CSV ONLY, annotated in WFDB. The annotated ECG R peak (1 = peak, 
	0 = no peak)
•	pleth_1: MAX30101 red wavelength PPG from the distal phalanx (first segment) 
	of the left index finger palmar side (arbitrary units, 500Hz)
•	pleth_2: MAX30101 infrared wavelength PPG from the distal phalanx (first segment) 
	of the left index finger palmar side (arbitrary units, 500Hz)
•	pleth_3: MAX30101 green wavelength PPG from the distal phalanx (first segment) 
	of the left index finger palmar side (arbitrary units, 500Hz)
•	pleth_4: MAX30101 red wavelength PPG from the proximal phalanx (base segment) 
	of the left index finger palmar side (arbitrary units, 500Hz)
•	pleth_5: MAX30101 infrared wavelength PPG from the proximal phalanx (base segment) 
	of the left index finger palmar side (arbitrary units, 500Hz)
•	pleth_6: MAX30101 green wavelength PPG from the proximal phalanx (base segment) 
	of the left index finger palmar side (arbitrary units, 500Hz)
•	lc_1: TAL221 load cell proximal phalanx (first segment) PPG sensor attachment 
	pressure (arbitrary units, 80Hz)
•	lc_2: TAL221 load cell (base segment) PPG sensor attachment pressure (arbitrary 
	units, 80Hz)
•	temp_1: distal phalanx (first segment) PPG sensor temperature (°C, 10Hz)
•	temp_2: proximal phalanx (base segment) PPG sensor temperature in (°C, 10Hz)
•	temp_3: InvenSenseMPU-9250 IMU temperature (°C, 500Hz)
•	a_x: InvenSenseMPU-9250 IMU acceleration in x-direction (g, 500Hz)
•	a_y: InvenSenseMPU-9250 IMU acceleration in y-direction (g, 500Hz)
•	a_z: InvenSenseMPU-9250 IMU acceleration in z-direction (g, 500Hz)
•	g_x: InvenSenseMPU-9250 IMU angular velocity around x-axis (°/s, 500Hz)            
•	g_y: InvenSenseMPU-9250 IMU angular velocity around y-axis (°/s, 500Hz)            
•	g_z: InvenSenseMPU-9250 IMU angular velocity around z-axis (°/s, 500Hz)

Each CSV record includes a "time" column that was date shifted to de-indentify 
participants. All WFDB header files or subjects_info.csv contain the following 
information for each participant:

•	<filename>: record filename
•	<activity>: sit, walk or run
•	<gender>: male or female
•	<height>: in increments of 5 (cm)
•	<weight>: in increments of 5 (kg)
•	<age>: in increments of 5 (years)
•	<bp_sys_start>: systolic blood pressure at the start of the measurement (mmHg)
•	<bp_sys_end>: systolic blood pressure at the end of the measurement (mmHg)
•	<bp_dia_start>: diastolic blood pressure at the start of the measurement (mmHg)
•	<bp_dia_end>: diastolic blood pressure at the end of the measurement (mmHg)
•	<hr_1_start>: heart rate as measured with the OMRON HEM-7322 blood pressure
	monitor at the start of the measurement (bpm)
•	<hr_2_start>: heart rate as measured with the iHealth Air Wireless Pulse Oximeter
	at the start of the measurement (bpm)
•	<hr_1_end>: heart rate as measured with the OMRON HEM-7322 blood pressure monitor
	at the end of the measurement (bpm)
•	<hr_2_end>: heart rate as measured with the iHealth Air Wireless Pulse Oximeter
	at the end of the measurement (bpm)
•	<spo2_start>: SpO2 at the start of the measurement (%)
•	<spo2_end>: SpO2 at the end of the measurement (%)


Usage Notes:
The WFDB files can be found in the root directory. The participants are denoted by 
their filename, e.g. s1_run indicating subject 1, running. There are 3 files for 
each of the subjects’ 3 activities, for example for subject 1, running:

•	s1_run.head is the header file, which also contains participant information 
	such as participant weight
•	s1_run.dat contains subject 1 raw recording (19 channels) while running
•	s1_run.atr contains the annotations for subject 1’s ECG R peaks

The CSV files containing 19 signals each can be found in the \CSV folder. The ECG
R peak annotations are coded in an additional “peaks” column where “1” represents
an R peak and “0” no peak. The subjects_info.csv file contains the numerics such
as participant weight for all participants.

The data has been used in an unpublished study for accurate heart rate detection. 
It can be reused for time series investigations where accurate inter-channel time 
synchronisation and high time resolution are required, such as pulse transit time 
derived applications. The data can also be used to investigate pulse wave-induced 
dynamic pressure changes at fingers.

It should be noted that the sensor data is unfiltered to retain all timing 
information and to allow direct experimentation, whereas most published PPG data 
is filtered. To convert the data, we found that removing the DC component by 
subtracting the output of a centered mean rolling gaussian window and adding a 
0.75-5Hz bandpass provided results similar to filtered datasets.

The limitations are that for subject 13 the ECG data is particularly noisy during 
the walking exercise and that the used InvenSenseMPU-9250 IMU occasionally showed 
single-sample artifacts, including for temperature.


Acknowledgements
This work was supported by the University of Sydney Cardiovascular Initiative 
funding. Dr. Withana is the recipient of an Australian Research Council Discovery 
Early Career Award (DE200100479) funded by the Australian Government.


References
1.	Lane, J.D., et al., Pulse Transit Time and Blood Pressure: An Intensive 
Analysis. Psychophysiology, 1983. 20(1): p. 45-49.
2.	Geddes, L.A., et al., Pulse Transit Time as an Indicator of Arterial 
Blood Pressure. Psychophysiology, 1981. 18(1): p. 71-74.
3.	Ghosh, S., et al. Continuous blood pressure prediction from pulse transit 
time using ECG and PPG signals. in 2016 IEEE Healthcare Innovation Point-Of-Care 
Technologies Conference (HI-POCT). 2016.
4.	Gesche, H., et al., Continuous blood pressure measurement by using the 
pulse transit time: Comparison to a cuff-based method. European journal of applied 
physiology, 2011. 112: p. 309-15.
5.	Lee, H., H. Chung, and J. Lee, Motion Artifact Cancellation in Wearable 
Photoplethysmography Using Gyroscope. IEEE Sensors Journal, 2018. PP: p. 1-1.
6.	Foo, J.Y.A. and S.J. Wilson, A computational system to optimise noise 
rejection in photoplethysmography signals during motion or poor perfusion states. 
Medical and Biological Engineering and Computing, 2006. 44(1): p. 140-145.
7.	van Velzen, M.H.N., et al., Increasing accuracy of pulse transit time 
measurements by automated elimination of distorted photoplethysmography waves. 
Medical & biological engineering & computing, 2017. 55(11): p. 1989-2000.


In case of problems contact: 
Philip Mehrgardt (philip DOT mehrgardt AT uni DOT sydney DOT edu DOT au)