#!/usr/bin/env python
# coding: utf-8

# In[135]:

import redis
import pyodbc

import numpy as np
import pandas as pd
import sys

import json
import logging
from logging import config
import os
import re
import hashlib

import urllib.parse
import requests

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging()


class ValidationException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)


def get_env():
    return os.getenv("ENV", "dev")


def open_conn(name, data_source_prefix=None):
    if data_source_prefix is None:
        env_server = os.getenv("ODBC_SERVER_" + name.upper(), "")
        env_database = os.getenv("ODBC_DATABASE_" + name.upper(), "")
        env_user = os.getenv("ODBC_UID_" + name.upper(), "")
        env_password = os.getenv("ODBC_PWD_" + name.upper(), "")

        if (env_server != "") and (env_database != "") and (env_user != ""):
            conn_str = 'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format("{ODBC Driver 17 for SQL Server}",
                                                                              env_server,
                                                                              env_database, env_user,
                                                                              env_password)
            return pyodbc.connect(conn_str)
        else:
            file_name = os.getcwd() + "/{}-{}.txt".format(name, get_env())
            prefix = ""
    else:
        file_name = os.getcwd() + "/{}-{}.txt".format(name, get_env())
        prefix = "{}.".format(data_source_prefix)

    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            conn_info = {line.rstrip("\n")[:line.find("=")]: line.rstrip("\n")[line.find("=") + 1:]
                         for line in f.readlines()
                         }
            conn_str = 'DRIVER={};SERVER={};DATABASE={};UID={};PWD={}'.format("{ODBC Driver 17 for SQL Server}",
                                                                                  conn_info[prefix + "server"],
                                                                                  conn_info[prefix + "database"],
                                                                                  conn_info[prefix + "uid"],
                                                                                  conn_info[prefix + "pwd"])
            return pyodbc.connect(conn_str)
    else:
        raise Exception("Cannot open ODBC connection because there is no connection information found at {}".format(file_name))


def open_redis(name=None, data_source_prefix=None):
    if name is None:
        file_name = os.getcwd() + "/redis-{}.txt".format(get_env())
        env_host = os.getenv("REDIS_HOST", "")
        env_port = os.getenv("REDIS_PORT", "")
        env_password = os.getenv("REDIS_PASSWORD", "")
        env_ssl = os.getenv("REDIS_SSL", "False")
        env_strict = os.getenv("REDIS_STRICT", "False")
        prefix = ""
    elif data_source_prefix is None:
        file_name = os.getcwd() + "/{}-{}.txt".format(name, get_env())
        env_host = os.getenv("REDIS_HOST_" + name.upper(), "")
        env_port = os.getenv("REDIS_PORT_" + name.upper(), "")
        env_password = os.getenv("REDIS_PASSWORD_" + name.upper(), "")
        env_ssl = os.getenv("REDIS_SSL_" + name.upper(), "False")
        env_strict = os.getenv("REDIS_STRICT_" + name.upper(), "False")
        prefix = ""
    else:
        file_name = os.getcwd() + "/{}-{}.txt".format(name, get_env())
        env_host = ""
        env_port = ""
        env_password = ""
        env_ssl = "False"
        env_strict = "False"
        prefix = "{}.".format(data_source_prefix)

    if env_host != "":
        if env_strict.lower() == "true":
            return redis.StrictRedis(host=env_host, port=int(env_port) if env_port != "" else 6379, password=env_password,
                                     ssl=bool(env_ssl))
        else:
            return redis.Redis(host=env_host, port=int(env_port) if env_port != "" else 6379, password=env_password, ssl=bool(env_ssl))
    elif os.path.exists(file_name):
        with open(file_name, "r") as f:
            conn_info = {line.rstrip("\n")[:line.find("=")]: line.rstrip("\n")[line.find("=") + 1:] for line in
                         f.readlines()}
        port = int(conn_info[prefix + "port"]) if conn_info.__contains__(prefix + "port") and (conn_info[prefix + "port"] != "") else 6379
        ssl = bool(conn_info[prefix + "ssl"]) if conn_info.__contains__(prefix + "ssl") and (conn_info[prefix + "ssl"] != "") else False
        strict = bool(conn_info[prefix + "strict"]) if conn_info.__contains__(prefix + "strict") and (conn_info[prefix + "strict"] != "") else False
        if strict:
            return redis.StrictRedis(host=conn_info[prefix + "host"], password=conn_info[prefix + "password"], port=port, ssl=ssl)
        else:
            return redis.Redis(host=conn_info[prefix + "host"], password=conn_info[prefix + "password"], port=port, ssl=ssl)
    else:
        raise Exception("Cannot open redis connection because there is no connection information found at {}".format(file_name))


def query_sql(conn, command, *params):
    cursor = conn.cursor()
    if (params is None) or (len(params) == 0):
        cursor.execute(command) 
    else:
        cursor.execute(command.format(*params)) 
    row = cursor.fetchone() 
    nrow = 0
    columns = {}
    while row: 
        if len(columns) == 0:
            for c in range(len(row)):
                columns["col_{}".format(c)] = list()
        for c in range(len(row)):
            columns["col_{}".format(c)].append(row[c])
        nrow += 1
        row = cursor.fetchone()
    df = pd.DataFrame()
    for key in columns.keys():
        df.loc[:, key] = columns[key]
    return df


def exec_sql(conn, command, *params):
    try:
        if (params is None) or (len(params) == 0):
            cursor = conn.execute(command) 
        else:
            cursor = conn.execute(command.format(*params))
        conn.commit()
        return cursor
    except:
        if (params is None) or (len(params) == 0):
            print(command)
        else:
            print(command.format(*params))
        raise Exception("Error has occured during SQL execution. Details: " + str(sys.exc_info()))


def get_md5(text):
    m = hashlib.md5()
    m.update(text.encode('utf-16'))
    return m.digest().hex()


def decode_html(encoded):
    if encoded is None:
        return ""
    else:
        return encoded.replace("&nbsp;", " ").replace("&lt;", "<").replace("&gt", ">").replace("&amp;", "&")


def html_to_plain(html, return_segments=False):
    cursor = 0
    html2 = ""
    while cursor < len(html):
        cha = html[cursor]
        if cha == "<":
            remaining = html[cursor+1:]
            closing_ind = remaining.find(">")
            if closing_ind > 0:
                if not (remaining.startswith("span") or remaining.startswith("/span") or remaining.startswith(
                        "font") or remaining.startswith("/font") or remaining.startswith(
                        "strong") or remaining.startswith("/strong")):
                    html2 += html[cursor:cursor + closing_ind + 2]
                cursor += closing_ind + 2
            else:
                html2 += html[cursor:]
                break
        else:
            opening_ind = html[cursor + 1:].find("<")
            if opening_ind > 0:
                html2 += html[cursor:cursor + opening_ind + 1]
                cursor += opening_ind + 1
            elif opening_ind == 0:
                cursor += 1
            else:
                html2 += html[cursor:]
                break

    cursor = 0
    segments = list()
    nnewline = 0
    nparam = 0
    while cursor < len(html2):
        cha = html2[cursor]
        if cha == "<":
            remaining = html2[cursor+1:]
            closing_ind = remaining.find(">")
            if closing_ind > 0:
                if remaining.startswith("div") or remaining.startswith("tr"):
                    nnewline += 1
                elif remaining.startswith("/div") or remaining.startswith("/tr"):
                    if nnewline > 0:
                        segments.append("\n" * nnewline)
                        nnewline = 0
                elif remaining.startswith("br>") or remaining.startswith("br/>") or remaining.startswith("br />"):
                    segments.append("\n")
                elif remaining.startswith("p") or remaining.startswith("h1") or remaining.startswith(
                        "h2") or remaining.startswith("h3") or remaining.startswith("h4") or remaining.startswith("h5"):
                    segments.append("\n")
                    nparam += 1
                elif remaining.startswith("/p") or remaining.startswith("/h1") or remaining.startswith(
                        "/h2") or remaining.startswith("/h3") or remaining.startswith("/h4") or remaining.startswith("/h5"):
                    segments.append("\n"*nparam)
                    nparam = 0
                cursor += closing_ind + 2
            else:
                break
        else:
            opening_ind = html2[cursor + 1:].find("<")
            if opening_ind > 0:
                segments.append(decode_html(html2[cursor:cursor+opening_ind+1]))
                segments.append("\n" * nparam)
                nparam = 0
                cursor += opening_ind + 1
            elif opening_ind == 0:
                cursor += 1
            else:
                segments.append(decode_html(html2[cursor:]))
                break

    if return_segments:
        return segments
    else:
        return "".join(segments).strip('\n')


def parse_htm(text):
    if (text.find("</div>") > 0) or (text.find("</span>") > 0) or (text.find("</strong>") > 0) or (text.find("<br") > 0) or (text.find("<p") > 0) or (text.find("<table") > 0):
        return html_to_plain(text.replace("\r", "").replace("\n", ""))
    else:
        return text
    
        
def touch_up_col(series, maxlen=None, encode_text_qualifier=False, encode_crlf=False, parse_html=False, fillna=None):
    
    if fillna is not None:
        array = series.fillna(fillna).values
    else:
        array = series.values
        
    if parse_html:
        array = [parse_htm(s) for s in array]
    else:
        array = [s.replace("<p>", "").replace("</p>", "; ").replace("                                 ", " ") for s in array]
        
    if encode_text_qualifier and encode_crlf:
        array = [s.replace("'", "''").replace("\r", "").replace("\n", "; ") for s in array]
    elif encode_text_qualifier:
        array = [s.replace("'", "''") for s in array]
    elif encode_crlf:
        array = [s.replace("\r", "").replace("\n", "; ") for s in array]
        
    if maxlen is not None:
        array = [s[:maxlen] if len(s) > maxlen else s for s in array]
    
    return array


def char_level(txt):
    for word in txt.split():
        for cha in word:
            yield cha


def token_level(txt):
    for word in txt.split(" "):
        yield word.strip(",")


def str_match(text, pattern, take_parts=0):
    if type(pattern) == str:
        pattern = re.compile(pattern)
    
    if text is None:
        return None
    elif (type(text) == list) or (type(text) == np.ndarray) or (type(text) == pd.Series):
        results = [pattern.search(s) for s in text]
        if type(take_parts) == int:
            return [r.group(take_parts) if r is not None else None for r in results]
        elif (type(take_parts) == list) or (type(take_parts) == np.ndarray):
            df = pd.DataFrame()
            for i, p in enumerate(take_parts):
                df["p" + str(p)] = [r.group(p) if r is not None else None for r in results]
            return df
        else:
            return results
    else:
        results = pattern.search(text)
        if results is None:
            return None
        elif type(take_parts) == int:
            return results.group(take_parts)
        elif (type(take_parts) == list) or (type(take_parts) == np.ndarray):
            return [results.group(p) for p in take_parts]
        else:
            return results


ADDR_COMP_PRECEDING = "(?:^|(?<=[\s\.,:<>@\(]))"
ROAD_SYNONYMS = "road|rd|street|st|avenue|ave|av|drive|dr|central|ctrl|circuit|close|crescent|cresent|cres|place|terrace|circle|cir|highway|way|view|boulevard|blvd|lane|ln|link|quay|loop|sector|sect|walk|farmway|Penjuru|Ampat|estate|promenade|heights|height|green|junction|grove|bahru|vale|rise|grande|toa payoh|hill|turn|garden|marine parade"
PARK_SYNONYMS = "industrial estate|park|square|plaza|north|south|east|west|center|centre|vista"
EXACT_ROAD_NAMES = "queensway|keppel distripark|pasir laba"
LEVEL_SYNONYMS = "level|story|storey|floor|lv|basement"
POSTAL_REGEX_CAPTURE = "(?i)" + ADDR_COMP_PRECEDING + "((?:Singapore|SG|S)?\s*[\(\-]?([0-9]{6})\)?)(?![0-9a-zA-Z\-/_])"
BLOCK_PART_WSPACE_CAPTURE = "(?:BLOCK |BLK |BLOCK|BLK|[A-Z]{1,2})?\d+[A-Z]?(?:\s*[/\-]\s*(?:[A-Z]|\d+[A-Z]?)){0,2}(?:[\s,])"
BLOCK_PART_DENSE_CAPTURE = "(?:BLOCK |BLK |BLOCK|BLK|[A-Z]{1,2})?(\d+[A-Z]?(?:[/\-](?:[A-Z]|\d+[A-Z]?)){0,2})(?:[\s,])"
BLOCK_NUM_PART_DENSE_CAPTURE = "(?:BLOCK |BLK |BLOCK|BLK|[A-Z]{1,2})?(\d+(?:[/\-]\d+){0,2})(?:[\s,]?)"
ROAD_NAME_PART = "(?:(?:lorong|lor)\s+\d{1,2}|[A-Z|']+(?:\s+[A-Z|']+)*)\s+"
ROAD_SUFFIX_PART = "\s?(?:\d{1,3}|III|II|I)"
BLOCK_STREET_REGEX1a = "(?i)" + ADDR_COMP_PRECEDING + "(?:" + BLOCK_PART_DENSE_CAPTURE + "|" + BLOCK_NUM_PART_DENSE_CAPTURE + ")[\s,]*(" + ROAD_NAME_PART + "(?:" + ROAD_SYNONYMS + ")(?:" + ROAD_SUFFIX_PART + ")?)(?:[\s\(\)\.,]|$)"
BLOCK_STREET_REGEX1b = "(?i)" + ADDR_COMP_PRECEDING + "(" + ROAD_NAME_PART + "(?:" + ROAD_SYNONYMS + ")(?:" + ROAD_SUFFIX_PART + ")?)(?:[\s\(\)\.,]|$)"
BLOCK_STREET_REGEX2a = "(?i)" + ADDR_COMP_PRECEDING + "(?:" + BLOCK_PART_DENSE_CAPTURE + "|" + BLOCK_NUM_PART_DENSE_CAPTURE + ")[\s,]*((?:" + ROAD_NAME_PART + ")?(?:jalan|jln|lorong|lor|mount|pulau)(?:\s+[A-Z]+)*(?:" + ROAD_SUFFIX_PART + ")?)(?:[\s\(\)\.,]|$)"
BLOCK_STREET_REGEX2b = "(?i)" + ADDR_COMP_PRECEDING + "((?:" + ROAD_NAME_PART + ")?(?:jalan|jln|lorong|lor|mount|pulau)(?:\s+[A-Z]+)*(?:" + ROAD_SUFFIX_PART + ")?)(?:[\s\(\)\.,]|$)"
BLOCK_STREET_REGEX3 = "(?i)" + ADDR_COMP_PRECEDING + "(?:" + BLOCK_PART_DENSE_CAPTURE + "|" + BLOCK_NUM_PART_DENSE_CAPTURE + ")?[\s,]*(" + EXACT_ROAD_NAMES + ")(?:[\s\(\)\.,]|$)"
BLOCK_STREET_REGEX4 = "(?i)" + ADDR_COMP_PRECEDING + "(?:" + BLOCK_PART_DENSE_CAPTURE + "|" + BLOCK_NUM_PART_DENSE_CAPTURE + ")?[\s,]*(" + ROAD_NAME_PART + "(?:" + PARK_SYNONYMS + ")(?:" + ROAD_SUFFIX_PART + ")?)(?:[\s\(\)\.,]|$)"
CORE_UNIT_PART = "B?\d+[A-Z]?\d?(?:[\-/]B?\d*[A-Z]?\d?){0,9}"
UNIT_PART_REGEX = "(?:unit\s|suite\s|#)" + CORE_UNIT_PART + "(?:\s?/\s?#" + CORE_UNIT_PART + "){0,5}"
UNIT_BUILDING_REGEX = "(?i)" + ADDR_COMP_PRECEDING + "(" + UNIT_PART_REGEX + ")(?:([\s,].*)|$)"
LEVEL_SUFFIX_PART = "\s+B?\d+[A-Za-z]?"
LEVEL_BUILDING_REGEX = "(?i)" + ADDR_COMP_PRECEDING + "((?:\d+(?:st|nd|rd|th)\s+)?(?:" + LEVEL_SYNONYMS + ")(?:" + LEVEL_SUFFIX_PART + ")?)(?:([\s,].*)|$)"
MAILBOX_BUILDING_REGEX = "(?i)" + ADDR_COMP_PRECEDING + "(?:mail\sbox|mailbox|box)\s+\d+(?:([\s,].+)|$)"


