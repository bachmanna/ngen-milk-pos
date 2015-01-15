import gobject
import gtk

from models import *
from configuration_manager import ConfigurationManager


class SettingsUI:
    def __init__(self, parent, navigate):
        self.navigate = navigate
        self.parent = parent
        self.builder = gtk.Builder()
        self.builder.add_from_file("resources/glade/system_settings.glade")
        self.container = self.builder.get_object("settingContainer")

        self.btnSave = self.builder.get_object("btnSettingsSave")
        self.btnSave.connect("clicked", self.save)

        self.load_combobox_values()
        self.load_settings()

        self.parent.add(self.container)
        self.container.show()
        pass

    def set_combobox_values(self, obj_id, values):
        combobox = self.builder.get_object(obj_id)
        store = gtk.ListStore(gobject.TYPE_STRING)

        for x in values:
            store.append([x])

        combobox.set_model(store)
        combobox.set_active(0)

        cell = gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, "text", 0)
        pass

    def get_control_value(self, obj_id):
        control = self.builder.get_object(obj_id)
        value = None
        if isinstance(control, gtk.ComboBox):
            value = control.get_active_text()
        elif isinstance(control, gtk.CheckButton):
            value = control.get_active()

        return value

    def save(self, obj):
        settings = {}
        settings[SystemSettings.SCALE_TYPE] = self.get_control_value("cbScaleType")
        settings[SystemSettings.ANALYZER_TYPE] = self.get_control_value("cbAnalyzerType")
        settings[SystemSettings.RATE_TYPE] = self.get_control_value("cbRateType")
        settings[SystemSettings.COLLECTION_PRINTER_TYPE] = self.get_control_value("cbCollectionPrinterType")

        settings[SystemSettings.BILL_OVERWRITE] = self.get_control_value("chkBillOverwrite")
        settings[SystemSettings.MANUAL_FAT] = self.get_control_value("chkManualFAT")
        settings[SystemSettings.MANUAL_SNF] = self.get_control_value("chkManualSNF")
        settings[SystemSettings.MANUAL_QTY] = self.get_control_value("chkManualQTY")
        settings[SystemSettings.PRINT_CLR] = self.get_control_value("chkPrintCLR")
        settings[SystemSettings.PRINT_WATER] = self.get_control_value("chkPrintWater")
        settings[SystemSettings.PRINT_BILL] = self.get_control_value("chkPrintBill")
        settings[SystemSettings.QUANTITY_2_DECIMAL] = self.get_control_value("chkQuantity2Decimal")
        settings[SystemSettings.EXTERNAL_DISPLAY] = self.get_control_value("chkExternalDisplay")

        config_manager = ConfigurationManager()
        config_manager.set_all_settings(settings)
        self.destroy()
        pass

    def destroy(self):
        if self.navigate:
            self.navigate.back()
        pass

    def load_settings(self):
        config_manager = ConfigurationManager()
        settings = config_manager.get_all_settings()

        self.set_control_value("cbScaleType", settings[SystemSettings.SCALE_TYPE])
        self.set_control_value("cbAnalyzerType", settings[SystemSettings.ANALYZER_TYPE])
        self.set_control_value("cbRateType", settings[SystemSettings.RATE_TYPE])
        self.set_control_value("cbCollectionPrinterType", settings[SystemSettings.COLLECTION_PRINTER_TYPE])

        self.set_control_value("chkBillOverwrite", settings[SystemSettings.BILL_OVERWRITE])
        self.set_control_value("chkManualFAT", settings[SystemSettings.MANUAL_FAT])
        self.set_control_value("chkManualSNF", settings[SystemSettings.MANUAL_SNF])
        self.set_control_value("chkManualQTY", settings[SystemSettings.MANUAL_QTY])
        self.set_control_value("chkPrintCLR", settings[SystemSettings.PRINT_CLR])
        self.set_control_value("chkPrintWater", settings[SystemSettings.PRINT_WATER])
        self.set_control_value("chkPrintBill", settings[SystemSettings.PRINT_BILL])
        self.set_control_value("chkQuantity2Decimal", settings[SystemSettings.QUANTITY_2_DECIMAL])
        self.set_control_value("chkExternalDisplay", settings[SystemSettings.EXTERNAL_DISPLAY])


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

    def load_combobox_values(self):
        self.set_combobox_values("cbScaleType", ScaleType._get_keys())
        self.set_combobox_values("cbAnalyzerType", AnalyzerType._get_keys())
        self.set_combobox_values("cbRateType", CollectionRateType._get_keys())
        self.set_combobox_values("cbCollectionPrinterType", CollectionPrinterType._get_keys())
