# -*- coding: utf-8 -*-

from Plugins.Extensions.CSFD.CSFDSettings2 import config
#
#pokud chcete změnit vzhled CSFD přímo ve skinu, tak musíte nastavit položku "Povolit změnit CSFD ve skinu" na Ano přímo v pluginu v Menu/Nastavení
#to samé platí i pro "Povolit změnit OLED displej ve skinu"
#jména jednotlivých obrazovek, které lze použít ve skinu, jsou uvedena v závorkách [ ]
#

#***************************************************************************************************************************************************************************************
#HLAVNI INFORMACE O SKINU
#jmeno skinu
CSFD_SKIN_NAME = "Default"
#autor skinu
CSFD_SKIN_AUTHOR = "petrkl12"
#kontakt na autora skinu
CSFD_SKIN_AUTHOR_CONTACT = "petrkl12@tvplugins.cz"
#jak vypada nahled na tento skin
CSFD_SKIN_PREVIEW = "/usr/lib/enigma2/python/Plugins/Extensions/CSFD/skins/Default.jpg"
#popis skinu - co vsechno meni v nastavenich, pro jaky typ boxu je urceny apod.
CSFD_SKIN_DESCRIPTION = "Default skin pro plugin CSFD pro všechny typy boxů"
#***************************************************************************************************************************************************************************************
#Tato procedura SKIN_DefaultSetup se vola JEN pri prvnim nastaveni tohoto skinu a take pri volbe Obnovit nastaveni skinu
#Zde mate moznost nastavit/prenastavit ruzne volby dostupne v Nastavenich a to jak graficke tak i treba zmenit ovladani, ktere potrebujete jednorazove zmenit
#Uzivatele si pak ale muzou jednotlive volby zapnout nebo vypnout dle vlastniho uvazeni
def SKIN_DefaultSetup():

	config.misc.CSFD.Skinxml.setValue(False)
	config.misc.CSFD.SkinOLEDxml.setValue(True)
	config.misc.CSFD.Resolution.setValue("0")
	config.misc.CSFD.Design.setValue("0")
	config.misc.CSFD.FontHeight.setValue("22")
	config.misc.CSFD.FontHeightFullHD.setValue("33")
	config.misc.CSFD.PosterBasicSlide.setValue(True)
	config.misc.CSFD.PosterBasicSlideInclGallery.setValue(True)
	config.misc.CSFD.GallerySlide.setValue(True)
	config.misc.CSFD.PosterSlide.setValue(True)
	config.misc.CSFD.TipsShow.setValue(True)
	config.misc.CSFD.ShowLine.setValue(True)

	return

#***************************************************************************************************************************************************************************************
#Tato procedura SKIN_Setup se vola vzdy pri spusteni pluginu a take pri volbe Obnovit nastaveni skinu
#Zde mate moznost nastavit/prenastavit ruzne volby dostupne v Nastavenich a to jak graficke tak i treba zmenit ovladani
#Uzivatele si NEMUZOU tyto volby zmenit resp. vzdy po novem spusteni pluginu se tyto zmeny vrati zpet
def SKIN_Setup():


	return

#***************************************************************************************************************************************************************************************
#PARAMETRY, KTERE LZE NASTAVIT VE SKIN_DefaultSetup a SKIN_Setup
#Nakopirujte prislusny radek do dane procedury, odstrante krizek na zacatku radku a nastavte vasi pozadovanou hodnotu

#Rozlišení? "0" = automaticky, "720" = SD rozliseni, "1280" = HD rozliseni, "1920" = FullHD rozliseni
#	config.misc.CSFD.Resolution.setValue("0")

#Při plné shodě ihned načíst detail? True=Ano, False=Ne
#	config.misc.CSFD.Detail100.setValue(True)

#Načítat poster?
#	config.misc.CSFD.PosterBasic.setValue(True)

#Při zadávání předvyplnit poslední hledaný pořad?
#	config.misc.CSFD.SaveSearch.setValue(False)

#Při dlouhém stisku tlačítka INFO(EPG)? "0" = rovnou vyhledat aktuální pořad, "1" = zobrazit EPG aktuálního kanálu, "2" = zobrazit seznam kanálů
#	config.misc.CSFD.Info_EPG.setValue("0")

#Vyhledané výsledky třídit defaultně podle? "0" = vhodnosti názvu, "1" = abecedy, "2" = podle CSFD
#	config.misc.CSFD.Default_Sort.setValue("0")

#Zadávání znaků? "0" = pomocí virtuální klávesnice, "1" = výběrem znaků opakovaným stiskem klávesy
#	config.misc.CSFD.Input_Type.setValue("0")

#Design CSFD obrazovek? "0" = barva textu dle hodnocení, "1" = barvy stejné bez ohledu na hodnocení, "2" = barvy stejné bez ohledu na hodnocení + zvýraznění kategorií
#	config.misc.CSFD.Design.setValue("0")

#Komentáře? "" = seřadit podle počtu bodů uživatele, "podle-datetime/" = seřadit od nejnovějších po nejstarší, "podle-rating/" = seřadit podle hodnocení
#	config.misc.CSFD.Comment_Sort.setValue("")

#Velikost fontu
#	config.misc.CSFD.FontHeight.setValue("22")

#Velikost fontu pro FullHD rozlišení
#	config.misc.CSFD.FontHeightFullHD.setValue("33")

#Oddělovač tisíců: "" = žádný, " " = mezera, "." = tečka, "," = čárka
#	config.misc.CSFD.ThousandsSeparator.setValue("")

#Zobrazit CSFD v Hlavním menu?
#	config.misc.CSFD.ShowInMenuStart.setValue(False)

#Zobrazit CSFD v EPGSubMenu v PLI?
#	config.misc.CSFD.ShowInEPGSubMenu.setValue(False)

#Zobrazit CSFD v menu Pluginů?
#	config.misc.CSFD.ShowInPluginMenu.setValue(True)

#Zobrazit CSFD v menu INFO(EPG)?
#	config.misc.CSFD.ShowInEventInfoMenu.setValue(True)

#Zobrazit CSFD v menu Extension?
#	config.misc.CSFD.ShowInExtensionMenu.setValue(False)

#Vyhledat defaultně všechny podobné pořady?
#	config.misc.CSFD.FindAllItems.setValue(False)

#Zobrazit CSFD v EPG místo MultiEPG?
#	config.misc.CSFD.ShowEPGMulti.setValue(True)

#Zobrazit CSFD v EPG výběru?
#	config.misc.CSFD.ShowInEPGList.setValue(True)

#Zobrazit CSFD v EPG výběru - modré tlačítko?
#	config.misc.CSFD.ShowInEPGListBlueButton.setValue(False)

#Zobrazit CSFD v EPG detailu?
#	config.misc.CSFD.ShowInEPGDetail.setValue(True)

#Zobrazit CSFD ve výběru nahraných pořadů?
#	config.misc.CSFD.ShowInMovieSelection.setValue(True)

#Volat místo IMDB plugin CSFD?
#	config.misc.CSFD.CSFDreplaceIMDB.setValue(True)

#Třídit EPG podle CZ&SK abecedy?
#	config.misc.CSFD.SortEPG_CZ_SK.setValue(True)

#Priorita pluginu v menu: od 0 do 200
#	config.misc.CSFD.PriorityInMenu.setValue(100)

#Povolit slideshow pro poster v základu?
#	config.misc.CSFD.PosterBasicSlide.setValue(True)

#Změna posteru při slideshow v základu: od 2 do 50
#	config.misc.CSFD.PosterBasicSlideTime.setValue(10)

#Poster slideshow včetně fotek z galerie v základu?
#	config.misc.CSFD.PosterBasicSlideInclGallery.setValue(True)

#Povolit slideshow pro galerii v detailu?
#	config.misc.CSFD.GallerySlide.setValue(True)

#Změna galerie při slideshow v detailu: od 2 do 50
#	config.misc.CSFD.GallerySlideTime.setValue(10)

#Povolit slideshow pro poster v detailu?
#	config.misc.CSFD.PosterSlide.setValue(True)

#Změna posteru při slideshow v detailu: od 2 do 50
#	config.misc.CSFD.PosterSlideTime.setValue(10)

#Zobrazovat tipy?
#	config.misc.CSFD.TipsShow.setValue(True)

#Změna zobrazovaných tipů: od 2 do 50
#	config.misc.CSFD.TipsTime.setValue(15)

#Při volání IMDB odstranit diakritiku?
#	config.misc.CSFD.IMDBCharsConversion.setValue(True)

#Zobrazit oddělovací linku v detailu?
#	config.misc.CSFD.ShowLine.setValue(True)

#Preferované rozlišení videa? "sd" = SD rozliseni, "hd" = HD rozliseni
#	config.misc.CSFD.VideoResolution.setValue("sd")

#Akce pro klávesu 4
#	config.misc.CSFD.HotKey4.setValue("aktEPG")

#Akce pro klávesu 5
#	config.misc.CSFD.HotKey5.setValue("spustitIMDB")

#Akce pro klávesu 6
#	config.misc.CSFD.HotKey6.setValue("komentare")

#Akce pro klávesu 7
#	config.misc.CSFD.HotKey7.setValue("zajimavosti")

#Akce pro klávesu 8
#	config.misc.CSFD.HotKey8.setValue("galerie")

#Akce pro klávesu 9
#	config.misc.CSFD.HotKey9.setValue("postery")

