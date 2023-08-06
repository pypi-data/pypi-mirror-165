#! /usr/bin/env python3
import os, sys
from pathlib import Path
import wx

import wx.adv
import wx.html
from kvh.kvh import tlist2kvh
from vkvh.parcours import *
import vkvh
diri=Path(vkvh.__file__).parent

import wx.lib.dialogs
import wx.aui

#import pdb;

wildcard="All files (*.*)|*.*"

class HistSearchCtrl(wx.SearchCtrl):
	maxSearches = 5

	def __init__(self, parent, id=-1, value="",
				 pos=wx.DefaultPosition, size=wx.DefaultSize, style=0,
				 doSearch=None, name="searchCtrl"):
		style |= wx.TE_PROCESS_ENTER
		wx.SearchCtrl.__init__(self, parent, id, value, pos, size, style, name=name)
		self.Bind(wx.EVT_TEXT_ENTER, self.OnTextEntered)
		self.Bind(wx.EVT_SEARCHCTRL_SEARCH_BTN, self.OnTextEntered)
		self.Bind(wx.EVT_MENU_RANGE, self.OnMenuItem, id=1, id2=self.maxSearches)
		self.doSearch = doSearch
		self.searches = []

	def OnTextEntered(self, evt):
		#pdb.set_trace()
		text = self.GetValue()
		if not text:
			if self.searches:
				text=self.searches[-1]
			else:
				return
		if self.doSearch(text):
			if text not in self.searches:
				self.searches.append(text)
			if len(self.searches) > self.maxSearches:
				del self.searches[0]
			self.SetMenu(self.MakeMenu())
		#self.SetValue("")

	def OnMenuItem(self, evt):
		text = self.searches[evt.GetId()-1]
		self.SetValue(text)
		self.doSearch(text)

	def MakeMenu(self):
		menu = wx.Menu()
		item = menu.Append(-1, "Recent Searches")
		item.Enable(False)
		for idx, txt in enumerate(self.searches):
			#try:
			menu.Append(1+idx, txt)
			#except:
				#import pdb; pdb.set_trace()
		return menu
