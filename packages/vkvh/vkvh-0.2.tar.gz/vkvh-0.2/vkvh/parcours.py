import os
import wx
from itertools import chain
from operator import itemgetter as iget
import wx.lib.agw.hypertreelist as HTL
from kvh.kvh import kvh_read

#import pdb;

class TreeCreation(wx.Panel):
	"""
	Create a panel and tree list control from path
	
	:param parent: Parent element (notebook) of the tree.
	:type parent: wx.aui.AuiNotebook
	
	:param path: Path to a kvh file.
	:type path: str
	"""
	def __init__(self, parent, path):
		wx.Panel.__init__(self, parent, -1)
		self.Bind(wx.EVT_SIZE, self.OnSize)
		self.make_tree(path)
	def make_tree(self, path):
		if "tree" in self.__dict__:
			self.DestroyChildren()
		self.tree=HTL.HyperTreeList(self, -1, style=0, agwStyle=wx.TR_HAS_BUTTONS | wx.TR_EDIT_LABELS | wx.TR_FULL_ROW_HIGHLIGHT)
		
		self.tree.AddColumn("N°")
		self.tree.AddColumn("Key")
		self.tree.AddColumn("Value")
		self.tree.SetMainColumn(1) 

		content=kvh_read(path, strip_white=True)
		self.path=path
		self.bpath=os.path.basename(path)
		root=self.tree.AddRoot("Root")
		root.SetText(2, "")
		self.tree.itlist=[]
		self.tree.it2i={}
		for k,v in content:
			AddItem(self.tree, (k,v), root)
		
		cwi=[[self.tree.GetMainWindow().GetItemWidth(item, i) for i in range(3)] for item in self.tree.itlist]
		cwi=[max(cwi, key=iget(i))[i] for i in range(3)]
		
		self.tree.SetColumnWidth(0, cwi[0]+10)
		self.tree.SetColumnWidth(1, cwi[1]+20)
		self.tree.SetColumnWidth(2, cwi[2]+10)
		self.tree.Expand(root)
		self.tree.GetMainWindow().Bind(wx.EVT_LEFT_DCLICK, self.OnLeftDClick)
		self.tree.GetMainWindow().Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
		self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelect)
		self.tree.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnLabelEdit)
		self.tree.edited=False
		
		win=self.Parent.Parent
		w,h=win.GetSize()
		win.SetSize(w,h+1)
		wx.CallAfter(win.SetSize, w,h)

	def OnSize(self, evt):
		self.tree.SetSize(self.GetSize())
	def OnSelect(self, evt):
		PathCreation(self)
	def OnLabelEdit(self, evt):
		#pdb.set_trace()
		if evt.IsEditCancelled():
			return
		evt.EventObject.edited=True
		tab=evt.EventObject.Parent
		nb=tab.Parent
		# add '*' in tab title
		nb.SetPageText(nb.GetPageIndex(tab), "*"+tab.bpath)

	def OnLeftDClick(self, event):
		pt = event.GetPosition()
		item, flags, column = self.tree.HitTest(pt)
		if item and item != self.tree.GetRootItem() and (column == 1 or (not item.HasChildren() and column == 2)):
			self.tree.EditLabel(item, column)
			# tree labeled as edited in OnLabelEdit()
		event.Skip()
	def OnRightUp(self, event):
		"create popup menu on rightclick"
		pt = event.GetPosition()
		item, flags, column = self.tree.HitTest(pt)
		self.tree.current = item
		if not item:
			event.Skip()
			return
		if not self.tree.IsItemEnabled(item):
			event.Skip()
			return
		# populate popup menu 
		menu = wx.Menu()
		item01 = menu.Append(wx.ID_ANY, "Expand all in '%s'"%item.GetText())
		item02 = menu.Append(wx.ID_ANY, "Collapse all in '%s'"%item.GetText())
		if not item.HasChildren():
			item01.Enable(False)
			item02.Enable(False)
		menu.AppendSeparator()
		item11 = menu.Append(wx.ID_ANY, "Add a sub-key to '%s'"%item.GetText())
		if item.GetText(2):
			item11.Enable(False)
		item12 = menu.Append(wx.ID_ANY, "Add a key after '%s'"%item.GetText())
		item13 = menu.Append(wx.ID_ANY, "Add a key before '%s'"%item.GetText())
		if item == self.tree.GetRootItem():
			item12.Enable(False)
			item13.Enable(False)
		menu.AppendSeparator()
		item10 = menu.Append(wx.ID_ANY, "Delete Item '%s'"%item.GetText())
		if item == self.tree.GetRootItem():
			item10.Enable(False)

		self.tree.Bind(wx.EVT_MENU, self.OnExpand, item01)
		self.tree.Bind(wx.EVT_MENU, self.OnCollapse, item02)
		self.tree.Bind(wx.EVT_MENU, self.OnItemDelete, item10)
		self.tree.Bind(wx.EVT_MENU, self.OnSubKey, item11)
		self.tree.Bind(wx.EVT_MENU, self.OnKeyAfter, item12)
		self.tree.Bind(wx.EVT_MENU, self.OnKeyBefore, item13)
		self.tree.PopupMenu(menu)
		menu.Destroy()
		event.Skip()
	def OnExpand(self, evt):
		lich=sorted(get_desc(self.tree, self.tree.current), key=lambda t: t[0], reverse=True)
		for i,item in lich:
			if item.HasChildren():
				self.tree.Expand(item)
	def OnCollapse(self, evt):
		lich=sorted(get_desc(self.tree, self.tree.current), key=lambda t: t[0], reverse=True)[:-1]
		for i,item in lich:
			if item.HasChildren():
				self.tree.Collapse(item)
	def OnItemDelete(self, event):
		ok=self.Parent.Parent.noyes("Are You Sure You Want To Delete Item '%s'?"%self.tree.current.GetText())
		if not ok:
			return
		# update itlist and it2i
		lich=sorted(get_desc(self.tree, self.tree.current), key=lambda t: t[0], reverse=True)
		for i,ch in lich:
			del(self.tree.itlist[i])
			del(self.tree.it2i[ch])
		self.tree.it2i=dict((ch, i) for i,ch in enumerate(self.tree.itlist))
		# del in tree
		self.tree.DeleteChildren(self.tree.current)
		self.tree.Delete(self.tree.current)
		self.tree.current = None
		# update N° labels
		for i,ch in enumerate(self.tree.itlist):
			ch.SetText(0, str(i+1))
		self.tree.edited=True
		# add '*' in tab title
		nb=self.Parent
		nb.SetPageText(nb.GetPageIndex(self), "*"+self.bpath)

		event.Skip()
	def OnSubKey(self, event):
		dlg = wx.TextEntryDialog(self, "Please Enter The New Sub-Key", 'Sub-Key Naming', 'sub-key')
		if dlg.ShowModal() == wx.ID_OK:
			newname = dlg.GetValue()
			#pdb.set_trace()
			firstch, coockie=self.tree.GetFirstChild(self.tree.current)
			ins=0 if firstch is None else self.tree.it2i[firstch]
			newitem = self.tree.PrependItem(self.tree.current, newname)
			self.tree.EnsureVisible(newitem)
			# update itlist, ...
			self.tree.itlist.insert(ins, newitem)
			self.tree.it2i=dict((ch, i) for i,ch in enumerate(self.tree.itlist))
			for i,ch in enumerate(self.tree.itlist):
				ch.SetText(0, str(i+1))
			self.tree.edited=True
			# add '*' in tab title
			nb=self.Parent
			nb.SetPageText(nb.GetPageIndex(self), "*"+self.bpath)

		dlg.Destroy()
		event.Skip()
	def OnAddKey(self, event, after=1):
		#pdb.set_trace()
		dlg = wx.TextEntryDialog(self, "Please Enter The New Key Name", 'Key Naming', 'new key '+('after' if after == 1 else 'before'))
		if dlg.ShowModal() == wx.ID_OK:
			newname = dlg.GetValue()
			parent=self.tree.current.GetParent()
			next_item=self.tree.GetNextSibling(self.tree.current)
			ins=self.tree.it2i[self.tree.current] if after != 1 else (self.tree.it2i[next_item] if next_item else self.tree.it2i[self.tree.current]+len(get_desc(self.tree, self.tree.current)))
			myi=[i for i,ch in enumerate(parent.GetChildren()) if ch == self.tree.current][0]
			newitem = self.tree.InsertItem(parent, myi+after, newname)
			# update itlist & it2i & "N°"
			self.tree.itlist.insert(ins, newitem)
			self.tree.it2i=dict((ch, i) for i,ch in enumerate(self.tree.itlist))
			for i,ch in enumerate(self.tree.itlist):
				ch.SetText(0, str(i+1))
			self.tree.EnsureVisible(newitem)
			self.tree.edited=True
			# add '*' in tab title
			nb=self.Parent
			nb.SetPageText(nb.GetPageIndex(self), "*"+self.bpath)

		dlg.Destroy()
		event.Skip()
	def OnKeyBefore(self, event):
		self.OnAddKey(event, after=0)
	def OnKeyAfter(self, event):
		self.OnAddKey(event, after=1)