#Akce pro klávesu 0
#	config.misc.CSFD.HotKey0.setValue("video")

#Akce pro dlouhý stisk červeného tlačítka
#	config.misc.CSFD.HotKeyLR.setValue("diskuze")

#Akce pro dlouhý stisk zeleného tlačítka
#	config.misc.CSFD.HotKeyLG.setValue("postery")

#Akce pro dlouhý stisk modrého tlačítka
#	config.misc.CSFD.HotKeyLB.setValue("premiery")

#Akce pro dlouhý stisk žlutého tlačítka
#	config.misc.CSFD.HotKeyLY.setValue("ownrating")

#Položka 01 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet1.setValue("komentare")

#Položka 02 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet2.setValue("diskuze")

#Položka 03 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet3.setValue("zajimavosti")

#Položka 04 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet4.setValue("premiery")

#Položka 05 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet5.setValue("hodnoceni")

#Položka 06 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet6.setValue("fanousci")

#Položka 07 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet7.setValue("galerie")

#Položka 08 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet8.setValue("postery")

#Položka 09 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet9.setValue("video")

#Položka 10 pro rotaci v BOUQUETech
#	config.misc.CSFD.Bouquet10.setValue("ext.recenze")

#Povolit změnit CSFD ve hlavnim skinu
#	config.misc.CSFD.Skinxml.setValue(False)

#Povolit změnit OLED displej ve skinu
#	config.misc.CSFD.SkinOLEDxml.setValue(True)

#***************************************************************************************************************************************************************************************
#DEFINICE VZHLEDU JENOTLIVYCH OBAZOVEK

#hlavni obrazovka CSFD pluginu pro SD rozliseni
#self.skinName = ["CSFD_SD", "CSFD"]
Screen_CSFD_SD = """
	<screen name="CSFD_SD" position="center,center" size="605,530" zPosition="0" backgroundColor="#31000000" title="Filmová databáze CSFD" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="9,483" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="158,483" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="307,483" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="456,483" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="9,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="158,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="307,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="456,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="titellabel" position="10,2" size="370,24" valign="center" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="sortlabel" position="10,30" size="350,28" font="Regular;17" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="detailslabel" position="180,53" size="415,201" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="contentlabel" position="10,258" size="585,201" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="extralabel" position="10,53" size="585,376" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="photolabel" position="10,53" size="585,376" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="playbutton" position="277,216" size="50,50" zPosition="2" transparent="1" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/play_button.png"/>
		<widget name="statusbar" position="10,465" size="585,17" font="Regular;15" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="4"	transparent="1" />
		<widget name="poster" position="4,53" size="170,201" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="menu" position="10,53" size="585,397" zPosition="3" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="servicemenuBackG" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/border_menu_430.png" position="85,50" size="430,340" zPosition="4" alphatest="on" />
		<widget name="servicemenuTop" position="90,55" size="420,25" valign="center" halign="center" backgroundColor="black" foregroundColor="#f0b400" font="Regular;22" zPosition="4" />
		<widget name="servicemenu" position="90,80" size="420,305" backgroundColor="black" foregroundColor="#cccccc" zPosition="4" transparent="1" scrollbarMode="showOnDemand" backgroundColorSelected="black" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="ratinglabel" position="285,24" size="310,22" halign="right" font="Regular;21" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="starsbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty.png" position="385,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars" position="385,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled.png" zPosition="2" transparent="1" />
		<widget name="starsmtbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_mt.png" position="385,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="starsmt" position="385,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_mt.png" zPosition="2" transparent="1" />
		<widget name="starsbg0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_0.png" position="385,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars0" position="385,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_0.png" zPosition="2" transparent="1" />
		<widget name="starsbg50" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_50.png" position="385,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars50" position="385,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_50.png" zPosition="2" transparent="1" />
		<widget name="starsbg100" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_100.png" position="385,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars100" position="385,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_100.png" zPosition="2" transparent="1" />
		<widget name="pagebg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/pagebg.png" position="158,432" size="284,44" zPosition="1" alphatest="on" />
		<widget name="pageb1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_1.png" position="162,439" size="35,25" zPosition="3" alphatest="on" />
		<widget name="pageb3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_3.png" position="407,439" size="35,25" zPosition="3" alphatest="on" />
		<widget name="paget1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_left.png" position="197,439" size="35,25" zPosition="3" alphatest="on" />
		<widget name="paget3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_right.png" position="372,439" size="35,25" zPosition="3" alphatest="on" />
		<widget name="page" position="232,438" size="140,28" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" valign="center" halign="center" zPosition="2" transparent="1" />
	</screen>"""

#hlavni obrazovka CSFD pluginu pro HD rozliseni
#self.skinName = ["CSFD_HD", "CSFD"]
Screen_CSFD_HD = """
	<screen name="CSFD_HD" position="center,70" size="1100,613" zPosition="0" backgroundColor="#31000000" title="Filmová databáze CSFD" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="5,543" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="280,543" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="555,543" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="830,543" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="5,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="280,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="555,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="830,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="titellabel" position="10,2" size="865,26" valign="center" font="Regular;24" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="sortlabel" position="10,30" size="350,28" font="Regular;18" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="detailslabel" position="320,53" size="770,230" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="line" position="320,285" zPosition="1" size="750,1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/line.png" />
		<widget name="contentlabel" position="320,289" size="770,228" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="extralabel" position="10,53" size="1080,436" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="photolabel" position="10,53" size="1080,436" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="playbutton" position="525,246" size="50,50" zPosition="2" transparent="1" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/play_button.png"/>
		<widget name="statusbar" position="10,525" size="1080,17" font="Regular;16" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="4" transparent="1" />
		<widget name="poster" position="4,53" size="310,460" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="menu" position="10,53" size="1080,455" zPosition="3" scrollbarMode="showOnDemand" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="servicemenuBackG" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/border_menu_430.png" position="335,50" size="430,340" zPosition="4" alphatest="on" />
		<widget name="servicemenuTop" position="340,55" size="420,25" valign="center" halign="center" backgroundColor="black" foregroundColor="#f0b400" font="Regular;22" zPosition="4" />
		<widget name="servicemenu" position="340,80" size="420,305" backgroundColor="black" foregroundColor="#cccccc" zPosition="4" transparent="1" scrollbarMode="showOnDemand" backgroundColorSelected="black" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="ratinglabel" position="780,24" size="310,22" halign="right" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="starsbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty.png" position="880,2" zPosition="0" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars" position="880,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled.png" transparent="1" />
		<widget name="starsmtbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_mt.png" position="880,2" zPosition="0" size="210,21" transparent="1" alphatest="on" />
		<widget name="starsmt" position="880,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_mt.png" transparent="1" />
		<widget name="starsbg0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_0.png" position="880,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars0" position="880,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_0.png" zPosition="2" transparent="1" />
		<widget name="starsbg50" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_50.png" position="880,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars50" position="880,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_50.png" zPosition="2" transparent="1" />
		<widget name="starsbg100" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_100.png" position="880,2" zPosition="1" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars100" position="880,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_100.png" zPosition="2" transparent="1" />
		<widget name="pagebg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/pagebg.png" position="402,492" size="290,46" zPosition="1" alphatest="on" />
		<widget name="pageb1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_1.png" position="407,498" size="35,25" zPosition="3" alphatest="on" />
		<widget name="pageb3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_3.png" position="657,498" size="35,25" zPosition="3" alphatest="on" />
		<widget name="paget1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_left.png" position="442,498" size="35,25" zPosition="3" alphatest="on" />
		<widget name="paget3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_right.png" position="622,498" size="35,25" zPosition="3" alphatest="on" />
		<widget name="page" position="477,496" size="145,28" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" valign="center" halign="center" zPosition="2" transparent="1" />
		<widget name="tips_label" position="5,590" size="50,20" font="Regular;16" foregroundColor="#cccccc" backgroundColor="#31000000" halign="left" valign="center" zPosition="3" transparent="1" />
		<widget name="tips_detail" position="60,590" size="910,20" font="Regular;16" foregroundColor="#cccccc" backgroundColor="#31000000" halign="left" valign="center" zPosition="3" transparent="1" />
		<widget name="tips_icon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_help.png" position="60,588" size="35,25" backgroundColor="#31000000" zPosition="3" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_menu.png" position="1010,588" size="35,25" backgroundColor="#31000000" zPosition="3" alphatest="on" />
		<eLabel text="Menu" position="1047,590" size="53,20" font="Regular;16" foregroundColor="#cccccc" backgroundColor="#31000000" halign="left" valign="center" zPosition="3" transparent="1" />
	</screen>"""

