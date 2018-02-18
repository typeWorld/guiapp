# -*- coding: utf-8 -*-

import wx, os, webbrowser, urllib, base64, plistlib
from threading import Thread
import threading
import wx.html2
import locales
import sys
import urllib, time
from functools import partial

from ynlib.files import ReadFromFile
from ynlib.strings import kashidas, kashidaSentence

from typeWorld.client import APIClient, AppKitNSUserDefaults

from AppKit import NSScreen, NSLocale

APPNAME = 'Type.World'
APPVERSION = '0.1.2'


if not '.app/Contents' in os.path.dirname(__file__):
	DESIGNTIME = True
else:
	DESIGNTIME = False

if not DESIGNTIME:
	plist = plistlib.readPlist(os.path.join(os.path.dirname(__file__), '..', 'Info.plist'))
	APPVERSION = plist['CFBundleShortVersionString']


class AppFrame(wx.Frame):
	def __init__(self, parent):        


		self.client = APIClient(preferences = AppKitNSUserDefaults('world.type.clientapp' if DESIGNTIME else None))
		self.justAddedPublisher = None
		self.fullyLoaded = False
		self.panelVisible = False

		# Window Size
		minSize = [1000, 700]
		if self.client.preferences.get('sizeMainWindow'):
			size = list(self.client.preferences.get('sizeMainWindow'))
			screenSize = NSScreen.mainScreen().frame().size
			if size[0] > screenSize.width:
				size[0] = screenSize.width - 50
			if size[1] > screenSize.height:
				size[1] = screenSize.height - 50
		else:
			size=[1000,700]
		size[0] = max(size[0], minSize[0])
		size[1] = max(size[1], minSize[1])
		super(AppFrame, self).__init__(parent, size = size)
		self.SetMinSize(minSize)

		self.Title = '%s %s' % (APPNAME, APPVERSION)

		self.html = wx.html2.WebView.New(self)
		self.Bind(wx.html2.EVT_WEBVIEW_NAVIGATING, self.onNavigate, self.html)
		self.Bind(wx.html2.EVT_WEBVIEW_ERROR, self.onError, self.html)
		self.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.onLoad, self.html)
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.html, 1, wx.EXPAND)
		self.SetSizer(sizer)

		### Preferences
		if not self.client.preferences.get('localizationType'):
			self.client.preferences.set('localizationType', 'systemLocale')
		if not self.client.preferences.get('customLocaleChoice'):
			self.client.preferences.set('customLocaleChoice', self.systemLocale())

		### Menus
		menuBar = wx.MenuBar()

		# Exit
		menu = wx.Menu()
		m_exit = menu.Append(wx.ID_EXIT, "%s\tCtrl-X" % (self.localize('Exit')))
		self.Bind(wx.EVT_MENU, self.onQuit, m_exit)
		m_opensubscription = menu.Append(wx.ID_OPEN, "%s\tCtrl-O" % (self.localize('Add Subscription')))
		self.Bind(wx.EVT_MENU, self.showAddPublisher, m_opensubscription)
		m_CheckForUpdates = menu.Append(wx.NewId(), "%s..." % (self.localize('Check for Updates')))
		self.Bind(wx.EVT_MENU, self.onCheckForUpdates, m_CheckForUpdates)
		m_closewindow = menu.Append(wx.ID_CLOSE, "%s\tCtrl-W" % (self.localize('Close Window')))
		self.Bind(wx.EVT_MENU, self.onClose, m_closewindow)


		menuBar.Append(menu, "&%s" % (self.localize('File')))

		# Edit
		# if 'wxMac' in wx.PlatformInfo and wx.VERSION >= (3,0):
		# 	wx.ID_COPY = wx.NewId()
		# 	wx.ID_PASTE = wx.NewId()
		editMenu = wx.Menu()
		editMenu.Append(wx.ID_SELECTALL, "%s\tCTRL+A" % (self.localize('Select All')))
		editMenu.Append(wx.ID_COPY, "%s\tCTRL+C" % (self.localize('Copy')))
		editMenu.Append(wx.ID_CUT, "%s\tCTRL+X" % (self.localize('Cut')))
		editMenu.Append(wx.ID_PASTE, "%s\tCTRL+V" % (self.localize('Paste')))
		menuBar.Append(editMenu, "&%s" % (self.localize('Edit')))

		# About
		menu = wx.Menu()
		m_about = menu.Append(wx.ID_ABOUT, "&%s %s" % (self.localize('About'), APPNAME))
		self.Bind(wx.EVT_MENU, self.onAbout, m_about)
		menuBar.Append(menu, "&%s" % (self.localize('Help')))
		# Preferences
		m_prefs = menu.Append(wx.ID_PREFERENCES, "&%s\tCtrl-," % (self.localize('Preferences')))
		self.Bind(wx.EVT_MENU, self.onPreferences, m_prefs)        

		self.SetMenuBar(menuBar)

		self.CentreOnScreen()
