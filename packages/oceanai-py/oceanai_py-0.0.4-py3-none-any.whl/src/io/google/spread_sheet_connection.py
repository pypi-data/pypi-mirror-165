from src.io.google.google_api_connection import GoogleAPIConnector,GoogleCredentials

class SheetDataRequestArgs():
    
    def __init__(self) -> None:
        self.spreadSheetId = ""
        self.sheet = ""
        self.fromColumn = ""
        self.toColumn = ""
        self.fromRow = 0
        self.toRow = 0
        
class SpreadSheetConnection():
    
    def __init__(self,connection:GoogleAPIConnector) -> None:
        self.connection = connection
        self. sheets = None
        
    