#hlavni obrazovka CSFD pluginu pro FullHD rozliseni
#self.skinName = ["CSFD_FullHD", "CSFD"]
Screen_CSFD_FullHD = """
	<screen name="CSFD_FullHD" position="center,105" size="1635,920" zPosition="0" backgroundColor="#31000000" title="Filmová databáze CSFD" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="72,830" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="481,830" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="890,830" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="1299,830" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="72,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="481,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="890,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="1299,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="titellabel" position="15,3" size="1280,39" valign="center" font="Regular;32" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="sortlabel" position="15,45" size="520,42" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="detailslabel" position="475,80" size="1140,345" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="line" position="475,428" zPosition="1" size="1110,2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/line.png" />
		<widget name="contentlabel" position="475,435" size="1140,343" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="extralabel" position="15,80" size="1600,654" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="photolabel" position="15,80" size="1600,654" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="playbutton" position="780,369" size="50,50" zPosition="2" transparent="1" alphatest="on" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/play_button.png"/>
		<widget name="statusbar" position="15,785" size="1600,26" font="Regular;21" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="4" transparent="1" />
		<widget name="poster" position="6,80" size="460,690" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="menu" position="15,80" size="1600,680" zPosition="3" scrollbarMode="showOnDemand" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" enableWrapAround="1" />
		<widget name="servicemenuBackG" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/border_menu_520.png" position="470,75" size="660,520" zPosition="4" alphatest="on" />
		<widget name="servicemenuTop" position="475,83" size="650,36" valign="center" halign="center" backgroundColor="black" foregroundColor="#f0b400" font="Regular;28" zPosition="4" />
		<widget name="servicemenu" position="475,120" size="650,466" backgroundColor="black" foregroundColor="#cccccc" zPosition="4" transparent="1" scrollbarMode="showOnDemand" backgroundColorSelected="black" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="ratinglabel" position="1160,36" size="460,33" halign="right" font="Regular;28" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="starsbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty.png" position="1410,3" zPosition="2" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars" position="1410,3" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled.png" zPosition="1" transparent="1" />
		<widget name="starsmtbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_mt.png" position="1410,3" zPosition="2" size="210,21" transparent="1" alphatest="on" />
		<widget name="starsmt" position="1410,3" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_mt.png" zPosition="1" transparent="1" />
		<widget name="starsbg0" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_0.png" position="1410,3" zPosition="2" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars0" position="1410,3" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_0.png" zPosition="1" transparent="1" />
		<widget name="starsbg50" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_50.png" position="1410,3" zPosition="2" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars50" position="1410,3" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_50.png" zPosition="1" transparent="1" />
		<widget name="starsbg100" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty_100.png" position="1410,3" zPosition="2" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars100" position="1410,3" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled_100.png" zPosition="1" transparent="1" />
		<widget name="pagebg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/pagebghd.png" position="585,739" size="430,45" zPosition="1" alphatest="on" />
		<widget name="pageb1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_1.png" position="604,750" size="35,25" zPosition="3" alphatest="on" />
		<widget name="pageb3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_3.png" position="963,750" size="35,25" zPosition="3" alphatest="on" />
		<widget name="paget1" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_left.png" position="644,750" size="35,25" zPosition="3" alphatest="on" />
		<widget name="paget3" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_right.png" position="923,750" size="35,25" zPosition="3" alphatest="on" />
		<widget name="page" position="708,744" size="215,42" font="Regular;28" foregroundColor="#f0b400" backgroundColor="#31000000" valign="center" halign="center" zPosition="2" transparent="1" />
		<widget name="tips_label" position="7,885" size="75,30" font="Regular;21" foregroundColor="#cccccc" backgroundColor="#31000000" halign="left" valign="center" zPosition="3" transparent="1" />
		<widget name="tips_detail" position="90,885" size="1465,30" font="Regular;21" foregroundColor="#cccccc" backgroundColor="#31000000" halign="left" valign="center" zPosition="3" transparent="1" />
		<widget name="tips_icon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_help.png" position="90,887" size="35,25" backgroundColor="#31000000" zPosition="3" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_menu.png" position="1470,887" size="35,25" backgroundColor="#31000000" zPosition="3" alphatest="on" />
		<eLabel text="Menu" position="1510,885" size="100,30" font="Regular;21" foregroundColor="#cccccc" backgroundColor="#31000000" halign="left" valign="center" zPosition="3" transparent="1" />
	</screen>"""

#obrazovka pro vzhled IMDB pluginu volaneho z CSFD pro SD rozliseni
#self.skinName = ["CSFDIMDB_SD", "CSFDIMDB"]
Screen_CSFDIMDB_SD = """
	<screen name="CSFDIMDB_SD" position="center,center" size="605,530" zPosition="0" backgroundColor="#31000000" title="Internet Movie Database Details (IMDB)" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="9,483" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="158,483" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="307,483" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="456,483" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="9,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="158,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="307,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="10" transparent="1" />
		<widget name="key_blue" position="456,493" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="titlelabel" position="10,0" size="370,46" valign="center" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="detailslabel" position="180,53" size="415,201" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="castlabel" position="10,258" size="292,200" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="storylinelabel" position="303,258" size="292,201" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="extralabel" position="10,53" size="585,376" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="statusbar" position="10,465" size="585,17" font="Regular;15" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="4" transparent="1" />
		<widget name="poster" position="4,53" size="170,201" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="ratinglabel" position="375,24" size="220,22" halign="right" font="Regular;21" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="menu" position="10,53" size="585,397" zPosition="3" foregroundColor="#cccccc" backgroundColor="#31000000" scrollbarMode="showOnDemand" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="starsbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty.png" position="385,2" zPosition="0" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars" position="385,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled.png" transparent="1" />
	</screen>"""

#obrazovka pro vzhled IMDB pluginu volaneho z CSFD pro HD rozliseni
#self.skinName = ["CSFDIMDB_HD", "CSFDIMDB"]
Screen_CSFDIMDB_HD = """
	<screen name="CSFDIMDB_HD" position="center,center" size="1100,590" zPosition="0" backgroundColor="#31000000" title="Internet Movie Database Details (IMDB)" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="5,543" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="280,543" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="555,543" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="830,543" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="5,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="280,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="555,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="830,553" size="265,28" font="Regular;22" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="titlelabel" position="10,0" size="850,46" valign="center" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="detailslabel" position="320,53" size="770,230" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="castlabel" position="320,289" size="383,230" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="storylinelabel" position="705,289" size="385,230" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="extralabel" position="10,53" size="1080,436" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="statusbar" position="10,525" size="1080,17" font="Regular;16" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="4" transparent="1" />
		<widget name="poster" position="4,53" size="310,460" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="ratinglabel" position="870,24" size="220,22" halign="right" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="menu" position="10,53" size="1080,455" zPosition="3" foregroundColor="#cccccc" backgroundColor="#31000000" scrollbarMode="showOnDemand" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="starsbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty.png" position="880,2" zPosition="0" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars" position="880,2" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled.png" transparent="1" />
	</screen>"""

#obrazovka pro vzhled IMDB pluginu volaneho z CSFD pro FullHD rozliseni
#self.skinName = ["CSFDIMDB_FullHD", "CSFDIMDB"]
Screen_CSFDIMDB_FullHD = """
	<screen name="CSFDIMDB_FullHD" position="center,center" size="1635,920" zPosition="0" backgroundColor="#31000000" title="Internet Movie Database Details (IMDB)" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="72,830" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="481,830" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="890,830" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="1299,830" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="72,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="481,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="890,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="1299,830" size="265,44" font="Regular;28" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="titlelabel" position="15,3" size="1280,39" valign="center" font="Regular;32" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="detailslabel" position="475,80" size="1140,345" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="castlabel" position="475,435" size="568,345" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="storylinelabel" position="1045,435" size="570,345" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="extralabel" position="15,80" size="1600,654" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;%s" />
		<widget name="statusbar" position="15,785" size="1600,26" font="Regular;21" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="4" transparent="1" />
		<widget name="poster" position="6,80" size="460,690" backgroundColor="#31000000" zPosition="1" alphatest="on" />
		<widget name="ratinglabel" position="1160,36" size="460,33" halign="right" font="Regular;28" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="menu" position="15,80" size="1600,680" zPosition="3" foregroundColor="#cccccc" backgroundColor="#31000000" scrollbarMode="showOnDemand" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" enableWrapAround="1" />
		<widget name="starsbg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_empty.png" position="1410,3" zPosition="0" size="210,21" transparent="1" alphatest="on" />
		<widget name="stars" position="1410,3" size="210,21" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/starsbar_filled.png" transparent="1" />
	</screen>"""

#obrazovka pro vzhled LCD panelu pro DM 900
#self.skinName = ["CSFDLCDSummary900", "CSFDLCDSummary"]
Screen_CSFDLCDSummary900 = """
	<screen name="CSFDLCDSummary900" position="0,0" size="400,240">
		<widget name="headline" position="0,20" size="400,45" foregroundColor="#f0b400" font="Display;40"/>
		<widget name="infomovie" position="0,80" size="400,150" foregroundColor="white" font="Display;38"/>
	</screen>"""

#obrazovka pro vzhled LCD panelu pro DM 8000 a 7020HD 
#self.skinName = ["CSFDLCDSummary8000_7020hd", "CSFDLCDSummary"]
Screen_CSFDLCDSummary8000_7020hd = """
	<screen name="CSFDLCDSummary8000_7020hd" position="0,0" size="132,64">
		<widget name="headline" position="6,0" size="120,14" font="Display;14"/>
		<widget name="infomovie" position="6,16" size="120,48" font="Display;12"/>
	</screen>"""

#obrazovka pro vzhled LCD panelu pro DM 800SE
#self.skinName = ["CSFDLCDSummary800SE", "CSFDLCDSummary"]
Screen_CSFDLCDSummary800SE = """
	<screen name="CSFDLCDSummary800SE" position="0,0" size="96,64" id="2">
		<widget name="headline" position="0,0" size="96,14" foregroundColor="#f0b400" font="Display;12"/>
		<widget name="infomovie" position="0,18" size="96,42" foregroundColor="white" font="Display;10"/>
	</screen>"""

