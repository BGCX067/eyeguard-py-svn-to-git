#!/usr/bin/python
# encoding: utf-8
# main.py
# Copyright (C) 2012 ythink <ythink@YTHINK>
# 
# eyeguard_py is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# eyeguard_py is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, GObject,GdkPixbuf, Gdk
import os, sys
from EgSetting import EgData,SettingDialog
from EgLockScreen import LockScreen

		
# 主窗口类		
class MyWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self,title="EyeGuard")
		self.connect('destroy', self.destroy)
		#self.resize(400,200)

		self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0) 
		self.add(self.box)
		
		self.toolbar = Gtk.Toolbar()
		self.infoview = Gtk.TextView()
		self.cdview = Gtk.TextView()
		self.btnbox = Gtk.Box(spacing=10)
		
		self.CreateToolbar()
		self.CreateText()
		self.CreateBtn()
		self.PackWidget()
		self.show_all()

	def CreateToolbar(self):# 工具条
		self.toolbar.set_style(Gtk.ToolbarStyle.ICONS)
		self.toolbar.set_border_width(2)	
		self.set = Gtk.ToolButton(Gtk.STOCK_PREFERENCES)
		self.picker = Gtk.ToolButton(Gtk.STOCK_COLOR_PICKER)
		self.about = Gtk.ToolButton( Gtk.STOCK_ABOUT)
		self.sep = Gtk.SeparatorToolItem()
		self.exit = Gtk.ToolButton(Gtk.STOCK_QUIT)

		self.toolbar.insert(self.set,-1)
		self.toolbar.insert(self.picker,-1)
		self.toolbar.insert(self.about,-1)
		self.toolbar.insert(self.sep,-1)
		self.toolbar.insert(self.exit,-1)
		
		self.set.connect("clicked",self.CbSetting)
		self.picker.connect("clicked",self.CbPicker)
		self.about.connect("clicked",self.CbAbout)	
		self.exit.connect("clicked",Gtk.main_quit)
	#赋初始值
	def GetDefaultValue(self):
		self.wtime_min = EgData.wtime_min
		self.wtime_sec = EgData.wtime_sec	
		self.bakwtime = self.wtime_min*60 + self.wtime_sec
		
	def CreateText(self):
		# 倒计时文本
		self.GetDefaultValue()
		cdtext='\t倒计时：{0:02d}:{1:02d}'.format (self.wtime_min,self.wtime_sec)
		# 介绍文本
		itext="\n\t欢迎使用护眼提示! ^_^ \n\t请设置好休息时间，并按下『开始』计时。\n\t温馨提示：默认时间是45分钟。\n"
		
		self.cdbuf = Gtk.TextBuffer()
		self.cdbuf.set_text(cdtext)
		self.cdview.set_buffer(self.cdbuf)
		self.cdview.set_editable(False)

		ibuf = Gtk.TextBuffer()
		ibuf.set_text(itext)
		self.infoview.set_buffer(ibuf)
		self.infoview.set_editable(False)		
		
		color = Gdk.RGBA()
		color.parse("#F2F1F0")
		self.infoview.override_background_color(Gtk.StateFlags.NORMAL,color)	
		self.cdview.override_background_color(Gtk.StateFlags.NORMAL,color)

		self.timeflag = True
		self.timeout_id = GObject.timeout_add_seconds(1, self.set_buff, None)
		
	def CreateBtn(self):	
		'''创建按钮 
		'''
		self.btnnow = Gtk.Button(label="立即休息")
		self.btndelay = Gtk.Button(label="推迟休息")
		self.btn1min = Gtk.RadioButton(label="1分钟")
		self.btn3min = Gtk.RadioButton(group=self.btn1min,label="3分钟")
		self.btn8min = Gtk.RadioButton(group=self.btn1min,label="8分钟")

		self.delaynum = 3

		self.btnnow.connect("clicked",self.CbBtnNow)
		self.btndelay.connect("clicked",self.CbBtnDelay)

	def PackWidget(self):
		self.btnbox.pack_start(self.btnnow,False,False,10)
		self.btnbox.pack_start(self.btndelay,False,False,0)
		self.btnbox.pack_start(self.btn1min,False,False,0)
		self.btnbox.pack_start(self.btn3min,False,False,0)
		self.btnbox.pack_start(self.btn8min,False,False,0)
		
		self.box.pack_start(self.toolbar,False,False,3)
		self.box.pack_start(self.infoview,False,False,3)
		self.box.pack_start(self.cdview,False,False,0)
		self.box.pack_start(self.btnbox,False,False,10)
		
	def set_buff(self,widget):
		if not self.timeflag:
			return False
			
		if not self.wtime_sec:
			if not self.wtime_min:
				self.CbBtnNow(None)
				return False
			self.wtime_min = self.wtime_min - 1
			self.wtime_sec = 60
		self.wtime_sec = self.wtime_sec - 1
			
		cdtext='\t倒计时：{0:02d}:{1:02d}'.format (self.wtime_min,self.wtime_sec)
		self.cdbuf.set_text(cdtext)
		return True
	
	def CbBtnNow(self,widget):
		'''『立即休息』按钮 
		'''
		self.timeflag = False
		self.lockdialog = LockScreen(self,EgData.rtime_min)
		self.lockdialog.connect("response",self.DestroyLockScreen)

	def DestroyLockScreen(self,dialog,response_id):
		print('response:%d',response_id)
		#赋初始值，并继续倒计时
		self.GetDefaultValue()
		if self.timeflag == False:
			self.timeflag = True
			self.timeout_id = GObject.timeout_add_seconds(1, self.set_buff, None)
			
		if response_id == Gtk.ResponseType.CANCEL:
			print('destroy dialog')
			dialog.destroy()
		self.delaynum = 3	
		self.btndelay.set_sensitive(True)
		
	def CbBtnDelay(self,widget):
		'''『推迟休息』按钮,推迟时间不能超过设置的时间
		'''
		if True == self.btn1min.get_active():
			delaytime = 1
		elif True == self.btn3min.get_active():
			delaytime = 3
		elif True == self.btn8min.get_active():
			delaytime = 8 

		self.wtime_min += delaytime
		if self.wtime_min >= EgData.wtime_min :
			self.wtime_min = EgData.wtime_min
			self.wtime_sec = EgData.wtime_sec

		self.delaynum -= 1
		if 0 == self.delaynum:
			self.btndelay.set_sensitive(False)
		print("CbBtnDelay:%d",self.delaynum)
		
	def CbSetting(self,widget):
		self.dialog = SettingDialog(self)
		self.dialog.connect("response",self.DestroySDialog)
		
		print("setting")	

	def DestroySDialog(self,dialog,response_id):
		#判断值是否改变
		temp = EgData.wtime_min *60 + EgData.wtime_sec
		if True == dialog.ValueChangeflag:
			dialog.ValueChangeflag = False
			self.GetDefaultValue()
		
	def CbPicker(self,widget):
		print("CbPicker")		
		
	def CbAbout(self,widget):
		print("CbAbout")		

	def destroy(window, self):
		Gtk.main_quit()
		
def main():
	win = MyWindow()
	Gtk.main()

		
if __name__ == "__main__":
    sys.exit(main())
