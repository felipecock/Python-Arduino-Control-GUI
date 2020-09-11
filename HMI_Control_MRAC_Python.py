#!/usr/bin/env python
# Este archivo usa el encoding: utf-8
"""
GP:
Changed datasource, title, and refresh interval to use
as a poor man's Arduino oscilliscope.

This demo demonstrates how to draw a dynamic mpl (matplotlib) 
plot in a wxPython application.

It allows "live" plotting as well as manual zooming to specific
regions.

Both X and Y axes allow "auto" or "manual" settings. For Y, auto
mode sets the scaling of the graph to see all the data points.
For X, auto mode makes the graph "follow" the data. Set it X min
to manual 0 to always see the whole data from the beginning.

Note: press Enter in the 'manual' text box to make a new value 
affect the plot.

Eli Bendersky (eliben@gmail.com)
License: this code is in the public domain
Last modified: 31.07.2008
"""
import os
import pprint
import random
import sys
import wx
import wx.lib.intctrl  #Nuevo
from wx.lib.embeddedimage import PyEmbeddedImage
icono = PyEmbeddedImage(
	"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"
    "AElFTkSuQmCC")

REFRESH_INTERVAL_MS = 200
SAMPLING_RATE_MS = 50  #Nuevo
AUTO_RANGE = 20000/SAMPLING_RATE_MS #Nuevo

# The recommended way to use wx with mpl is with the WXAgg
# backend. 
#
import matplotlib
matplotlib.use('WXAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigCanvas, \
    NavigationToolbar2WxAgg as NavigationToolbar
import numpy as np
import pylab
import csv  #Nuevo
from array import *  #Nuevo

#Data comes from here
from Arduino_Monitor_MRAC import SerialData as DataGen


class BoundControlBox(wx.Panel):
	"""  A static box with a couple of radio buttons and a text
		box. Allows to switch between an automatic mode and a 
		manual mode with an associated value.
	"""
	def __init__(self, parent, ID, label, initval):
		wx.Panel.__init__(self, parent, ID)

		self.value = initval

		box = wx.StaticBox(self, -1, label)
		sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

		self.radio_auto = wx.RadioButton(self, -1, 
			label="Auto", style=wx.RB_GROUP)
		self.radio_manual = wx.RadioButton(self, -1,
			label="Manual")
		self.manual_text = wx.TextCtrl(self, -1, 
			size=(35,-1),
			value=str(initval),
			style=wx.TE_PROCESS_ENTER)
		    
		self.Bind(wx.EVT_UPDATE_UI, self.on_update_manual_text, self.manual_text)
		self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.manual_text)


		manual_box = wx.BoxSizer(wx.HORIZONTAL)
		manual_box.Add(self.radio_manual, flag=wx.ALIGN_CENTER_VERTICAL)
		manual_box.Add(self.manual_text, flag=wx.ALIGN_CENTER_VERTICAL)

		sizer.Add(self.radio_auto, 0, wx.ALL, 10)
		sizer.Add(manual_box, 0, wx.ALL, 10)

		self.SetSizer(sizer)
		sizer.Fit(self)

	def on_update_manual_text(self, event):
	   self.manual_text.Enable(self.radio_manual.GetValue())

	def on_text_enter(self, event):
	   self.value = self.manual_text.GetValue()

	def is_auto(self):
	   return self.radio_auto.GetValue()

	def manual_value(self):
	   return self.value

class SystemInputBox(wx.Panel):

	def __init__(self, parent, ID, label, initval, minval, maxval):
		wx.Panel.__init__(self, parent, ID)

		self.value = initval

		box = wx.StaticBox(self, 0, label)
		sizer = wx.StaticBoxSizer(box, wx.HORIZONTAL)

		self.system_input = wx.lib.intctrl.IntCtrl(self,
			id=0, 
			size=(50,30),
			value=initval,
			min=minval,
			max=maxval,
			style=wx.TE_PROCESS_ENTER|wx.TE_CENTRE)
		  
		self.Bind(wx.EVT_TEXT_ENTER, self.on_text_enter, self.system_input)

		sizer.Add(self.system_input, 0, wx.ALL, 10)

		self.SetSizer(sizer)
		sizer.Fit(self)   
    
	def on_text_enter(self, event):
		if self.system_input.GetValue() >= self.system_input.GetMin() and self.system_input.GetValue() <= self.system_input.GetMax():
			self.value = self.system_input.GetValue()
			self.system_input.SelectAll()
  
	def step_value(self):
		return float(self.value)