#obrazovka pro vzhled LCD panelu pro DM 800
#self.skinName = ["CSFDLCDSummary800", "CSFDLCDSummary"]
Screen_CSFDLCDSummary800 = """
	<screen name="CSFDLCDSummary800" position="0,0" size="96,64">
		<widget name="headline" position="0,0" size="96,14" font="Display;12"/>
		<widget name="infomovie" position="0,18" size="96,42" font="Display;10"/>
	</screen>"""

#obrazovka pro vzhled LCD panelu pro ostatni boxy DMM
#self.skinName = ["CSFDLCDSummaryElseDMM", "CSFDLCDSummary"]
Screen_CSFDLCDSummaryElseDMM = """
	<screen name="CSFDLCDSummaryElseDMM" position="0,0" size="96,64">
		<widget name="headline" position="0,0" size="96,14" font="Display;12"/>
		<widget name="infomovie" position="0,18" size="96,42" font="Display;10"/>
	</screen>"""

#obrazovka pro vzhled LCD panelu pro ostatni boxy mimo DMM
#self.skinName = ["CSFDLCDSummaryElse", "CSFDLCDSummary"]
Screen_CSFDLCDSummaryElse = """
	<screen name="CSFDLCDSummaryElse" position="0,0" size="96,64">
		<widget name="headline" position="0,0" size="96,14" font="Regular;12"/>
		<widget name="infomovie" position="0,18" size="96,42" font="Regular;10"/>
	</screen>"""

#obrazovka pro Nastaveni - SD rozliseni
#self.skinName = ["CSFDSetupSD", "CSFDSetup"]
Screen_CSFDSetupSD = """
	<screen name="CSFDSetupSD" position="center,center" size="680,518" zPosition="0" backgroundColor="#31000000" title="CSFD - Nastavení">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="24,430" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="188,430" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="352,430" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="516,430" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup_l.png" position="323,21" size="342,5" zPosition="2" alphatest="on" />
		<widget name="key_red" position="24,440" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="188,440" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="352,440" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="516,440" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_info" position="74,490" size="350,25" font="Regular;16" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="VKeyText" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_text.png" position="442,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="VKeyIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_icon.png" position="475,478" alphatest="on" size="60,48" backgroundColor="#31000000" zPosition="3" />
		<widget name="info_icon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_info.png" position="24,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="info_epg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_epg.png" position="57,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="key_menu" position="583,490" size="50,25" font="Regular;16" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="info_menu" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_menu.png" position="550,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="tabbar"  position="5,1" size="320,25" alphatest="on" zPosition="1" pixmaps="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup1.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup2.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup3.png" />
		<widget name="config" position="20,26" size="640,378" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" transparent="1" />
		<widget name="info" position="0,405" size="680,26" font="Regular;16" foregroundColor="#f0b400" backgroundColor="#31000000" shadowColor="#000000" shadowOffset="-2,-2" valign="center" halign="center" transparent="1" /> 
		<widget name="config0" position="5,1" size="108,22" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;18" />
		<widget name="config1" position="111,1" size="108,22" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;18" />
		<widget name="config2" position="216,1" size="108,22" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;18" />
	</screen>"""

#obrazovka pro Nastaveni - HD rozliseni
#self.skinName = ["CSFDSetupHD", "CSFDSetup"]
Screen_CSFDSetupHD = """
	<screen name="CSFDSetupHD" position="center,center" size="1100,518" zPosition="0" backgroundColor="#31000000" title="CSFD - Nastavení">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="5,440" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="280,440" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="555,440" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="830,440" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup_l.png" position="323,21" size="777,5" zPosition="2" alphatest="on" />
		<widget name="key_red" position="5,440" size="265,44" font="Regular;21" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="280,440" size="265,44" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="555,440" size="265,44" font="Regular;21" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="830,440" size="265,44" font="Regular;21" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_info" position="74,490" size="350,25" font="Regular;16" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="VKeyText" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_text.png" position="842,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="VKeyIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_icon.png" position="875,478" alphatest="on" size="60,48" backgroundColor="#31000000" zPosition="3" />
		<widget name="info_icon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_info.png" position="24,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="info_epg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_epg.png" position="57,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="key_menu" position="983,490" size="50,25" font="Regular;16" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="info_menu" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_menu.png" position="950,490" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="tabbar"  position="5,1" size="320,25" alphatest="on" zPosition="1" pixmaps="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup1.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup2.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup3.png" />
		<widget name="config" position="20,26" size="1060,378" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" transparent="1" />
		<widget name="info" position="0,405" size="1100,26" font="Regular;16" foregroundColor="#f0b400" backgroundColor="#31000000" shadowColor="#000000" shadowOffset="-2,-2" valign="center" halign="center" transparent="1" /> 
		<widget name="config0" position="5,1" size="108,22" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;18" />
		<widget name="config1" position="111,1" size="108,22" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;18" />
		<widget name="config2" position="216,1" size="108,22" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;18" />
	</screen>"""

#obrazovka pro Nastaveni - FullHD rozliseni
#self.skinName = ["CSFDSetupFullHD", "CSFDSetup"]
Screen_CSFDSetupFullHD = """
	<screen name="CSFDSetupFullHD" position="center,center" size="1635,777" zPosition="0" backgroundColor="#31000000" title="CSFD - Nastavení">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="72,660" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="481,660" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="890,660" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="1299,660" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup_lfhd.png" position="488,32" size="1147,8" zPosition="2" alphatest="on" />
		<widget name="key_red" position="72,660" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="481,660" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="890,660" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="1299,660" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_info" position="116,735" size="520,28" font="Regular;24" halign="left" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="VKeyText" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_text.png" position="1360,735" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="VKeyIcon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/vkey_icon.png" position="1400,723" alphatest="on" size="60,48" backgroundColor="#31000000" zPosition="3" />
		<widget name="info_icon" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_info.png" position="36,735" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="info_epg" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_epg.png" position="76,735" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="key_menu" position="1526,735" size="75,28" font="Regular;24" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="info_menu" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/key_menu.png" position="1486,735" alphatest="on" size="35,25" backgroundColor="#31000000" zPosition="3" />
		<widget name="tabbar"  position="8,2" size="480,38" alphatest="on" zPosition="1" pixmaps="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup1fhd.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup2fhd.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/setup3fhd.png" />
		<widget name="config" position="30,39" size="1575,560" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" enableWrapAround="1" transparent="1" />
		<widget name="info" position="0,618" size="1635,28" font="Regular;20" foregroundColor="#f0b400" backgroundColor="#31000000" shadowColor="#000000" shadowOffset="-2,-2" valign="center" halign="center" transparent="1" /> 
		<widget name="config0" position="8,2" size="160,38" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;26" />
		<widget name="config1" position="168,2" size="160,38" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;26" />
		<widget name="config2" position="328,2" size="160,38" valign="center" transparent="1" foregroundColor="#cccccc" backgroundColor="#31000000" zPosition="2" halign="center" font="Regular;26" />
	</screen>"""

#obrazovka pro Informace o pluginu - SD rozliseni
#self.skinName = ["CSFDAboutSD", "CSFDAbout"]
Screen_CSFDAboutSD = """
	<screen name="CSFDAboutSD" position="center,center" size="604,335" zPosition="0" backgroundColor="#31000000" title="Informace o pluginu CSFD">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="230,292" size="140,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="230,302" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="label1" position="4,2" size="600,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label2" position="4,24" size="600,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label3" position="4,46" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label4" position="4,68" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label5" position="4,90" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label6" position="4,112" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label7" position="4,134" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label8" position="4,156" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label9" position="4,178" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label10" position="4,200" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label11" position="4,222" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label12" position="4,244" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label13" position="4,266" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro Informace o pluginu - HD rozliseni
#self.skinName = ["CSFDAboutHD", "CSFDAbout"]
Screen_CSFDAboutHD = """
	<screen name="CSFDAboutHD" position="center,center" size="604,335" zPosition="0" backgroundColor="#31000000" title="Informace o pluginu CSFD">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="230,292" size="140,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="230,302" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="label1" position="4,2" size="600,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label2" position="4,24" size="600,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label3" position="4,46" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label4" position="4,68" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label5" position="4,90" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label6" position="4,112" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label7" position="4,134" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label8" position="4,156" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label9" position="4,178" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label10" position="4,200" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label11" position="4,222" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label12" position="4,244" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label13" position="4,266" size="600,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro Informace o pluginu - FullHD rozliseni
#self.skinName = ["CSFDAboutFullHD", "CSFDAbout"]
Screen_CSFDAboutFullHD = """
	<screen name="CSFDAboutFullHD" position="center,center" size="900,500" zPosition="0" backgroundColor="#31000000" title="Informace o pluginu CSFD">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="340,450" size="140,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="340,450" size="140,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="label1" position="6,3" size="890,28" font="Regular;26" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label2" position="6,31" size="890,28" font="Regular;26" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label3" position="6,59" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label4" position="6,87" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label5" position="6,115" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label6" position="6,143" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label7" position="6,171" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label8" position="6,199" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label9" position="6,227" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label10" position="6,255" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label11" position="6,283" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label12" position="6,311" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label13" position="6,339" size="890,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro Historii verzi pluginu - SD rozliseni
#self.skinName = ["CSFDHistorySD", "CSFDHistory"]
Screen_CSFDHistorySD = """
	<screen name="CSFDHistorySD" position="center,center" size="605,530" zPosition="0" backgroundColor="#31000000" title="Historie změn v pluginu CSFD">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="230,487" size="140,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="230,497" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="text" position="10,10" size="585,475" zPosition="3" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" />
		<widget name="calc_text" position="10,10" size="585,475" foregroundColor="#cccccc" zPosition="3" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro Historii verzi pluginu - HD rozliseni