def to_sg_address_object(addr_text, as_tuple=False, include_unit_level=False):
    postal_code, block1, block2, street, unit_level = None, None, None, None, None
    for line in addr_text.split("\n"):
        match_postal = re.search(POSTAL_REGEX_CAPTURE, line)
        if match_postal is not None:
            postal_code = match_postal[2]

        match_blk_street1a = re.search(BLOCK_STREET_REGEX1a, line)
        if match_blk_street1a is not None:
            block1, block2, street = match_blk_street1a[1], match_blk_street1a[2], match_blk_street1a[3]
        else:
            match_blk_street2a = re.search(BLOCK_STREET_REGEX2a, line)
            if match_blk_street2a is not None:
                block1, block2, street = match_blk_street2a[1], match_blk_street2a[2], match_blk_street2a[3]
            else:
                match_blk_street1b = re.search(BLOCK_STREET_REGEX1b, line)
                if match_blk_street1b is not None:
                    street = match_blk_street1b[1]
                else:
                    match_blk_street2b = re.search(BLOCK_STREET_REGEX2b, line)
                    if match_blk_street2b is not None:
                        street = match_blk_street2b[1]
                    else:
                        match_blk_street3 = re.search(BLOCK_STREET_REGEX3, line)
                        if match_blk_street3 is not None:
                            block1, block2, street = match_blk_street3[1], match_blk_street3[2], match_blk_street3[3]
                        else:
                            match_blk_street4 = re.search(BLOCK_STREET_REGEX4, line)
                            if match_blk_street4 is not None:
                                block1, block2, street = match_blk_street4[1], match_blk_street4[2], match_blk_street4[3]

        if include_unit_level:
            match_unit_building = re.search(UNIT_BUILDING_REGEX, line)
            if match_unit_building is not None:
                unit_level = match_unit_building[1]
            else:
                match_level_building = re.search(LEVEL_BUILDING_REGEX, line)
                if match_level_building is not None:
                    unit_level = match_level_building[1]
                else:
                    match_mailbox_building = re.search(MAILBOX_BUILDING_REGEX, line)
                    if match_mailbox_building is not None:
                        unit_level = match_mailbox_building[1]

    if as_tuple:
        if include_unit_level:
            return block1 if block1 is not None else block2, street, unit_level, postal_code
        else:
            return block1 if block1 is not None else block2, street, postal_code
    else:
        return {
            "text": addr_text,
            "block": block1 if block1 is not None else block2,
            "street": street,
            "unit_level": unit_level,
            "postal_code": postal_code
        }


def extract_sg_address(text):
    if text is None:
        return None
    elif type(text) == str:
        text_arr = np.array([text])
    else:
        text_arr = np.array(text)

    df = pd.DataFrame({"block_road_name": [""] * len(text_arr),
                       "block_number": [""] * len(text_arr),
                       "road_name": [""] * len(text_arr),
                       "postal_code": [""] * len(text_arr)})

    for i in range(len(text_arr)):
        if pd.isna(text_arr[i]) == False:
            block, street, postal_code = to_sg_address_object(text_arr[i], as_tuple=True)
            if (block is None) or (block == ""):
                block_street = street
            else:
                block_street = block + " " + street

            df.iloc[i, :] = [block_street, block, street, postal_code]

    return df.fillna("")


def token_level(txt):
    return txt.split()


def char_level(txt):
    for cha in txt.replace(" ", ""):
        yield cha


def pre_process_sg_addr(addr_text, remove_postal=True):
    processed_text = addr_text.replace("(", " ").replace(")", " ").replace("@", " ").replace(",", " ").replace(" - ", " ").replace("\n",
                                                                                                                                   " ")

    match = re.findall("(?i)((?:" + ROAD_SYNONYMS + ")(?:" + ROAD_SUFFIX_PART + ")?)", processed_text)
    for frag in match:
        space_ind = frag.rfind(" ")
        if space_ind > 0:
            frag1 = frag[:space_ind] + "_" + frag[space_ind + 1:]
            processed_text = processed_text.replace(frag, frag1)

    match = re.search("(?i)(?:" + PARK_SYNONYMS + ")(?:" + ROAD_SUFFIX_PART + ")?", processed_text)
    if match is not None:
        frag = match[0]
        space_ind = frag.rfind(" ")
        if space_ind > 0:
            frag1 = frag[:space_ind] + "_" + frag[space_ind + 1:]
            processed_text = processed_text.replace(frag, frag1)

    match = re.search("(?i)(?:" + LEVEL_SYNONYMS + ")(?:" + LEVEL_SUFFIX_PART + ")", processed_text)
    if match is not None:
        frag = match[0]
        space_ind = frag.rfind(" ")
        if space_ind > 0:
            frag1 = frag[:space_ind] + "_" + frag[space_ind + 1:]
            processed_text = processed_text.replace(frag, frag1)

    if remove_postal:
        match = re.search(POSTAL_REGEX_CAPTURE, processed_text)
        if match is not None:
            processed_text = processed_text.replace(match[0], " ")
        processed_text = processed_text.replace("SINGAPORE", " ").replace("Singapore", " ")

    return processed_text.strip()


SG_CP_DEPOT_TOKEN_VECTORIZER = CountVectorizer(tokenizer=token_level, lowercase=True, stop_words=None, ngram_range=(1, 1), binary=True)
SG_CP_DEPOT_CHAR_VECTORIZER = TfidfVectorizer(tokenizer=char_level, lowercase=True, stop_words=None, ngram_range=(1, 1), binary=True)
SG_CP_PORT_TOKEN_VECTORIZER = CountVectorizer(tokenizer=token_level, lowercase=True, stop_words=None, ngram_range=(1, 1), binary=True)
SG_CP_PORT_CHAR_VECTORIZER = TfidfVectorizer(tokenizer=char_level, lowercase=True, stop_words=None, ngram_range=(1, 1), binary=True)
SG_CP_PORT_DEPOT_TOKEN_VECTORIZER = CountVectorizer(tokenizer=token_level, lowercase=True, stop_words=None, ngram_range=(1, 1), binary=True)
SG_CP_PORT_DEPOT_CHAR_VECTORIZER = TfidfVectorizer(tokenizer=char_level, lowercase=True, stop_words=None, ngram_range=(1, 1), binary=True)

SG_CP_DEPOT_TOKEN_FEATS, SG_CP_DEPOT_CHAR_FEATS, SG_CP_DEPOTS = None, None, None
SG_CP_PORT_TOKEN_FEATS, SG_CP_PORT_CHAR_FEATS, SG_CP_PORTS = None, None, None
SG_CP_PORT_DEPOT_TOKEN_FEATS, SG_CP_PORT_DEPOT_CHAR_FEATS, SG_CP_PORTS_DEPOTS = None, None, None


def match_sg_cp_depot(company_name, address, geo_master, top=1, thresh_sim=0.5):
    global SG_CP_DEPOT_TOKEN_FEATS
    global SG_CP_DEPOT_CHAR_FEATS
    global SG_CP_DEPOTS
    if SG_CP_DEPOT_TOKEN_FEATS is None:
        texts = list()
        if SG_CP_DEPOTS is None:
            latest_key = geo_master.loc[(pd.isna(geo_master["depot_id"]) == False), ["key", "source_id"]].groupby("source_id").last()
            SG_CP_DEPOTS = geo_master[["key", "road", "addr_postal"]].merge(latest_key, on="key", how="inner")
            SG_CP_DEPOTS.columns = ["key", "name", "addr"]
        for i, row in SG_CP_DEPOTS.iterrows():
            name = row["name"]
            addr = row["addr"]
            text = name + " " + pre_process_sg_addr(addr)

            if text != "":
                texts.append(text)

        SG_CP_DEPOT_TOKEN_FEATS = SG_CP_DEPOT_TOKEN_VECTORIZER.fit_transform(texts).toarray()
        SG_CP_DEPOT_CHAR_FEATS = SG_CP_DEPOT_CHAR_VECTORIZER.fit_transform(texts).toarray()

    if (company_name is not None) and (company_name != ""):
        my_addr = pre_process_sg_addr(company_name + " " + address)
    else:
        my_addr = pre_process_sg_addr(address)
    my_token_feats = SG_CP_DEPOT_TOKEN_VECTORIZER.transform([my_addr]).toarray()
    my_char_feats = SG_CP_DEPOT_CHAR_VECTORIZER.transform([my_addr]).toarray()

    t_sim = cosine_similarity(SG_CP_DEPOT_TOKEN_FEATS, my_token_feats).flatten()
    c_sim = cosine_similarity(SG_CP_DEPOT_CHAR_FEATS, my_char_feats).flatten()
    sim = np.mean([t_sim, c_sim], axis=0)

    if top == 1:
        max_ind = np.argmax(sim)
        if sim[max_ind] > thresh_sim:
            return SG_CP_DEPOTS.iat[max_ind, 0], sim[max_ind]
        else:
            return None, 0
    else:
        records = list()
        for i, row in pd.DataFrame({
            "id": SG_CP_DEPOTS.iloc[:, 0],
            "sim": sim
        }).sort_values("sim", ascending=False).head(top).iterrows():
            if row["sim"] > thresh_sim:
                records.append({
                    "depot_id": int(row["id"]),
                    "sim": row["sim"]
                })
        return records


def match_sg_cp_port(port_name, geo_master, top=2, thresh_sim=0.5):
    global SG_CP_PORT_TOKEN_FEATS
    global SG_CP_PORT_CHAR_FEATS
    global SG_CP_PORTS
    if SG_CP_PORT_TOKEN_FEATS is None:
        texts = list()
        if SG_CP_PORTS is None:
            latest_key = geo_master.loc[(pd.isna(geo_master["port_id"]) == False), ["key", "source_id"]].groupby("source_id").last()
            SG_CP_PORTS = geo_master[["key", "road", "addr_postal"]].merge(latest_key, on="key", how="inner")
            SG_CP_PORTS.columns = ["key", "name", "addr"]
        for i, row in SG_CP_PORTS.iterrows():
            name = row["name"]
            text = pre_process_sg_addr(name)

            if text != "":
                texts.append(text)

        SG_CP_PORT_TOKEN_FEATS = SG_CP_PORT_TOKEN_VECTORIZER.fit_transform(texts).toarray()
        SG_CP_PORT_CHAR_FEATS = SG_CP_PORT_CHAR_VECTORIZER.fit_transform(texts).toarray()

    my_name = pre_process_sg_addr(port_name)
    my_token_feats = SG_CP_PORT_TOKEN_VECTORIZER.transform([my_name]).toarray()
    my_char_feats = SG_CP_PORT_CHAR_VECTORIZER.transform([my_name]).toarray()

    t_sim = cosine_similarity(SG_CP_PORT_TOKEN_FEATS, my_token_feats).flatten()
    c_sim = cosine_similarity(SG_CP_PORT_CHAR_FEATS, my_char_feats).flatten()
    sim = np.mean([t_sim, c_sim], axis=0)

    if top == 1:
        max_ind = np.argmax(sim)
        if sim[max_ind] > thresh_sim:
            return SG_CP_PORTS.iat[max_ind, 0], sim[max_ind], t_sim[max_ind], c_sim[max_ind]
        else:
            return None, 0, 0, 0
    else:
        records = list()
        for i, row in pd.DataFrame({
            "id": SG_CP_PORTS.iloc[:, 0],
            "sim": sim
        }).sort_values("sim", ascending=False).head(top).iterrows():
            if row["sim"] > thresh_sim:
                records.append({
                    "port_id": int(row["id"]),
                    "sim": row["sim"]
                })
        return records


