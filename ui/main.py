import gtk
import pango

from configuration_manager import ConfigurationManager, ResourceFilesConstants
from models import *
from ui.MainMenuUI import MainMenuUI


class PosMain:
    key_maps = {
        65360: "MainMenuUI",  # HOME
        65476: "MainMenuUI",  #F7
        65470: "CollectionUI",  #F1
        65471: "SalesUI",  #F2
        65472: "BasicSetupUI",  #F3
        65473: "SystemSetupUI",  #F4
        65474: "ReportsUI",  #F5
        65475: "DataResetUI",  #F6
    }

    def __init__(self):
        self.builder = gtk.Builder()
        self.currentPage = None
        self.previousPage = None

        config_manager = ConfigurationManager()
        settings = config_manager.get_all_settings()

        self.builder.add_from_file(ResourceFilesConstants.HOME_GLADE_FILE)
        self.builder.connect_signals(self)

        self.window = self.builder.get_object("mainWindow")
        self.window.connect('key-press-event', self.keypress)
        self.window.connect("destroy", self.destroy)

        self.mainContainer = self.builder.get_object("mainContainer")
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("white"))

        self.builder.get_object("vbox1").connect('expose-event', self.draw_pixbuf)

        # set colors
        hc = self.builder.get_object("headerContainer")
        hc.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#1eb3d9"))

        self.builder.get_object("breadcrumbContainer").modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ad85cc"))
        self.builder.get_object("footerContainer").modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("#ad85cc"))

        # set logo
        logo = self.builder.get_object("imgLogo")
        logo.set_from_file(ResourceFilesConstants.LOGO_IMAGE_FILE)

        title = self.builder.get_object("lblCompanyName")
        address = self.builder.get_object("lblCompanyAddress")
        date = self.builder.get_object("lblDate")
        time = self.builder.get_object("lblTime")

        if settings[SystemSettings.SOCIETY_NAME]:
            title.set_text(settings[SystemSettings.SOCIETY_NAME])
        if settings[SystemSettings.SOCIETY_ADDRESS]:
            address.set_text(settings[SystemSettings.SOCIETY_ADDRESS])

        title.modify_font(pango.FontDescription("LucidaGrande 36"))
        address.modify_font(pango.FontDescription("LucidaGrande 22"))
        #date.modify_font(pango.FontDescription("sans 16"))
        #time.modify_font(pango.FontDescription("sans 16"))


        self.currentPage = MainMenuUI(self)
        self.change_app_theme(ResourceFilesConstants.GTK_THEME_FILE, self.window)

    def draw_pixbuf(self, widget, event):
        path = ResourceFilesConstants.BG_IMAGE_FILE
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        widget.window.draw_pixbuf(widget.style.bg_gc[gtk.STATE_NORMAL], pixbuf, 0, 0, 0,0)

    def change_app_theme(self, theme_rc_file, win):
        gtk.rc_set_default_files([theme_rc_file])
        gtk.rc_reparse_all_for_settings(gtk.settings_get_default(), True)
        gtk.rc_reset_styles(gtk.settings_get_for_screen(win.get_screen()))
        # gtk.rc_parse(theme_rc_file)
        # screen = self.window.get_screen()
        # settings = gtk.settings_get_for_screen(screen)
        # gtk.rc_reset_styles(settings)


    def destroy(self, widget, data=None):
        gtk.main_quit()


    def show_window(self):
        self.window.show_all()
        # self.window.fullscreen()

    def keypress(self, widget, data=None):
        mod = gtk.accelerator_get_label(data.keyval, data.state)
        print "This key was pressed ", data.keyval, mod
        handled = False

        if self.currentPage and getattr(self.currentPage, "handle_keypress", None) is not None:
            handled = self.currentPage.handle_keypress(widget, data)

        if not handled and data.keyval in self.key_maps.keys():
            page = self.key_maps[data.keyval]
            # if page == "MainMenuUI" or isinstance(self.currentPage, MainMenuUI):
            self.change_page(page)

        return handled

    def btnClicked(self, widget, data=None):
        name = gtk.Buildable.get_name(widget)
        page_name = name[3:]
        self.change_page(page_name)

    def change_page(self, class_name):
        module_name = "ui." + class_name
        m = __import__(module_name, globals(), locals(), class_name)
        c = getattr(m, class_name)

        if c != self.currentPage:
            self.clear_container()
            self.previousPage = self.currentPage
            self.currentPage = c(self)

    def clear_container(self):
        for item in self.mainContainer.get_children():
            self.mainContainer.remove(item)

    def add(self, child):
        self.mainContainer.add(child)