#self.skinName = ["CSFDHistoryHD", "CSFDHistory"]
Screen_CSFDHistoryHD = """
	<screen name="CSFDHistoryHD" position="center,center" size="1100,590" zPosition="0" backgroundColor="#31000000" title="Historie změn v pluginu CSFD">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="480,547" size="140,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="480,557" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="text" position="10,10" size="1080,531" zPosition="3" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" />
		<widget name="calc_text" position="10,10" size="1080,531" foregroundColor="#cccccc" zPosition="3" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro Historii verzi pluginu - FullHD rozliseni
#self.skinName = ["CSFDHistoryFullHD", "CSFDHistory"]
Screen_CSFDHistoryFullHD = """
	<screen name="CSFDHistoryFullHD" position="center,center" size="1635,920" zPosition="0" backgroundColor="#31000000" title="Historie změn v pluginu CSFD">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="685,860" size="265,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="685,860" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="text" position="15,20" size="1605,800" zPosition="3" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" />
		<widget name="calc_text" position="15,20" size="1605,800" foregroundColor="#cccccc" zPosition="3" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro výběr skinu pro plugin CSFD - SD rozliseni
#self.skinName = ["CSFDSkinSelectSD", "CSFDSkinSelect"]
Screen_CSFDSkinSelectSD = """
	<screen name="CSFDSkinSelectSD" position="center,center" size="680,518" zPosition="0" backgroundColor="#31000000" title="Výběr skinu pro plugin CSFD">
		<widget name="menu" position="10,10" size="200,458" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="author" position="220,10" size="440,22" font="Regular;20" valign="center" halign="left" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="email" position="220,34" size="440,22" font="Regular;20" valign="center" halign="left" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="description" position="220,58" size="440,124" font="Regular;20" valign="top" halign="left" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="preview" position="220,190" size="440,280" alphatest="on" backgroundColor="#31000000" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="100,470" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_green" position="100,480" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="270,470" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_blue" position="270,480" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="440,470" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="440,480" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro výběr skinu pro plugin CSFD - HD rozliseni
#self.skinName = ["CSFDSkinSelectHD", "CSFDSkinSelect"]
Screen_CSFDSkinSelectHD = """
	<screen name="CSFDSkinSelectHD" position="center,center" size="680,518" zPosition="0" backgroundColor="#31000000" title="Výběr skinu pro plugin CSFD">
		<widget name="menu" position="10,10" size="200,458" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" />
		<widget name="author" position="220,10" size="440,22" font="Regular;20" valign="center" halign="left" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="email" position="220,34" size="440,22" font="Regular;20" valign="center" halign="left" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="description" position="220,58" size="440,124" font="Regular;20" valign="top" halign="left" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="preview" position="220,190" size="440,280" alphatest="on" backgroundColor="#31000000" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="100,470" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_green" position="100,480" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="270,470" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_blue" position="270,480" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="440,470" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="440,480" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro výběr skinu pro plugin CSFD - FullHD rozliseni
#self.skinName = ["CSFDSkinSelectFullHD", "CSFDSkinSelect"]
Screen_CSFDSkinSelectFullHD = """
	<screen name="CSFDSkinSelectFullHD" position="center,center" size="1010,777" zPosition="0" backgroundColor="#31000000" title="Výběr skinu pro plugin CSFD">
		<widget name="menu" position="15,15" size="297,687" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" enableWrapAround="1" />
		<widget name="author" position="326,15" size="653,28" font="Regular;26" valign="center" halign="left" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="email" position="326,45" size="653,28" font="Regular;26" valign="center" halign="left" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="description" position="326,75" size="653,186" font="Regular;26" valign="top" halign="left" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="preview" position="326,263" size="653,420" alphatest="on" backgroundColor="#31000000" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="54,705" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_green" position="54,705" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="373,705" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_blue" position="373,705" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="692,705" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="692,705" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro Informace o prehravanem videu (stisk tl. INFO(EPG) během přehrávání videa) - SD rozliseni
#self.skinName = ["CSFDVideoInfoScreenSD", "CSFDVideoInfoScreen"]
Screen_CSFDVideoInfoScreenSD = """
	<screen name="CSFDVideoInfoScreenSD" position="center,center" size="504,270" zPosition="0" backgroundColor="#31000000" title="Video">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="180,226" size="140,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="180,236" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="label1" position="4,2" size="500,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label2" position="4,24" size="500,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label3" position="4,46" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label4" position="4,68" size="500,66" font="Regular;20" valign="top" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label5" position="4,134" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label6" position="4,156" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label7" position="4,178" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label8" position="4,200" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro Informace o prehravanem videu (stisk tl. INFO(EPG) během přehrávání videa) - HD rozliseni
#self.skinName = ["CSFDVideoInfoScreenHD", "CSFDVideoInfoScreen"]
Screen_CSFDVideoInfoScreenHD = """
	<screen name="CSFDVideoInfoScreenHD" position="center,center" size="504,270" zPosition="0" backgroundColor="#31000000" title="Video">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="180,226" size="140,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="180,236" size="140,28" font="Regular;21" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="label1" position="4,2" size="500,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label2" position="4,24" size="500,22" font="Regular;20" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label3" position="4,46" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label4" position="4,68" size="500,66" font="Regular;20" valign="top" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label5" position="4,134" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label6" position="4,156" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label7" position="4,178" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label8" position="4,200" size="500,22" font="Regular;20" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro Informace o prehravanem videu (stisk tl. INFO(EPG) během přehrávání videa) - FullHD rozliseni
#self.skinName = ["CSFDVideoInfoScreenFullHD", "CSFDVideoInfoScreen"]
Screen_CSFDVideoInfoScreenFullHD = """
	<screen name="CSFDVideoInfoScreenFullHD" position="center,center" size="748,405" zPosition="0" backgroundColor="#31000000" title="Video">
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="267,339" size="265,44" zPosition="1" alphatest="on" />
		<widget name="oktext" position="267,339" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="label1" position="6,3" size="742,28" font="Regular;26" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label2" position="6,31" size="742,28" font="Regular;26" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" transparent="1" />
		<widget name="label3" position="6,59" size="742,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label4" position="6,87" size="742,28" font="Regular;26" valign="top" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label5" position="6,115" size="742,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label6" position="6,143" size="742,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label7" position="6,171" size="742,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="label8" position="6,199" size="742,28" font="Regular;26" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro prehravac videi - SD rozliseni
#self.skinName = ["CSFDPlayerSD", "CSFDPlayer"]
Screen_CSFDPlayerSD = """
	<screen name="CSFDPlayerSD" position="0,380" size="720,160" title="InfoBar" backgroundColor="#31000000" flags="wfNoBorder">
		<ePixmap position="0,0" zPosition="-10" size="720,160" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/back-media-dvd-sd.png" transparent="1" />
		<widget source="session.CurrentService" render="Label" position="230,73" size="360,40" font="Regular;18" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="ServiceName">Name</convert>
		</widget>
		<ePixmap position="48,70" size="154,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/csfdplayerlogo.png" zPosition="1" alphatest="on" />
		<widget source="session.CurrentService" render="PositionGauge" position="300,133" size="270,10" zPosition="2" pointer="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/pointer.png:13,3">
			<convert type="ServicePosition">Gauge</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="205,129" size="100,20" font="Regular;18" halign="center" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Position</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="576,129" size="100,20" font="Regular;18" halign="center" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Remaining,Negate</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="580,73" size="90,24" font="Regular;20" halign="right" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Length</convert>
		</widget>
	</screen>"""

#obrazovka pro prehravac videi - HD rozliseni
#self.skinName = ["CSFDPlayerHD", "CSFDPlayer"]
Screen_CSFDPlayerHD = """
	<screen name="CSFDPlayerHD" position="0,525" size="1280,181" title="InfoBar" backgroundColor="#31000000" flags="wfNoBorder">
		<ePixmap position="0,0" zPosition="-10" size="1280,181" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/back-media-dvd.png" transparent="1" />
		<widget source="global.CurrentTime" render="Label" position="990,115" size="103,24" font="Regular;18" valign="top" halign="right" backgroundColor="#00333333" foregroundColor="#00cccccc" transparent="1">
			<convert type="ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="1074,116" size="45,20" font="Regular;14" valign="top" halign="right" backgroundColor="#00333333" foregroundColor="#00cccccc" transparent="1">
			<convert type="ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="941,84" size="278,20" font="Regular;18" halign="center" backgroundColor="#353e575e" foregroundColor="#00cccccc" transparent="1">
			<convert type="ClockToText">Format:%d.%m. %Y</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="50,32" size="1180,30" font="Regular;22" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="ServiceName">Name</convert>
		</widget>
		<ePixmap position="110,82" size="154,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/csfdplayerlogo.png" zPosition="1" alphatest="on" />
		<ePixmap position="340,90" size="600,16" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/mpslider.png" zPosition="3" alphatest="on" />
		<widget source="session.CurrentService" render="PositionGauge" position="360,91" size="560,14" zPosition="2" pointer="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/pointer.png:13,3">
			<convert type="ServicePosition">Gauge</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="340,118" size="200,20" font="Regular;18" halign="left" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Position</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="740,118" size="200,20" font="Regular;18" halign="right" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Remaining</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="540,118" size="200,20" font="Regular;18" halign="center" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Length</convert>
		</widget>
	</screen>"""