def AddItem(tree,content,parent):
	"""
	Recursive function, without return value, which add items to the tree
	
	
		:param tree: Tree list control
		:type tree: wx.lib.gizmos.treelistctrl.TreeListCtrl
		
		:param content: Content of the kvh file in the form of the list which contains couples of keys and values
		:type content: list[tuple] 
		
		:param parent: Initially, the root of the tree, then parents for each level recursively
		:type parent: wx.lib.agw.hypertreelist.TreeListItem
	"""
	
	if type(content) is list:
		for elem in content:
			AddItem(tree,elem,parent)
	
	if type(content) is tuple:
		key,value=content
		child=tree.AppendItem(parent,key)
		i=len(tree.itlist)
		tree.it2i[child]=i
		tree.itlist.append(child)
		if type(value) is str:
			child.SetText(0, str(i+1))
			child.SetText(2, value)
		else:
			child.SetText(0, str(i+1))
			AddItem(tree,value,child)

def get_desc(tree, item):
	"Collect tuples (index, item) of the item and all its descendants in the tree"
	if item.HasChildren():
		return [t for ch in item.GetChildren() for t in get_desc(tree, ch)]+[(tree.it2i.get(item, -1), item)]
	else:
		return [(tree.it2i[item], item)]
def text_in_item(search_text, item, in_kv, wholeWord, matchCase):
	
	"""Returns True or False if the search_text is found or not in the item
		
		:param search_text: search text
		:type search_text: str
		
		:param item: tree item ( root item for the first search )
		
		:param in_kv: have we search in the key, in the value or both? Takes value one of "k", "v", "kv".
		:type in_kv: string
		
		:param wholeWord: True if the whole word must be found
		:type wholeWord:  Bool
		
		:param matchCase: True if a case of the element must correspond to the case of the search text
		:type matchCase: Bool
	
		:return: True if text was found in the item
	"""
	if not in_kv:
		return False
	text=""
	if "k" in in_kv:
		text=item.GetText(1)
	if "v" in in_kv:
		text += "\t"+item.GetText(2)
	if not matchCase:
		text=text.lower() # search_text is lowered in caller
	if wholeWord:
		text=text.split()
	return search_text in text

