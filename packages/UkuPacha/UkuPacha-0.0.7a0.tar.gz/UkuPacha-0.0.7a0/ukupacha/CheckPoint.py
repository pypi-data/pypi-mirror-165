from pymongo import MongoClient
from ukupacha.Utils import Utils
from joblib import Parallel, delayed
import pandas as pd
import numpy as np
import time


class UkuPachaCheckPoint:
    def __init__(self, user="system", password="colavudea", dburi="localhost:1521", mongodb_uri="mongodb://localhost:27017/"):
        self.client = MongoClient(mongodb_uri)
        # Oracle utls functions.
        self.utils = Utils(user=user, password=password, dburi=dburi)

    def create(self, keys: list, oracle_db: str, main_table: str, mongo_db: str, mongo_collection: str):
        # Exmplae query="select COD_RH,COD_PRODUCTO from UDEA_CV.EN_PRODUCTO"
        query = "select "
        for key in keys:
            query += key+","
        query = query[0:-1]
        query += f" from {oracle_db}.{main_table}"
        data = self.utils.request(query)
        data["status"] = np.zeros(data.shape[0], dtype=int)
        self.client[mongo_db][f"{mongo_collection}_checkpoint"].drop()
        self.client[mongo_db][f"{mongo_collection}_checkpoint"].insert_many(
            data.to_dict('records'))

    def exists(self, mongo_db: str, mongo_collection: str):
        ckp_col = f"{mongo_collection}_checkpoint"
        return ckp_col in self.client[mongo_db].list_collection_names()

    def drop(self, mongo_db: str, mongo_collection: str):
        self.client[mongo_db][f"{mongo_collection}_checkpoint"].drop()

    def update(self, mongo_db: str, mongo_collection: str, keys: dict):
        #print(mongo_db, mongo_collection,keys)
        self.client[mongo_db][f"{mongo_collection}_checkpoint"].update_one(
            keys, {"$set": {"status": 1}})

    def get_regs(self, mongo_db: str, mongo_collection: str):
        """
        Function to get registers from the ckp collection that are not already downloaded
        """
        ckp_col = self.client[mongo_db][f"{mongo_collection}_checkpoint"]
        ckpdata = list(ckp_col.find({"status": 0}, {"_id": 0, "status": 0}))
        return ckpdata

    def get_data_chunk(self, oracle_db: str, main_table: str, mongo_db: str, mongo_collection: str, chunk: int, chunk_size: int, ckpdata):
        query = f"select * from {oracle_db}.{main_table} WHERE "
        last_chunk = chunk+chunk_size
        if last_chunk > len(ckpdata):
            last_chunk = chunk + last_chunk - len(ckpdata)
        for row in ckpdata[chunk:last_chunk]:
            req_query = " ("
            for key in row.keys():
                req_query += f" {key}='{row[key]}' AND"
            req_query = req_query[0:-3]
            req_query += ") OR"
            query += req_query
        query = query[0:-3]
        data = self.utils.request(query)
        return data

    def get_data_p(self, oracle_db: str, main_table: str, mongo_db: str, mongo_collection: str, chunk_size=300, jobs=2):
        ckpdata = self.get_regs(mongo_db, mongo_collection)
        chunks = Parallel(n_jobs=jobs, backend='threading', verbose=10)(delayed(self.get_data_chunk)(
            oracle_db, main_table, mongo_db, mongo_collection, chunk, chunk_size, ckpdata) for chunk in range(0, len(ckpdata), chunk_size))
        if len(chunks) > 0:
            data = pd.concat(chunks)
        else:
            data = pd.DataFrame()
        return data

    def get_data(self, oracle_db: str, main_table: str, mongo_db: str, mongo_collection: str, chunk_size=300):
        ckpdata = self.get_regs(mongo_db, mongo_collection)
        chunks = []
        for chunk in range(0, len(ckpdata), chunk_size):
            query = f"select * from {oracle_db}.{main_table} WHERE "
            last_chunk = chunk+chunk_size
            if last_chunk > len(ckpdata):
                last_chunk = chunk + last_chunk - len(ckpdata)
            for row in ckpdata[chunk:last_chunk]:
                req_query = " ("
                for key in row.keys():
                    req_query += f" {key}='{row[key]}' AND"
                req_query = req_query[0:-3]
                req_query += ") OR"
                query += req_query
            query = query[0:-3]
            data = self.utils.request(query)
            chunks.append(data)
        if len(chunks) > 0:
            return pd.concat(chunks)
        else:
            return pd.DataFrame()
