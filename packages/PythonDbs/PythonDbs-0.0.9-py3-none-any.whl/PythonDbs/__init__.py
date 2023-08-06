from errno import E2BIG
import sqlite3





class DB(sqlite3.Connection):
    """
    Creates a conection to the database that is passed in
    a temp database is (``":memory:"``)
    """

    def __init__(self,db) -> None:
        self.inst = super().__init__(db)
        self.cur = self.cursor()

   
    def createTableD(self,TableName:str,colums:dict) -> bool:
        """
        creates table by taking a dict 
        eg
        ``{"colum name":"colum type","colum name":"colum type", ...}``
        
        """

        try:
            data = ""
            datal = list()
            for i,t in colums.items():
                datal.append(str(i) + " " + str(t))            
            data = ",".join(datal)
            self.cur.execute(f"create table {TableName}({data});")
            return True
        except sqlite3.OperationalError:
            return False

    
    def createTableS(self,tableName:str,colums:str) -> bool:
        """Creates table by using a string
        eg
        ``"colum name colum type, colum name colum type, ..."``
        """
        
        try:
            self.cur.execute(f"create table {tableName}({colums});")
            
            return True
        except sqlite3.OperationalError:
            return False

    
    def fetchAll(self,TableName:str) -> list:
        self.cur.execute(f"select * from {TableName}")
        return self.cur.fetchall()

    def fetchAllWhere(self,TableName:str,ColName:str,checkVal:str):
        self.cur.execute(f"select * from {TableName} where {ColName}={checkVal}")
        return self.cur.fetchall()

    def fetchAllCol(self,TableName:str,colName:str):
        self.cur.execute(f"select {colName} from {TableName}")
        self.commit()
        return self.cur.fetchall()
        

    def fetchAllColWhere(self,TableName:str,colName:str,cond,val) -> tuple:
        self.cur.execute(f"select {colName} from {TableName} where {cond} = ?",(val,))
        return self.cur.fetchall()
        


    def fetchOne(self,TableName:str) -> tuple:
        self.cur.execute(f"select * from {TableName};")
        return self.cur.fetchone()

        

    def fetchOneWhere(self,TableName:str,cond,val) -> tuple:
        """
        gets one entry from database
        
        
        
        """
        self.cur.execute(f"select * from {TableName} where {cond} = ?",(val,))
        return self.cur.fetchone()

    
    def alterColType(self,TableName:str,colName:str,newType:str) -> bool:
        self.cur.execute(f"select * from {TableName}")
        data = [("yes",1),("no",2)]
        self.cur.execute(f"PRAGMA table_info({TableName});")
        col = self.cur.fetchall() 
        arr = ["?" for i in range(len(col))]
        arr = ",".join(arr)
        colnew = {}
        for i in col:
            if i[1] == colName:
                colnew[i[1]] = newType
            else:
                colnew[i[1]] = i[2]
        print(colnew)
        
        colL = []
        self.cur.execute(f"drop table {TableName};")
        for i,k in colnew.items():
            colL.append(f"{i} {k}")
        final = ",".join(colL)
        print(final)
        self.cur.execute(f"create table {TableName}({final});")
        self.executemany(f"insert into {TableName} values({arr});",data)



        self.commit()

    def delRowWhere(self,TableName:str,cond,val) -> bool:
        self.cur.execute(f"delete from {TableName} where {cond} = ?",(val,))
        self.commit()

    def delTable(self,TableName:str):
        """
        Deletes table from database 
        
        """
        self.cur.execute(f"drop table {TableName};")
        self.commit()




    def alterRowValues(self,TableName:str,valdict:dict,val:str = None,cond:str = None)-> bool:
        """
        key name in dict is name of row and value stroed under key is new value 
        """
        pairs = [f"{i} = {k}" for i,k in valdict.items()]
        final = ",".join(pairs)

        print(final)
        print()

        if cond == None:
            querry = "update " + TableName + " set " + final + ";"
            self.cur.execute(querry)
            self.commit()
        else:
            querry = "update " + TableName + " set " + final + " where " + cond + " = " + val +";"

            print(querry)
            self.cur.execute(querry)
            self.commit()
            
            


    def InsertIntoFullRow(self,TableName,data:list):

        arr = ["?" for i in range(len(data))]
        newarr = []
        for i in range(len(data)):
            if data[i] == "null":
                arr[i] = "null"
            else:
                newarr.append(data[i])
                
        
        
        query = ",".join(arr)

        self.cur.execute(f"insert into {TableName} values({query});",newarr)
        
        self.commit()

    def InsertIntoCols(self,TableName,cols,data:list):
        query1 = ",".join(cols)
        arr = ["?" for i in range(len(data))]
        newarr = []
        for i in range(len(data)):
            if data[i] == "null":
                arr[i] = "null"
            else:
                newarr.append(data[i])
        query2 = ",".join(arr)
        

        self.cur.execute(f"insert into {TableName} ({query1}) values ({query2});",newarr)
        self.cur
        self.commit()