#		self.ShowWithEffect()
		self.Show()


		self.Bind(wx.EVT_SIZE, self.onResize, self)
		self.Bind(wx.EVT_ACTIVATE, self.onActivate, self)


		# self.Bind(wx.EVT_ACTIVATE, self.onActivate)

		# if wx.Platform == '__WXMAC__':
		# 	w = self.nsapp.mainWindow()

		# 	from AppKit import NSFullSizeContentViewWindowMask, NSWindowTitleHidden, NSBorderlessWindowMask, NSResizableWindowMask, NSTitledWindowMask, NSFullSizeContentViewWindowMask, NSWindowStyleMaskFullSizeContentView

#			w.setStyleMask_(NSFullSizeContentViewWindowMask)

			# 0: NSWindowStyleMaskTitled
			# 1: NSWindowStyleMaskClosable
			# 2: NSWindowStyleMaskMiniaturizable
			# 3: NSWindowStyleMaskResizable
			# 8: NSWindowStyleMaskTexturedBackground
			# 12: NSWindowStyleMaskUnifiedTitleAndToolbar
			# 14: NSWindowStyleMaskFullScreen
			# 15: NSWindowStyleMaskFullSizeContentView
			# 4: NSWindowStyleMaskUtilityWindow
			# 6: NSWindowStyleMaskDocModalWindow
			# 7: NSWindowStyleMaskNonactivatingPanel
			# 13: NSWindowStyleMaskHUDWindow


			# w.setStyleMask_(1 << 0 | 1 << 1 | 1 << 2 | 1 << 3)
			# w.setTitlebarAppearsTransparent_(True)
			# w.setTitleVisibility_(NSWindowTitleHidden)


#			w.setTitle_(' ')


#			w.setStyleMask_(NSBorderlessWindowMask)
			#w.setTitlebarAppearsTransparent_(1)
#			w.setIsMovable_(True)
			#w.setTitleVisibility_(0)
			#w.setMovableByWindowBackground_(True)
			# js = '$("#sidebar").css("padding-top", "18px");'
			# self.html.RunScript(js)


		if not DESIGNTIME:
			# Your Qt QApplication instance
			QT_APP = self
			# URL to Appcast.xml, eg. https://yourserver.com/Appcast.xml
			APPCAST_URL = 'https://type.world/downloads/guiapp/appcast.xml'
			# Path to Sparkle's "Sparkle.framework" inside your app bundle

			if '.app' in os.path.dirname(__file__):
				SPARKLE_PATH = os.path.join(os.path.dirname(__file__), '..', 'Frameworks', 'Sparkle.framework')
			else:
				SPARKLE_PATH = '/Users/yanone/Code/Sparkle/Sparkle.framework'

			from objc import pathForFramework, loadBundle
			sparkle_path = pathForFramework(SPARKLE_PATH)
			self.objc_namespace = dict()
			loadBundle('Sparkle', self.objc_namespace, bundle_path=sparkle_path)
			def about_to_quit():
				# See https://github.com/sparkle-project/Sparkle/issues/839
				self.objc_namespace['NSApplication'].sharedApplication().terminate_(None)

	#		QT_APP.aboutToQuit.connect(about_to_quit)
			self.sparkle = self.objc_namespace['SUUpdater'].sharedUpdater()
			self.sparkle.setAutomaticallyChecksForUpdates_(True)
	#		self.sparkle.setAutomaticallyDownloadsUpdates_(True)
			NSURL = self.objc_namespace['NSURL']
			self.sparkle.setFeedURL_(NSURL.URLWithString_(APPCAST_URL))
			self.sparkle.checkForUpdatesInBackground()




	def publishersNames(self):
		# Build list, sort it
		publishers = []
		for i, key in enumerate(self.client.endpoints.keys()):
			endpoint = self.client.endpoints[key]
			name, language = endpoint.latestVersion().name.getTextAndLocale(locale = self.locale())
			publishers.append((i, name, language))
		return publishers


	def onCheckForUpdates(self, event):
		self.sparkle.checkForUpdates_(None)

	def onActivate(self, event):
		self.errorMessage('Activated: %s' % sys.argv)

	def onClose(self, event):
		if self.panelVisible:
			self.html.RunScript('hidePanel();')
		else:
			self.Destroy()

	def onQuit(self, event):
		self.Destroy()

	def onActivate(self, event):

		size = list(self.GetSize())

		resize = False
		screenSize = NSScreen.mainScreen().frame().size
		if size[0] > screenSize.width:
			size[0] = screenSize.width - 50
			resize = True
		if size[1] > screenSize.height:
			size[1] = screenSize.height - 50
			resize = True

		if resize:
			self.SetSize(size)


	def onResize(self, event):
		# Make title bar transparent
		# https://developer.apple.com/documentation/appkit/nswindowstylemask?language=objc
#		if False:
		# if wx.Platform == '__WXMAC__':
		# 	w = self.nsapp.mainWindow()
			# w.setStyleMask_(1 << 0 | 1 << 1 | 1 << 2 | 1 << 3 | 1 << 15)
			# w.setTitlebarAppearsTransparent_(1)
#			w.setTitle_(' ')
#		print w.title(), w.titlebarAppearsTransparent(), w.styleMask()
		self.client.preferences.set('sizeMainWindow', (self.GetSize()[0], self.GetSize()[1]))
		event.Skip()