def match_sg_cp_depot_or_port(company_name, address, geo_master, top=1, depot_thresh_sim=0.5, port_thresh_sim=0.5):
    global SG_CP_PORT_DEPOT_TOKEN_FEATS
    global SG_CP_PORT_DEPOT_CHAR_FEATS
    global SG_CP_PORTS_DEPOTS
    global SG_CP_DEPOTS
    global SG_CP_PORTS
    if SG_CP_PORT_DEPOT_TOKEN_FEATS is None:
        texts = list()
        if SG_CP_DEPOTS is None:
            latest_key = geo_master.loc[(pd.isna(geo_master["depot_id"]) == False), ["key", "source_id"]].groupby("source_id").last()
            SG_CP_DEPOTS = geo_master[["key", "road", "addr_postal"]].merge(latest_key, on="key", how="inner")
            SG_CP_DEPOTS.columns = ["key", "name", "addr"]
        for i, row in SG_CP_DEPOTS.iterrows():
            name = row["name"]
            addr = row["addr"]
            text = name + " " + pre_process_sg_addr(addr)
            if text != "":
                texts.append(text)
        SG_CP_DEPOTS["type"] = "depot"

        if SG_CP_PORTS is None:
            latest_key = geo_master.loc[(pd.isna(geo_master["port_id"]) == False), ["key", "source_id"]].groupby("source_id").last()
            SG_CP_PORTS = geo_master[["key", "road", "addr_postal"]].merge(latest_key, on="key", how="inner")
            SG_CP_PORTS.columns = ["key", "name", "addr"]
        for i, row in SG_CP_PORTS.iterrows():
            name = row["name"]
            text = pre_process_sg_addr(name)

            if text != "":
                texts.append(text)
        SG_CP_PORTS["addr"] = ""
        SG_CP_PORTS["type"] = "port"

        if SG_CP_PORTS_DEPOTS is None:
            SG_CP_PORTS_DEPOTS = pd.concat([SG_CP_DEPOTS, SG_CP_PORTS], ignore_index=True)

        SG_CP_PORT_DEPOT_TOKEN_FEATS = SG_CP_PORT_DEPOT_TOKEN_VECTORIZER.fit_transform(texts).toarray()
        SG_CP_PORT_DEPOT_CHAR_FEATS = SG_CP_PORT_DEPOT_CHAR_VECTORIZER.fit_transform(texts).toarray()

    if (company_name is not None) and (company_name != ""):
        my_addr = pre_process_sg_addr(company_name + " " + address)
    else:
        my_addr = pre_process_sg_addr(address)
    my_token_feats = SG_CP_PORT_DEPOT_TOKEN_VECTORIZER.transform([my_addr]).toarray()
    my_char_feats = SG_CP_PORT_DEPOT_CHAR_VECTORIZER.transform([my_addr]).toarray()

    t_sim = cosine_similarity(SG_CP_PORT_DEPOT_TOKEN_FEATS, my_token_feats).flatten()
    c_sim = cosine_similarity(SG_CP_PORT_DEPOT_CHAR_FEATS, my_char_feats).flatten()
    sim = np.mean([t_sim, c_sim], axis=0)

    if top == 1:
        max_ind = np.argmax(sim)
        if (SG_CP_PORTS_DEPOTS.iat[max_ind, 3] == "depot") and (sim[max_ind] > depot_thresh_sim):
            return "depot", SG_CP_PORTS_DEPOTS.iat[max_ind, 0], sim[max_ind]
        elif (SG_CP_PORTS_DEPOTS.iat[max_ind, 3] == "port") and (sim[max_ind] > port_thresh_sim):
            return "port", SG_CP_PORTS_DEPOTS.iat[max_ind, 0], sim[max_ind]
        else:
            return None, 0, 0
    else:
        records = list()
        for i, row in pd.DataFrame({
            "type": SG_CP_PORTS_DEPOTS.iloc[:, 3],
            "id": SG_CP_PORTS_DEPOTS.iloc[:, 0],
            "sim": sim
        }).sort_values("sim", ascending=False).head(top).iterrows():
            if (row["type"] == "depot") and (row["sim"] > depot_thresh_sim):
                records.append({
                    "depot_id": int(row["id"]),
                    "sim": row["sim"]
                })
            elif (row["type"] == "port") and (row["sim"] > port_thresh_sim):
                records.append({
                    "port_id": int(row["id"]),
                    "sim": row["sim"]
                })
        return records


def load_geoloc_cache(data):
    sg_geoloc_cache = dict()
    if type(data) == str:
        data = pd.read_csv(data)
    addr_postal_arr = data["addr_postal"].values
    lat_arr = data["lat"].values
    lng_arr = data["lng"].values
    for i in range(len(data)):
        addr_postal = addr_postal_arr[i]
        lat = lat_arr[i]
        lng = lng_arr[i]
        sg_geoloc_cache[addr_postal] = (lat, lng)
    return sg_geoloc_cache


def save_geoloc_cache(cache, path):
    df = pd.DataFrame({"addr_postal": [""] * len(cache), "lat": [0.0] * len(cache), "lng": [0.0] * len(cache)})
    for i, key in enumerate(cache.keys()):
        tup = cache[key]
        df.iat[i, 0] = key
        df.iat[i, 1] = tup[0]
        df.iat[i, 2] = tup[1]
    df.to_csv(path, index=False)


def get_geoloc(text1, text2=None, text3=None, cache=None, return_tuple_list=False):
    return get_sg_geoloc(text1, text2, text3, cache, return_tuple_list)


def get_sg_geoloc(text1, text2=None, text3=None, cache=None, return_tuple_list=False):
    if return_tuple_list:
        out = [None] * len(text1)
    else:
        out = np.empty((len(text1), 2))

    headers = {'Content-Type': 'application/json'}
    if (text2 is None) and (text3 is None):
        keys = [""]
    elif text3 is None:
        keys = ["", ""]
    else:
        keys = ["", "", ""]
    is_queryable = True
    for i in range(len(text1)):
        keys[0] = text1[i].strip()
        if len(keys) > 1:
            keys[1] = text2[i].strip()
        if len(keys) > 2:
            keys[2] = text3[i].strip()

        for key in keys:
            if pd.isna(key) or (key == "") or (key == "nan"):
                continue

            if (cache is not None) and cache.__contains__(key):
                tup = cache[key]
                if (not pd.isna(tup[0])) and (tup[0] != 0.0):
                    if return_tuple_list:
                        out[i] = tup
                    else:
                        out[i, :] = tup
                    break
            elif is_queryable:
                print("query: {}".format(key))
                api_url = "https://developers.onemap.sg/commonapi/search?" + urllib.parse.urlencode(
                    {"searchVal": key}) + "&returnGeom=Y&getAddrDetails=N&pageNum=1"

                response = requests.get(api_url, headers=headers)

                if (len(response.content) > 0) and (str(response.content).find("DOCTYPE html") == -1):
                    try:
                        obj = json.loads(response.content.decode('utf-8'))
                        if obj.__contains__("results") and len(obj["results"]) > 0:
                            record = obj["results"][0]
                            tup = (record["LATITUDE"], record["LONGITUDE"])
                            if cache is not None:
                                cache[key] = tup

                            if (not pd.isna(tup[0])) and (tup[0] != 0.0):
                                if return_tuple_list:
                                    out[i] = tup
                                else:
                                    out[i, :] = tup
                                break
                        elif cache is not None:
                            cache[key] = (None, None)
                    except Exception:
                        print(response.content)
                else:
                    is_queryable = False
                    print(response.content)

    return out