class MyForm(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, wx.ID_ANY, size=(800, 600),
						  title="vkvh")
		self.nb = wx.aui.AuiNotebook(self, -1)
		self.nb.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnTabChange)
		self.nb.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnTabClose)
		self.SetSizer(wx.BoxSizer(wx.VERTICAL))
		self.GetSizer().Add(self.nb, 1,  wx.EXPAND)
		
		menubar = wx.MenuBar()
		fileMenu = wx.Menu()
		helpMenu=wx.Menu()
		
		open_item = fileMenu.Append(wx.ID_ANY, "&Open\tCtrl-O", "")
		new_item = fileMenu.Append(wx.ID_ANY, "&New\tCtrl-N", "")
		reload_item = fileMenu.Append(wx.ID_ANY, "&Reload from disk\tCtrl-R", "")
		save_item = fileMenu.Append(wx.ID_ANY, "&Save\tCtrl-S", "")
		saveas_item = fileMenu.Append(wx.ID_ANY, "Save As ...", "")
		close_menu_item=fileMenu.Append(wx.ID_ANY,"&Quit\tCtrl-Q")
		
		# search options
		smenu=wx.Menu()
		self.sopt=dict()
		self.sopt["key"]=smenu.AppendCheckItem(-1, "Search in Key")
		self.sopt["key"].Check()
		
		self.sopt["val"]=smenu.AppendCheckItem(-1, "Search in Value")
		self.sopt["whole"]=smenu.AppendCheckItem(-1, "Whole Word")
		self.sopt["up"]=smenu.AppendCheckItem(-1, "Backward")
		self.sopt["case"]=smenu.AppendCheckItem(-1, "Match Case")

		aide_menu_item=helpMenu.Append(wx.ID_ANY,"Manual")
		infos_menu_item=helpMenu.Append(wx.ID_ANY,"About")
		
		
		self.Bind(wx.EVT_MENU,self.onSwitchAide, aide_menu_item)
		
		self.Bind(wx.EVT_MENU, self.OnOpen, open_item)
		self.Bind(wx.EVT_MENU, self.OnNew, new_item)
		self.Bind(wx.EVT_MENU, self.OnReload, reload_item)
		self.Bind(wx.EVT_MENU, self.OnSave, save_item)
		self.Bind(wx.EVT_MENU, self.OnSaveAs, saveas_item)
		
		self.Bind(wx.EVT_MENU,self.onSwitchInfo,infos_menu_item)
		self.Bind(wx.EVT_MENU,self.onQuit,close_menu_item)
		self.Bind(wx.EVT_CLOSE,self.onQuit)
		
		menubar.Append(fileMenu, '&File')
		menubar.Append(smenu, '&Options')
		menubar.Append(helpMenu,'&Help')
		self.SetMenuBar(menubar)
		
		self.tb=self.CreateToolBar()
		self.tb.AddControl(HistSearchCtrl(self.tb, size=(150,-1), doSearch=self.DoSearch, name="ctrl_find"))
		self.tb.Realize()
		
		self.statusbar=self.CreateStatusBar(2)
		self.statusbar.SetStatusText("Click 'File > Open' (or Ctrl-O) to start")
	def err_mes(self, mes):
		"Show dialog with error message"
		dlg=wx.MessageDialog(self, mes, 'Error', wx.OK|wx.ICON_ERROR)
		dlg.ShowModal()
		dlg.Destroy()
	def noyes(self, mes):
		"Show Yes/No dialog with 'No' default. Returns True for Yes, False for No"
		dlg=wx.MessageDialog(self, mes, 'Error', wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT)
		res=(dlg.ShowModal()==wx.ID_YES)
		dlg.Destroy()
		return res
	def f2tab(self, path, tab=None):
		if tab is None:
			pan=TreeCreation(self.nb, path)
			self.nb.AddPage(pan, pan.bpath)
			self.nb.ChangeSelection(self.nb.GetPageCount()-1)
		else:
			tab.make_tree(path)
			self.nb.SetPageText(self.nb.GetPageIndex(tab), tab.bpath)

		self.statusbar.SetStatusText("read from '%s'"%path)
		self.statusbar.SetStatusText("", 1)
		self.tb.FindWindowByName("ctrl_find").SetFocus()
	def OnOpen(self,evt):
		""" 
		Called with "File > Open".
		User can choose a file from his directories.
		It creates a new tab of the NoteBook, where a tree list control will be created
		"""
		dlg=wx.FileDialog(
			self, message="Choose a file to open",
			defaultDir=os.getcwd(),
			defaultFile="",
			wildcard=wildcard,
			style=wx.FD_OPEN | wx.FD_MULTIPLE | wx.FD_CHANGE_DIR|wx.FD_FILE_MUST_EXIST|wx.FD_PREVIEW)
		
		if dlg.ShowModal()==wx.ID_OK:
			path=dlg.GetPaths()
			for p in path:
				self.f2tab(p)
			dlg.Destroy()
	def OnNew(self,evt):
		""" 
		Create a new KVH file and a tab for editing its content. Must be followed by "Save" or "Save as".
		"""
		dlg=wx.FileDialog(
			self, message="Choose a new file to create",
			defaultDir=os.getcwd(),
			defaultFile="new.kvh",
			wildcard=wildcard,
			style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT | wx.FD_PREVIEW | wx.FD_CHANGE_DIR)
		
		if dlg.ShowModal()==wx.ID_OK:
			p=dlg.GetPath()
			with open(p, "w") as fc:
				pass
			self.f2tab(p)
			dlg.Destroy()
	def OnReload(self,evt):
		""" 
		Re-read KVH file into current tab for editing its content.
		"""
		tab=self.nb.GetCurrentPage()
		if tab is None:
			return
		if tab.tree.edited:
			ok=self.noyes("Tab '%s' was edited. Reloading it will cancel the changes.\n Continue anyway?"%tab.bpath)
		else:
			ok=True
		if ok:
			self.f2tab(tab.path, tab)
	def OnSave(self,evt):
		""" 
		Save current tab in its path
		"""
		tab=self.nb.GetCurrentPage()
		if tab is None:
			return
		tlist2kvh(tree2tlist(tab.tree), tab.path)
		tab.tree.edited=False
		# remove '*' in tab title
		self.nb.SetPageText(self.nb.GetPageIndex(tab), tab.bpath)
		
		self.statusbar.SetStatusText("saved in '%s'"%tab.path)
		self.statusbar.SetStatusText("", 1)
	def OnSaveAs(self,evt):
		""" 
		Save current tab in asked path
		"""
		tab=self.nb.GetCurrentPage()
		if tab is None:
			return
		dlg=wx.FileDialog(
		self, message="Choose a file to save to",
		defaultDir=os.path.dirname(tab.path),
		defaultFile=tab.bpath,
		wildcard=wildcard,
		style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
		
		if dlg.ShowModal()==wx.ID_OK:
			p=dlg.GetPath()
			tlist2kvh(tree2tlist(tab.tree), p)
			tab.tree.edited=False
			tab.path=p
			tab.bpath=os.path.basename(p)
			self.nb.SetPageText(self.nb.GetPageIndex(tab), tab.bpath)
			self.statusbar.SetStatusText("saved in '%s'"%p)
			self.statusbar.SetStatusText("", 1)
			
			dlg.Destroy()
	def onQuit(self,event):
		"""Function to quit application"""
		# get names of edited tabs
		if "CanVeto" in dir(event) or event.IsCommandEvent():
			li_ed=[self.nb.GetPageText(i) for i in range(self.nb.GetPageCount()) if self.nb.GetPage(i).tree.edited]
			if li_ed:
				ok=self.noyes("Folowing tabs were edited: '%s'.\n Closing application will result in change loss.\n Continue anyway?"%"', '".join(li_ed))
			else:
				ok=True
			if ok:
				wx.CallAfter(self.Destroy)
			elif "Veto" in dir(event):
				event.Veto()
	def DoSearch(self,  text):
		"called by HistSearchCtrl"
		itab=self.nb.GetSelection()
		if itab < 0:
			self.err_mes("Open file first. Then you could search for some text in it.")
			return False
		tab=self.nb.GetPage(itab)
		flags=0
		in_kv=""
		if self.sopt["key"].IsChecked():
			in_kv += "k"
		if self.sopt["val"].IsChecked():
			in_kv += "v"
		if not in_kv:
			self.err_mes("At least one of 'In Key' or 'In Value' options must be checked")
			return False
		result=parcours_tree_by_label(tab.tree, text, self.sopt["up"].IsChecked(), in_kv, self.sopt["whole"].IsChecked(), self.sopt["case"].IsChecked())
		if result is not None:
			tab.tree.SelectItem(result)
			tab.tree.Expand(result.GetParent())
			tab.SetSize(tab.tree.GetSize())
			tab.tree.EnsureVisible(result)
			PathCreation(tab)
		else:
			"""Error dialog if element does not exist"""
			self.err_mes(f"Text '{text}' was not found in '{self.nb.GetPageText(itab)}'")
			return False
		# return true to tell the search ctrl to remember the text
		return True
	def onSwitchAide(self,event):
		"""Function for Help message dialog"""
		hlp.AddBook(str(diri/"help"/"vkvh.hhp"));
		hlp.DisplayContents()

	def onSwitchInfo(self,event):
		"""Function for Information message dialog"""
		info=wx.adv.AboutDialogInfo()
		info.Name="vkvh"
		info.Version=vkvh.__version__
		info.Help="help"
		info.Copyright="© Copyright 2022, INRAE/INSA/CNRS"
		info.Description="KVH files viewer/editor"
		info.Developers=["Maria Morozova","Serguei Sokol"]
		
		wx.adv.AboutBox(info)
	def OnTabChange(self, evt):
		PathCreation(self.nb.GetCurrentPage())
	def OnTabClose(self, evt):
		tab=self.nb.GetCurrentPage()
		if tab.tree.edited:
			ok=self.noyes("Tab '%s' was edited. Closing it will result in change loss.\n Continue anyway?"%tab.bpath)
		else:
			ok=True
		if not ok:
			evt.Veto()
		self.statusbar.SetStatusText("")
		self.statusbar.SetStatusText("", 1)
def main():
	global hlp
	app = wx.App(False)
	frame = MyForm()
	frame.Show()
	hlp=wx.html.HtmlHelpController();

	for p in sys.argv[1:]:
		frame.f2tab(p)
	app.MainLoop()

if __name__ == "__main__":
	main()
	