#		print event.Veto()
#		return


	def onAbout(self, event):
		self.html.RunScript('showAbout();')

	def onPreferences(self, event):


		html = []

		html.append('<h1>App Localization</h1>')
		html.append('<div>')
		html.append('<span><input id="systemLocale" value="systemLocale" type="radio" name="localizationType" %s><label for="systemLocale">Use System Locale (%s)</label></span>' % ('checked' if self.client.preferences.get('localizationType') == 'systemLocale' else '', self.systemLocale()))
		html.append('<script>$("#preferences #systemLocale").click(function() {setPreference("localizationType", "systemLocale");});</script>')
		html.append('<br />')
		html.append('<span><input id="customLocale" value="customLocale" type="radio" name="localizationType" %s><label for="customLocale">Use Custom Locale (choose below). Requires restart to take full effect.</label></span>' % ('checked' if self.client.preferences.get('localizationType') == 'customLocale' else ''))
		html.append('<script>$("#preferences #customLocale").click(function() {setPreference("localizationType", "customLocale");});</script>')
		html.append('<br />')
		html.append('<select id="customLocaleChoice" style="">')
		for code, name in locales.locales:
			html.append('<option value="%s" %s>%s</option>' % (code, 'selected' if code == self.client.preferences.get('customLocaleChoice') else '', name))
		html.append('</select>')
		html.append('<script>$("#preferences #customLocaleChoice").click(function() {setPreference("customLocaleChoice", $("#preferences #customLocaleChoice").val());});</script>')
		html.append('</div>')




		# Print HTML
		html = ''.join(html)
		html = html.replace('"', '\'')
		html = html.replace('\n', '')
		html = self.localizeString(html)
#		print html
		js = '$("#preferences .inner").html("' + html + '");'
		self.html.RunScript(js)

		self.html.RunScript('showPreferences();')


	def onNavigate(self, evt):
		uri = evt.GetURL() # you may need to deal with unicode here
		if uri.startswith('x-python://'):
			code = uri.split("x-python://")[1]
			code = urllib.unquote(code).decode('utf8')
			code = code.replace('http//', 'http://')
			code = code.replace('https//', 'https://')
			code = code.replace('____', '\'')
			exec(code)
			evt.Veto()
		elif uri.startswith('http://') or uri.startswith('https://'):
			
			webbrowser.open_new_tab('https://type.world/linkRedirect/?url=' + urllib.quote(uri))
			evt.Veto()
		# else:
		# 	code = uri
		# 	code = urllib.unquote(code).decode('utf8')
		# 	print code
		# 	exec(code)
		# 	evt.Veto()

	def onError(self, evt):
		print evt.GetString()
