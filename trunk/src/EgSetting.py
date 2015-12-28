#!/usr/bin/python
# encoding: utf-8
# Filename: EgSetting.py

from gi.repository import Gtk, Gdk
import os
SET_FILENAME = 'usr.eg'


# 配置文件类
class SettingFile:
	def __init__(self):
		self.GetInfo()
			
	def GetInfo(self):
		fexist = os.path.exists(SET_FILENAME)
		if fexist:
			with open (SET_FILENAME,'r') as self.sfile: 
				self.data = self.sfile.read()
			if self.data:
				print('file exist')
				self.ResolveInfo()	
				return True
		print('file not exist,and create file')							
		self.CreateFile()
		return True

			
	def CreateFile(self):
		self.SetDefault()
		self.WriteInfo()
		
	def SetDefault(self):
		Data.__init__(EgData)	
		
	def WriteInfo(self):
		self.PackInfo()
		with open (SET_FILENAME,'w') as self.sfile:
			self.sfile.write(self.data)
	
	def ResolveInfo(self):
		temp = self.data.split(',')
		EgData.wtime_min = int(temp[0])/60
		EgData.wtime_sec = int(temp[0])%60
		EgData.rtime_min = int(temp[1])/60
		EgData.color = temp[2]

	def PackInfo(self):
		worktime = EgData.wtime_min*60 + EgData.wtime_sec
		resttime = EgData.rtime_min*60
		color = None
		self.data = '{0},{1},{2}'.format (worktime,resttime,color)


# 数据类
class Data():
	def __init__(self):
		self.wtime_min = 45
		self.wtime_sec = 0
		self.rtime_min = 2
		self.color = None

	def set_time(self,wtmin,wtsec,rtmin):
		self.wtime_min = wtmin
		self.wtime_sec = wtsec
		self.rtime_min = rtmin

# 数据对象		
EgData = Data()
EgFile = SettingFile()


# 设置对话框类		
class SettingDialog(Gtk.Dialog):
	def __init__(self,window):
		Gtk.Dialog.__init__(self,title="Setting",parent=window)
		self.ValueChangeflag = False #值是否改变标志
		self.set_modal(True)
		
		self.content_area = self.get_content_area()
		self.textbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing = 10) 
		self.btnbox = Gtk.Box(spacing=10) 
		self.hbox1 = Gtk.Box(spacing=10) 
		self.hbox2 = Gtk.Box(spacing=10) 

		self.CreateText()
		self.CreateBtn()
		self.PackWidget()
		self.show_all()

	def CreateText(self):
		work_text="工作时间:"
		rest_text="休息时间:"
				
		self.work_view = Gtk.TextView()
		buffer1 = Gtk.TextBuffer()
		buffer1.set_text(work_text)
		self.work_view.set_buffer(buffer1)
		self.work_view.set_editable(False)

		self.rest_view = Gtk.TextView()
		buffer2 = Gtk.TextBuffer()
		buffer2.set_text(rest_text)
		self.rest_view.set_buffer(buffer2)	
		self.rest_view.set_editable(False)
	
		color = Gdk.RGBA()
		color.parse("#F2F1F0")
		self.work_view.override_background_color(Gtk.StateFlags.NORMAL,color)	
		self.rest_view.override_background_color(Gtk.StateFlags.NORMAL,color)	
		
	def CreateBtn(self):
		self.btnapply = Gtk.Button(label="应用")
		self.btndef = Gtk.Button(label="恢复默认")
		self.btnapply.set_sensitive(False)
		
		adjust = Gtk.Adjustment( EgData.wtime_min,1.0, 59.0, 1.0, 5.0, 0.0)
		self.btnw_min = Gtk.SpinButton()
		self.btnw_min.configure(adjust,1.0,0.0)
		adjust = Gtk.Adjustment( EgData.wtime_sec,0.0, 59.0, 1.0, 5.0, 0.0)
		self.btnw_sec = Gtk.SpinButton()
		self.btnw_sec.configure(adjust,1.0,0.0)
		adjust = Gtk.Adjustment( EgData.rtime_min,1.0, 59.0, 1.0, 5.0, 0.0)
		self.btnr_min = Gtk.SpinButton()	
		self.btnr_min.configure(adjust,1.0,0.0)	

		
		self.btnw_min.connect("value-changed",self.cbValueChanged)
		self.btnw_sec.connect("value-changed",self.cbValueChanged)
		self.btnr_min.connect("value-changed",self.cbValueChanged)
		
		self.btnapply.connect("clicked",self.cbBtnApply)
		self.btndef.connect("clicked",self.cbBtnDefault)

	def cbValueChanged(self,widget):
		if not self.btnapply.get_sensitive():
			self.btnapply.set_sensitive(True)
		
	def cbBtnApply(self,widget):
		self.btnapply.set_sensitive(False)
		self.ValueChangeflag = True
		
		wtmin = self.btnw_min.get_value_as_int()
		wtsec = self.btnw_sec.get_value_as_int()
		rtmin = self.btnr_min.get_value_as_int()
		
		EgData.set_time(wtmin,wtsec,rtmin)
		EgFile.WriteInfo()
		print('cbBtnApply')
	
	def cbBtnDefault(self,widget):
		self.btnapply.set_sensitive(True)
		self.ValueChangeflag = True
		EgFile.SetDefault()
		self.btnw_min.set_value(EgData.wtime_min)
		self.btnw_sec.set_value(EgData.wtime_sec)
		self.btnr_min.set_value(EgData.rtime_min)
		
		print('cbBtnDefault')		

	def PackWidget(self):
		self.hbox1.pack_start(self.work_view,False,False,12)
		self.hbox1.pack_start(self.btnw_min,False,False,10)
		self.hbox1.pack_start(self.btnw_sec,False,False,0)
	
		self.hbox2.pack_start(self.rest_view,False,False,12)		
		self.hbox2.pack_start(self.btnr_min,False,False,10)	
	
		self.textbox.pack_start(self.hbox1,False,False,10)
		self.textbox.pack_start(self.hbox2,False,False,0)	
			
		self.btnbox.pack_end(self.btnapply,False,False,0)
		self.btnbox.pack_end(self.btndef,False,False,0)		
		
		self.content_area.pack_start(self.textbox,False,False,0)
		self.content_area.pack_start(self.btnbox,False,False,10)


		
