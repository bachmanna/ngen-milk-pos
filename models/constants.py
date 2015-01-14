class BaseType(object):
    @classmethod
    def _get_keys(cls):
        keys = []
        for x in dir(cls):
            if x[:1] != '_':
                keys.append(x)
        return keys


class CattleType(BaseType):
    COW = "C"
    BUFFALO = "B"


class CollectionShift(BaseType):
    MORNING = "M"
    EVENING = "E"


class SalesRate(BaseType):
    COW = "SALESRATE_COW"
    BUFFALO = "SALESRATE_BUFFALO"


class CollectionRateType(BaseType):
    FAT = "FAT"
    FAT_AND_SNF = "FAT_AND_SNF"
    TS_1 = "TS_1"
    TS_2 = "TS_2"


class ScaleType(BaseType):
    HEAVY = "HEAVY"


class AnalyzerType(BaseType):
    TVS = "TVS"


class SystemSettings(BaseType):
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