#		raise Exception(evt.GetString())


	def showAddPublisher(self, evt):
		self.html.RunScript('showAddPublisher();')
		

	def addPublisher(self, url):

		url = url.replace('typeworldjson//', 'typeworldjson://')
		url = url.replace('http//', 'http://')
		url = url.replace('https//', 'https://')


		# fremove URI
		url = url.replace('typeworldjson://', '')


		print 'addPublisher', url

		success, message, publisher = self.client.addSubscription(url)

		if success:

			b64ID = self.b64encode(publisher.canonicalURL)

			self.setSideBarHTML()
			self.setPublisherHTML(b64ID)
			self.html.RunScript("hidePanel();")

		else:
			self.errorMessage(message)


	def removePublisher(self, evt, b64ID):

		publisher = self.client.publisher(self.b64decode(b64ID))
		publisher.delete()
		self.client.preferences.set('currentPublisher', None)
		self.setSideBarHTML()
		self.html.RunScript("hideMain();")

	def removeSubscription(self, evt, b64ID):

		for publisher in self.client.publishers():
			for subscription in publisher.subscriptions():
				if subscription.url == self.b64decode(b64ID):
					subscription.delete()

		self.html.RunScript("hideMain();")
		self.setSideBarHTML()

	def publisherPreferences(self, i):
		print 'publisherPreferences', i

	def removeFont(self, b64publisherURL, b64subscriptionURL, b64fontID):

		publisherURL = self.b64decode(b64publisherURL)
		subscriptionURL = self.b64decode(b64subscriptionURL)
		fontID = self.b64decode(b64fontID)

		publisher = self.client.publisher(publisherURL)
		subscription = publisher.subscription(subscriptionURL)
		api = subscription.latestVersion()

		success, message = subscription.removeFont(fontID)

		if success:

			self.setPublisherBadge(self.b64encode(subscription.parent.canonicalURL), subscription.parent.amountInstalledFonts())
			self.setPublisherHTML(self.b64encode(subscription.parent.canonicalURL))

		else:

			if type(message) in (str, unicode):
				self.errorMessage(message)
			else:
				self.errorMessage('Server: %s' % message.getText(self.locale()))

			self.html.RunScript("$('#%s .statusButton').hide();" % b64fontID)
			self.html.RunScript("$('#%s .removeButton').show();" % b64fontID)

	def removeAllFonts(self, b64publisherURL, b64subscriptionURL, b64familyID):

		print b64publisherURL

		publisherURL = self.b64decode(b64publisherURL)
		subscriptionURL = self.b64decode(b64subscriptionURL)
		familyID = self.b64decode(b64familyID)

		publisher = self.client.publisher(publisherURL)
		subscription = publisher.subscription(subscriptionURL)
		api = subscription.latestVersion()

		for foundry in api.response.getCommand().foundries: 
			for family in foundry.families:
				if family.uniqueID == familyID:
					for font in family.fonts:

						# Check if font is already installed
						if subscription.installedFontVersion(font.uniqueID):
							self.removeFont(b64publisherURL, b64subscriptionURL, self.b64encode(font.uniqueID))

					break
		self.setPublisherBadge(self.b64encode(publisherURL), publisher.amountInstalledFonts())
		self.setSubscriptionsHTML(self.b64encode(publisherURL))


	def installAllFonts(self, b64publisherURL, b64subscriptionURL, b64familyID):

		print b64publisherURL

		publisherURL = self.b64decode(b64publisherURL)
		subscriptionURL = self.b64decode(b64subscriptionURL)
		familyID = self.b64decode(b64familyID)


		publisher = self.client.publisher(publisherURL)
		subscription = publisher.subscription(subscriptionURL)
		api = subscription.latestVersion()

		for foundry in api.response.getCommand().foundries: 
			for family in foundry.families:

				if family.uniqueID.encode('utf-8') == familyID:
					for font in family.fonts:

						# Check if font is already installed
						if not subscription.installedFontVersion(font.uniqueID):
							self.installFont(b64publisherURL, b64subscriptionURL, self.b64encode(font.uniqueID), font.getSortedVersions()[-1].number)

					break
		self.setPublisherBadge(self.b64encode(publisherURL), publisher.amountInstalledFonts())
		self.setSubscriptionsHTML(self.b64encode(publisherURL))



	def installFont(self, b64publisherURL, b64subscriptionURL, b64fontID, version):


		publisherURL = self.b64decode(b64publisherURL)
		subscriptionURL = self.b64decode(b64subscriptionURL)
		fontID = self.b64decode(b64fontID)

		# self.html.RunScript("$('#%s .installButton').hide();" % b64fontID)
		# self.html.RunScript("$('#%s .status').show();" % b64fontID)

		print 'installFont', publisherURL, subscriptionURL, fontID

		publisher = self.client.publisher(publisherURL)
		subscription = publisher.subscription(subscriptionURL)
		api = subscription.latestVersion()
		b64ID = self.b64encode(publisherURL)

		# Check if font is already installed
		if subscription.installedFontVersion(fontID):
			success, message = subscription.removeFont(fontID)

			if not success:
				self.errorMessage(message)

			else:
				success, message = subscription.installFont(fontID, version)

		else:
			success, message = subscription.installFont(fontID, version)

		if success:

			self.setPublisherBadge(self.b64encode(subscription.parent.canonicalURL), subscription.parent.amountInstalledFonts())
			self.setPublisherHTML(self.b64encode(subscription.parent.canonicalURL))
			
		else:

			if type(message) in (str, unicode):
				
				if message == 'seatAllowanceReached':
					self.errorMessage('seatAllowanceReached')

				else:
					self.errorMessage(message)
			else:
				self.errorMessage('Server: %s' % message.getText(self.locale()))

			self.html.RunScript("$('#%s .statusButton').hide();" % b64fontID)
			self.html.RunScript("$('#%s .installButton').show();" % b64fontID)



	def onContextMenu(self, x, y, target, b64ID):
		print x, y, target, b64ID#, self.b64decode(ID)


		if 'contextmenu publisher' in target:


			menu = wx.Menu()

			item = wx.MenuItem(menu, wx.NewId(), self.localizeString('#(Reload)'))
			menu.Append(item)
			menu.Bind(wx.EVT_MENU, partial(self.reloadPublisherJavaScript, b64ID = b64ID), item)

			item = wx.MenuItem(menu, wx.NewId(), self.localizeString('#(Remove)'))
			menu.Append(item)
			menu.Bind(wx.EVT_MENU, partial(self.removePublisher, b64ID = b64ID), item)

			self.PopupMenu(menu, wx.Point(int(x), int(y)))
			menu.Destroy()


		elif 'contextmenu subscription' in target:
			menu = wx.Menu()

			item = wx.MenuItem(menu, wx.NewId(), self.localizeString('#(Reload)'))
			menu.Append(item)
			menu.Bind(wx.EVT_MENU, partial(self.reloadSubscriptionJavaScript, b64ID = b64ID), item)

			item = wx.MenuItem(menu, wx.NewId(), self.localizeString('#(Remove)'))
			menu.Append(item)
			menu.Bind(wx.EVT_MENU, partial(self.removeSubscription, b64ID = b64ID), item)

			self.PopupMenu(menu, wx.Point(int(x), int(y)))
			menu.Destroy()

		elif 'contextmenu font' in target:
			menu = wx.Menu()

			fontID = self.b64decode(b64ID)

			for publisher in self.client.publishers():
				for subscription in publisher.subscriptions():
					for foundry in subscription.latestVersion().response.getCommand().foundries:
						for family in foundry.families:
							for font in family.fonts:
								if font.uniqueID == fontID:

									# create a submenu
									subMenu = wx.Menu()
									menu.AppendMenu(wx.NewId(), self.localizeString('#(Install Version)'), subMenu)

									for version in font.getSortedVersions():

										if subscription.installedFontVersion(fontID) == version.number:
											installVersionsSubmenu = subMenu.Append(wx.NewId(), str(version.number), "", wx.ITEM_RADIO)
										else:
											installVersionsSubmenu = subMenu.Append(wx.NewId(), str(version.number))

										subMenu.Bind(wx.EVT_MENU, partial(self.installFontFromMenu, subscription = subscription, fontID = fontID, version = version.number), installVersionsSubmenu)

										# item = wx.MenuItem(subMenu, wx.NewId(), version.number)
										# subMenu.Append(item)
										#menu.Bind(wx.EVT_MENU, partial(self.reloadSubscriptionJavaScript, b64ID = b64ID), item)


									self.PopupMenu(menu, wx.Point(int(x), int(y)))
									menu.Destroy()

									break

	def installFontFromMenu(self, event, subscription, fontID, version):

		self.html.RunScript('installFont("%s", "%s", "%s", "%s");' % (self.b64encode(subscription.parent.canonicalURL), self.b64encode(subscription.url), self.b64encode(fontID), version))

	def installFontVersion(self, event, subscription, fontID, version):




		if subscription.installedFontVersion(fontID) != version:

			if subscription.installedFontVersion(fontID):
				subscription.removeFont(fontID)

			success, message = subscription.installFont(fontID, version)

			if not success:
				if type(message) in (str, unicode):
					
					if message == 'seatAllowanceReached':
						self.errorMessage('seatAllowanceReached')

					else:
						self.errorMessage(message)
				else:
					self.errorMessage('Server: %s' % message.getText(self.locale()))

			self.setPublisherHTML(self.b64encode(subscription.parent.canonicalURL))
			self.setPublisherBadge(self.b64encode(subscription.parent.canonicalURL), subscription.parent.amountInstalledFonts())


	def reloadSubscriptionJavaScript(self, evt, b64ID):
		print 'reloadSubscriptionJavaScript', b64ID
		self.html.RunScript('reloadSubscription("%s");' % (b64ID))

	def reloadPublisherJavaScript(self, evt, b64ID):
		print 'reloadPublisherJavaScript', b64ID
		self.html.RunScript('reloadPublisher("%s");' % (b64ID))

	def reloadPublisher(self, evt, b64ID):

		# processThread = threading.Thread(target=self.reloadPublisherShowAnimation, args=(evt, b64ID));
		# processThread.start()


		print 'reloadPublisher', b64ID


		ID = base64.b64decode(b64ID.replace('-', '='))

		success, message = self.client.publisher(ID).update()

		if success:

			self.setSubscriptionsHTML(b64ID)
			self.setPublisherHTML(b64ID)
			
		else:

			if type(message) in (str, unicode):
				
				self.errorMessage(message)
			else:
				self.errorMessage('Server: %s' % message.getText(self.locale()))


		self.html.RunScript('finishReloadPublisher("%s");' % (b64ID))


		print 'Done'

	def reloadSubscription(self, evt, b64ID):

		# processThread = threading.Thread(target=self.reloadPublisherShowAnimation, args=(evt, b64ID));
		# processThread.start()


		print 'reloadSubscription', b64ID

		success = False
		message = 'Couldnt find subscription.'

		ID = self.b64decode(b64ID)

		for publisher in self.client.publishers():
			if publisher.subscription(ID):
				success, message = publisher.subscription(ID).update()
				break



		if success:

			self.setSubscriptionsHTML(self.b64encode(publisher.canonicalURL))
			self.setPublisherHTML(self.b64encode(publisher.canonicalURL))
			
		else:

			if type(message) in (str, unicode):
				
				self.errorMessage(message)
			else:
				self.errorMessage('Server: %s' % message.getText(self.locale()))


		self.html.RunScript('finishReloadSubscription("%s");' % (b64ID))


		print 'Done'

	def errorMessage(self, message):
		dlg = wx.MessageDialog(self, message, '', wx.ICON_ERROR)
		result = dlg.ShowModal()
		dlg.Destroy()


	def fontHTML(self, font):

		subscription = font.parent.parent.parent

		html = []
		html.append('<div class="clear">')
		html.append('<div class="left" style="width: 50%;">')
		html.append(font.name.getText(self.locale()))
		if font.free:
			html.append('<span class="label free">free</span>')
		if font.beta:
			html.append('<span class="label beta">beta</span>')
		if font.variableFont:
			html.append('<span class="label var">OTVar</span>')
		html.append('</div>') # .left
		html.append('<div class="left">')
		installedVersion = subscription.installedFontVersion(font.uniqueID)
		if installedVersion:
			html.append('#(Installed): <span class="label installedVersion %s">%s</a>' % ('latestVersion' if installedVersion == font.getSortedVersions()[-1].number else 'olderVersion', installedVersion))
		else:
			html.append('<span class="notInstalled">#(Not Installed)</span>')
		html.append('</div>') # .left
		html.append('<div class="installButton right" style="display: %s;">' % ('none' if installedVersion else 'block'))
		html.append('<a class="install" publisherid="%s" subscriptionid="%s" fontid="%s" version="%s">' % (self.b64encode(subscription.parent.canonicalURL), self.b64encode(subscription.url), self.b64encode(font.uniqueID), font.getSortedVersions()[-1].number))