class GraphFrame(wx.Frame):
	""" The main frame of the application
	"""
	title = 'Monitoreo del Sistema'

	def __init__(self):
		wx.Frame.__init__(self, None, -1, self.title)

		self.datagen = DataGen()
		self.ArduinoState = self.datagen.next(0)
		self.step = [0.0]
		self.sysresp = [0.0]
		self.actuator = [0.0]
		self.refresp = [0.0]
		self.obserr2 = [0.0]
		self.paused = False

		self.create_menu()
		self.create_status_bar()
		self.create_main_panel()

		self.redraw_timer = wx.Timer(self)
		self.sampling_timer = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.on_redraw_timer, self.redraw_timer)  
		self.Bind(wx.EVT_TIMER, self.on_sampling_timer, self.sampling_timer)   #Nuevo
		self.redraw_timer.Start(REFRESH_INTERVAL_MS)
		self.sampling_timer.Start(SAMPLING_RATE_MS) #Nuevo

	def create_menu(self):
		self.menubar = wx.MenuBar()

		menu_file = wx.Menu()
		m_expt = menu_file.Append(-1, "&Guardar Gráfico\tCtrl-G", "Guardar gráfico en un archivo.")
		self.Bind(wx.EVT_MENU, self.on_save_plot, m_expt)
		m_savedata = menu_file.Append(-1, "Guardar &Datos\tCtrl-D", "Guardar gráfico en un archivo.")
		self.Bind(wx.EVT_MENU, self.on_save_data, m_savedata)
		menu_file.AppendSeparator()
		m_exit = menu_file.Append(-1, "S&alir\tCtrl-Q", "Salir de la aplicación.")
		self.Bind(wx.EVT_MENU, self.on_exit, m_exit)
		self.menubar.Append(menu_file, "&Archivo")
		self.SetMenuBar(self.menubar)

	def create_main_panel(self):
		
		self.SetIcon(icono.GetIcon())
		self.panel = wx.Panel(self)
		self.init_plot()
		self.canvas = FigCanvas(self.panel, -1, self.fig)

		self.xmin_control = BoundControlBox(self.panel, -1, "X mín", 0)
		self.xmax_control = BoundControlBox(self.panel, -1, "X máx", 50)
		self.ymin_control = BoundControlBox(self.panel, -1, "Y mín", -1)
		self.ymax_control = BoundControlBox(self.panel, -1, "Y máx", 101)


		self.ymax_control.radio_manual.SetValue(1) #Nuevo
		self.ymin_control.radio_manual.SetValue(1) #Nuevo

		self.pause_button = wx.Button(self.panel, -1, "Pause")

		self.setpoint = SystemInputBox(self.panel, -1, "SetPoint", 0, 0, 100)  #Nuevo

		self.Bind(wx.EVT_BUTTON, self.on_pause_button, self.pause_button)
		self.Bind(wx.EVT_UPDATE_UI, self.on_update_pause_button, self.pause_button)

		self.cb_grid = wx.CheckBox(self.panel, -1, 
			"Mostrar Cuadrícula",
			style=wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_CHECKBOX, self.on_cb_grid, self.cb_grid)
		self.cb_grid.SetValue(True)
		self.cb_xlab = wx.CheckBox(self.panel, -1, 
			"Mostrar Etiquetas en X",
			style=wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_CHECKBOX, self.on_cb_xlab, self.cb_xlab)
		self.cb_xlab.SetValue(True)

		self.cb_actua = wx.CheckBox(self.panel, -1,
			"Mostrar Sañal de Control",
			style=wx.ALIGN_RIGHT)
		self.Bind(wx.EVT_CHECKBOX, self.on_cb_actua, self.cb_actua) 
		self.cb_actua.SetValue(True)

		self.hbox1 = wx.BoxSizer(wx.VERTICAL)
		self.hbox1.Add(self.cb_grid, border=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
		self.hbox1.Add(self.cb_xlab, border=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
		self.hbox1.Add(self.cb_actua, border=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)

		self.hbox2 = wx.BoxSizer(wx.HORIZONTAL)
		self.hbox2.Add(self.pause_button, border=10, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
		self.hbox2.Add(self.setpoint, border=10, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL)
		self.hbox2.AddSpacer(20)
		self.hbox2.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL) #Nuevo FCM.
		self.hbox2.AddSpacer(20)
		self.hbox2.Add(self.xmin_control, border=5, flag=wx.ALL)
		self.hbox2.Add(self.xmax_control, border=5, flag=wx.ALL)
		self.hbox2.AddSpacer(20)
		self.hbox2.Add(self.ymin_control, border=5, flag=wx.ALL)
		self.hbox2.Add(self.ymax_control, border=5, flag=wx.ALL)

		self.vbox = wx.BoxSizer(wx.VERTICAL)
		self.vbox.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
		#~ self.vbox.Add(self.hbox1, 0, flag=wx.ALIGN_LEFT | wx.TOP)  #Nuevo
		self.vbox.Add(self.hbox2, 0, flag=wx.ALIGN_LEFT | wx.TOP)

		self.panel.SetSizer(self.vbox)
		self.vbox.Fit(self)
		self.setpoint.SetFocus()

	def create_status_bar(self):
		self.statusbar = self.CreateStatusBar()

	def init_plot(self):
		self.dpi = 100
		self.fig = Figure((5.0, 5.0), dpi=self.dpi)
		#self.fig.set_facecolor('#beb7b4')
		
		self.axes = self.fig.add_subplot(111)
		self.axes.set_axis_bgcolor('black')
		self.axes.set_title('Control MRAC del Sistema de Iluminación\n'.decode('utf-8'), size=14)

		x_label = 'Tiempo (x' + str(SAMPLING_RATE_MS) + ' ms)'
		pylab.setp(self.axes.set_xlabel(x_label), fontsize=10)
		pylab.setp(self.axes.set_ylabel('Intensidad Lumínica (Lux)'.decode('utf-8')), fontsize=10)
		pylab.setp(self.axes.get_xticklabels(), fontsize=8)
		pylab.setp(self.axes.get_yticklabels(), fontsize=8)

		# plot the data as a line series, and save the reference 
		# to the plotted line series
		  
		self.plot_step = self.axes.plot(	#Nuevo
			self.step,						#Nuevo
			linewidth=1,					#Nuevo
			color=(0, 1, 0),				#Nuevo
			label='SetPoint'				#Nuevo
			)[0]							#Nuevo
			
		self.plot_actuator = self.axes.plot(#Nuevo
			self.step,						#Nuevo
			linewidth=1,					#Nuevo
			color=(0, 0, 0.75),				#Nuevo
			label='Señal de Control'.decode('utf-8')		#Nuevo
			)[0]							#Nuevo
			
		self.plot_refresp = self.axes.plot(	#Nuevo
			self.step, 						#Nuevo
			linewidth=1,					#Nuevo
			color=(1, 0, 0.7),				#Nuevo
			label='Modelo de Referencia'	#Nuevo
			)[0]							#Nuevo
			
		self.plot_obserr2 = self.axes.plot(	#Nuevo
			self.step,						#Nuevo
			linewidth=1,					#Nuevo
			color=(1, 0.5, 0),				#Nuevo
			label='Error Sistema-Modelo'	#Nuevo
			)[0]							#Nuevo

		self.plot_sysresp = self.axes.plot(	#Nuevo
			self.step,						#Nuevo
			linewidth=1,					#Nuevo
			color=(1, 1, 0),				#Nuevo
			label='Respuesta del Sistema'	#Nuevo
			)[0]							#Nuevo
		
		
		
		self.axes.legend(bbox_to_anchor=(1.0, 0.5), loc=3, frameon=False, labelspacing=1.0, prop={'size':9})
		self.fig.subplots_adjust(left=0.05, right=0.85, top=0.9, bottom=0.1)
		
	def draw_plot(self):
		""" Redraws the plot
		"""
		# when xmin is on auto, it "follows" xmax to produce a 
		# sliding window effect. therefore, xmin is assigned after
		# xmax.
		#
		
		if self.xmax_control.is_auto():
			xmax = len(self.sysresp) if len(self.sysresp) > AUTO_RANGE else AUTO_RANGE
		else:
			xmax = int(self.xmax_control.manual_value())
		if self.xmin_control.is_auto():            
			xmin = xmax - AUTO_RANGE
		else:
			xmin = int(self.xmin_control.manual_value())

		# for ymin and ymax, find the minimal and maximal values
		# in the data set and add a mininal margin.
		# 
		# note that it's easy to change this scheme to the 
		# minimal/maximal value in the current display, and not
		# the whole data set.
		#
		if self.ymin_control.is_auto():
			ymin = round(min(self.sysresp), 0) - 1
		else:
			ymin = int(self.ymin_control.manual_value())

		if self.ymax_control.is_auto():
			ymax = round(max(self.sysresp), 0) + 1
		else:
			ymax = int(self.ymax_control.manual_value())

		self.axes.set_xbound(lower=xmin, upper=xmax)
		self.axes.set_ybound(lower=ymin, upper=ymax)
		
		# anecdote: axes.grid assumes b=True if any other flag is
		# given even if b is set to False.
		# so just passing the flag into the first statement won't
		# work.
		#
		if self.cb_grid.IsChecked():
			self.axes.grid(True, color='gray')
		else:
			self.axes.grid(False)
		

		# Using setp here is convenient, because get_xticklabels
		# returns a list over which one needs to explicitly 
		# iterate, and setp already handles this.
		#  
		pylab.setp(self.axes.get_xticklabels(), 
			visible=self.cb_xlab.IsChecked())

		self.plot_sysresp.set_xdata(np.arange(len(self.step)))
		self.plot_sysresp.set_ydata(np.array(self.sysresp))
		self.plot_step.set_xdata(np.arange(len(self.step)))
		self.plot_step.set_ydata(np.array(self.step))
		
		if self.cb_actua.IsChecked():
			self.plot_actuator.set_xdata(np.arange(len(self.actuator)))
			self.plot_actuator.set_ydata(np.array(self.actuator))
		else:
			self.plot_actuator.set_xdata([0])
			self.plot_actuator.set_ydata([0])

		self.plot_refresp.set_xdata(np.arange(len(self.refresp)))
		self.plot_refresp.set_ydata(np.array(self.refresp))
		self.plot_obserr2.set_xdata(np.arange(len(self.obserr2)))
		self.plot_obserr2.set_ydata(np.array(self.obserr2))

		self.canvas.draw()

	def on_pause_button(self, event):
		self.paused = not self.paused

	def on_update_pause_button(self, event):
		label = "Reanudar" if self.paused else "Pausar"
		self.pause_button.SetLabel(label)

	def on_cb_grid(self, event):
		self.draw_plot()
    
	def on_cb_xlab(self, event):
		self.draw_plot()
	
	def on_cb_actua(self, event):
		self.draw_plot() 
    
	def on_save_plot(self, event):
		file_choices = "PNG (*.png)|*.png|SVG (*.svg)|*.svg"
	   
		dlg = wx.FileDialog(
			self, 
			message="Guardar gáfico como...",
			defaultDir=os.getcwd(),
			defaultFile="Gráfico",
			wildcard=file_choices,
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
	
		if dlg.ShowModal() == wx.ID_OK:
			if (dlg.GetFilterIndex() == 0):
				if not(".png" in dlg.GetFilename()):
					dlg.SetFilename(dlg.GetFilename() + ".png")
			else:
				if not(".svg" in dlg.GetFilename()):
					dlg.SetFilename(dlg.GetFilename() + ".svg")
			path = dlg.GetPath()
			self.canvas.print_figure(path, dpi=self.dpi*3)
			self.flash_status_message("Guardado en %s" % path)

	def on_save_data(self, event):
		file_choices = "CSV (*.csv)|*.csv"
		
		dlg = wx.FileDialog(
			self, 
			message="Guardar datos como...",
			defaultDir=os.getcwd(),
			defaultFile="Respuesta_del_Sistema.csv",
			wildcard=file_choices,
			style=wx.SAVE)
		  
		if dlg.ShowModal() == wx.ID_OK:
			path = dlg.GetPath()
			with open(path, 'w') as fp:
				a = csv.writer(fp, delimiter=';')
				times = array('i',[])
				k = 0
				for time in self.sysresp:
					times.append(SAMPLING_RATE_MS*k)
					k=k+1
				steps = array('f',np.array(self.step))
				sysresponses = array('f',np.array(self.sysresp))
				k = 0
				a.writerows([['Tiempo (ms)','Escalón','Respuesta']]) #Nuevo
				for step in steps:
					a.writerows([[times[k],steps[k],sysresponses[k]]])
					k=k+1
			self.flash_status_message("Guardado en %s" % path)

	def on_redraw_timer(self, event):
	   # if paused do not add data, but still redraw the plot
	   # (to respond to scale modifications, grid change, etc.)
	   if not self.paused:
			self.draw_plot()
	def on_sampling_timer(self, event):
		if not self.paused:
			self.ArduinoState = self.datagen.next(int(self.setpoint.step_value()*2.55)) #Nuevo
			self.sysresp.append(self.ArduinoState[0])		#Nuevo
			self.actuator.append(self.ArduinoState[1])	#Nuevo
			self.refresp.append(self.ArduinoState[2])	#Nuevo
			self.obserr2.append(self.ArduinoState[3])	#Nuevo
			self.step.append(self.setpoint.step_value())	#Nuevo

	def on_exit(self, event):
		self.Destroy()

	def flash_status_message(self, msg, flash_len_ms=1500):
		self.statusbar.SetStatusText(msg)
		self.timeroff = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, 
			self.on_flash_status_off, 
			self.timeroff)
		self.timeroff.Start(flash_len_ms, oneShot=True)

	def on_flash_status_off(self, event):
		self.statusbar.SetStatusText('')

if __name__ == '__main__':
	app = wx.PySimpleApp()
	app.frame = GraphFrame()
	app.frame.Show()
	app.MainLoop()
