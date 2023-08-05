from pymongo import MongoClient
import pandas as pd
from ukupacha.Utils import Utils
from ukupacha.Utils import is_dict, is_list, is_serie, section_exist, table_exists, parse_table, JsonEncoder, oracle_codec_options
from ukupacha.CheckPoint import UkuPachaCheckPoint
from joblib import Parallel, delayed
import traceback
from tqdm import tqdm
import psutil
import json
import sys


class UkuPachaGraph:
    """
    Class to perform the relations in the database across mutiples tables, databases or table spaces.
    """

    def __init__(self, user="system", password="colavudea", dburi="localhost:1521"):
        """
        Constructor to create an UkuPachaGraph Object
        Parameters:
        ----------
        user:str
            Oracle user, by default system, other users can be provided but be sure they have the right permissions in the DB.
        password:str
            Oracle pass for given user
        dburi:str
            Oracle db uri for connector, default "localhost:1521"

        """
        self.utils = Utils(user=user, password=password, dburi=dburi)

    def request_graph(self, data_row, tables, main_table=None, debug=False):
        """
        Recursive algorithm to walk the graph, performing the requests.
        """
        if debug:
            print("="*30)
        if not data_row.empty:
            ndata = []
            if main_table is None:
                ndata.append(data_row)
            else:
                ndata.append({"table": main_table, "data": [data_row]})

            for table_dict in tables:
                table = list(table_dict.keys())[0]
                if debug:
                    print(f"table = {table}")
                    print(list(table_dict.keys()))
                if table_dict[table] is not None:
                    for table_relations in table_dict[table]:
                        db = table_relations["DB"]
                        keys = {}
                        for key in table_relations["KEYS"]:
                            alias = key
                            if '/' in key:
                                tmp_keys = key.split('/')
                                key = tmp_keys[0]
                                alias = tmp_keys[1]
                            try:
                                value = data_row[key]
                                if value is not None:
                                    keys[alias] = value
                                else:
                                    if debug:
                                        print(f"None value for key = {key}")
                                        print(data_row)
                                    keys = None
                            except:
                                if debug:
                                    print("-"*30)
                                    print(f"key = {key}")
                                    print(data_row)
                                keys = None
                                continue
                        # con malas llaves no se ppuede hacer el request
                        # y no se puede continuar en profundidad
                        if keys == None:
                            if debug:
                                print("/"*30)
                            continue
                        sub_tables_dict = table_relations["TABLES"]
                        if debug:
                            print(f"len subtables = {len(sub_tables_dict)}")
                        for sub_table_dict in sub_tables_dict:
                            sub_table = list(sub_table_dict.keys())[0]
                            if debug:
                                print(f"sub_table = {sub_table}")

                            try:
                                sub_table_data = []
                                tmp_data = self.utils.request_register(
                                    db, keys, sub_table)
                                for i, row in tmp_data.iterrows():
                                    req_data = self.request_graph(
                                        row, [sub_table_dict], None, debug)
                                    # sub_table_data.append({"table":sub_table,"data":req_data})
                                    sub_table_data.append(req_data)
                                ndata.append(
                                    {"table": sub_table, "data": sub_table_data, "keys": keys})

                            except:
                                if debug:
                                    print(data_row)
                                    print(
                                        f"db = {db} keys={keys} sub_table={sub_table}")
                                    print("|"*30)
                                continue
                else:
                    if debug:
                        print("*"*30)

            return ndata

    def graph2json(self, fields, regs, filter_function=None):
        """
        Recursive algorithm to parse the graph to a json structure.
        """
        output = {}
        if is_dict(regs):
            table = regs["table"]
            data = regs["data"]
            for i in data:
                value = {}
                if is_serie(i):
                    if table_exists(fields, table):
                        # this allows to jump relatioship tables that are not wanted
                        value = parse_table(fields, table, i, filter_function)
                        output.update(value)
                if is_list(i):
                    last_dict = {}
                    for j in i:
                        if is_serie(j):
                            value = parse_table(
                                fields, table, j, filter_function)

                        if is_dict(j):
                            last_dict = j
                            out = self.graph2json(fields, j, filter_function)
                            value.update(out)
                    if table_exists(fields, table):
                        section = fields[table]["alias"]
                        if section == "":
                            output.update(value)
                        else:
                            if section_exist(section, output.keys()):
                                output[section].append(value)
                            else:
                                output[section] = [value]
                    else:
                        if last_dict:
                            sub_table = last_dict["table"]
                            if table_exists(fields, sub_table):
                                section = fields[sub_table]["alias"]
                                if section == "":
                                    output.update(value)
                                else:
                                    if section_exist(section, output.keys()):
                                        if value:  # value !={}
                                            output[section].append(
                                                value[section][0])
                                    else:
                                        if value:
                                            output[section] = [
                                                value[section][0]]
                            else:
                                if section_exist("unkown", output.keys()):
                                    output["unkown"].append(value)
                                else:
                                    output["unkown"] = [value]
        else:
            for reg in regs:
                out = self.graph2json(fields, reg, filter_function)
                output.update(out)
        return output

    def parse_subsections(self, regs, graph_fields):
        """
        Method to parse subsections for multiple register gotten from the DB.
        """
        sub_section = {}
        for i in graph_fields.keys():
            alias = graph_fields[i]["alias"]
            if "sub_section" in graph_fields[i].keys():
                sub_section[alias] = graph_fields[i]["sub_section"]

        for i in range(len(regs)):
            old_reg = regs[i]
            new_reg = {}
            for j in old_reg.keys():
                if j in sub_section.keys():
                    if sub_section[j] in new_reg.keys():
                        new_reg[sub_section[j]].append({j: old_reg[j]})
                    else:
                        new_reg[sub_section[j]] = [{j: old_reg[j]}]
                else:
                    new_reg[j] = old_reg[j]
            regs[i] = new_reg
        return regs

    def parse_subsection(self, reg, sub_sections):
        """
        Allows to parce the subsection for an specific register from the DB.
        """
        new_reg = {}
        for j in reg.keys():
            if j in sub_sections.keys():
                if sub_sections[j] in new_reg.keys():
                    new_reg[sub_sections[j]].append({j: reg[j]})
                else:
                    new_reg[sub_sections[j]] = [{j: reg[j]}]
            else:
                new_reg[j] = reg[j]
        return new_reg

    def run_graph(self, data, graph_schema, max_threads=None, debug=False):
        """
        Allows to perform the relations for multiple registers in parallel.
        User this with careful, it's doesn´t support checkpoint and the regs are allocate in RAM memory,
        then this cna be expensive.
        """
        if max_threads is None:
            jobs = psutil.cpu_count()
        else:
            jobs = max_threads
        regs = []
        if jobs == 1:
            for i, row in tqdm(data.iterrows(), total=data.shape[0]):
                reg = self.request_graph(
                    row, graph_schema["GRAPH"], main_table=graph_schema["MAIN_TABLE"], debug=0)
                regs.append(reg)
        else:
            regs = Parallel(n_jobs=jobs, backend='threading', verbose=10)(delayed(self.request_graph)(
                row, graph_schema["GRAPH"], main_table=graph_schema["MAIN_TABLE"], debug=0) for i, row in data.iterrows())
        return regs

    def run_graph2json(self, regs, graph_fields, filter_function=None):
        """
        Allows to parse multiple registers from the graph to json and apply the filter function provided by the user.
        """
        output = []
        for reg in regs:
            out = self.graph2json(graph_fields, reg, filter_function)
            output.append(out)
        return output

    def request_graph2mongodb(self, dbclient, db_name, data_row, graph_schema, main_table, graph_fields, sub_sections, filter_function=None, checkpoint=None):
        """
        method to extract the data from Oracle and save the results in MongoDB.
        Allows to:
        * Walk the graph
        * Parse the graph to json
        * Paser subsection to put some information in a specific keys ex: for scienti the field details.
        * do checkpoints
        * save failed registers in a collection_failed.
        """
        tables = graph_schema["GRAPH"]
        try:
            reg = self.request_graph(data_row, tables, main_table)
            raw = self.graph2json(graph_fields, reg, filter_function)
            out = self.parse_subsection(raw, sub_sections)
            dbclient[db_name].get_collection(
                graph_fields[main_table]["alias"], codec_options=oracle_codec_options).insert_one(out)
            if checkpoint:
                ckp_info = graph_schema["CHECKPOINT"]
                reg = {}
                for key in ckp_info["KEYS"]:
                    reg[key] = data_row[key]
                checkpoint.update(
                    db_name, graph_fields[main_table]["alias"], reg)

        except Exception as e:
            failed_collection = graph_fields[main_table]["alias"]+"_failed"
            print(
                f"Error parsing register, record added to the collection = {failed_collection} ")
            error_info = sys.exc_info()
            print(error_info[0])
            print(error_info[1])
            print(traceback.format_exc())
            failed_register = {"register": data_row.to_dict()}
            failed_register["type"] = str(error_info[0])
            failed_register["value"] = str(error_info[1])
            failed_register["traceback"] = traceback.format_exc()
            dbclient[db_name].get_collection(
                failed_collection, codec_options=oracle_codec_options).insert_one(failed_register)

    def run2mongodb(self, data, graph_schema, graph_fields, db_name, mongodb_uri="mongodb://localhost:27017/", max_threads=None, filter_function=None, checkpoint: UkuPachaCheckPoint = None):
        """
        Method to run all in parallel
        """
        sub_sections = {}
        for i in graph_fields.keys():
            alias = graph_fields[i]["alias"]
            if "sub_section" in graph_fields[i].keys():
                sub_sections[alias] = graph_fields[i]["sub_section"]
        dbclient = MongoClient(mongodb_uri)
        if max_threads is None:
            jobs = psutil.cpu_count()
        else:
            jobs = max_threads

        if jobs == 1:
            for i, row in tqdm(data.iterrows(), total=data.shape[0]):
                self.request_graph2mongodb(
                    dbclient, db_name, row, graph_schema, graph_schema["MAIN_TABLE"], graph_fields, sub_sections, filter_function)
        else:
            Parallel(n_jobs=jobs, backend='threading', verbose=10)(delayed(self.request_graph2mongodb)(
                dbclient, db_name, row, graph_schema, graph_schema["MAIN_TABLE"], graph_fields, sub_sections, filter_function, checkpoint) for i, row in data.iterrows())

    def save_json(self, output_file, data):
        """
        Method to save data to json file.
        """
        with open(output_file, 'w') as fp:
            json.dump(data, fp, cls=JsonEncoder, indent=4)

    def run2file(self, output_file, data, graph_schema, graph_fields, max_threads=None, debug=False, save_regs=False, save_raws=False, filter_function=None):
        regs = self.run_graph(data, graph_schema, max_threads, debug)
        if save_regs:
            self.save_json(output_file+".regs.json", regs)

        raws = self.run_graph2json(regs, graph_fields, filter_function)
        if save_raws:
            self.save_json(output_file+".raws.json", raws)

        output = self.parse_subsections(raws, graph_fields)
        self.save_json(output_file, output)
        print(f"Process finished, file {output_file} save")