#obrazovka pro prehravac videi - FullHD rozliseni
#self.skinName = ["CSFDPlayerFullHD", "CSFDPlayer"]
Screen_CSFDPlayerFullHD = """
	<screen name="CSFDPlayerFullHD" position="0,815" size="1900,270" title="InfoBar" backgroundColor="#31000000" flags="wfNoBorder">
		<ePixmap position="0,0" zPosition="-10" size="1900,270" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/back-media-dvd-fhd.png" transparent="1" />
		<widget source="global.CurrentTime" render="Label" position="1470,170" size="150,24" font="Regular;22" valign="top" halign="right" backgroundColor="#00333333" foregroundColor="#00cccccc" transparent="1">
			<convert type="ClockToText">Default</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="1590,174" size="65,22" font="Regular;18" valign="top" halign="right" backgroundColor="#00333333" foregroundColor="#00cccccc" transparent="1">
			<convert type="ClockToText">Format::%S</convert>
		</widget>
		<widget source="global.CurrentTime" render="Label" position="1395,126" size="412,24" font="Regular;22" halign="center" backgroundColor="#353e575e" foregroundColor="#00cccccc" transparent="1">
			<convert type="ClockToText">Format:%d.%m. %Y</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="75,48" size="1750,34" font="Regular;28" halign="center" backgroundColor="#353e575e" shadowColor="#1A58A6" shadowOffset="-2,-1" transparent="1">
			<convert type="ServiceName">Name</convert>
		</widget>
		<ePixmap position="165,123" size="154,60" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/csfdplayerlogo.png" zPosition="1" alphatest="on" />
		<ePixmap position="505,135" size="890,24" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/mpslider_fhd.png" zPosition="3" alphatest="on" />
		<widget source="session.CurrentService" render="PositionGauge" position="535,136" size="830,21" zPosition="2" pointer="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/pointer.png:13,3">
			<convert type="ServicePosition">Gauge</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="505,177" size="295,24" font="Regular;22" halign="left" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Position</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="1100,177" size="295,24" font="Regular;22" halign="right" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Remaining</convert>
		</widget>
		<widget source="session.CurrentService" render="Label" position="800,177" size="295,24" font="Regular;22" halign="center" valign="center" backgroundColor="#80000000" transparent="1">
			<convert type="ServicePosition">Length</convert>
		</widget>
	</screen>"""

#obrazovka pro vstup znaku z virtualni klavesnice - SD rozliseni
#self.skinName = ["CSFDVirtualKeyBoardSD", "CSFDVirtualKeyBoard"]
Screen_CSFDVirtualKeyBoardSD = """
	<screen name="CSFDVirtualKeyBoardSD" position="center,center" size="720,560" zPosition="99"	 backgroundColor="#31000000" title="Virtuální klávesnice pro CSFD">
		<widget name="header" position="0,30" size="720,30" font="Regular;24" foregroundColor="#cccccc" transparent="1" noWrap="1" halign="center" backgroundColor="#31000000" />
		<widget name="text" position="110,90" size="536,46" font="Regular;26" foregroundColor="#cccccc" transparent="1" noWrap="1" halign="right" backgroundColor="#31000000" />
		<widget name="list" position="100,170" size="540,225" selectionDisabled="1" foregroundColor="#cccccc" transparent="1" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" />
		<widget name="countryFlag" position="340,440" size="60,40" backgroundColor="#31000000" alphatest="on" />
		<eLabel text="Žlutým tlačítkem změníte jazyk pro klávesnici" position="0,510" size="720,23" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" valign="center" halign="center" transparent="1"/>
	</screen>"""

#obrazovka pro vstup znaku z virtualni klavesnice - HD rozliseni
#self.skinName = ["CSFDVirtualKeyBoardHD", "CSFDVirtualKeyBoard"]
Screen_CSFDVirtualKeyBoardHD = """
	<screen name="CSFDVirtualKeyBoardHD" position="center,center" size="720,560" zPosition="99"	 backgroundColor="#31000000" title="Virtuální klávesnice pro CSFD">
		<widget name="header" position="0,30" size="720,30" font="Regular;24" foregroundColor="#cccccc" transparent="1" noWrap="1" halign="center" backgroundColor="#31000000" />
		<widget name="text" position="110,90" size="536,46" font="Regular;26" foregroundColor="#cccccc" transparent="1" noWrap="1" halign="right" backgroundColor="#31000000" />
		<widget name="list" position="100,170" size="540,225" selectionDisabled="1" foregroundColor="#cccccc" transparent="1" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" />
		<widget name="countryFlag" position="340,440" size="60,40" backgroundColor="#31000000" alphatest="on" />
		<eLabel text="Žlutým tlačítkem změníte jazyk pro klávesnici" position="0,510" size="720,23" font="Regular;22" foregroundColor="#f0b400" backgroundColor="#31000000" valign="center" halign="center" transparent="1"/>
	</screen>"""

#obrazovka pro vstup znaku z virtualni klavesnice - FullHD rozliseni
#self.skinName = ["CSFDVirtualKeyBoardFullHD", "CSFDVirtualKeyBoard"]
Screen_CSFDVirtualKeyBoardFullHD = """
	<screen name="CSFDVirtualKeyBoardFullHD" position="center,center" size="1070,840" zPosition="99"  backgroundColor="#31000000" title="Virtuální klávesnice pro CSFD">
		<widget name="header" position="0,45" size="1070,45" font="Regular;26" foregroundColor="#cccccc" transparent="1" noWrap="1" halign="center" backgroundColor="#31000000" />
		<widget name="text" position="135,135" size="800,34" font="Regular;28" foregroundColor="#cccccc" transparent="1" noWrap="1" halign="right" backgroundColor="#31000000" />
		<widget name="list" position="145,255" size="780,325" selectionDisabled="1" foregroundColor="#cccccc" transparent="1" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" />
		<widget name="countryFlag" position="505,660" size="60,40" backgroundColor="#31000000" alphatest="on" />
		<eLabel text="Žlutým tlačítkem změníte jazyk pro klávesnici" position="0,765" size="1070,26" font="Regular;24" foregroundColor="#f0b400" backgroundColor="#31000000" valign="center" halign="center" transparent="1"/>
	</screen>"""

#obrazovka pro zadani textu - SD rozliseni
#self.skinName = ["CSFDInputTextSD", "CSFDInputText"]
Screen_CSFDInputTextSD = """
	<screen name="CSFDInputTextSD" position="center,100" size="680,100" zPosition="0" backgroundColor="#31000000" title="CSFD">
		<widget name="config" position="20,10" size="640,50" foregroundColor="#cccccc" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" transparent="1" />
	</screen>"""

#obrazovka pro zadani textu - HD rozliseni
#self.skinName = ["CSFDInputTextHD", "CSFDInputText"]
Screen_CSFDInputTextHD = """
	<screen name="CSFDInputTextSD" position="center,100" size="680,100" zPosition="0" backgroundColor="#31000000" title="CSFD">
		<widget name="config" position="20,10" size="640,50" foregroundColor="#cccccc" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" transparent="1" />
	</screen>"""

#obrazovka pro zadani textu - FullHD rozliseni
#self.skinName = ["CSFDInputTextFullHD", "CSFDInputText"]
Screen_CSFDInputTextFullHD = """
	<screen name="CSFDInputTextFullHD" position="center,150" size="1010,150" zPosition="0" backgroundColor="#31000000" title="CSFD">
		<widget name="config" position="30,15" size="950,75" foregroundColor="#cccccc" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" transparent="1" />
	</screen>"""

#obrazovka pro zadani textu - pro cast s napovedou resp. aktualne vybranym znakem - SD rozliseni
#self.skinName = ["CSFDNumericalTextInputHelpDialogSD", "CSFDNumericalTextInputHelpDialog"]
Screen_CSFDNumericalTextInputHelpDialogSD = """
	<screen name="CSFDNumericalTextInputHelpDialogSD" position="center,380" size="680,164" zPosition="20" backgroundColor="#00000000" flags="wfNoBorder" >
		<widget name="key1" position="10,2" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key2" position="230,2" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key3" position="450,2" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key4" position="10,42" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key5" position="230,42" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key6" position="450,42" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key7" position="10,82" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key8" position="230,82" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key9" position="450,82" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="help1" position="10,122" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key0" position="230,122" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="help2" position="450,122" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro zadani textu - pro cast s napovedou resp. aktualne vybranym znakem - HD rozliseni
#self.skinName = ["CSFDNumericalTextInputHelpDialogHD", "CSFDNumericalTextInputHelpDialog"]
Screen_CSFDNumericalTextInputHelpDialogHD = """
	<screen name="CSFDNumericalTextInputHelpDialogHD" position="center,380" size="680,164" zPosition="20" backgroundColor="#00000000" flags="wfNoBorder" >
		<widget name="key1" position="10,2" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key2" position="230,2" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key3" position="450,2" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key4" position="10,42" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key5" position="230,42" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key6" position="450,42" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key7" position="10,82" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key8" position="230,82" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key9" position="450,82" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="help1" position="10,122" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key0" position="230,122" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="help2" position="450,122" size="220,40" font="Regular;20" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro zadani textu - pro cast s napovedou resp. aktualne vybranym znakem - FullHD rozliseni