def process_sg_job_location_data(fact_data, geo_master, next_geo_key=1):
    # in Version2, all addr_a is delivery location, and all addr_b is depot location. port location is not saved
    version2_filt = fact_data.v2 == 1
    fact_data.loc[version2_filt, "delivery_addr"] = fact_data.loc[version2_filt, "addr_a"].values
    fact_data.loc[version2_filt, "delivery_postal"] = fact_data.loc[version2_filt, "postalcode_a"].values
    fact_data.loc[version2_filt, "depot_addr"] = fact_data.loc[version2_filt, "addr_b"].values
    fact_data.loc[version2_filt, "depot_postal"] = fact_data.loc[version2_filt, "postalcode_b"].values

    # in version3, addr_cat = 2, indicating it is a delivery location
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_c_cat == 2)
    fact_data.loc[version3_filt, "delivery_addr"] = fact_data.loc[version3_filt, "addr_c"].values
    fact_data.loc[version3_filt, "delivery_postal"] = fact_data.loc[version3_filt, "postalcode_c"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_b_cat == 2)
    fact_data.loc[version3_filt, "delivery_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "delivery_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_a_cat == 2)
    fact_data.loc[version3_filt, "delivery_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "delivery_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values

    # in version3, addr_cat = 1, indicating it is a depot location
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_c_cat == 1)
    fact_data.loc[version3_filt, "depot_addr"] = fact_data.loc[version3_filt, "addr_c"].values
    fact_data.loc[version3_filt, "depot_postal"] = fact_data.loc[version3_filt, "postalcode_c"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_b_cat == 1)
    fact_data.loc[version3_filt, "depot_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "depot_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_a_cat == 1)
    fact_data.loc[version3_filt, "depot_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "depot_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values

    # in version3, addr_cat = 0, indicating it is a port location
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_c_cat == 0)
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_c"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_c"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_b_cat == 0)
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_a_cat == 0)
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values

    # in version3, despite the addr_cat, if it is an import case, addr_a is always the port
    version3_filt = (fact_data.v2 == 0) & (fact_data.job_type == 1)
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values
    # in version3, despite the addr_cat, if it is a round-trip export case, addr_c is always the port
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & (fact_data.job_type == 2))
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_c"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_c"].values
    # in version3, despite the addr_cat, if it is a one-way export case, addr_b is always the port
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 2) & (fact_data.job_type == 2))
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values

    # in version3, despite the addr_cat, if it is a round-trip import case, addr_c is always the depot
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & (fact_data.job_type == 1))
    fact_data.loc[version3_filt, "depot_addr"] = fact_data.loc[version3_filt, "addr_c"].values
    fact_data.loc[version3_filt, "depot_postal"] = fact_data.loc[version3_filt, "postalcode_c"].values
    # in version3, despite the addr_cat, if it is a round-trip export case, addr_a is always the depot
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & (fact_data.job_type == 2))
    fact_data.loc[version3_filt, "depot_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "depot_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values

    # in version3, despite the addr_cat, if it is a round-trip import/export case, addr_b is always the delivery location
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & fact_data.job_type.isin([1, 2]))
    fact_data.loc[version3_filt, "delivery_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "delivery_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values

    extracted_port_road = extract_sg_address(fact_data["port_addr"].str.lower())
    extracted_depot_road = extract_sg_address(fact_data["depot_addr"].str.lower())
    extracted_delivery_road = extract_sg_address(fact_data["delivery_addr"].str.lower())
    extracted_loc_a_road = extract_sg_address(fact_data["addr_a"].str.lower())
    extracted_loc_b_road = extract_sg_address(fact_data["addr_b"].str.lower())
    extracted_loc_c_road = extract_sg_address(fact_data["addr_c"].str.lower())

    #     extracted_port_road["addr"] = fact_data["port_addr"].values
    #     extracted_depot_road["addr"] = fact_data["depot_addr"].values
    #     extracted_delivery_road["addr"] = fact_data["delivery_addr"].values

    filt = (pd.isna(fact_data["port_postal"]) == False) & (fact_data["port_postal"] != "")
    extracted_port_road.loc[filt, "postal_code"] = fact_data.loc[filt, "port_postal"].values
    filt = (pd.isna(fact_data["delivery_postal"]) == False) & (fact_data["delivery_postal"] != "")
    extracted_delivery_road.loc[filt, "postal_code"] = fact_data.loc[filt, "delivery_postal"].values
    filt = (pd.isna(fact_data["depot_postal"]) == False) & (fact_data["depot_postal"] != "")
    extracted_depot_road.loc[filt, "postal_code"] = fact_data.loc[filt, "depot_postal"].values
    filt = (pd.isna(fact_data["postalcode_a"]) == False) & (fact_data["postalcode_a"] != "")
    extracted_loc_a_road.loc[filt, "postal_code"] = fact_data.loc[filt, "postalcode_a"].values
    filt = (pd.isna(fact_data["postalcode_b"]) == False) & (fact_data["postalcode_b"] != "")
    extracted_loc_b_road.loc[filt, "postal_code"] = fact_data.loc[filt, "postalcode_b"].values
    filt = (pd.isna(fact_data["postalcode_c"]) == False) & (fact_data["postalcode_c"] != "")
    extracted_loc_b_road.loc[filt, "postal_code"] = fact_data.loc[filt, "postalcode_c"].values

    if type(geo_master) == pd.core.frame.DataFrame:
        sg_geo_cache = load_geoloc_cache(geo_master)
        exist_searchkeys = set(sg_geo_cache.keys())
    elif type(geo_master) == dict:
        sg_geo_cache = geo_master
    else:
        sg_geo_cache = None

    if np.sum(fact_data.columns.values == "delivery_key") > 0:
        port_loc_filt = pd.isna(fact_data["port_key"]) | (fact_data["port_key"] <= 0)
        delivery_loc_filt = pd.isna(fact_data["delivery_key"]) | (fact_data["delivery_key"] <= 0)
        depot_loc_filt = pd.isna(fact_data["depot_key"]) | (fact_data["depot_key"] <= 0)
        loc_a_filt = pd.isna(fact_data["loc_a_key"]) | (fact_data["loc_a_key"] <= 0)
        loc_b_filt = pd.isna(fact_data["loc_b_key"]) | (fact_data["loc_b_key"] <= 0)
        loc_c_filt = pd.isna(fact_data["loc_c_key"]) | (fact_data["loc_c_key"] <= 0)

        port_loc = get_sg_geoloc(extracted_port_road["block_road_name"].values[port_loc_filt],
                                 extracted_port_road["postal_code"].values[port_loc_filt],
                                 extracted_port_road["road_name"].values[port_loc_filt], cache=sg_geo_cache)
        delivery_loc = get_sg_geoloc(extracted_delivery_road["block_road_name"].values[delivery_loc_filt],
                                     extracted_delivery_road["postal_code"].values[delivery_loc_filt],
                                     extracted_delivery_road["road_name"].values[delivery_loc_filt], cache=sg_geo_cache)
        depot_loc = get_sg_geoloc(extracted_depot_road["block_road_name"].values[depot_loc_filt],
                                  extracted_depot_road["postal_code"].values[depot_loc_filt],
                                  extracted_depot_road["road_name"].values[depot_loc_filt], cache=sg_geo_cache)
        loc_a = get_sg_geoloc(extracted_loc_a_road["block_road_name"].values[loc_a_filt],
                              extracted_loc_a_road["postal_code"].values[loc_a_filt], extracted_loc_a_road["road_name"].values[loc_a_filt],
                              cache=sg_geo_cache)
        loc_b = get_sg_geoloc(extracted_loc_b_road["block_road_name"].values[loc_b_filt],
                              extracted_loc_b_road["postal_code"].values[loc_b_filt], extracted_loc_b_road["road_name"].values[loc_b_filt],
                              cache=sg_geo_cache)
        loc_c = get_sg_geoloc(extracted_loc_c_road["block_road_name"].values[loc_c_filt],
                              extracted_loc_c_road["postal_code"].values[loc_c_filt], extracted_loc_c_road["road_name"].values[loc_c_filt],
                              cache=sg_geo_cache)
    else:
        port_loc_filt = np.ones(len(fact_data)).astype(bool)
        delivery_loc_filt = np.ones(len(fact_data)).astype(bool)
        depot_loc_filt = np.ones(len(fact_data)).astype(bool)
        loc_a_filt = np.ones(len(fact_data)).astype(bool)
        loc_b_filt = np.ones(len(fact_data)).astype(bool)
        loc_c_filt = np.ones(len(fact_data)).astype(bool)

        port_loc = get_sg_geoloc(extracted_port_road["block_road_name"].values, extracted_port_road["postal_code"].values,
                                 extracted_port_road["road_name"].values, cache=sg_geo_cache)
        delivery_loc = get_sg_geoloc(extracted_delivery_road["block_road_name"].values, extracted_delivery_road["postal_code"].values,
                                     extracted_delivery_road["road_name"].values, cache=sg_geo_cache)
        depot_loc = get_sg_geoloc(extracted_depot_road["block_road_name"].values, extracted_depot_road["postal_code"].values,
                                  extracted_depot_road["road_name"].values, cache=sg_geo_cache)
        loc_a = get_sg_geoloc(extracted_loc_a_road["block_road_name"].values, extracted_loc_a_road["postal_code"].values,
                              extracted_loc_a_road["road_name"].values, cache=sg_geo_cache)
        loc_b = get_sg_geoloc(extracted_loc_b_road["block_road_name"].values, extracted_loc_b_road["postal_code"].values,
                              extracted_loc_b_road["road_name"].values, cache=sg_geo_cache)
        loc_c = get_sg_geoloc(extracted_loc_c_road["block_road_name"].values, extracted_loc_c_road["postal_code"].values,
                              extracted_loc_c_road["road_name"].values, cache=sg_geo_cache)

    update_filters = [port_loc_filt, delivery_loc_filt, depot_loc_filt, loc_a_filt, loc_b_filt, loc_c_filt]

    port_loc = np.round(port_loc, 7)
    delivery_loc = np.round(delivery_loc, 7)
    depot_loc = np.round(depot_loc, 7)
    loc_a = np.round(loc_a, 7)
    loc_b = np.round(loc_b, 7)
    loc_c = np.round(loc_c, 7)

    if type(geo_master) == pd.core.frame.DataFrame:
        extracted_port_road.loc[port_loc_filt, "lat"] = port_loc[:, 0]
        extracted_port_road.loc[port_loc_filt, "lng"] = port_loc[:, 1]
        extracted_delivery_road.loc[delivery_loc_filt, "lat"] = delivery_loc[:, 0]
        extracted_delivery_road.loc[delivery_loc_filt, "lng"] = delivery_loc[:, 1]
        extracted_depot_road.loc[depot_loc_filt, "lat"] = depot_loc[:, 0]
        extracted_depot_road.loc[depot_loc_filt, "lng"] = depot_loc[:, 1]
        extracted_loc_a_road.loc[loc_a_filt, "lat"] = loc_a[:, 0]
        extracted_loc_a_road.loc[loc_a_filt, "lng"] = loc_a[:, 1]
        extracted_loc_b_road.loc[loc_b_filt, "lat"] = loc_b[:, 0]
        extracted_loc_b_road.loc[loc_b_filt, "lng"] = loc_b[:, 1]
        extracted_loc_c_road.loc[loc_c_filt, "lat"] = loc_c[:, 0]
        extracted_loc_c_road.loc[loc_c_filt, "lng"] = loc_c[:, 1]

        geo_master["key"] = geo_master["key"].astype(str)
        geo_master0 = geo_master.loc[
            (pd.isna(geo_master.addr_postal) == False) & (geo_master.addr_postal != "") & (geo_master.lat != 0), ["key",
                                                                                                                  "addr_postal"]].groupby(
            "addr_postal", as_index=False).last()

        processed_addr_list = list()
        for i, extracted in enumerate(
                [extracted_port_road, extracted_delivery_road, extracted_depot_road, extracted_loc_a_road, extracted_loc_b_road,
                 extracted_loc_c_road]):
            extracted_port_key = extracted.merge(geo_master0, how="left", left_on="block_road_name", right_on="addr_postal")
            del extracted_port_key["addr_postal"]
            extracted_port_key = extracted_port_key.rename(columns={"key": "key.block_road_name"})

            extracted_port_key = extracted_port_key.merge(geo_master0, how="left", left_on="postal_code", right_on="addr_postal")
            del extracted_port_key["addr_postal"]
            extracted_port_key = extracted_port_key.rename(columns={"key": "key.postal_code"})

            extracted_port_key = extracted_port_key.merge(geo_master0, how="left", left_on="road_name", right_on="addr_postal")
            del extracted_port_key["addr_postal"]
            extracted_port_key = extracted_port_key.rename(columns={"key": "key.road_name"})

            processed_addr_list.append(extracted_port_key)

        added_searchkeys = dict()
        new_geo_master_key = list()
        new_geo_master_searchkey = list()
        new_geo_master_block = list()
        new_geo_master_road = list()
        new_geo_master_postal = list()
        new_geo_master_lat = list()
        new_geo_master_lng = list()

        for m, processed_addr in enumerate(processed_addr_list):
            update_key_filt = pd.isna(processed_addr["key.block_road_name"]) & update_filters[m]
            update_key_df = processed_addr.loc[update_key_filt, :]
            block_road_name_arr = update_key_df["block_road_name"].values
            block_number_arr = update_key_df["block_number"].values
            road_name_arr = update_key_df["road_name"].values
            postal_code_arr = update_key_df["postal_code"].values
            lat_arr = update_key_df["lat"].values
            lng_arr = update_key_df["lng"].values
            key_block_road_name_arr = update_key_df["key.block_road_name"].values
            for i in range(len(update_key_df)):
                block_road_name = block_road_name_arr[i]
                block_number = block_number_arr[i]
                road_name = road_name_arr[i]
                postal_code = postal_code_arr[i]
                lat = lat_arr[i]
                lng = lng_arr[i]
                if sg_geo_cache.__contains__(block_road_name) and (not exist_searchkeys.__contains__(block_road_name)):
                    if not added_searchkeys.__contains__(block_road_name):
                        added_searchkeys[block_road_name] = str(next_geo_key)
                        key_block_road_name_arr[i] = str(next_geo_key)
                        new_geo_master_key.append(str(next_geo_key))
                        new_geo_master_searchkey.append(block_road_name)
                        new_geo_master_block.append(block_number)
                        new_geo_master_road.append(road_name)
                        new_geo_master_postal.append(postal_code)
                        new_geo_master_lat.append(lat)
                        new_geo_master_lng.append(lng)
                        next_geo_key += 1
                    elif pd.isna(key_block_road_name_arr[i]) and (lat != 0):
                        key_block_road_name_arr[i] = added_searchkeys[block_road_name]
            processed_addr.loc[update_key_filt, "key.block_road_name"] = key_block_road_name_arr

            update_key_filt = pd.isna(processed_addr["key.postal_code"]) & update_filters[m]
            update_key_df = processed_addr.loc[update_key_filt, :]
            block_road_name_arr = update_key_df["block_road_name"].values
            block_number_arr = update_key_df["block_number"].values
            road_name_arr = update_key_df["road_name"].values
            postal_code_arr = update_key_df["postal_code"].values
            lat_arr = update_key_df["lat"].values
            lng_arr = update_key_df["lng"].values
            key_postal_code_arr = update_key_df["key.postal_code"].values
            for i in range(len(update_key_df)):
                block_road_name = block_road_name_arr[i]
                block_number = block_number_arr[i]
                road_name = road_name_arr[i]
                postal_code = postal_code_arr[i]
                lat = lat_arr[i]
                lng = lng_arr[i]
                if sg_geo_cache.__contains__(postal_code) and (not exist_searchkeys.__contains__(postal_code)):
                    if not added_searchkeys.__contains__(postal_code):
                        added_searchkeys[postal_code] = str(next_geo_key)
                        key_postal_code_arr[i] = str(next_geo_key)
                        new_geo_master_key.append(str(next_geo_key))
                        new_geo_master_searchkey.append(block_road_name)
                        new_geo_master_block.append(block_number)
                        new_geo_master_road.append(road_name)
                        new_geo_master_postal.append(postal_code)
                        new_geo_master_lat.append(lat)
                        new_geo_master_lng.append(lng)
                        next_geo_key += 1
                    elif pd.isna(key_postal_code_arr[i]) and (lat != 0):
                        key_postal_code_arr[i] = added_searchkeys[postal_code]
            processed_addr.loc[update_key_filt, "key.postal_code"] = key_postal_code_arr

            update_Key_filt = pd.isna(processed_addr["key.road_name"]) & update_filters[m]
            update_key_df = processed_addr.loc[update_Key_filt, :]
            block_road_name_arr = update_key_df["block_road_name"].values
            block_number_arr = update_key_df["block_number"].values
            road_name_arr = update_key_df["road_name"].values
            postal_code_arr = update_key_df["postal_code"].values
            lat_arr = update_key_df["lat"].values
            lng_arr = update_key_df["lng"].values
            key_road_name_arr = update_key_df["key.road_name"].values
            for i in range(len(update_key_df)):
                block_road_name = block_road_name_arr[i]
                block_number = block_number_arr[i]
                road_name = road_name_arr[i]
                postal_code = postal_code_arr[i]
                lat = lat_arr[i]
                lng = lng_arr[i]
                if sg_geo_cache.__contains__(road_name) and (not exist_searchkeys.__contains__(postal_code)):
                    if not added_searchkeys.__contains__(road_name):
                        added_searchkeys[road_name] = str(next_geo_key)
                        key_road_name_arr[i] = str(next_geo_key)
                        new_geo_master_key.append(str(next_geo_key))
                        new_geo_master_searchkey.append(block_road_name)
                        new_geo_master_block.append(block_number)
                        new_geo_master_road.append(road_name)
                        new_geo_master_postal.append(postal_code)
                        new_geo_master_lat.append(lat)
                        new_geo_master_lng.append(lng)
                        next_geo_key += 1
                    elif pd.isna(key_road_name_arr[i]) and (lat != 0):
                        key_road_name_arr[i] = added_searchkeys[road_name]
            processed_addr.loc[update_Key_filt, "key.road_name"] = key_road_name_arr

            processed_addr["key"] = None
            filt = pd.isna(processed_addr["key"]) & (pd.isna(processed_addr["key.block_road_name"]) == False)
            processed_addr.loc[filt, "key"] = processed_addr.loc[filt, "key.block_road_name"]
            filt = pd.isna(processed_addr["key"]) & (pd.isna(processed_addr["key.postal_code"]) == False)
            processed_addr.loc[filt, "key"] = processed_addr.loc[filt, "key.postal_code"]
            filt = pd.isna(processed_addr["key"]) & (pd.isna(processed_addr["key.road_name"]) == False)
            processed_addr.loc[filt, "key"] = processed_addr.loc[filt, "key.road_name"]

        fact_data.loc[port_loc_filt, "port_key"] = processed_addr_list[0]["key"].values[port_loc_filt]
        fact_data.loc[delivery_loc_filt, "delivery_key"] = processed_addr_list[1]["key"].values[delivery_loc_filt]
        fact_data.loc[depot_loc_filt, "depot_key"] = processed_addr_list[2]["key"].values[depot_loc_filt]
        fact_data.loc[loc_a_filt, "loc_a_key"] = processed_addr_list[3]["key"].values[loc_a_filt]
        fact_data.loc[loc_b_filt, "loc_b_key"] = processed_addr_list[4]["key"].values[loc_b_filt]
        fact_data.loc[loc_c_filt, "loc_c_key"] = processed_addr_list[5]["key"].values[loc_c_filt]

        return fact_data, new_geo_master_key, new_geo_master_searchkey, new_geo_master_block, new_geo_master_road, new_geo_master_postal, new_geo_master_lat, new_geo_master_lng
    else:
        fact_data.loc[port_loc_filt, "port_lat"] = port_loc[:, 0]
        fact_data.loc[port_loc_filt, "port_lng"] = port_loc[:, 1]
        fact_data.loc[delivery_loc_filt, "delivery_lat"] = delivery_loc[:, 0]
        fact_data.loc[delivery_loc_filt, "delivery_lng"] = delivery_loc[:, 1]
        fact_data.loc[depot_loc_filt, "depot_lat"] = depot_loc[:, 0]
        fact_data.loc[depot_loc_filt, "depot_lng"] = depot_loc[:, 1]
        fact_data.loc[loc_a_filt, "loc_a_lat"] = loc_a[:, 0]
        fact_data.loc[loc_a_filt, "loc_a_lng"] = loc_a[:, 1]
        fact_data.loc[loc_b_filt, "loc_b_lat"] = loc_b[:, 0]
        fact_data.loc[loc_b_filt, "loc_b_lng"] = loc_b[:, 1]
        fact_data.loc[loc_c_filt, "loc_c_lat"] = loc_c[:, 0]
        fact_data.loc[loc_c_filt, "loc_c_lng"] = loc_c[:, 1]

        return fact_data


def process_sg_trip_location_data(fact_data, geo_master, next_geo_key=1):
    # addr_cat = 2, indicating it is likily a delivery location
    version3_filt = (fact_data.addr_b_cat == 2)
    fact_data.loc[version3_filt, "delivery_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "delivery_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values
    version3_filt = (fact_data.addr_a_cat == 2)
    fact_data.loc[version3_filt, "delivery_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "delivery_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values

    # addr_cat = 1, indicating it is likily a depot location
    version3_filt = (fact_data.addr_b_cat == 1)
    fact_data.loc[version3_filt, "depot_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "depot_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values
    version3_filt = (fact_data.addr_a_cat == 1)
    fact_data.loc[version3_filt, "depot_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "depot_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values

    # addr_cat = 0, indicating it is likily a port location
    version3_filt = (fact_data.addr_b_cat == 0)
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_b"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_b"].values
    version3_filt = (fact_data.addr_a_cat == 0)
    fact_data.loc[version3_filt, "port_addr"] = fact_data.loc[version3_filt, "addr_a"].values
    fact_data.loc[version3_filt, "port_postal"] = fact_data.loc[version3_filt, "postalcode_a"].values

    extracted_port_road = extract_sg_address(fact_data["port_addr"].str.lower())
    extracted_depot_road = extract_sg_address(fact_data["depot_addr"].str.lower())
    extracted_delivery_road = extract_sg_address(fact_data["delivery_addr"].str.lower())
    extracted_loc_a_road = extract_sg_address(fact_data["addr_a"].str.lower())
    extracted_loc_b_road = extract_sg_address(fact_data["addr_b"].str.lower())

    filt = (pd.isna(fact_data["port_postal"]) == False) & (fact_data["port_postal"] != "")
    extracted_port_road.loc[filt, "postal_code"] = fact_data.loc[filt, "port_postal"].values
    filt = (pd.isna(fact_data["delivery_postal"]) == False) & (fact_data["delivery_postal"] != "")
    extracted_delivery_road.loc[filt, "postal_code"] = fact_data.loc[filt, "delivery_postal"].values
    filt = (pd.isna(fact_data["depot_postal"]) == False) & (fact_data["depot_postal"] != "")
    extracted_depot_road.loc[filt, "postal_code"] = fact_data.loc[filt, "depot_postal"].values
    filt = (pd.isna(fact_data["postalcode_a"]) == False) & (fact_data["postalcode_a"] != "")
    extracted_loc_a_road.loc[filt, "postal_code"] = fact_data.loc[filt, "postalcode_a"].values
    filt = (pd.isna(fact_data["postalcode_b"]) == False) & (fact_data["postalcode_b"] != "")
    extracted_loc_b_road.loc[filt, "postal_code"] = fact_data.loc[filt, "postalcode_b"].values

    if type(geo_master) == pd.core.frame.DataFrame:
        sg_geo_cache = load_geoloc_cache(geo_master)
        exist_searchkeys = set(sg_geo_cache.keys())
    elif type(geo_master) == dict:
        sg_geo_cache = geo_master
    else:
        sg_geo_cache = None

    if np.sum(fact_data.columns.values == "delivery_key") > 0:
        port_loc_filt = pd.isna(fact_data["port_key"]) | (fact_data["port_key"] <= 0)
        delivery_loc_filt = pd.isna(fact_data["delivery_key"]) | (fact_data["delivery_key"] <= 0)
        depot_loc_filt = pd.isna(fact_data["depot_key"]) | (fact_data["depot_key"] <= 0)
        loc_a_filt = pd.isna(fact_data["loc_a_key"]) | (fact_data["loc_a_key"] <= 0)
        loc_b_filt = pd.isna(fact_data["loc_b_key"]) | (fact_data["loc_b_key"] <= 0)

        port_loc = get_sg_geoloc(extracted_port_road["block_road_name"].values[port_loc_filt],
                                 extracted_port_road["postal_code"].values[port_loc_filt],
                                 extracted_port_road["road_name"].values[port_loc_filt], cache=sg_geo_cache)
        delivery_loc = get_sg_geoloc(extracted_delivery_road["block_road_name"].values[delivery_loc_filt],
                                     extracted_delivery_road["postal_code"].values[delivery_loc_filt],
                                     extracted_delivery_road["road_name"].values[delivery_loc_filt], cache=sg_geo_cache)
        depot_loc = get_sg_geoloc(extracted_depot_road["block_road_name"].values[depot_loc_filt],
                                  extracted_depot_road["postal_code"].values[depot_loc_filt],
                                  extracted_depot_road["road_name"].values[depot_loc_filt], cache=sg_geo_cache)
        loc_a = get_sg_geoloc(extracted_loc_a_road["block_road_name"].values[loc_a_filt],
                              extracted_loc_a_road["postal_code"].values[loc_a_filt], extracted_loc_a_road["road_name"].values[loc_a_filt],
                              cache=sg_geo_cache)
        loc_b = get_sg_geoloc(extracted_loc_b_road["block_road_name"].values[loc_b_filt],
                              extracted_loc_b_road["postal_code"].values[loc_b_filt], extracted_loc_b_road["road_name"].values[loc_b_filt],
                              cache=sg_geo_cache)
    else:
        port_loc_filt = np.ones(len(fact_data)).astype(bool)
        delivery_loc_filt = np.ones(len(fact_data)).astype(bool)
        depot_loc_filt = np.ones(len(fact_data)).astype(bool)
        loc_a_filt = np.ones(len(fact_data)).astype(bool)
        loc_b_filt = np.ones(len(fact_data)).astype(bool)

        port_loc = get_sg_geoloc(extracted_port_road["block_road_name"].values, extracted_port_road["postal_code"].values,
                                 extracted_port_road["road_name"].values, cache=sg_geo_cache)
        delivery_loc = get_sg_geoloc(extracted_delivery_road["block_road_name"].values, extracted_delivery_road["postal_code"].values,
                                     extracted_delivery_road["road_name"].values, cache=sg_geo_cache)
        depot_loc = get_sg_geoloc(extracted_depot_road["block_road_name"].values, extracted_depot_road["postal_code"].values,
                                  extracted_depot_road["road_name"].values, cache=sg_geo_cache)
        loc_a = get_sg_geoloc(extracted_loc_a_road["block_road_name"].values, extracted_loc_a_road["postal_code"].values,
                              extracted_loc_a_road["road_name"].values, cache=sg_geo_cache)
        loc_b = get_sg_geoloc(extracted_loc_b_road["block_road_name"].values, extracted_loc_b_road["postal_code"].values,
                              extracted_loc_b_road["road_name"].values, cache=sg_geo_cache)

    update_filters = [port_loc_filt, delivery_loc_filt, depot_loc_filt, loc_a_filt, loc_b_filt]

    port_loc = np.round(port_loc, 7)
    delivery_loc = np.round(delivery_loc, 7)
    depot_loc = np.round(depot_loc, 7)
    loc_a = np.round(loc_a, 7)
    loc_b = np.round(loc_b, 7)

    if type(geo_master) == pd.core.frame.DataFrame:
        extracted_port_road.loc[port_loc_filt, "lat"] = port_loc[:, 0]
        extracted_port_road.loc[port_loc_filt, "lng"] = port_loc[:, 1]
        extracted_delivery_road.loc[delivery_loc_filt, "lat"] = delivery_loc[:, 0]
        extracted_delivery_road.loc[delivery_loc_filt, "lng"] = delivery_loc[:, 1]
        extracted_depot_road.loc[depot_loc_filt, "lat"] = depot_loc[:, 0]
        extracted_depot_road.loc[depot_loc_filt, "lng"] = depot_loc[:, 1]
        extracted_loc_a_road.loc[loc_a_filt, "lat"] = loc_a[:, 0]
        extracted_loc_a_road.loc[loc_a_filt, "lng"] = loc_a[:, 1]
        extracted_loc_b_road.loc[loc_b_filt, "lat"] = loc_b[:, 0]
        extracted_loc_b_road.loc[loc_b_filt, "lng"] = loc_b[:, 1]

        geo_master["key"] = geo_master["key"].astype(str)
        geo_master0 = geo_master.loc[
            (pd.isna(geo_master.addr_postal) == False) & (geo_master.addr_postal != "") & (geo_master.lat != 0), ["key",
                                                                                                                  "addr_postal"]].groupby(
            "addr_postal", as_index=False).last()

        processed_addr_list = list()
        for i, extracted in enumerate(
                [extracted_port_road, extracted_delivery_road, extracted_depot_road, extracted_loc_a_road, extracted_loc_b_road]):
            extracted_key = extracted.merge(geo_master0, how="left", left_on="block_road_name", right_on="addr_postal")
            del extracted_key["addr_postal"]
            extracted_key = extracted_key.rename(columns={"key": "key.block_road_name"})

            extracted_key = extracted_key.merge(geo_master0, how="left", left_on="postal_code", right_on="addr_postal")
            del extracted_key["addr_postal"]
            extracted_key = extracted_key.rename(columns={"key": "key.postal_code"})

            extracted_key = extracted_key.merge(geo_master0, how="left", left_on="road_name", right_on="addr_postal")
            del extracted_key["addr_postal"]
            extracted_key = extracted_key.rename(columns={"key": "key.road_name"})

            processed_addr_list.append(extracted_key)

        added_searchkeys = dict()
        new_geo_master_key = list()
        new_geo_master_searchkey = list()
        new_geo_master_block = list()
        new_geo_master_road = list()
        new_geo_master_postal = list()
        new_geo_master_lat = list()
        new_geo_master_lng = list()

        for m, processed_addr in enumerate(processed_addr_list):
            update_key_filt = pd.isna(processed_addr["key.block_road_name"]) & update_filters[m]
            update_key_df = processed_addr.loc[update_key_filt, :]
            block_road_name_arr = update_key_df["block_road_name"].values
            block_number_arr = update_key_df["block_number"].values
            road_name_arr = update_key_df["road_name"].values
            postal_code_arr = update_key_df["postal_code"].values
            lat_arr = update_key_df["lat"].values
            lng_arr = update_key_df["lng"].values
            key_block_road_name_arr = update_key_df["key.block_road_name"].values
            for i in range(len(update_key_df)):
                block_road_name = block_road_name_arr[i]
                block_number = block_number_arr[i]
                road_name = road_name_arr[i]
                postal_code = postal_code_arr[i]
                lat = lat_arr[i]
                lng = lng_arr[i]
                if sg_geo_cache.__contains__(block_road_name) and (not exist_searchkeys.__contains__(block_road_name)):
                    if not added_searchkeys.__contains__(block_road_name):
                        added_searchkeys[block_road_name] = str(next_geo_key)
                        key_block_road_name_arr[i] = str(next_geo_key)
                        new_geo_master_key.append(str(next_geo_key))
                        new_geo_master_searchkey.append(block_road_name)
                        new_geo_master_block.append(block_number)
                        new_geo_master_road.append(road_name)
                        new_geo_master_postal.append(postal_code)
                        new_geo_master_lat.append(lat)
                        new_geo_master_lng.append(lng)
                        next_geo_key += 1
                    elif pd.isna(key_block_road_name_arr[i]) and (lat != 0):
                        key_block_road_name_arr[i] = added_searchkeys[block_road_name]
            processed_addr.loc[update_key_filt, "key.block_road_name"] = key_block_road_name_arr

            update_key_filt = pd.isna(processed_addr["key.postal_code"]) & update_filters[m]
            update_key_df = processed_addr.loc[update_key_filt, :]
            block_road_name_arr = update_key_df["block_road_name"].values
            block_number_arr = update_key_df["block_number"].values
            road_name_arr = update_key_df["road_name"].values
            postal_code_arr = update_key_df["postal_code"].values
            lat_arr = update_key_df["lat"].values
            lng_arr = update_key_df["lng"].values
            key_postal_code_arr = update_key_df["key.postal_code"].values
            for i in range(len(update_key_df)):
                block_road_name = block_road_name_arr[i]
                block_number = block_number_arr[i]
                road_name = road_name_arr[i]
                postal_code = postal_code_arr[i]
                lat = lat_arr[i]
                lng = lng_arr[i]
                if sg_geo_cache.__contains__(postal_code) and (not exist_searchkeys.__contains__(postal_code)):
                    if not added_searchkeys.__contains__(postal_code):
                        added_searchkeys[postal_code] = str(next_geo_key)
                        key_postal_code_arr[i] = str(next_geo_key)
                        new_geo_master_key.append(str(next_geo_key))
                        new_geo_master_searchkey.append(block_road_name)
                        new_geo_master_block.append(block_number)
                        new_geo_master_road.append(road_name)
                        new_geo_master_postal.append(postal_code)
                        new_geo_master_lat.append(lat)
                        new_geo_master_lng.append(lng)
                        next_geo_key += 1
                    elif pd.isna(key_postal_code_arr[i]) and (lat != 0):
                        key_postal_code_arr[i] = added_searchkeys[postal_code]
            processed_addr.loc[update_key_filt, "key.postal_code"] = key_postal_code_arr

            update_Key_filt = pd.isna(processed_addr["key.road_name"]) & update_filters[m]
            update_key_df = processed_addr.loc[update_Key_filt, :]
            block_road_name_arr = update_key_df["block_road_name"].values
            block_number_arr = update_key_df["block_number"].values
            road_name_arr = update_key_df["road_name"].values
            postal_code_arr = update_key_df["postal_code"].values
            lat_arr = update_key_df["lat"].values
            lng_arr = update_key_df["lng"].values
            key_road_name_arr = update_key_df["key.road_name"].values
            for i in range(len(update_key_df)):
                block_road_name = block_road_name_arr[i]
                block_number = block_number_arr[i]
                road_name = road_name_arr[i]
                postal_code = postal_code_arr[i]
                lat = lat_arr[i]
                lng = lng_arr[i]
                if sg_geo_cache.__contains__(road_name) and (not exist_searchkeys.__contains__(postal_code)):
                    if not added_searchkeys.__contains__(road_name):
                        added_searchkeys[road_name] = str(next_geo_key)
                        key_road_name_arr[i] = str(next_geo_key)
                        new_geo_master_key.append(str(next_geo_key))
                        new_geo_master_searchkey.append(block_road_name)
                        new_geo_master_block.append(block_number)
                        new_geo_master_road.append(road_name)
                        new_geo_master_postal.append(postal_code)
                        new_geo_master_lat.append(lat)
                        new_geo_master_lng.append(lng)
                        next_geo_key += 1
                    elif pd.isna(key_road_name_arr[i]) and (lat != 0):
                        key_road_name_arr[i] = added_searchkeys[road_name]
            processed_addr.loc[update_Key_filt, "key.road_name"] = key_road_name_arr

            processed_addr["key"] = None
            filt = pd.isna(processed_addr["key"]) & (pd.isna(processed_addr["key.block_road_name"]) == False)
            processed_addr.loc[filt, "key"] = processed_addr.loc[filt, "key.block_road_name"]
            filt = pd.isna(processed_addr["key"]) & (pd.isna(processed_addr["key.postal_code"]) == False)
            processed_addr.loc[filt, "key"] = processed_addr.loc[filt, "key.postal_code"]
            filt = pd.isna(processed_addr["key"]) & (pd.isna(processed_addr["key.road_name"]) == False)
            processed_addr.loc[filt, "key"] = processed_addr.loc[filt, "key.road_name"]

        fact_data.loc[port_loc_filt, "port_key"] = processed_addr_list[0]["key"].values[port_loc_filt]
        fact_data.loc[delivery_loc_filt, "delivery_key"] = processed_addr_list[1]["key"].values[delivery_loc_filt]
        fact_data.loc[depot_loc_filt, "depot_key"] = processed_addr_list[2]["key"].values[depot_loc_filt]
        fact_data.loc[loc_a_filt, "loc_a_key"] = processed_addr_list[3]["key"].values[loc_a_filt]
        fact_data.loc[loc_b_filt, "loc_b_key"] = processed_addr_list[4]["key"].values[loc_b_filt]

        return fact_data, new_geo_master_key, new_geo_master_searchkey, new_geo_master_block, new_geo_master_road, new_geo_master_postal, new_geo_master_lat, new_geo_master_lng
    else:
        fact_data.loc[port_loc_filt, "port_lat"] = port_loc[:, 0]
        fact_data.loc[port_loc_filt, "port_lng"] = port_loc[:, 1]
        fact_data.loc[delivery_loc_filt, "delivery_lat"] = delivery_loc[:, 0]
        fact_data.loc[delivery_loc_filt, "delivery_lng"] = delivery_loc[:, 1]
        fact_data.loc[depot_loc_filt, "depot_lat"] = depot_loc[:, 0]
        fact_data.loc[depot_loc_filt, "depot_lng"] = depot_loc[:, 1]
        fact_data.loc[loc_a_filt, "loc_a_lat"] = loc_a[:, 0]
        fact_data.loc[loc_a_filt, "loc_a_lng"] = loc_a[:, 1]
        fact_data.loc[loc_b_filt, "loc_b_lat"] = loc_b[:, 0]
        fact_data.loc[loc_b_filt, "loc_b_lng"] = loc_b[:, 1]

        return fact_data


def pre_derive_sg_job_geo_keys(fact_data, geo_master):
    fact_data["loc_a_id"] = fact_data["loc_a_id"].fillna(-1).astype(int)
    fact_data["loc_b_id"] = fact_data["loc_b_id"].fillna(-1).astype(int)
    fact_data["loc_c_id"] = fact_data["loc_c_id"].fillna(-1).astype(int)

    filt = pd.isna(fact_data["loc_a_as_building_id"]) | (fact_data["loc_a_as_building_id"] == 0)
    fact_data.loc[filt, "loc_a_as_building_id"] = fact_data.loc[filt, "loc_a_as_pic_building_id"].values
    filt = pd.isna(fact_data["loc_b_as_building_id"]) | (fact_data["loc_b_as_building_id"] == 0)
    fact_data.loc[filt, "loc_b_as_building_id"] = fact_data.loc[filt, "loc_b_as_pic_building_id"].values
    filt = pd.isna(fact_data["loc_c_as_building_id"]) | (fact_data["loc_c_as_building_id"] == 0)
    fact_data.loc[filt, "loc_c_as_building_id"] = fact_data.loc[filt, "loc_c_as_pic_building_id"].values

    fact_data["loc_a_as_building_id"] = fact_data["loc_a_as_building_id"].fillna(-1).astype(int)
    fact_data["loc_b_as_building_id"] = fact_data["loc_b_as_building_id"].fillna(-1).astype(int)
    fact_data["loc_c_as_building_id"] = fact_data["loc_c_as_building_id"].fillna(-1).astype(int)
    fact_data["end_cust_building_id"] = fact_data["end_cust_building_id"].fillna(-1).astype(int)

    fact_data["port_id"] = -1
    fact_data["delivery_building_id"] = -1
    fact_data["depot_id"] = -1

    def infer_sg_cp_depot_or_port(addr_arr, depot_thresh_sim=0.5, port_thresh_sim=0.5):
        inferred_types, inferred_keys, inferred_sims = [None] * len(addr_arr), [-1] * len(addr_arr), [0] * len(addr_arr)
        cache = {}
        for addr in pd.Series(addr_arr).astype(str).unique():
            if pd.isna(addr) == False:
                t, k, s = match_sg_cp_depot_or_port(None, addr, geo_master, depot_thresh_sim=depot_thresh_sim,
                                                    port_thresh_sim=port_thresh_sim)
                cache[addr] = (t, k if t is not None else -1, s)
        for i, addr in enumerate(addr_arr):
            if pd.isna(addr) == False:
                t, k, s = cache[addr]
                inferred_types[i] = t
                inferred_keys[i] = k
                inferred_sims[i] = s
        return np.array([inferred_types, inferred_keys, inferred_sims]).transpose()

    fact_data["infer_loc_a_type"] = None
    fact_data["infer_loc_a_key"] = -1
    fact_data["infer_loc_a_sim"] = 0
    fact_data["infer_loc_b_type"] = None
    fact_data["infer_loc_b_key"] = -1
    fact_data["infer_loc_b_sim"] = 0
    fact_data["infer_loc_c_type"] = None
    fact_data["infer_loc_c_key"] = -1
    fact_data["infer_loc_c_sim"] = 0

    fact_data[["infer_loc_a_type", "infer_loc_a_key", "infer_loc_a_sim"]] = infer_sg_cp_depot_or_port(fact_data["addr_a"],
                                                                                                      depot_thresh_sim=0.8,
                                                                                                      port_thresh_sim=0.8)
    fact_data.loc[(fact_data["infer_loc_a_type"] == "port"), "addr_a_cat"] = 0
    fact_data.loc[(fact_data["infer_loc_a_type"] == "depot"), "addr_a_cat"] = 1

    fact_data[["infer_loc_b_type", "infer_loc_b_key", "infer_loc_b_sim"]] = infer_sg_cp_depot_or_port(fact_data["addr_b"],
                                                                                                      depot_thresh_sim=0.8,
                                                                                                      port_thresh_sim=0.8)
    fact_data.loc[(fact_data["infer_loc_b_type"] == "port"), "addr_b_cat"] = 0
    fact_data.loc[(fact_data["infer_loc_b_type"] == "depot"), "addr_b_cat"] = 1

    fact_data[["infer_loc_c_type", "infer_loc_c_key", "infer_loc_c_sim"]] = infer_sg_cp_depot_or_port(fact_data["addr_c"],
                                                                                                      depot_thresh_sim=0.8,
                                                                                                      port_thresh_sim=0.8)
    fact_data.loc[(fact_data["infer_loc_c_type"] == "port"), "addr_c_cat"] = 0
    fact_data.loc[(fact_data["infer_loc_c_type"] == "depot"), "addr_c_cat"] = 1

    # in version3, addr_cat = 2, indicating it is a delivery location
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_a_cat == 2) & (fact_data["loc_a_as_building_id"] > 0)
    fact_data.loc[version3_filt, "delivery_building_id"] = fact_data.loc[version3_filt, "loc_a_as_building_id"].values
    fact_data.loc[version3_filt, "loc_a_id"] = fact_data.loc[version3_filt, "loc_a_as_building_id"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_b_cat == 2) & (fact_data["loc_b_as_building_id"] > 0)
    fact_data.loc[version3_filt, "delivery_building_id"] = fact_data.loc[version3_filt, "loc_b_as_building_id"].values
    fact_data.loc[version3_filt, "loc_b_id"] = fact_data.loc[version3_filt, "loc_b_as_building_id"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_c_cat == 2) & (fact_data["loc_c_as_building_id"] > 0)
    fact_data.loc[version3_filt, "delivery_building_id"] = fact_data.loc[version3_filt, "loc_c_as_building_id"].values
    fact_data.loc[version3_filt, "loc_c_id"] = fact_data.loc[version3_filt, "loc_c_as_building_id"].values

    # in version3, addr_cat = 1, indicating it is a depot location
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_c_cat == 1)
    fact_data.loc[version3_filt, "depot_id"] = fact_data.loc[version3_filt, "loc_c_id"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_b_cat == 1)
    fact_data.loc[version3_filt, "depot_id"] = fact_data.loc[version3_filt, "loc_b_id"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_a_cat == 1)
    fact_data.loc[version3_filt, "depot_id"] = fact_data.loc[version3_filt, "loc_a_id"].values

    # in version3, addr_cat = 0, indicating it is a port location
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_c_cat == 0)
    fact_data.loc[version3_filt, "port_id"] = fact_data.loc[version3_filt, "loc_c_id"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_b_cat == 0)
    fact_data.loc[version3_filt, "port_id"] = fact_data.loc[version3_filt, "loc_b_id"].values
    version3_filt = (fact_data.v2 == 0) & (fact_data.addr_a_cat == 0)
    fact_data.loc[version3_filt, "port_id"] = fact_data.loc[version3_filt, "loc_a_id"].values

    # in version3, despite the addr_cat, if it is an import case, addr_a is always the port
    version3_filt = (fact_data.v2 == 0) & (fact_data.job_type == 1) & (fact_data["loc_a_id"] > 0)
    fact_data.loc[version3_filt, "port_id"] = fact_data.loc[version3_filt, "loc_a_id"].values
    fact_data.loc[version3_filt, "addr_a_cat"] = 0
    # in version3, despite the addr_cat, if it is a round-trip export case, addr_c is always the port
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & (fact_data.job_type == 2)) & (fact_data["loc_c_id"] > 0)
    fact_data.loc[version3_filt, "port_id"] = fact_data.loc[version3_filt, "loc_c_id"].values
    fact_data.loc[version3_filt, "addr_c_cat"] = 0
    # in version3, despite the addr_cat, if it is a one-way export case, addr_b is always the port
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 2) & (fact_data.job_type == 2)) & (fact_data["loc_b_id"] > 0)
    fact_data.loc[version3_filt, "port_id"] = fact_data.loc[version3_filt, "loc_b_id"].values
    fact_data.loc[version3_filt, "addr_b_cat"] = 0

    # in version3, despite the addr_cat, if it is a round-trip import case, addr_c is always the depot
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & (fact_data.job_type == 1)) & (fact_data["loc_c_id"] > 0)
    fact_data.loc[version3_filt, "depot_id"] = fact_data.loc[version3_filt, "loc_c_id"].values
    fact_data.loc[version3_filt, "addr_c_cat"] = 1
    # in version3, despite the addr_cat, if it is a round-trip export case, addr_a is always the depot
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & (fact_data.job_type == 2)) & (fact_data["loc_a_id"] > 0)
    fact_data.loc[version3_filt, "depot_id"] = fact_data.loc[version3_filt, "loc_a_id"].values
    fact_data.loc[version3_filt, "addr_a_cat"] = 1

    # in version3, despite the addr_cat, if it is a round-trip import/export case, addr_b is always the delivery location
    version3_filt = (fact_data.v2 == 0) & ((fact_data.main_job_type == 1) & fact_data.job_type.isin([1, 2])) & (
                fact_data["loc_b_as_building_id"] > 0)
    fact_data.loc[version3_filt, "delivery_building_id"] = fact_data.loc[version3_filt, "loc_b_as_building_id"].values
    fact_data.loc[version3_filt, "loc_b_id"] = fact_data.loc[version3_filt, "loc_b_as_building_id"].values
    fact_data.loc[version3_filt, "addr_b_cat"] = 2

    # if has end_cust_building_id, use end_cust_building_id for delivery locatoin
    end_cust_building_filt = (fact_data["end_cust_building_id"] > 0)
    fact_data.loc[end_cust_building_filt, "delivery_building_id"] = fact_data.loc[end_cust_building_filt, "end_cust_building_id"].values

    latest_key = geo_master.loc[(geo_master.type == "Port") & (pd.isna(geo_master["source_id"]) == False), ["key", "source_id"]].groupby(
        "source_id", as_index=False).last()
    latest_key["source_id"] = latest_key["source_id"].astype(int)
    latest_key.columns = ["port_id", "port_key"]
    fact_data = fact_data.merge(latest_key, how="left", on="port_id")
    filt = (fact_data["addr_a_cat"] == 0) & (fact_data["infer_loc_a_key"] != -1)
    fact_data.loc[filt, "port_key"] = fact_data.loc[filt, "infer_loc_a_key"].values
    filt = (fact_data["addr_b_cat"] == 0) & (fact_data["infer_loc_b_key"] != -1)
    fact_data.loc[filt, "port_key"] = fact_data.loc[filt, "infer_loc_b_key"].values
    filt = (fact_data["addr_c_cat"] == 0) & (fact_data["infer_loc_c_key"] != -1)
    fact_data.loc[filt, "port_key"] = fact_data.loc[filt, "infer_loc_c_key"].values
    fact_data["port_key"] = fact_data["port_key"].fillna(-1).astype(int)

    latest_key = geo_master.loc[(geo_master.type == "Depot") & (pd.isna(geo_master["source_id"]) == False), ["key", "source_id"]].groupby(
        "source_id", as_index=False).last()
    latest_key["source_id"] = latest_key["source_id"].astype(int)
    latest_key.columns = ["depot_id", "depot_key"]
    fact_data = fact_data.merge(latest_key, how="left", on="depot_id")
    filt = pd.isna(fact_data["depot_key"]) & (fact_data["addr_a_cat"] == 1) & (fact_data["infer_loc_a_key"] != -1)
    fact_data.loc[filt, "depot_key"] = fact_data.loc[filt, "infer_loc_a_key"].values
    filt = pd.isna(fact_data["depot_key"]) & (fact_data["addr_b_cat"] == 1) & (fact_data["infer_loc_b_key"] != -1)
    fact_data.loc[filt, "depot_key"] = fact_data.loc[filt, "infer_loc_b_key"].values
    filt = pd.isna(fact_data["depot_key"]) & (fact_data["addr_c_cat"] == 1) & (fact_data["infer_loc_c_key"] != -1)
    fact_data.loc[filt, "depot_key"] = fact_data.loc[filt, "infer_loc_c_key"].values
    fact_data["depot_key"] = fact_data["depot_key"].fillna(-1).astype(int)

    latest_key = geo_master.loc[
        (geo_master.type == "Delivery") & (pd.isna(geo_master["source_id"]) == False), ["key", "source_id"]].groupby("source_id",
                                                                                                                     as_index=False).last()
    latest_key["source_id"] = latest_key["source_id"].astype(int)
    latest_key.columns = ["delivery_building_id", "delivery_key"]
    fact_data = fact_data.merge(latest_key, how="left", on="delivery_building_id")
    fact_data["delivery_key"] = fact_data["delivery_key"].fillna(-1).astype(int)

    geo_master.loc[geo_master.type == "Port", "cat"] = 0
    geo_master.loc[geo_master.type == "Depot", "cat"] = 1
    geo_master.loc[geo_master.type == "Delivery", "cat"] = 2
    latest_key = geo_master.loc[
        (pd.isna(geo_master["type"]) == False) & (pd.isna(geo_master["source_id"]) == False), ["key", "source_id", "cat"]].groupby(
        ["cat", "source_id"], as_index=False).last()
    latest_key["cat"] = latest_key["cat"].astype(int)
    latest_key["source_id"] = latest_key["source_id"].astype(int)

    latest_key.columns = ["addr_a_cat", "loc_a_id", "loc_a_key"]
    fact_data = fact_data.merge(latest_key, how="left", on=["loc_a_id", "addr_a_cat"])
    filt = fact_data["infer_loc_a_key"] != -1
    fact_data.loc[filt, "loc_a_key"] = fact_data.loc[filt, "infer_loc_a_key"].values
    fact_data["loc_a_key"] = fact_data["loc_a_key"].fillna(-1).astype(int)

    latest_key.columns = ["addr_b_cat", "loc_b_id", "loc_b_key"]
    fact_data = fact_data.merge(latest_key, how="left", on=["loc_b_id", "addr_b_cat"])
    filt = fact_data["infer_loc_b_key"] != -1
    fact_data.loc[filt, "loc_b_key"] = fact_data.loc[filt, "infer_loc_b_key"].values
    fact_data["loc_b_key"] = fact_data["loc_b_key"].fillna(-1).astype(int)

    latest_key.columns = ["addr_c_cat", "loc_c_id", "loc_c_key"]
    fact_data = fact_data.merge(latest_key, how="left", on=["loc_c_id", "addr_c_cat"])
    filt = fact_data["infer_loc_c_key"] != -1
    fact_data.loc[filt, "loc_c_key"] = fact_data.loc[filt, "infer_loc_c_key"].values
    fact_data["loc_c_key"] = fact_data["loc_c_key"].fillna(-1).astype(int)

    fact_data["addr_a_cat_name"] = "None"
    fact_data.loc[(fact_data["addr_a_cat"] == 0) & (fact_data["infer_loc_a_type"] == "port"), "addr_a_cat_name"] = "Port"
    fact_data.loc[fact_data["addr_a_cat"] == 1, "addr_a_cat_name"] = "Depot"
    fact_data.loc[fact_data["addr_a_cat"] == 2, "addr_a_cat_name"] = "Delivery"
    fact_data["addr_b_cat_name"] = "None"
    fact_data.loc[(fact_data["addr_b_cat"] == 0) & (fact_data["infer_loc_b_type"] == "port"), "addr_b_cat_name"] = "Port"
    fact_data.loc[fact_data["addr_b_cat"] == 1, "addr_b_cat_name"] = "Depot"
    fact_data.loc[fact_data["addr_b_cat"] == 2, "addr_b_cat_name"] = "Delivery"
    fact_data["addr_c_cat_name"] = "None"
    fact_data.loc[(fact_data["addr_c_cat"] == 0) & (fact_data["infer_loc_c_type"] == "port"), "addr_c_cat_name"] = "Port"
    fact_data.loc[fact_data["addr_c_cat"] == 1, "addr_c_cat_name"] = "Depot"
    fact_data.loc[fact_data["addr_c_cat"] == 2, "addr_c_cat_name"] = "Delivery"

    return fact_data