#		html.append('''<a href="JavaScript:installFont('%s', '%s', '%s', '%s')">''' % (self.b64encode(api.canonicalURL), self.b64encode(repo.url), self.b64encode(font.uniqueID), font.getSortedVersions()[-1].number))
		html.append('#(Install)')
		html.append('</a>')
		html.append('</div>') # .right
		html.append('<div class="right removeButton" style="display: %s;">' % ('block' if installedVersion else 'none'))
		html.append('<a class="remove" publisherid="%s" subscriptionid="%s" fontid="%s">' % (self.b64encode(subscription.parent.canonicalURL), self.b64encode(subscription.url), self.b64encode(font.uniqueID)))
		html.append('#(Remove)')
		html.append('</a>')
		html.append('</div>') # .right
		html.append('<div class="statusButton right">')
		html.append('<a class="status">...</a>')
		html.append('</div>') # .right
		html.append('</div>') # .clear

		html.append('''<script>
$( document ).ready(function() {

	$(".font .installButton").click(function() {
		fontLink = $(this).closest('.font').find('a.install');
		installFont(fontLink.attr('publisherid'), fontLink.attr('subscriptionid'), fontLink.attr('fontid'), fontLink.attr('version'));
	}); 
 
	$(".font .removeButton").click(function() {
		fontLink = $(this).closest('.font').find('a.remove');
		removeFont(fontLink.attr('publisherid'), fontLink.attr('subscriptionid'), fontLink.attr('fontid'));
	}); 

});
</script>''')

		# Print HTML
		html = ''.join(html)
		html = html.replace('"', '\'')
		html = html.replace('\n', '')
		html = self.localizeString(html)

		return html


	def setActiveSubscription(self, publisherB64ID, subscriptionB64ID):

		publisherID = self.b64decode(publisherB64ID)
		repositoryID = self.b64decode(subscriptionB64ID)

		publisher = self.client.publisher(publisherID)
		publisher.set('currentSubscription', repositoryID)
		self.setPublisherHTML(publisherB64ID)


	def getSubscriptionsHTML(self, b64ID):
		ID = self.b64decode(b64ID)

		print 'setSubscriptionsHTML', ID

		html = []
		repos = []
		publisher = self.client.publisher(ID)
		for subscription in publisher.subscriptions():

			amountInstalledFonts = subscription.amountInstalledFonts()
			selected = subscription == publisher.currentSubscription()

			string = []
			string.append('<a href="x-python://self.setActiveSubscription(____%s____, ____%s____)">' % (b64ID, self.b64encode(subscription.url)))
			string.append('<div class="contextmenu subscription publisher clear %s" lang="%s" dir="%s" id="%s">' % ('selected' if selected else '', 'en', 'ltr', self.b64encode(subscription.url)))
			string.append('<div class="name">')
			string.append(subscription.latestVersion().response.getCommand().name.getText(self.locale()) or '#(Undefined)')
			string.append('</div>')

			string.append('<div class="badges">')
			string.append('<div class="badge installed" style="display: %s;">' % ('block' if amountInstalledFonts else 'none'))
			string.append('%s' % amountInstalledFonts)
			string.append('</div>')
			string.append('</div>')
			string.append('</div>')
			string.append('</a>')

			html.append(''.join(string))


			html.append('''<script>

$( document ).ready(function() {

	$("#subscriptions .publisher").hover(function() {
		$( this ).addClass( "hover" );
	  }, function() {
		$( this ).removeClass( "hover" );
	  }
	);


});


</script>''')


		html.append(', '.join(repos))


		# Print HTML
		html = ''.join(html)
		html = html.replace('"', '\'')
		html = html.replace('\n', '')
		html = self.localizeString(html)

		return html

	def setSubscriptionsHTML(self, b64ID):

		html = self.getSubscriptionsHTML(b64ID)

		js = '$("#subscriptions #content").html("' + html + '");'
		self.html.RunScript(js)


	def setPublisherHTML(self, b64ID):