#self.skinName = ["CSFDNumericalTextInputHelpDialogFullHD", "CSFDNumericalTextInputHelpDialog"]
Screen_CSFDNumericalTextInputHelpDialogFullHD = """
	<screen name="CSFDNumericalTextInputHelpDialogFullHD" position="center,450" size="1240,296" zPosition="20" backgroundColor="#00000000" flags="wfNoBorder" >
		<widget name="key1" position="20,3" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key2" position="420,3" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key3" position="820,3" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key4" position="20,63" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key5" position="420,63" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key6" position="820,63" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key7" position="20,123" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key8" position="420,123" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key9" position="820,123" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="help1" position="20,183" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="key0" position="420,183" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
		<widget name="help2" position="820,183" size="400,60" font="Regular;28" halign="center" valign="center" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#obrazovka pro vyber TV kanalu z pluginu (EPG) - SD rozliseni
#self.skinName = ["CSFDSimpleChannelSelectionSD", "SimpleChannelSelection"]
Screen_CSFDSimpleChannelSelectionSD = """
	<screen name="CSFDSimpleChannelSelectionSD" position="center,center" size="605,490" backgroundColor="#31000000" title="Channel Selection">
		<widget name="list" position="9,5" size="587,430" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" enableWrapAround="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="9,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="158,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="307,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="456,443" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="9,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="158,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="307,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="456,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro vyber TV kanalu z pluginu (EPG) - HD rozliseni
#self.skinName = ["CSFDSimpleChannelSelectionHD", "SimpleChannelSelection"]
Screen_CSFDSimpleChannelSelectionHD = """
	<screen name="CSFDSimpleChannelSelectionHD" position="center,100" size="1100,560" backgroundColor="#31000000" title="Channel Selection">
		<widget name="list" position="10,20" size="1080,475" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" enableWrapAround="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="5,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="280,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="555,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="830,508" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="5,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="280,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="555,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="830,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro vyber TV kanalu z pluginu (EPG) - FullHD rozliseni
#self.skinName = ["CSFDSimpleChannelSelectionFullHD", "SimpleChannelSelection"]
Screen_CSFDSimpleChannelSelectionFullHD = """
	<screen name="CSFDSimpleChannelSelectionFullHD" position="center,center" size="1635,840" backgroundColor="#31000000" title="Channel Selection">
		<widget name="list" position="15,30" size="1600,713" serviceItemHeight="31" serviceNameFont="Regular;28" serviceInfoFont="Regular;28" serviceNumberFont="Regular;28" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" enableWrapAround="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="72,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="481,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="890,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="1299,762" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="72,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="481,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="890,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="1299,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro vyber poradu z EPG - SD rozliseni
#self.skinName = ["CSFDEPGSelectionSD", "EPGSelection"]
Screen_CSFDEPGSelectionSD = """
	<screen name="CSFDEPGSelectionSD" position="center,center" size="605,490" zPosition="0" backgroundColor="#31000000" title="EPG Selection">
		<widget name="list" position="9,5" size="587,430" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" enableWrapAround="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="9,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="158,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="307,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="456,443" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="9,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="158,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="307,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="456,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro vyber poradu z EPG - HD rozliseni
#self.skinName = ["CSFDEPGSelectionHD", "EPGSelection"]
Screen_CSFDEPGSelectionHD = """
	<screen name="CSFDEPGSelectionHD" position="center,100" size="1100,560" zPosition="0" backgroundColor="#31000000" title="EPG Selection">
		<eLabel backgroundColor="#31000000" position="759,20" size="1,475" />
		<widget name="list" position="20,20" size="740,475" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" enableWrapAround="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="5,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="280,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="555,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="830,508" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="5,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="280,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="555,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="830,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro vyber poradu z EPG - FullHD rozliseni
#self.skinName = ["CSFDEPGSelectionFullHD", "EPGSelection"]
Screen_CSFDEPGSelectionFullHD = """
	<screen name="CSFDEPGSelectionFullHD" position="center,center" size="1635,840" zPosition="0" backgroundColor="#31000000" title="EPG Selection">
		<eLabel backgroundColor="#31000000" position="1126,30" size="2,713" />
		<widget name="list" position="30,30" size="1100,713" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" enableWrapAround="1" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" transparent="1" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="72,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="481,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="890,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="1299,762" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="72,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="481,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="890,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="1299,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
	</screen>"""

#obrazovka pro instalace a konzolove prikazy - SD rozliseni
#self.skinName = ["CSFDConsoleSD", "CSFDConsole"]
Screen_CSFDConsoleSD = """
	<screen name="CSFDConsoleSD" position="center,center" size="550,400" title="Console" zPosition="0" backgroundColor="#31000000">
		<widget name="text" position="0,0" size="550,400" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;21" />
	</screen>"""

#obrazovka pro instalace a konzolove prikazy - HD rozliseni
#self.skinName = ["CSFDConsoleHD", "CSFDConsole"]
Screen_CSFDConsoleHD = """
	<screen name="CSFDConsoleHD" position="center,center" size="1100,550" title="Console" zPosition="0" backgroundColor="#31000000">
		<widget name="text" position="0,0" size="1100,550" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;21" />
	</screen>"""

#obrazovka pro instalace a konzolove prikazy - FullHD rozliseni
#self.skinName = ["CSFDConsoleFullHD", "CSFDConsole"]
Screen_CSFDConsoleFullHD = """
	<screen name="CSFDConsoleFullHD" position="center,center" size="1635,920" title="Console" zPosition="0" backgroundColor="#31000000">
		<widget name="text" position="0,0" size="1635,920" zPosition="1" foregroundColor="#cccccc" backgroundColor="#31000000" transparent="1" font="Regular;28" />
	</screen>"""

#Help menu - SD rozliseni
#self.skinName = ["CSFDHelpMenuSD", "CSFDHelpMenu"]
Screen_CSFDHelpMenuSD = """
	<screen name="CSFDHelpMenuSD" position="center,center" size="720,576" title="Menu" backgroundColor="#31000000" flags="wfNoBorder"> 
		<eLabel text="help..." position="30,40" size="220,60" font="Regular;30" backgroundColor="#31000000" transparent="1" />
		<widget name="list" position="30,100" size="470,380" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" />
		<widget name="rc" pixmaps="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc0.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc1.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc2.png" position="540,10" zPosition="10" size="154,500" alphatest="on" />
		<widget name="arrowdown" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowdown.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowdown2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowdown.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowup" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowup.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowup2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowup.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="long_key" position="530,520" size="174,50" font="Regular;25" halign="center" foregroundColor="yellow" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#Help menu - HD rozliseni
#self.skinName = ["CSFDHelpMenuHD", "CSFDHelpMenu"]
Screen_CSFDHelpMenuHD = """
	<screen name="CSFDHelpMenuHD" position="center,center" size="1100,613" title="Menu" backgroundColor="#31000000" flags="wfNoBorder"> 
		<eLabel text="help..." position="30,40" size="336,60" font="Regular;40" backgroundColor="#31000000" transparent="1" />
		<widget name="list" position="30,100" size="738,410" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" />
		<widget name="rc" pixmaps="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc0.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc1.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc2.png" position="826,40" zPosition="10" size="154,500" alphatest="on" />
		<widget name="arrowdown" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowdown.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowdown2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowdown.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowup" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowup.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowup2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowup.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="long_key" position="815,540" size="174,50" font="Regular;25" halign="center" foregroundColor="yellow" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#Help menu - FullHD rozliseni
#self.skinName = ["CSFDHelpMenuFullHD", "CSFDHelpMenu"]
Screen_CSFDHelpMenuFullHD = """
	<screen name="CSFDHelpMenuFullHD" position="center,center" size="1635,920" title="Menu" backgroundColor="#31000000" flags="wfNoBorder"> 
		<eLabel text="help..." position="45,60" size="500,90" font="Regular;50" backgroundColor="#31000000" transparent="1" />
		<widget name="list" position="45,150" size="1020,684" scrollbarMode="showOnDemand" backgroundColor="#31000000" transparent="1" />
		<widget name="rc" pixmaps="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc0_fhd.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc1_fhd.png,/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/rc2_fhd.png" position="1225,60" zPosition="10" size="231,750" alphatest="on" />
		<widget name="arrowdown" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowdown.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowdown2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowdown.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowup" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowup.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="arrowup2" pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/arrowup.png" position="-100,-100" zPosition="11" size="37,70" alphatest="on" />
		<widget name="long_key" position="1210,820" size="258,75" font="Regular;30" halign="center" foregroundColor="yellow" backgroundColor="#31000000" transparent="1" />
	</screen>"""

#Titulky - SD rozliseni
#self.skinName = ["CSFDSubtitleDisplaySD", "CSFDSubtitleDisplay"]
Screen_CSFDSubtitleDisplaySD = """
	<screen name="CSFDSubtitleDisplaySD" position="0,0" size="%s,%s" zPosition="-1" backgroundColor="transparent" flags="wfNoBorder">
		<widget name="delay" position="%s,%s" size="140,35" valign="center" halign="center" font="Regular;30" transparent="1" foregroundColor="yellow" backgroundColor="transparent" shadowColor="#40101010" shadowOffset="3,3" />
		<widget name="subtitles" position="0,%s" size="%s,%s" valign="center" halign="center" font="%s;%s" transparent="1" foregroundColor="%s" backgroundColor="transparent" shadowColor="#40101010" shadowOffset="3,3" />
	</screen>"""

