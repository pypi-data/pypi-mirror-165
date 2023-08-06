from abc import abstractmethod
import pyodbc
from .models.model import ClientModel

class DatabaseClient(ClientModel):
    ''' database client is a client model that is used to get data from a database '''
    def __init__(self, server, database, username, password, driver_location, *args, **kwargs):
        self.server=server
        self.database=database
        self.username=username
        self.password=password
        self.driver_location=driver_location
        if self.database_type().lower() == "mssql":
            self.cnxn = pyodbc.connect(
                "DRIVER="+str(driver_location)+";"+
                "SERVER="+str(server)+";"+
                "DATABASE="+str(database)+";"+
                "UID="+str(username)+";"+
                "PWD="+str(password)+";"
            , timeout=5)
            self.cursor = self.cnxn.cursor()
        else:
            self.cursor=self.get_cursor_from_database(
                self.server,
                self.database,
                self.username,
                self.password,
                self.driver_location
            )
        super().__init__(*args, **kwargs)

    @abstractmethod
    def database_type(self):
        ''' abstract method to get the database type '''
        return "MSSQL"

    def get_cursor_from_database(self,
        server:str,
        database:str,
        username:str,
        password:str,
        driver_location:str
    ):
        ''' get the cursor from the database '''
        raise NotImplementedError("get_cursor_from_database is not implemented")

    def fetchall(self, query:str):
        ''' fetch all the rows from the database '''
        self.cursor.execute(query)
        row_all = self.cursor.fetchall()
        return row_all

    def fetchone(self, query:str):
        ''' fetch one row from the database '''
        self.cursor.execute(query)
        row = self.cursor.fetchone()
        return row