#		print b64ID

		ID = self.b64decode(b64ID)

		if self.client.preferences:
			self.client.preferences.set('currentPublisher', ID)

		html = []

		publisher = self.client.publisher(ID)
		subscription = publisher.currentSubscription()
		api = subscription.latestVersion()
		print api

		name, locale = api.name.getTextAndLocale(locale = self.locale())


		html.append('<div class="publisher" id="%s">' % (b64ID))

		for foundry in subscription.foundries():


			html.append('<div class="foundry">')
			html.append('<div class="head" style="height: %spx; background-color: %s;">' % (110 if foundry.logo else 70, '#' + foundry.backgroundColor if foundry.backgroundColor else 'none'))

			if foundry.logo:
				success, logo = self.client.resourceByURL(foundry.logo, b64 = True)
				if success:
					html.append('<div class="logo">')
					html.append('<img src="data:image/svg+xml;base64,%s" style="width: 100px; height: 100px;" />' % logo)
					html.append('</div>') # publisher

			html.append('<div class="names centerOuter"><div class="centerInner">')
			html.append('<div class="name">%s</div>' % (foundry.name.getText(self.locale())))
			if foundry.website:
				html.append('<div class="website"><a href="%s">%s</a></div>' % (foundry.website, foundry.website))

			html.append('</div></div>') # .centerInner .centerOuter



			html.append('</div>') # .head


			html.append('<div class="families">')

			for family in foundry.families():
				html.append('<div class="contextmenu family" id="%s">' % self.b64encode(family.uniqueID))

				html.append('<div class="title">')
				html.append('<div class="clear">')
				html.append('<div class="left name">')
				html.append(family.name.getText(self.locale()))
				html.append('</div>') # .left.name
				html.append('<div class="right">')
				html.append('<a class="removeAllFonts" publisherid="%s" subscriptionid="%s" familyid="%s">' % (self.b64encode(ID), self.b64encode(subscription.url), self.b64encode(family.uniqueID)))
				html.append('#(Remove All)')
				html.append('</a>')
				html.append('</div>') # .right
				html.append('<div class="right">')
				html.append('<a class="installAllFonts" publisherid="%s" subscriptionid="%s" familyid="%s">' % (self.b64encode(ID), self.b64encode(subscription.url), self.b64encode(family.uniqueID)))
				html.append('#(Install All)')
				html.append('</a>')
				html.append('</div>') # .right
				html.append('</div>') # .clear
				html.append('</div>') # .title

				for font in family.fonts():
					html.append('<div class="contextmenu font" id="%s">' % self.b64encode(font.uniqueID))

					html.append(self.fontHTML(font))

					html.append('</div>') # .font

				html.append('</div>') # .family

				html.append('''<script> 	



	$(".family a.removeAllFonts").click(function() {
		removeAllFonts($(this).attr('publisherid'), $(this).attr('subscriptionid'), $(this).attr('familyid')); 
	});

	$(".family a.installAllFonts").click(function() {
		installAllFonts($(this).attr('publisherid'), $(this).attr('subscriptionid'), $(this).attr('familyid')); 
	});



</script>''')

			html.append('</div>') # .families




			html.append('</div>') # .foundry






		html.append('</div>') # .publisher





		html.append('''<script>


	$("#main .family .title").hover(function() {
		$( this ).closest(".family").addClass( "hover" );
		$( this ).closest(".family").children(".font").addClass( "hover" );
	  }, function() {
		$( this ).closest(".family").removeClass( "hover" );
		$( this ).closest(".family").children(".font").removeClass( "hover" );
	  }
	);

	$("#main .font").hover(function() {
		$( this ).addClass( "hover" );
	  }, function() {
		$( this ).removeClass( "hover" );
	  }
	);

	$("#main .publisher a.reloadPublisherButton").click(function() {
		$("#sidebar #%s .badges").hide();
		$("#sidebar #%s .reloadAnimation").show();
		python("self.reloadPublisher(None, ____%s____)");
	});



</script>''' % (b64ID, b64ID, b64ID))


		# Unused:
		'''
	$("#main .font, #main .family .title").click(function() {
		$("#main .font, #main .family .title").removeClass('selected');
		$( this ).addClass( "selected" );
	  });
'''










		# Print HTML
		html = ''.join(html)
		html = html.replace('"', '\'')
		html = html.replace('\n', '')
		html = self.localizeString(html)