#Titulky - HD rozliseni
#self.skinName = ["CSFDSubtitleDisplayHD", "CSFDSubtitleDisplay"]
Screen_CSFDSubtitleDisplayHD = """
	<screen name="CSFDSubtitleDisplayHD" position="0,0" size="%s,%s" zPosition="-1" backgroundColor="transparent" flags="wfNoBorder">
		<widget name="delay" position="%s,%s" size="140,35" valign="center" halign="center" font="Regular;30" transparent="1" foregroundColor="yellow" backgroundColor="transparent" shadowColor="#40101010" shadowOffset="3,3" />
		<widget name="subtitles" position="0,%s" size="%s,%s" valign="center" halign="center" font="%s;%s" transparent="1" foregroundColor="%s" backgroundColor="transparent" shadowColor="#40101010" shadowOffset="3,3" />
	</screen>"""

#Titulky - FullHD rozliseni
#self.skinName = ["CSFDSubtitleDisplayFullHD", "CSFDSubtitleDisplay"]
Screen_CSFDSubtitleDisplayFullHD = """
	<screen name="CSFDSubtitleDisplayFullHD" position="0,0" size="%s,%s" zPosition="-1" backgroundColor="transparent" flags="wfNoBorder">
		<widget name="delay" position="%s,%s" size="210,55" valign="center" halign="center" font="Regular;45" transparent="1" foregroundColor="yellow" backgroundColor="transparent" shadowColor="#40101010" shadowOffset="3,3" />
		<widget name="subtitles" position="0,%s" size="%s,%s" valign="center" halign="center" font="%s;%s" transparent="1" foregroundColor="%s" backgroundColor="transparent" shadowColor="#40101010" shadowOffset="3,3" />
	</screen>"""

#Menu - titulky - SD rozliseni
#self.skinName = ["CSFDSubsMenuSD", "CSFDSubsMenu"]
Screen_CSFDSubsMenuSD = """
	<screen name="CSFDSubsMenuSD" position="center,center" size="500,400" title="Main Menu" backgroundColor="#31000000">
		<widget name="info_sub" position="0,5" size="500,40" valign="center" halign="center" font="Regular;25" transparent="1" foregroundColor="white" backgroundColor="#31000000" />
		<widget name="info_subfile" position="0,55" size="500,40" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="#DAA520" backgroundColor="#31000000" />
		<widget name="enc_sub" position="0,90" size="100,25" valign="center" halign="left" font="Regular;16" transparent="1" foregroundColor="white" backgroundColor="#31000000" />
		<widget name="enc_subfile" position="110,90" size="200,25" valign="center" halign="left" font="Regular;16" transparent="1" foregroundColor="#DAA520" backgroundColor="#31000000" />
		<widget name="menu" position="0,125" size="500,275" transparent="1" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
	</screen>"""

#Menu - titulky - HD rozliseni
#self.skinName = ["CSFDSubsMenuHD", "CSFDSubsMenu"]
Screen_CSFDSubsMenuHD = """
	<screen name="CSFDSubsMenuHD" position="center,center" size="500,400" title="Main Menu" backgroundColor="#31000000">
		<widget name="info_sub" position="0,5" size="500,40" valign="center" halign="center" font="Regular;25" transparent="1" foregroundColor="white" backgroundColor="#31000000" />
		<widget name="info_subfile" position="0,55" size="500,40" valign="center" halign="center" font="Regular;22" transparent="1" foregroundColor="#DAA520" backgroundColor="#31000000" />
		<widget name="enc_sub" position="0,90" size="100,25" valign="center" halign="left" font="Regular;16" transparent="1" foregroundColor="white" backgroundColor="#31000000" />
		<widget name="enc_subfile" position="110,90" size="200,25" valign="center" halign="left" font="Regular;16" transparent="1" foregroundColor="#DAA520" backgroundColor="#31000000" />
		<widget name="menu" position="0,125" size="500,275" transparent="1" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
	</screen>"""

#Menu - titulky - FullHD rozliseni
#self.skinName = ["CSFDSubsMenuFullHD", "CSFDSubsMenu"]
Screen_CSFDSubsMenuFullHD = """
	<screen name="CSFDSubsMenuFullHD" position="center,center" size="740,600" title="Main Menu" backgroundColor="#31000000">
		<widget name="info_sub" position="0,7" size="740,60" valign="center" halign="center" font="Regular;38" transparent="1" foregroundColor="white" backgroundColor="#31000000" />
		<widget name="info_subfile" position="0,83" size="740,60" valign="center" halign="center" font="Regular;33" transparent="1" foregroundColor="#DAA520" backgroundColor="#31000000" />
		<widget name="enc_sub" position="0,135" size="150,38" valign="center" halign="left" font="Regular;26" transparent="1" foregroundColor="white" backgroundColor="#31000000" />
		<widget name="enc_subfile" position="165,135" size="300,38" valign="center" halign="left" font="Regular;26" transparent="1" foregroundColor="#DAA520" backgroundColor="#31000000" />
		<widget name="menu" position="5,210" size="730,350" transparent="1" scrollbarMode="showOnDemand" backgroundColor="#31000000" />
	</screen>"""

#Menu config - titulky - SD rozliseni
#self.skinName = ["CSFDSubsSetupSD", "CSFDSubsSetup"]
Screen_CSFDSubsSetupSD = """
	<screen name="CSFDSubsSetupSD" position="center,center" size="605,490" backgroundColor="#31000000" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="9,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="158,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="307,443" size="140,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="456,443" size="140,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="9,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="158,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="307,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="456,453" size="140,28" font="Regular;21" valign="center" halign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="config" position="9,5" size="587,430" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" transparent="1" />
	</screen>"""

#Menu config - titulky - HD rozliseni
#self.skinName = ["CSFDSubsSetupHD", "CSFDSubsSetup"]
Screen_CSFDSubsSetupHD = """
	<screen name="CSFDSubsSetupHD" position="center,100" size="1100,560" backgroundColor="#31000000" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="5,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="280,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="555,508" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="830,508" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="5,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="280,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="555,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="830,515" size="265,28" font="Regular;22" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="config" position="10,20" size="1080,475" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu.png" enableWrapAround="1" transparent="1" />
	</screen>"""

#Menu config - titulky - FullHD rozliseni
#self.skinName = ["CSFDSubsSetupFullHD", "CSFDSubsSetup"]
Screen_CSFDSubsSetupFullHD = """
	<screen name="CSFDSubsSetupFullHD" position="center,center" size="1635,840" backgroundColor="#31000000" >
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="72,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="481,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="890,762" size="265,44" zPosition="1" alphatest="on" />
		<ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/select_tv.png" position="1299,762" size="265,44" zPosition="1" alphatest="on" />
		<widget name="key_red" position="72,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="red" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_green" position="481,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="green" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_yellow" position="890,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="#f0b400" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="key_blue" position="1299,762" size="265,44" font="Regular;28" halign="center" valign="center" foregroundColor="blue" backgroundColor="#31000000" zPosition="2" transparent="1" />
		<widget name="config" position="15,30" size="1600,713" foregroundColor="#cccccc" scrollbarMode="showOnDemand" backgroundColor="#31000000" backgroundColorSelected="#31000000" foregroundColorSelected="#006cbcf0" selectionPixmap="/usr/lib/enigma2/python/Plugins/Extensions/CSFD/icons/selected-menu-fhd.png" enableWrapAround="1" transparent="1" />
	</screen>"""


#***************************************************************************************************************************************************************************************
#NASTAVENI NEKTERYCH BAREV, KTERE NELZE ZMENIT VE SKINU JEDNOTLIVYCH OBRAZOVEK

#obarvovani textu podle urovne hodnoceni poradu
CSFDratingColor_0 = 0x6C7373
CSFDratingColor_50 = 0x0064C7
CSFDratingColor_100 = 0xF23D21
#CSFDratingColor_Nothing = 0xCCCCCC
CSFDratingColor_Nothing = 0xFFCC99
#uplatni se v pripade nastaveni polozky "Design CSFD obrazovek" na "Barvy stejné bez ohledu na hodnocení + zvýraznění kategorií"
CSFDratingColor_HighlightKeyWords = 0xF0B400

#obarvovani hlavnich zahlavi - napr. v detailu komentaru apod.
CSFDColor_Titel = 0xF0B400

#obarvovani textu sekci v Historii pluginu - pokud text zacina na "Díky za pomoc"
CSFDColor_Highlight = 0x1E90FF

#obarvovani textu ratingu pro IMDB hodnoceni
CSFDColor_IMDB = 0xF0B400
#obarvovani textu ratingu pro Metacritic hodnoceni
CSFDColor_Metacritic = 0x008000

#obarvovani textu v zalozkach v Nastavenich - nevybrane sekce
CSFDColor_Tab = 0xCCCCCC
#obarvovani textu v zalozkach v Nastavenich - vybrana sekce
CSFDColor_Sel_Tab = 0x6CBCF0

#obarvovani textu v instalacich
CSFDColor_Console_Titel = 0xF0B400
CSFDColor_Console_Command = 0x238341

#***************************************************************************************************************************************************************************************
