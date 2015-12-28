#!/usr/bin/python
# encoding: utf-8
# Filename: EgLockScreen.py
from gi.repository import Gtk, GObject, Gdk

class LockScreen(Gtk.Dialog):
	def __init__(self,parent,rtmin):
		Gtk.Dialog.__init__(self)
		self.parent = parent
		self.fullscreen()
		self.set_modal(True)
		color = Gdk.RGBA()
		color.parse("#36763E")
		self.override_background_color(Gtk.StateFlags.NORMAL,color)	
		color.parse("#0606F4")
		self.override_color(Gtk.StateFlags.NORMAL,color)	
		self.rtime = rtmin * 60
		self.baktime = self.rtime 

		self.content_area = self.get_content_area()
		self.label = Gtk.Label()	
		self.content_area.add(self.label)	
		self.SetText()
		self.content_area.set_valign(Gtk.Align.CENTER)
		self.content_area.set_halign(Gtk.Align.CENTER)	

		animation = Gtk.Image()
		animation.set_from_file('1.gif')
		self.content_area.add(animation)
		
		
		self.timeout_id1 = GObject.timeout_add(100, self.KeepAbove, None)
		self.timeout_id2 = GObject.timeout_add_seconds(1, self.CountRest, None)
		self.connect("key-release-event",self.ShieldKey)#对应esc键
		self.connect("key-press-event",self.ShieldKey)#对应esc键		
		self.show_all()

	def CountRest(self,widget):
		if not self.rtime:
			self.response(Gtk.ResponseType.CANCEL)
			return False

		if (self.baktime - self.rtime)==60:
			self.CreateButton()#解锁按钮
		self.rtime -= 1
		self.SetText()
		return True

	def SetText(self):
		text = "\n休息时间到，请注意保护眼睛。\n劳逸结合，健康工作！\n"
		text += '{0:02d}:{1:02d}'.format (self.rtime/60,self.rtime%60)
		text += '后将解锁\n'
		self.label.set_text(text)
				

	def CreateButton(self):
		self.add_button("解锁",Gtk.ResponseType.CANCEL)

		
	def KeepAbove(self,widget):
		self.set_keep_above(True)
		return True

	def ShieldKey(self,widget,KeyValue):
		print('ShieldKey')
		return True

		