#		print html
		js = '$("#main").html("' + html + '");'
		self.html.RunScript(js)

		# Set Sidebar Focus
		self.html.RunScript("$('#sidebar .publisher').removeClass('selected');")
		self.html.RunScript("$('#sidebar #%s').addClass('selected');" % b64ID)
		self.setSubscriptionsHTML(b64ID)
		self.html.RunScript("showMain();")


	def b64encode(self, string):
		return base64.b64encode(string.encode('utf-8')).replace('=', '-')

	def b64decode(self, string):
		return base64.b64decode(string.replace('-', '=')) # .decode('utf-8')

	def setSideBarHTML(self):
		# Set publishers

		html = []


		# Sort
		# pass

		# Create HTML
		for publisher in self.client.publishers():

			b64ID = base64.b64encode(publisher.canonicalURL).replace('=', '-')

			name, language = publisher.subscriptions()[0].latestVersion().name.getTextAndLocale(locale = self.locale())

			if language in (u'ar', u'he'):
				direction = 'rtl'
				if language in (u'ar'):
					name = kashidaSentence(name, 20)
			else:
				direction = 'ltr'

			installedFonts = publisher.amountInstalledFonts()
			html.append(u'''
<a href="x-python://self.setPublisherHTML(____%s____)">
	<div id="%s" class="contextmenu publisher clear" lang="%s" dir="%s">
		<div class="name">
		%s
		</div>
		<div class="reloadAnimation" style="display: none;">
		↺
		</div>
		<div class="badges">
			<div class="badge installed" style="display: %s;">
			%s
			</div>
		</div>
	</div>
</a>''' % (b64ID, b64ID, language, direction, name, 'block' if installedFonts else 'none', installedFonts or ''))


		html.append('''<script>

$( document ).ready(function() {

	$("#sidebar .publisher").hover(function() {
		$( this ).addClass( "hover" );
	  }, function() {
		$( this ).removeClass( "hover" );
	  }
	);


});



</script>''')


		# Print HTML
		html = ''.join(html)
		html = html.replace('"', '\'')
		html = html.replace('\n', '')