def parcours_tree_by_label(tree, search_text, dir_up, in_kv, wholeWord, matchCase):
	
	"""
	Function for a search of the text.
	Returns ID of the found element, None otherwise.
		
		:param tree: Tree widget
		
		:param search_text: search text
		:type search_text: str
		
		:param dir_up: if True: search in backward direction
		
		:param in_kv: contains "k" and/or "v" for searching in keys/values
		:type in_kv: string
		
		:param wholeWord: if True: match only the whole word
		
		:param matchCase: if True: match case in the search
	
		:return: TreeId of the element of the tree widget if found
		:rtype: None  if no corresponding elements were found
	"""

	if not in_kv:
		return None
	if not matchCase:
		search_text=search_text.lower()
	item=tree.GetSelection()
	if item is None:
		item=tree.GetRootItem()
	# i=index in item list
	i=tree.it2i.get(item, -1)
	n=len(tree.itlist)
	found=False
	fwd = chain(range(i+1, n), range(0, i+1))
	bck = chain(range(i-1, -1, -1), range(n-1, i-1, -1))
	for ii in (bck if dir_up else fwd):
		treeId=tree.itlist[ii]
		if text_in_item(search_text, treeId, in_kv, wholeWord, matchCase):
			found=True
			break
	#import pdb; pdb.set_trace()
	return treeId if found else None

def PathCreation(tab):
	"""
	Show the path to the selected item in the status window
	
	:param tab:  Parent element (layer) of the tree 
	:type tab: Panel
	
	"""
	win=tab.Parent.Parent
	item=tab.tree.GetSelection()
	val=item.GetText(2)
	if not item:
		win.statusbar.SetStatusText("")
		return
	try:
		text = f"N° {tab.tree.it2i[item]+1}    ∕ "
	except:
		win.statusbar.SetStatusText("")
		return
	pieces=[]
	#import pdb; pdb.set_trace()
	while item:
		pieces.append(item.GetText(1))
		item=item.GetParent()
	text += " ∕ ".join(pieces[-2::-1])
	win.statusbar.SetStatusText(text) # key
	win.statusbar.SetStatusText(val, 1) # value

def tree2tlist(tree, li=None):
	"Translate a (sub-)tree in a list of kv-tuples for storing in kvh file"
	if li is None:
		return tree2tlist(tree, tree.GetRootItem().GetChildren())
	return [(ch.GetText(), tree2tlist(tree, ch.GetChildren())) if ch.HasChildren() else (ch.GetText(), ch.GetText(2)) for ch in li]
