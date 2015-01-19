import gobject
import gtk

from models import *
from configuration_manager import ConfigurationManager, ResourceFilesConstants


class TicketSettingsUI:

    def __init__(self, parent):
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file(ResourceFilesConstants.TICKET_SETTINGS_GLADE_FILE)
        self.container = self.builder.get_object("ticketSettingsContainer")

        self.btnSave = self.builder.get_object("btnSaveTicketSettings")
        self.btnSave.connect("clicked", self.save)

        self.load_settings()

        self.parent.add(self.container)
        self.container.show()
        self.builder.get_object("txtHeader1").grab_focus()
        pass

    def save(self, obj):
        settings = self.gather_settings()
        config_manager = ConfigurationManager()
        config_manager.set_all_settings(settings)
        self.set_control_value("txtPreviewTicket", self.get_ticket_template())


    def gather_settings(self):
        settings = {}
        settings[SystemSettings.HEADER_LINE1] = self.get_control_value("txtHeader1")
        settings[SystemSettings.HEADER_LINE2] = self.get_control_value("txtHeader2")
        settings[SystemSettings.HEADER_LINE3] = self.get_control_value("txtHeader3")
        settings[SystemSettings.HEADER_LINE4] = self.get_control_value("txtHeader4")
        settings[SystemSettings.FOOTER_LINE1] = self.get_control_value("txtFooter1")
        settings[SystemSettings.FOOTER_LINE2] = self.get_control_value("txtFooter2")

        settings[SystemSettings.TICKET_WIDTH] = self.get_control_value("txtTicketWidth")
        settings[SystemSettings.TICKET_HEIGHT] = self.get_control_value("txtTicketHeight")
        settings[SystemSettings.TICKET_MARGIN] = self.get_control_value("txtTicketMargin")
        settings[SystemSettings.TICKET_FONT_SIZE] = self.get_control_value("txtTicketFontSize")
        return settings


    def load_settings(self):
        config_manager = ConfigurationManager()
        settings = config_manager.get_all_settings()

        self.set_control_value("txtHeader1", settings[SystemSettings.HEADER_LINE1])
        self.set_control_value("txtHeader2", settings[SystemSettings.HEADER_LINE2])
        self.set_control_value("txtHeader3", settings[SystemSettings.HEADER_LINE3])
        self.set_control_value("txtHeader4", settings[SystemSettings.HEADER_LINE4])
        self.set_control_value("txtFooter1", settings[SystemSettings.FOOTER_LINE1])
        self.set_control_value("txtFooter2", settings[SystemSettings.FOOTER_LINE2])

        self.set_control_value("txtTicketWidth", settings[SystemSettings.TICKET_WIDTH])
        self.set_control_value("txtTicketHeight", settings[SystemSettings.TICKET_HEIGHT])
        self.set_control_value("txtTicketMargin", settings[SystemSettings.TICKET_MARGIN])
        self.set_control_value("txtTicketFontSize", settings[SystemSettings.TICKET_FONT_SIZE])

        self.set_control_value("txtPreviewTicket", self.get_ticket_template())

    def get_control_value(self, obj_id):
        control = self.builder.get_object(obj_id)
        value = None
        if isinstance(control, gtk.ComboBox):
            value = control.get_active_text()
        elif isinstance(control, gtk.CheckButton):
            value = control.get_active()
        elif isinstance(control, gtk.Entry):
            value = control.get_text()
        if value is None:
            value = ""
        return value

    def set_control_value(self, obj_id, value):
        control = self.builder.get_object(obj_id)
        if isinstance(control, gtk.ComboBox):
            model = control.get_model()
            index = 0
            for x in model:
                if model[index][0] == value:
                    control.set_active(index)
                    break
                index += 1
        elif isinstance(control, gtk.CheckButton):
            control.set_active(value == "True")
        elif isinstance(control, gtk.TextView):
            tbuffer = control.get_buffer()
            tbuffer.set_text(str(value))
        elif isinstance(control, gtk.Entry):
            if value is None:
                control.set_text("")
            else:
                control.set_text(str(value))

    def get_ticket_template(self):
        with open(ResourceFilesConstants.TICKET_TEMPLATE_THERMAL_FILE, "r") as template_file:
            template = template_file.read()
            transformed = template
            settings = self.gather_settings()
            for key in settings.keys():
                if settings[key] is not None:
                    transformed = transformed.replace(("{%s}" % key), settings[key])
            return transformed