def post_derive_sg_job_geo_keys(fact_data, geo_master, next_geo_key):
    fact_data, new_geo_master_key, new_geo_master_searchkey, new_geo_master_block, new_geo_master_road, new_geo_master_postal, new_geo_master_lat, new_geo_master_lng = process_sg_job_location_data(
        fact_data, geo_master, next_geo_key)

    if len(new_geo_master_key) > 0:
        df = pd.DataFrame({
            "key": new_geo_master_key,
            "searchkey": new_geo_master_searchkey,
            "block": new_geo_master_block,
            "road": new_geo_master_road,
            "postal": new_geo_master_postal,
            "lat": new_geo_master_lat,
            "lng": new_geo_master_lng,
            "valid": [True] * len(new_geo_master_key)
        })
        df["valid"] = (pd.isna(df["lat"]) == False) & (pd.isna(df["lng"]) == False) & (df["lat"] != 0) & (df["lng"] != 0) & (
                    np.abs(df["lat"]) < 90) & (np.abs(df["lng"]) < 180)
        df["key"] = df["key"].astype(int)

        invalid_keys = df.loc[df["valid"] == False, "key"].values
        fact_data.loc[fact_data["loc_a_key"].isin(invalid_keys), "loc_a_key"] = -1
        fact_data.loc[fact_data["loc_b_key"].isin(invalid_keys), "loc_b_key"] = -1
        fact_data.loc[fact_data["loc_c_key"].isin(invalid_keys), "loc_c_key"] = -1
        fact_data.loc[fact_data["depot_key"].isin(invalid_keys), "depot_key"] = -1
        fact_data.loc[fact_data["port_key"].isin(invalid_keys), "port_key"] = -1
        fact_data.loc[fact_data["delivery_key"].isin(invalid_keys), "delivery_key"] = -1

        new_geo_master_key = df.loc[df["valid"], "key"].values
        new_geo_master_searchkey = df.loc[df["valid"], "searchkey"].values
        new_geo_master_block = df.loc[df["valid"], "block"].values
        new_geo_master_road = df.loc[df["valid"], "road"].values
        new_geo_master_postal = df.loc[df["valid"], "postal"].values
        new_geo_master_lat = df.loc[df["valid"], "lat"].values
        new_geo_master_lng = df.loc[df["valid"], "lng"].values

    fact_data["port_key"] = fact_data["port_key"].fillna(-1).astype(int)
    fact_data["depot_key"] = fact_data["depot_key"].fillna(-1).astype(int)
    fact_data["delivery_key"] = fact_data["delivery_key"].fillna(-1).astype(int)
    fact_data["loc_a_key"] = fact_data["loc_a_key"].fillna(-1).astype(int)
    fact_data["loc_b_key"] = fact_data["loc_b_key"].fillna(-1).astype(int)
    fact_data["loc_c_key"] = fact_data["loc_c_key"].fillna(-1).astype(int)

    return fact_data, np.array(new_geo_master_key,
                               dtype=int), new_geo_master_searchkey, new_geo_master_block, new_geo_master_road, new_geo_master_postal, new_geo_master_lat, new_geo_master_lng


