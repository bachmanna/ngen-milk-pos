class BaseType(object):
    @classmethod
    def _get_keys(cls):
        keys = []
        for x in dir(cls):
            if x[:1] != '_':
                keys.append(x)
        return keys


class CattleType(BaseType):
    COW = "COW"
    BUFFALO = "BUFFALO"


class CollectionShift(BaseType):
    MORNING = "MORNING"
    EVENING = "EVENING"


class SalesRate(BaseType):
    COW = "SALESRATE_COW"
    BUFFALO = "SALESRATE_BUFFALO"


class CollectionRateType(BaseType):
    FAT = "FAT"
    FAT_AND_SNF = "FAT_AND_SNF"
    TS_1 = "TS_1"
    TS_2 = "TS_2"


class ScaleType(BaseType):
    SATHIYAM = "SATHIYAM"
    D_SONIC = "D_SONIC"
    ISHATA = "ISHATA"
    OPAL = "OPAL"


class AnalyzerType(BaseType):
    ULTRA = "ULTRA"
    ULTRA_PRO = "ULTRA_PRO"
    LACTO_SCAN = "LACTO_SCAN"
    KSHEERA = "KSHEERA"


class SystemSettings(BaseType):
    LANGUAGE = "LANGUAGE"
    TICKET_WIDTH = "TICKET_WIDTH"
    TICKET_HEIGHT = "TICKET_HEIGHT"
    TICKET_MARGIN = "TICKET_MARGIN"
    TICKET_FONT_SIZE = "TICKET_FONT_SIZE"

    SOCIETY_NAME = "SOCIETY_NAME"
    SOCIETY_ADDRESS = "SOCIETY_ADDRESS"
    SOCIETY_ADDRESS1 = "SOCIETY_ADDRESS1"

    HEADER_LINE1 = "HEADER_LINE1"
    HEADER_LINE2 = "HEADER_LINE2"
    HEADER_LINE3 = "HEADER_LINE3"
    HEADER_LINE4 = "HEADER_LINE4"
    FOOTER_LINE1 = "FOOTER_LINE1"
    FOOTER_LINE2 = "FOOTER_LINE2"

    SCALE_TYPE = "SCALE_TYPE"
    ANALYZER_TYPE = "ANALYZER_TYPE"
    RATE_TYPE = "RATE_TYPE"
    BILL_OVERWRITE = "BILL_OVERWRITE"
    MANUAL_FAT = "MANUAL_FAT"
    MANUAL_SNF = "MANUAL_SNF"
    MANUAL_QTY = "MANUAL_QTY"
    PRINT_CLR = "PRINT_CLR"
    PRINT_WATER = "PRINT_WATER"
    PRINT_BILL = "PRINT_BILL"
    QUANTITY_2_DECIMAL = "QUANTITY_2_DECIMAL"
    EXTERNAL_DISPLAY = "EXTERNAL_DISPLAY"
    COLLECTION_PRINTER_TYPE = "COLLECTION_PRINTER_TYPE"
    DATA_EXPORT_FORMAT = "DATA_EXPORT_FORMAT"

    SEND_SMS = "SEND_SMS"


class CollectionPrinterType(BaseType):
    THERMAL = "THERMAL"
    LPT = "LPT"
    LASER = "LASER"