#		print html
		js = '$("#publishers").html("' + html + '");'
		self.html.RunScript(js)




	def onLoad(self, event):

		self.setSideBarHTML()

		# Open drawer for newly added publisher
		if self.justAddedPublisher:
			self.addPublisher(self.justAddedPublisher)
			self.justAddedPublisher = None

		self.fullyLoaded = True

		if self.client.preferences.get('currentPublisher'):
			self.html.RunScript('$("#welcome").hide();')
			self.setPublisherHTML(self.b64encode(self.client.preferences.get('currentPublisher')))


	def log(self, message):

		from AppKit import NSLog
		NSLog('Type.World App: %s' % message)

	def setBadgeLabel(self, label):
		u'''\
		Set dock icon badge
		'''
		label = str(label)
		self._dockTile.display()
		self._dockTile.setBadgeLabel_(label)

	def localize(self, key, html = False):
		string = locales.localize(key, self.locale())
		if html:
			string = string.replace('\n', '<br />')
		return string

	def localizeString(self, string, html = False):
		string = locales.localizeString(string, languages = self.locale(), html = html)
		return string

	def replaceHTML(self, html):
		html = html.replace('##htmlroot##', os.path.join(os.path.dirname(__file__), 'html'))
		return html

	def systemLocale(self):
		return str(NSLocale.autoupdatingCurrentLocale().localeIdentifier().split('_')[0])

	def locale(self):
		u'''\
		Reads user locale from OS
		'''

		if not hasattr(self, '_locale'):

			if self.client.preferences.get('localizationType') == 'systemLocale':
				self._locale = [self.systemLocale(), 'en']
			elif self.client.preferences.get('localizationType') == 'customLocale':
				self._locale = [self.client.preferences.get('customLocaleChoice'), 'en']
			else:
				self._locale = [self.systemLocale(), 'en']
		return self._locale

	def setPublisherBadge(self, b64ID, string):
		if string:
			self.html.RunScript('$("#sidebar #%s .badge.installed").show(); $("#sidebar #%s .badge.installed").html("%s");' % (b64ID, b64ID, string))
		else:
			self.html.RunScript('$("#sidebar #%s .badge.installed").hide();' % b64ID)
		# if string:
		# 	self.html.RunScript('$("#sidebar #%s .badge.installed").fadeOut(200, function() { $("#sidebar #%s .badge.installed").html("%s"); $("#sidebar #%s .badge.installed").fadeIn(200); });' % (b64ID, b64ID, string, b64ID))
		# else:
		# 	self.html.RunScript('$("#sidebar #%s .badge.installed").fadeOut(200);' % b64ID)

	def debug(self, string):
		print string



class MyApp(wx.App):
	def MacOpenURL(self, url):
		if url.startswith('typeworldjson://'):
			url = url.replace('typeworldjson://', '')
			
			if self.frame.fullyLoaded:
				self.frame.addPublisher(url)
			else:
				self.frame.justAddedPublisher = url

			self.frame.Show()


			# from AppKit import NSApplicationActivateAllWindows
			# self.frame.nsapp.activateWithOptions_(NSApplicationActivateAllWindows)

	def OnInit(self):
		frame = AppFrame(None)
		self.frame = frame
		
		from AppKit import NSApp
		self.frame.nsapp = NSApp()
		self.frame._dockTile = self.frame.nsapp.dockTile()


		html = ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'index.html'))

		html = html.replace('##jquery##', str(ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'js', 'jquery-1.12.4.js'))))
		html = html.replace('##jqueryui##', str(ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'js', 'jquery-ui.js'))))
		html = html.replace('##js.js##', str(ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'js', 'js.js'))))
		html = html.replace('##cubic.js##', str(ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'js', 'splitcubicatt.js'))))
		html = html.replace('##atom.js##', str(ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'js', 'atom.js'))))
		html = html.replace('##css##', str(ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'css', 'index.css'))))
		html = html.replace('##jqueryuicss##', str(ReadFromFile(os.path.join(os.path.dirname(__file__), 'html', 'main', 'css', 'jquery-ui.css'))))

		html = frame.localizeString(html, html = True)
		html = frame.replaceHTML(html)

		# import cgi
		# html = cgi.escape(html)
	#	html = html.decode('windows-1252')

		frame.html.SetPage(html, os.path.join(os.path.dirname(__file__), 'html', 'main'))
		frame.Show()

		return True


if __name__ == '__main__':
	app = MyApp()


	app.MainLoop()