def pre_derive_sg_trip_geo_keys(fact_data, geo_master):
    fact_data["loc_a_id"] = -1
    fact_data["loc_b_id"] = -1
    non_send_filt = fact_data["job_type"].isin([0, 1, 2, 3])
    fact_data.loc[non_send_filt, "addr_a_cat"] = -1
    fact_data.loc[non_send_filt, "addr_b_cat"] = -1
    fact_data["delivery_building_id"] = fact_data["end_cust_building_id"]
    fact_data["port_id"] = -1
    fact_data["depot_id"] = -1

    is_from_cust_filt = fact_data["loc_a_as_building_id"] != -1
    is_to_cust_filt = fact_data["loc_b_as_building_id"] != -1

    def infer_sg_cp_depot_or_port(addr_arr, depot_thresh_sim=0.5, port_thresh_sim=0.5):
        inferred_types, inferred_keys, inferred_sims = [None] * len(addr_arr), [-1] * len(addr_arr), [0] * len(addr_arr)
        cache = {}
        for addr in pd.Series(addr_arr).astype(str).unique():
            if pd.isna(addr) == False:
                t, k, s = match_sg_cp_depot_or_port(None, addr, geo_master, depot_thresh_sim=depot_thresh_sim,
                                                    port_thresh_sim=port_thresh_sim)
                cache[addr] = (t, k if t is not None else -1, s)
        for i, addr in enumerate(addr_arr):
            if pd.isna(addr) == False:
                t, k, s = cache[addr]
                inferred_types[i] = t
                inferred_keys[i] = k
                inferred_sims[i] = s
        return np.array([inferred_types, inferred_keys, inferred_sims]).transpose()

    fact_data["infer_loc_a_type"] = None
    fact_data["infer_loc_a_key"] = -1
    fact_data["infer_loc_a_sim"] = 0
    fact_data["infer_loc_b_type"] = None
    fact_data["infer_loc_b_key"] = -1
    fact_data["infer_loc_b_sim"] = 0

    # export (a=customer/depot, b=port)
    export_filt = fact_data["job_type"] == 0

    fact_data.loc[export_filt, ["infer_loc_b_type", "infer_loc_b_key", "infer_loc_b_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[export_filt, "addr_b"])
    fact_data.loc[export_filt & (fact_data["infer_loc_b_type"] == "port"), "addr_b_cat"] = 0
    fact_data.loc[export_filt & (fact_data["infer_loc_b_type"] == "depot"), "addr_b_cat"] = 1

    fact_data.loc[export_filt, ["infer_loc_a_type", "infer_loc_a_key", "infer_loc_a_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[export_filt, "addr_a"], depot_thresh_sim=0.8, port_thresh_sim=0.8)
    fact_data.loc[export_filt & (fact_data["infer_loc_a_type"] == "port"), "addr_a_cat"] = 0
    fact_data.loc[export_filt & (fact_data["infer_loc_a_type"] == "depot"), "addr_a_cat"] = 1
    filt = export_filt & pd.isna(fact_data["infer_loc_a_type"])
    fact_data.loc[filt, "addr_a_cat"] = 2
    fact_data.loc[filt & is_from_cust_filt, "loc_a_id"] = fact_data.loc[filt & is_from_cust_filt, "loc_a_as_building_id"].values

    # import (a=port, b=customer/depot)
    import_filt = fact_data["job_type"] == 1

    fact_data.loc[import_filt, ["infer_loc_a_type", "infer_loc_a_key", "infer_loc_a_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[import_filt, "addr_a"])
    fact_data.loc[import_filt & (fact_data["infer_loc_a_type"] == "port"), "addr_a_cat"] = 0
    fact_data.loc[import_filt & (fact_data["infer_loc_a_type"] == "depot"), "addr_a_cat"] = 1

    fact_data.loc[import_filt, ["infer_loc_b_type", "infer_loc_b_key", "infer_loc_b_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[import_filt, "addr_b"], depot_thresh_sim=0.8, port_thresh_sim=0.8)
    fact_data.loc[import_filt & (fact_data["infer_loc_b_type"] == "port"), "addr_b_cat"] = 0
    fact_data.loc[import_filt & (fact_data["infer_loc_b_type"] == "depot"), "addr_b_cat"] = 1
    filt = import_filt & pd.isna(fact_data["infer_loc_b_type"])
    fact_data.loc[filt, "addr_b_cat"] = 2
    fact_data.loc[filt & is_to_cust_filt, "loc_b_id"] = fact_data.loc[filt & is_to_cust_filt, "loc_b_as_building_id"].values

    # collect (a=depot/port, b=customer)
    collect_filt = fact_data["job_type"] == 2

    fact_data.loc[collect_filt, ["infer_loc_a_type", "infer_loc_a_key", "infer_loc_a_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[collect_filt, "addr_a"])
    fact_data.loc[collect_filt & (fact_data["infer_loc_a_type"] == "port"), "addr_a_cat"] = 0
    fact_data.loc[collect_filt & (fact_data["infer_loc_a_type"] == "depot"), "addr_a_cat"] = 1

    fact_data.loc[collect_filt, ["infer_loc_b_type", "infer_loc_b_key", "infer_loc_b_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[collect_filt, "addr_b"], depot_thresh_sim=0.8, port_thresh_sim=0.8)
    fact_data.loc[collect_filt & (fact_data["infer_loc_b_type"] == "port"), "addr_b_cat"] = 0
    fact_data.loc[collect_filt & (fact_data["infer_loc_b_type"] == "depot"), "addr_b_cat"] = 1
    filt = collect_filt & pd.isna(fact_data["infer_loc_b_type"])
    fact_data.loc[filt, "addr_b_cat"] = 2
    fact_data.loc[filt & is_to_cust_filt, "loc_b_id"] = fact_data.loc[filt & is_to_cust_filt, "loc_b_as_building_id"].values

    # return (a=customer, b=depot/port)
    return_filt = fact_data["job_type"] == 3

    fact_data.loc[return_filt, ["infer_loc_b_type", "infer_loc_b_key", "infer_loc_b_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[return_filt, "addr_b"])
    fact_data.loc[return_filt & (fact_data["infer_loc_b_type"] == "port"), "addr_b_cat"] = 0
    fact_data.loc[return_filt & (fact_data["infer_loc_b_type"] == "depot"), "addr_b_cat"] = 1

    fact_data.loc[return_filt, ["infer_loc_a_type", "infer_loc_a_key", "infer_loc_a_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[return_filt, "addr_a"], depot_thresh_sim=0.8, port_thresh_sim=0.8)
    fact_data.loc[return_filt & (fact_data["infer_loc_a_type"] == "port"), "addr_a_cat"] = 0
    fact_data.loc[return_filt & (fact_data["infer_loc_a_type"] == "depot"), "addr_a_cat"] = 1
    filt = return_filt & pd.isna(fact_data["infer_loc_a_type"])
    fact_data.loc[filt, "addr_a_cat"] = 2
    fact_data.loc[filt & is_from_cust_filt, "loc_a_id"] = fact_data.loc[filt & is_from_cust_filt, "loc_a_as_building_id"].values

    # other types
    other_filt = fact_data["job_type"].isin([0, 1, 2, 3]) == False

    fact_data.loc[other_filt, ["infer_loc_a_type", "infer_loc_a_key", "infer_loc_a_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[other_filt, "addr_a"], depot_thresh_sim=0.8, port_thresh_sim=0.8)
    fact_data.loc[other_filt & (fact_data["infer_loc_a_type"] == "port"), "addr_a_cat"] = 0
    fact_data.loc[other_filt & (fact_data["infer_loc_a_type"] == "depot"), "addr_a_cat"] = 1
    filt = other_filt & pd.isna(fact_data["infer_loc_a_type"])
    fact_data.loc[filt, "addr_a_cat"] = 2
    fact_data.loc[filt & is_from_cust_filt, "loc_a_id"] = fact_data.loc[filt & is_from_cust_filt, "loc_a_as_building_id"].values

    fact_data.loc[other_filt, ["infer_loc_b_type", "infer_loc_b_key", "infer_loc_b_sim"]] = infer_sg_cp_depot_or_port(
        fact_data.loc[other_filt, "addr_b"], depot_thresh_sim=0.8, port_thresh_sim=0.8)
    fact_data.loc[other_filt & (fact_data["infer_loc_b_type"] == "port"), "addr_b_cat"] = 0
    fact_data.loc[other_filt & (fact_data["infer_loc_b_type"] == "depot"), "addr_b_cat"] = 1
    filt = other_filt & pd.isna(fact_data["infer_loc_b_type"])
    fact_data.loc[filt, "addr_b_cat"] = 2
    fact_data.loc[filt & is_to_cust_filt, "loc_b_id"] = fact_data.loc[filt & is_to_cust_filt, "loc_b_as_building_id"].values

    filt = other_filt & (fact_data["addr_a_cat"] == 2) & (fact_data["addr_b_cat"] == 2) & is_from_cust_filt & is_to_cust_filt & (
                fact_data["loc_a_id"] == fact_data["loc_b_id"]) & (fact_data["addr_a"] != fact_data["addr_b"])
    fact_data.loc[filt, ["loc_a_id", "loc_b_id"]] = -1

    filt = (fact_data["addr_a_cat"] == 0) & (fact_data["infer_loc_a_key"] != -1)
    fact_data.loc[filt, "port_key"] = fact_data.loc[filt, "infer_loc_a_key"].values
    filt = (fact_data["addr_b_cat"] == 0) & (fact_data["infer_loc_b_key"] != -1)
    fact_data.loc[filt, "port_key"] = fact_data.loc[filt, "infer_loc_b_key"].values
    fact_data["port_key"] = fact_data["port_key"].fillna(-1).astype(int)

    filt = (fact_data["addr_a_cat"] == 1) & (fact_data["infer_loc_a_key"] != -1)
    fact_data.loc[filt, "depot_key"] = fact_data.loc[filt, "infer_loc_a_key"].values
    filt = (fact_data["addr_b_cat"] == 1) & (fact_data["infer_loc_b_key"] != -1)
    fact_data.loc[filt, "depot_key"] = fact_data.loc[filt, "infer_loc_b_key"].values
    fact_data["depot_key"] = fact_data["depot_key"].fillna(-1).astype(int)

    latest_deloc_key = geo_master.loc[
        (geo_master.type == "Delivery") & (pd.isna(geo_master["source_id"]) == False), ["key", "source_id"]].groupby("source_id",
                                                                                                                     as_index=False).last()
    latest_deloc_key["source_id"] = latest_deloc_key["source_id"].astype(int)
    latest_deloc_key.columns = ["delivery_building_id", "delivery_key"]
    fact_data = fact_data.merge(latest_deloc_key, how="left", on="delivery_building_id")
    fact_data["delivery_key"] = fact_data["delivery_key"].fillna(-1).astype(int)

    geo_master.loc[geo_master.type == "Port", "cat"] = 0
    geo_master.loc[geo_master.type == "Depot", "cat"] = 1
    geo_master.loc[geo_master.type == "Delivery", "cat"] = 2
    latest_key = geo_master.loc[
        (pd.isna(geo_master["type"]) == False) & (pd.isna(geo_master["source_id"]) == False), ["key", "source_id", "cat"]].groupby(
        ["cat", "source_id"], as_index=False).last()
    latest_key["cat"] = latest_key["cat"].astype(int)
    latest_key["source_id"] = latest_key["source_id"].astype(int)

    latest_key.columns = ["addr_a_cat", "loc_a_id", "loc_a_key"]
    fact_data = fact_data.merge(latest_key, how="left", on=["loc_a_id", "addr_a_cat"])
    filt = fact_data["infer_loc_a_key"] != -1
    fact_data.loc[filt, "loc_a_key"] = fact_data.loc[filt, "infer_loc_a_key"].values
    fact_data["loc_a_key"] = fact_data["loc_a_key"].fillna(-1).astype(int)

    latest_key.columns = ["addr_b_cat", "loc_b_id", "loc_b_key"]
    fact_data = fact_data.merge(latest_key, how="left", on=["loc_b_id", "addr_b_cat"])
    filt = fact_data["infer_loc_b_key"] != -1
    fact_data.loc[filt, "loc_b_key"] = fact_data.loc[filt, "infer_loc_b_key"].values
    fact_data["loc_b_key"] = fact_data["loc_b_key"].fillna(-1).astype(int)

    return fact_data


def post_derive_sg_trip_geo_keys(fact_data, geo_master, next_geo_key):
    fact_data, new_geo_master_key, new_geo_master_searchkey, new_geo_master_block, new_geo_master_road, new_geo_master_postal, new_geo_master_lat, new_geo_master_lng = process_sg_trip_location_data(
        fact_data, geo_master, next_geo_key)

    if len(new_geo_master_key) > 0:
        df = pd.DataFrame({
            "key": new_geo_master_key,
            "searchkey": new_geo_master_searchkey,
            "block": new_geo_master_block,
            "road": new_geo_master_road,
            "postal": new_geo_master_postal,
            "lat": new_geo_master_lat,
            "lng": new_geo_master_lng,
            "valid": [True] * len(new_geo_master_key)
        })
        df["valid"] = (pd.isna(df["lat"]) == False) & (pd.isna(df["lng"]) == False) & (df["lat"] != 0) & (df["lng"] != 0) & (
                    np.abs(df["lat"]) < 90) & (np.abs(df["lng"]) < 180)
        df["key"] = df["key"].astype(int)

        invalid_keys = df.loc[df["valid"] == False, "key"].values
        fact_data.loc[fact_data["loc_a_key"].isin(invalid_keys), "loc_a_key"] = -1
        fact_data.loc[fact_data["loc_b_key"].isin(invalid_keys), "loc_b_key"] = -1
        fact_data.loc[fact_data["depot_key"].isin(invalid_keys), "depot_key"] = -1
        fact_data.loc[fact_data["port_key"].isin(invalid_keys), "port_key"] = -1
        fact_data.loc[fact_data["delivery_key"].isin(invalid_keys), "delivery_key"] = -1

        new_geo_master_key = df.loc[df["valid"], "key"].values
        new_geo_master_searchkey = df.loc[df["valid"], "searchkey"].values
        new_geo_master_block = df.loc[df["valid"], "block"].values
        new_geo_master_road = df.loc[df["valid"], "road"].values
        new_geo_master_postal = df.loc[df["valid"], "postal"].values
        new_geo_master_lat = df.loc[df["valid"], "lat"].values
        new_geo_master_lng = df.loc[df["valid"], "lng"].values

    fact_data["port_key"] = fact_data["port_key"].fillna(-1).astype(int)
    fact_data["depot_key"] = fact_data["depot_key"].fillna(-1).astype(int)
    fact_data["delivery_key"] = fact_data["delivery_key"].fillna(-1).astype(int)
    fact_data["loc_a_key"] = fact_data["loc_a_key"].fillna(-1).astype(int)
    fact_data["loc_b_key"] = fact_data["loc_b_key"].fillna(-1).astype(int)

    return fact_data, np.array(new_geo_master_key,
                               dtype=int), new_geo_master_searchkey, new_geo_master_block, new_geo_master_road, new_geo_master_postal, new_geo_master_lat, new_geo_master_lng


def get_key_location(job_data, city_geo_master, location_types="delivery"):
    fact_data = pre_derive_sg_job_geo_keys(job_data.copy(), city_geo_master)
    fact_data, new_geo_master_key, _, _, _, _, new_geo_master_lat, new_geo_master_lng = post_derive_sg_job_geo_keys(fact_data, city_geo_master, 200000000)

    new_geo_master_key = np.array(new_geo_master_key, dtype=int)

    if type(location_types) == str:
        location_type = location_types
        points = np.zeros((len(fact_data), 2), dtype=float)
        for i, key_val in enumerate(fact_data["{}_key".format(location_type)].values):
            if (pd.isna(key_val) == False) and (key_val != 0):
                if len(new_geo_master_key) > 0:
                    new_key_index = np.argwhere(new_geo_master_key == key_val)
                    if len(new_key_index) > 0:
                        points[i] = [new_geo_master_lat[new_key_index[0][0]], new_geo_master_lng[new_key_index[0][0]]]
                    elif key_val > 0:
                        points[i] = [city_geo_master.loc[key_val, "lat"], city_geo_master.loc[key_val, "lng"]]
                elif key_val > 0:
                    points[i] = [city_geo_master.loc[key_val, "lat"], city_geo_master.loc[key_val, "lng"]]
    elif (type(location_types) == list) or (type(location_types) == np.ndarray):
        points = np.zeros((len(location_types), len(fact_data), 2), dtype=float)
        for t, location_type in enumerate(location_types):
            for i, key_val in enumerate(fact_data["{}_key".format(location_type)].values):
                if (pd.isna(key_val) == False) and (key_val != 0):
                    if len(new_geo_master_key) > 0:
                        new_key_index = np.argwhere(new_geo_master_key == key_val)
                        if len(new_key_index) > 0:
                            points[t, i] = [new_geo_master_lat[new_key_index[0][0]],
                                               new_geo_master_lng[new_key_index[0][0]]]
                        elif key_val > 0:
                            points[t, i] = [city_geo_master.loc[key_val, "lat"], city_geo_master.loc[key_val, "lng"]]
                    elif key_val > 0:
                        points[t, i] = [city_geo_master.loc[key_val, "lat"], city_geo_master.loc[key_val, "lng"]]

    return points


def get_cluster(sorted_clust_params, lat, lng, allowance=0.001, n_std=3):
    for i, row in sorted_clust_params.iterrows():
        center_lat = row["center.lat"]
        center_lng = row["center.lng"]
        lat_std = max(row["lat.std"], allowance)
        lng_std = max(row["lng.std"], allowance)
        a, b = lat_std * n_std, lng_std * n_std
        if (lat - center_lat) ** 2 / a ** 2 + (lng - center_lng) ** 2 / b ** 2 < 1:
            return row[0]
    return -1
