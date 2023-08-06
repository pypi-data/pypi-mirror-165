import re
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import textdistance
import pickle

from ..shared import ValidationException

lv1_areas = None
lv2_areas = None
lv3_areas = None
lv3_native_vectorizer = None
lv2_native_vectorizer = None
lv1_native_vectorizer = None
lv3_en_vectorizer = None
lv2_en_vectorizer = None
lv1_en_vectorizer = None
lv3_concat_en_vectorizer = None
mtx_lv3_native = None
mtx_lv2_native = None
mtx_lv1_native = None
mtx_lv3_en = None
mtx_lv2_en = None
mtx_lv1_en = None
mtx_lv3_concat_en = None

POSTAL_CODE_EXP = "((\d{5})(?:$|[ ,]+.+$))"
PLUS_CODE_EXP = "(?:^|,|^.+ )([A-Z\d]+\+[A-Z\d]+)[ ,]+"
HOUSE_NO_EXP1 = "((?:^|,|^.+ )((\d{1,3})/\d{1,3}-\d{1,3}/\d{1,3})[ ,]+)\w"
HOUSE_NO_EXP2 = "((?:^|,|^.+ )((\d{1,3})/\d{1,3}-\d{1,3})[ ,]+)\w"
HOUSE_NO_EXP3 = "((?:^|,|^.+ )(\d{1,3}-\d{1,3}/(\d{1,3}))[ ,]+)\w"
HOUSE_NO_EXP4 = "((?:^|,|^.+ )((\d{1,3})[/ ]\d{1,3})[ ,]+)\w"
HOUSE_NO_EXP5 = "((?:^|,|^.+ )(?:No(?:\.|\. | ))?(\d{1,4})[ ,]+)\w"
VILLAGE_EXP = "(?i)(?:^|,| )(?:หมู่ที่|หมู่ที่|หมู่|ม .|ม.|Moo|Mu)\s?(\d+)"
ROAD_EXP1 = "(?i)(?:^|,| )(?:(Soi [A-Za-z\- ]+(?: \d{1,4})?)|((?:ซอย|ถนน) [^ ]+(?: \d{1,4})?)|((?:ถ |ถ|ชบ)\.[^ ]+(?: \d{1,4})?))(?: |,|$)"
ROAD_EXP2 = "(?i)(?:^|(?:[^A-Za-z\-\. ]))([A-Za-z\-\. ]+ (?:\d{1,4} )?(?:Soi|Road|Raod|Rd\.?|Highway|Alley)(?: \d{1,4})?)(?: |,|$)"


def load_thai_admin_areas(dir_path):
    global lv1_areas
    global lv2_areas
    global lv3_areas
    global lv3_native_vectorizer
    global lv2_native_vectorizer
    global lv1_native_vectorizer
    global lv3_en_vectorizer
    global lv2_en_vectorizer
    global lv1_en_vectorizer
    global lv3_concat_en_vectorizer
    global mtx_lv3_native
    global mtx_lv2_native
    global mtx_lv1_native
    global mtx_lv3_en
    global mtx_lv2_en
    global mtx_lv1_en
    global mtx_lv3_concat_en

    lv1_areas = pd.read_parquet(dir_path + "/thai_lv1_admin_areas.parquet")
    lv2_areas = pd.read_parquet(dir_path + "/thai_lv2_admin_areas.parquet")
    lv3_areas = pd.read_parquet(dir_path + "/thai_lv3_admin_areas.parquet")
    with open(dir_path + "/thai_lv3_native_vectorizer.pickle", "rb") as f:
        lv3_native_vectorizer = pickle.load(f)
    with open(dir_path + "/thai_lv2_native_vectorizer.pickle", "rb") as f:
        lv2_native_vectorizer = pickle.load(f)
    with open(dir_path + "/thai_lv1_native_vectorizer.pickle", "rb") as f:
        lv1_native_vectorizer = pickle.load(f)
    with open(dir_path + "/thai_lv3_en_vectorizer.pickle", "rb") as f:
        lv3_en_vectorizer = pickle.load(f)
    with open(dir_path + "/thai_lv2_en_vectorizer.pickle", "rb") as f:
        lv2_en_vectorizer = pickle.load(f)
    with open(dir_path + "/thai_lv1_en_vectorizer.pickle", "rb") as f:
        lv1_en_vectorizer = pickle.load(f)
    with open(dir_path + "/thai_lv3_concat_en_vectorizer.pickle", "rb") as f:
        lv3_concat_en_vectorizer = pickle.load(f)
    with open(dir_path + "/thai_mtx_lv3_native.pickle", "rb") as f:
        mtx_lv3_native = pickle.load(f)
    with open(dir_path + "/thai_mtx_lv2_native.pickle", "rb") as f:
        mtx_lv2_native = pickle.load(f)
    with open(dir_path + "/thai_mtx_lv1_native.pickle", "rb") as f:
        mtx_lv1_native = pickle.load(f)
    with open(dir_path + "/thai_mtx_lv3_en.pickle", "rb") as f:
        mtx_lv3_en = pickle.load(f)
    with open(dir_path + "/thai_mtx_lv2_en.pickle", "rb") as f:
        mtx_lv2_en = pickle.load(f)
    with open(dir_path + "/thai_mtx_lv1_en.pickle", "rb") as f:
        mtx_lv1_en = pickle.load(f)
    with open(dir_path + "/thai_mtx_lv3_concat_en.pickle", "rb") as f:
        mtx_lv3_concat_en = pickle.load(f)


def char_level(txt):
    for word in txt.split():
        for cha in word:
            yield cha


def token_level(txt):
    for word in txt.split(" "):
        yield word.strip(",")


def extract_postal(text, default_value=None):
    match = re.search(POSTAL_CODE_EXP, text[-20:])
    if match is not None:
        return match[2], match[1]
    else:
        return default_value, None


def extract_plus_code(text):
    substr = text[:40]

    match = re.search(PLUS_CODE_EXP, substr)
    if match is not None:
        return match[1], match[0]
    else:
        return None, None


def extract_village_no(text):
    substr = text[:40]

    match = re.search(VILLAGE_EXP, substr)
    if match is not None:
        return match[1], match[0]
    else:
        return None, None


def extract_street_name(text):
    match = re.search(ROAD_EXP1, text)
    if match is not None:
        for k in range(1, len(match.groups()) + 1):
            if match[k] is not None:
                return match[k], match[0]
        return match[0], match[0]

    match = re.search(ROAD_EXP2, text)
    if match is not None:
        return match[1].strip(), match[1]

    else:
        return None, None


def extract_house_no(text):
    substr = text[:30]

    match = re.search(HOUSE_NO_EXP1, substr)
    if match is not None:
        return match[2], match[1]

    match = re.search(HOUSE_NO_EXP2, substr)
    if match is not None:
        return match[2], match[1]

    match = re.search(HOUSE_NO_EXP3, substr)
    if match is not None:
        return match[2], match[1]

    match = re.search(HOUSE_NO_EXP4, substr)
    if match is not None:
        return match[2], match[1]

    match = re.search(HOUSE_NO_EXP5, substr)
    if match is not None:
        return match[2], match[1]

    return None, None


def reposition_and_replace(text, replace_postal_code=None):
    if replace_postal_code is None:
        processed = text
    else:
        processed = text.replace(replace_postal_code, "").strip()
    if processed.find("TAMBON ") >= 0:
        processed = processed.replace("TAMBON ", "") + " SUBDISTRICT"
    if processed.find("KHWAENG ") >= 0:
        processed = processed.replace("KHWAENG ", "") + " SUBDISTRICT"
    if processed.find("AMPHOE ") >= 0:
        processed = processed.replace("AMPHOE ", "") + " DISTRICT"
    if processed.find("KHET ") >= 0:
        processed = processed.replace("KHET ", "") + " DISTRICT"
    if processed.find("CHANG WAT ") >= 0:
        processed = processed.replace("CHANG WAT ", "") + " PROVINCE"
    if processed.find("KRUNG THEP MAHA NAKHON") >= 0:
        processed = processed.replace("KRUNG THEP MAHA NAKHON", "BANGKOK")
    if processed.find("ตำบล") == 0:
        processed = "ต." + processed[4:]
    if processed.find("อำเภอ") == 0:
        processed = "อ." + processed[5:]
    if processed.find("จังหวัด") == 0:
        processed = "จ." + processed[7:]
    if processed.find("เขต") == 0:
        processed = processed[3:]
    return processed.strip()


def derive_from_prev_levels(df_valid_match):
    df_valid_match_derived = (df_valid_match
        .merge(lv3_areas[["lv2_en", "lv1_en"]].rename(columns={
            "lv2_en": "lv2_en_derived_from_lv3",
            "lv1_en": "lv1_en_derived_from_lv3"}), left_on="lv3_area_ind", right_index=True, how="left")
        .merge(lv2_areas[["lv1_en"]].rename(columns={
            "lv1_en": "lv1_en_derived_from_lv2"}), left_on="lv2_area_ind", right_index=True, how="left")
    )
    df_valid_match_derived["lv2_en"] = df_valid_match_derived["lv2_en"].fillna(df_valid_match_derived["lv2_en_derived_from_lv3"])
    df_valid_match_derived["lv1_en"] = df_valid_match_derived["lv1_en"].fillna(df_valid_match_derived["lv1_en_derived_from_lv2"]).fillna(df_valid_match_derived["lv1_en_derived_from_lv3"])
    df_valid_match_derived["concat"] = df_valid_match_derived["lv3_en"].fillna("-") + ", " + df_valid_match_derived["lv2_en"].fillna("-") + ", " + df_valid_match_derived["lv1_en"].fillna("-")
    return df_valid_match_derived


def select_best(df_lv3_good_match_ind, df_lv2_good_match_ind, df_lv1_good_match_ind, skip_part_index_validation=False, print_log=False):
    df_good_match_ind = (df_lv3_good_match_ind
        .merge(df_lv2_good_match_ind, on="_", how="outer")
        .merge(df_lv1_good_match_ind, on="_", how="outer")
     )

    without_lv1_filt = pd.isna(df_good_match_ind["lv1_part_ind"])
    if not skip_part_index_validation:
        delta_lv1lv3 = df_good_match_ind["lv1_part_ind"] - df_good_match_ind["lv3_part_ind"]
        delta_lv1lv2 = df_good_match_ind["lv1_part_ind"] - df_good_match_ind["lv2_part_ind"]
        delta_lv2lv3 = df_good_match_ind["lv2_part_ind"] - df_good_match_ind["lv3_part_ind"]

        valid_lv3_given_lv1_filt = delta_lv1lv3.isin([1, 2, 3]) & (without_lv1_filt == False)
        odd_lv3_given_lv1_filt = (delta_lv1lv3.isin([1, 2, 3]) == False) & (without_lv1_filt == False)
        df_good_match_ind.loc[odd_lv3_given_lv1_filt, "lv3_part_ind"] = None
        df_good_match_ind.loc[odd_lv3_given_lv1_filt, "lv3_sim"] = 0
        df_good_match_ind.loc[odd_lv3_given_lv1_filt, "lv3_area_ind"] = -1
        df_good_match_ind.loc[odd_lv3_given_lv1_filt, "lv3_en"] = None
        df_good_match_ind.loc[odd_lv3_given_lv1_filt, "lv3_part_ind"] = None

        odd_lv3_given_lv1lv2_filt = delta_lv1lv2.isin([1, 2]) & (delta_lv2lv3 == 0)
        df_good_match_ind.loc[odd_lv3_given_lv1lv2_filt, "lv3_part_ind"] = None
        df_good_match_ind.loc[odd_lv3_given_lv1lv2_filt, "lv3_sim"] = 0
        df_good_match_ind.loc[odd_lv3_given_lv1lv2_filt, "lv3_area_ind"] = -1
        df_good_match_ind.loc[odd_lv3_given_lv1lv2_filt, "lv3_en"] = None
        df_good_match_ind.loc[odd_lv3_given_lv1lv2_filt, "lv3_part_ind"] = None

        odd_lv2_given_lv1lv3_filt = (df_good_match_ind["lv2_part_ind"].astype(float) >= df_good_match_ind["lv1_part_ind"].astype(float)) | (df_good_match_ind["lv3_part_ind"].astype(float) >= df_good_match_ind["lv2_part_ind"].astype(float))
        df_good_match_ind.loc[valid_lv3_given_lv1_filt & odd_lv2_given_lv1lv3_filt, "lv2_part_ind"] = None
        df_good_match_ind.loc[valid_lv3_given_lv1_filt & odd_lv2_given_lv1lv3_filt, "lv2_sim"] = 0
        df_good_match_ind.loc[valid_lv3_given_lv1_filt & odd_lv2_given_lv1lv3_filt, "lv2_area_ind"] = -1
        df_good_match_ind.loc[valid_lv3_given_lv1_filt & odd_lv2_given_lv1lv3_filt, "lv2_en"] = None

        odd_lv2_given_lv1_filt = (delta_lv1lv2.isin([1, 2]) == False) & (without_lv1_filt == False)
        df_good_match_ind.loc[odd_lv2_given_lv1_filt, "lv2_part_ind"] = None
        df_good_match_ind.loc[odd_lv2_given_lv1_filt, "lv2_sim"] = 0
        df_good_match_ind.loc[odd_lv2_given_lv1_filt, "lv2_area_ind"] = -1
        df_good_match_ind.loc[odd_lv2_given_lv1_filt, "lv2_en"] = None

        delta_lv2lv3 = df_good_match_ind["lv2_part_ind"] - df_good_match_ind["lv3_part_ind"]
        valid_lv3_lv2 = delta_lv2lv3.isin([1, 2]) | pd.isna(delta_lv2lv3)
    else:
        valid_lv3_lv2 = np.ones(len(df_good_match_ind), dtype=bool)

    df_good_match_ind["avg_sim"] = (df_good_match_ind["lv3_sim"]*0.1 + df_good_match_ind["lv2_sim"]*0.35 + df_good_match_ind["lv1_sim"]*0.55)
    df_good_match_ind["concat"] = df_good_match_ind["lv3_en"].fillna("-") + ", " + df_good_match_ind["lv2_en"].fillna("-") + ", " + df_good_match_ind["lv1_en"].fillna("-")

    df_valid_match = df_good_match_ind.loc[(valid_lv3_lv2 | without_lv1_filt) & (df_good_match_ind["avg_sim"] > 0), :].sort_values("avg_sim", ascending=False)

    if len(df_valid_match) > 0:
        tentative_best_match = df_valid_match.iloc[0, :]
        if print_log:
            print("temp best:", tentative_best_match["concat"])

        df_match_derived = derive_from_prev_levels(df_valid_match.sort_values("avg_sim", ascending=False))
        concat_en = lv3_concat_en_vectorizer.transform(df_match_derived["concat"].values)
        sim_concat = cosine_similarity(concat_en, mtx_lv3_concat_en)
        df_match_derived["concat_sim"] = np.max(sim_concat, axis=1)
        df_match_derived["sim"] = np.maximum(df_match_derived["concat_sim"], df_match_derived["avg_sim"])*0.9 + np.minimum(df_match_derived["concat_sim"], df_match_derived["avg_sim"])*0.1

        df_match_derived = df_match_derived.sort_values("sim", ascending=False)
        best_match = df_match_derived.iloc[0, :]
        if print_log:
            print("best:", best_match["concat"], best_match["sim"])
            print(df_match_derived[["lv3_en", "lv3_sim", "lv2_en", "lv2_sim", "lv1_en", "lv1_sim", "avg_sim", "concat_sim", "sim", "lv3_part_ind", "lv2_part_ind", "lv1_part_ind"]])
        return (
            None if pd.isna(best_match["lv3_en"]) else best_match["lv3_en"].replace(" SUBDISTRICT", ""),
            None if pd.isna(best_match["lv2_en"]) else best_match["lv2_en"].replace(" DISTRICT", ""),
            None if pd.isna(best_match["lv1_en"]) else best_match["lv1_en"].replace(" PROVINCE", ""),
            float(best_match["sim"])
        )
    else:
        if print_log:
            print("null")
        return None, None, None, 0


def jaro_winkler_similarity(arr_a, arr_b):
    mtx = np.zeros((len(arr_a), len(arr_b)))
    for i, text_a in enumerate(arr_a):
        for j, text_b in enumerate(arr_b):
            mtx[i, j] = textdistance.jaro_winkler(text_a, text_b)
    return mtx


def extract_admin_areas(text, print_log=False):
    parts_by_space = [p for p in [reposition_and_replace(p.strip().strip(",")) for p in text.upper().split(" ")] if p != ""]
    if print_log:
        print("input parts:", parts_by_space)

    parts_by_space_by_lv1_native = lv1_native_vectorizer.transform(np.array(parts_by_space))
    cos_sim_parts_by_space_vs_lv1_native = cosine_similarity(parts_by_space_by_lv1_native, mtx_lv1_native)
    jw_sim_parts_by_space_vs_lv1_native = jaro_winkler_similarity(parts_by_space, lv1_areas["lv1_native"])
    sim_parts_by_space_vs_lv1_native = np.maximum(cos_sim_parts_by_space_vs_lv1_native, jw_sim_parts_by_space_vs_lv1_native)
    good_filt = sim_parts_by_space_vs_lv1_native > 0.8
    lv1_good_match_ind = np.argwhere(good_filt)
    if len(lv1_good_match_ind) > 0:
        df_lv1_good_match_ind = pd.DataFrame({
            "lv1_part_ind": lv1_good_match_ind[:, 0],
            "lv1_area_ind": lv1_good_match_ind[:, 1],
            "lv1_en": lv1_areas["lv1_en"].values[lv1_good_match_ind[:, 1]],
            "lv1_sim": sim_parts_by_space_vs_lv1_native[good_filt],
            "_": ["_"] * len(lv1_good_match_ind)
        })
    else:
        df_lv1_good_match_ind = pd.DataFrame({
            "lv1_part_ind": [None],
            "lv1_area_ind": [-1],
            "lv1_en": [None],
            "lv1_sim": [0],
            "_": ["_"]
        })

    parts_by_space_by_lv2_native = lv2_native_vectorizer.transform(np.array(parts_by_space))
    lv1_good_match_names = [p.replace(" PROVINCE", "") for p in df_lv1_good_match_ind["lv1_en"] if p is not None]
    lv2_subset_indices = np.argwhere(lv2_areas["lv1_en"].isin(lv1_good_match_names).values).flatten()
    lv2_subset_indices = np.concatenate([lv2_subset_indices, lv2_subset_indices + 1])
    if len(lv2_subset_indices) > 0:
        cos_sim_parts_by_space_vs_lv2_native = cosine_similarity(parts_by_space_by_lv2_native, mtx_lv2_native[lv2_subset_indices, :])
        jw_sim_parts_by_space_vs_lv2_native = jaro_winkler_similarity(parts_by_space, lv2_areas["lv2_native"].values[lv2_subset_indices])
        sim_parts_by_space_vs_lv2_native = np.maximum(cos_sim_parts_by_space_vs_lv2_native, jw_sim_parts_by_space_vs_lv2_native)
        good_filt = sim_parts_by_space_vs_lv2_native > 0.9
        lv2_good_match_ind = np.argwhere(good_filt)
        if len(lv2_good_match_ind) > 0:
            area_ind = lv2_subset_indices[lv2_good_match_ind[:, 1]]
            df_lv2_good_match_ind = pd.DataFrame({
                "lv2_part_ind": lv2_good_match_ind[:, 0],
                "lv2_area_ind": area_ind,
                "lv2_en": lv2_areas["lv2_en"].values[area_ind],
                "lv2_sim": sim_parts_by_space_vs_lv2_native[good_filt],
                "_": ["_"] * len(lv2_good_match_ind)
            })
        else:
            df_lv2_good_match_ind = pd.DataFrame({
                "lv2_part_ind": [None],
                "lv2_area_ind": [-1],
                "lv2_en": [None],
                "lv2_sim": [0],
                "_": ["_"]
            })
    else:
        sim_parts_by_space_vs_lv2_native = cosine_similarity(parts_by_space_by_lv2_native, mtx_lv2_native)
        good_filt = sim_parts_by_space_vs_lv2_native > 0.9
        lv2_good_match_ind = np.argwhere(good_filt)
        if len(lv2_good_match_ind) > 0:
            df_lv2_good_match_ind = pd.DataFrame({
                "lv2_part_ind": lv2_good_match_ind[:, 0],
                "lv2_area_ind": lv2_good_match_ind[:, 1],
                "lv2_en": lv2_areas["lv2_en"].values[lv2_good_match_ind[:, 1]],
                "lv2_sim": sim_parts_by_space_vs_lv2_native[good_filt],
                "_": ["_"] * len(lv2_good_match_ind)
            })
        else:
            df_lv2_good_match_ind = pd.DataFrame({
                "lv2_part_ind": [None],
                "lv2_area_ind": [-1],
                "lv2_en": [None],
                "lv2_sim": [0],
                "_": ["_"]
            })

    parts_by_space_by_lv3_native = lv3_native_vectorizer.transform(np.array(parts_by_space))
    lv2_good_match_names = [p.replace(" DISTRICT", "") for p in df_lv2_good_match_ind["lv2_en"] if p is not None]
    lv3_subset_indices = np.argwhere(lv3_areas["lv2_en"].isin(lv2_good_match_names).values).flatten()
    if (len(lv3_subset_indices) == 0) and (len(lv1_good_match_names) > 0):
        lv3_subset_indices = np.argwhere(lv3_areas["lv1_en"].isin(lv1_good_match_names).values).flatten()
    lv3_subset_indices = np.concatenate([lv3_subset_indices, lv3_subset_indices + 1])
    if len(lv3_subset_indices) > 0:
        cos_sim_parts_by_space_vs_lv3_native = cosine_similarity(parts_by_space_by_lv3_native, mtx_lv3_native[lv3_subset_indices, :])
        jw_sim_parts_by_space_vs_lv3_native = jaro_winkler_similarity(parts_by_space, lv3_areas["lv3_native"].values[lv3_subset_indices])
        sim_parts_by_space_vs_lv3_native = np.maximum(cos_sim_parts_by_space_vs_lv3_native, jw_sim_parts_by_space_vs_lv3_native)
        filt_good = sim_parts_by_space_vs_lv3_native > 0.9
        lv3_good_match_ind = np.argwhere(filt_good)
        if len(lv3_good_match_ind) > 0:
            area_ind = lv3_subset_indices[lv3_good_match_ind[:, 1]]
            df_lv3_good_match_ind = pd.DataFrame({
                "lv3_part_ind": lv3_good_match_ind[:, 0],
                "lv3_area_ind": area_ind,
                "lv3_en": lv3_areas["lv3_en"].values[area_ind],
                "lv3_sim": sim_parts_by_space_vs_lv3_native[filt_good],
                "_": ["_"] * len(lv3_good_match_ind)
            })
        else:
            df_lv3_good_match_ind = pd.DataFrame({
                "lv3_part_ind": [None],
                "lv3_area_ind": [-1],
                "lv3_en": [None],
                "lv3_sim": [0],
                "_": ["_"]
            })
    else:
        sim_parts_by_space_vs_lv3_native = cosine_similarity(parts_by_space_by_lv3_native, mtx_lv3_native)
        filt_good = sim_parts_by_space_vs_lv3_native > 0.9
        lv3_good_match_ind = np.argwhere(filt_good)
        if len(lv3_good_match_ind) > 0:
            df_lv3_good_match_ind = pd.DataFrame({
                "lv3_part_ind": lv3_good_match_ind[:, 0],
                "lv3_area_ind": lv3_good_match_ind[:, 1],
                "lv3_en": lv3_areas["lv3_en"].values[lv3_good_match_ind[:, 1]],
                "lv3_sim": sim_parts_by_space_vs_lv3_native[filt_good],
                "_": ["_"] * len(lv3_good_match_ind)
            })
        else:
            df_lv3_good_match_ind = pd.DataFrame({
                "lv3_part_ind": [None],
                "lv3_area_ind": [-1],
                "lv3_en": [None],
                "lv3_sim": [0],
                "_": ["_"]
            })

    lv3_native, lv2_native, lv1_native, sim_native = select_best(df_lv3_good_match_ind, df_lv2_good_match_ind, df_lv1_good_match_ind)

    if (lv2_native is not None) and (lv1_native is not None) and (sim_native > 0.95):
        return lv3_native, lv2_native, lv1_native, sim_native
    else:
        native_en_mixed = False

        parts_by_comma = [p for p in [reposition_and_replace(p) for p in text.upper().split(",") if p != ""] if p != ""]
        if print_log:
            print("input english parts:", parts_by_comma)

        parts_by_comma_by_lv1_en = lv1_en_vectorizer.transform(np.array(parts_by_comma))
        cos_sim_parts_by_comma_vs_lv1_en = cosine_similarity(parts_by_comma_by_lv1_en, mtx_lv1_en)
        jw_sim_parts_by_comma_vs_lv1_en = jaro_winkler_similarity(parts_by_comma, lv1_areas["lv1_en"])
        sim_parts_by_comma_vs_lv1_en = np.maximum(cos_sim_parts_by_comma_vs_lv1_en, jw_sim_parts_by_comma_vs_lv1_en)
        good_filt = sim_parts_by_comma_vs_lv1_en > 0.9
        lv1_good_match_ind = np.argwhere(good_filt)
        if len(lv1_good_match_ind) > 0:
            df_lv1_good_match_ind = pd.DataFrame({
                "lv1_part_ind": lv1_good_match_ind[:, 0],
                "lv1_area_ind": lv1_good_match_ind[:, 1],
                "lv1_en": lv1_areas["lv1_en"].values[lv1_good_match_ind[:, 1]],
                "lv1_sim": sim_parts_by_comma_vs_lv1_en[good_filt],
                "_": ["_"] * len(lv1_good_match_ind)
            })
        elif np.any(pd.isna(df_lv1_good_match_ind["lv1_en"]) == False):
            native_en_mixed = True

        parts_by_comma_by_lv2_en = lv2_en_vectorizer.transform(np.array(parts_by_comma))
        lv1_good_match_names = [p.replace(" PROVINCE", "") for p in df_lv1_good_match_ind["lv1_en"] if p is not None]
        lv2_subset_indices = np.argwhere(lv2_areas["lv1_en"].isin(lv1_good_match_names).values).flatten()
        lv2_subset_indices = np.concatenate([lv2_subset_indices, lv2_subset_indices + 1])
        if len(lv2_subset_indices) > 0:
            cos_sim_parts_by_comma_vs_lv2_en = cosine_similarity(parts_by_comma_by_lv2_en, mtx_lv2_en[lv2_subset_indices, :])
            jw_sim_parts_by_comma_vs_lv2_en = jaro_winkler_similarity(parts_by_comma, lv2_areas["lv2_en"].values[lv2_subset_indices])
            sim_parts_by_comma_vs_lv2_en = np.maximum(cos_sim_parts_by_comma_vs_lv2_en, jw_sim_parts_by_comma_vs_lv2_en)
            good_filt = sim_parts_by_comma_vs_lv2_en > 0.9
            lv2_good_match_ind = np.argwhere(good_filt)
            if len(lv2_good_match_ind) > 0:
                area_ind = lv2_subset_indices[lv2_good_match_ind[:, 1]]
                df_lv2_good_match_ind = pd.DataFrame({
                    "lv2_part_ind": lv2_good_match_ind[:, 0],
                    "lv2_area_ind": area_ind,
                    "lv2_en": lv2_areas["lv2_en"].values[area_ind],
                    "lv2_sim": sim_parts_by_comma_vs_lv2_en[good_filt],
                    "_": ["_"] * len(lv2_good_match_ind)
                })
            elif np.any(pd.isna(df_lv2_good_match_ind["lv2_en"]) == False):
                native_en_mixed = True
        else:
            sim_parts_by_comma_vs_lv2_en = cosine_similarity(parts_by_comma_by_lv2_en, mtx_lv2_en)
            good_filt = sim_parts_by_comma_vs_lv2_en > 0.9
            lv2_good_match_ind = np.argwhere(good_filt)
            if len(lv2_good_match_ind) > 0:
                df_lv2_good_match_ind = pd.DataFrame({
                    "lv2_part_ind": lv2_good_match_ind[:, 0],
                    "lv2_area_ind": lv2_good_match_ind[:, 1],
                    "lv2_en": lv2_areas["lv2_en"].values[lv2_good_match_ind[:, 1]],
                    "lv2_sim": sim_parts_by_comma_vs_lv2_en[good_filt],
                    "_": ["_"] * len(lv2_good_match_ind)
                })
            elif np.any(pd.isna(df_lv2_good_match_ind["lv2_en"]) == False):
                native_en_mixed = True

        parts_by_comma_by_lv3_en = lv3_en_vectorizer.transform(np.array(parts_by_comma))
        lv2_good_match_names = [p.replace(" DISTRICT", "") for p in df_lv2_good_match_ind["lv2_en"] if p is not None]
        lv3_subset_indices = np.argwhere(lv3_areas["lv2_en"].isin(lv2_good_match_names).values).flatten()
        if (len(lv3_subset_indices) == 0) and (len(lv1_good_match_names) > 0):
            lv3_subset_indices = np.argwhere(lv3_areas["lv1_en"].isin(lv1_good_match_names).values).flatten()
        lv3_subset_indices = np.concatenate([lv3_subset_indices, lv3_subset_indices + 1])
        if len(lv3_subset_indices) > 0:
            cos_sim_parts_by_comma_vs_lv3_en = cosine_similarity(parts_by_comma_by_lv3_en, mtx_lv3_en[lv3_subset_indices, :])
            jw_sim_parts_by_comma_vs_lv3_en = jaro_winkler_similarity(parts_by_comma, lv3_areas["lv3_en"].values[lv3_subset_indices])
            sim_parts_by_comma_vs_lv3_en = np.maximum(cos_sim_parts_by_comma_vs_lv3_en, jw_sim_parts_by_comma_vs_lv3_en)
            filt_good = sim_parts_by_comma_vs_lv3_en > 0.85
            lv3_good_match_ind = np.argwhere(filt_good)
            if len(lv3_good_match_ind) > 0:
                area_ind = lv3_subset_indices[lv3_good_match_ind[:, 1]]
                df_lv3_good_match_ind = pd.DataFrame({
                    "lv3_part_ind": lv3_good_match_ind[:, 0],
                    "lv3_area_ind": area_ind,
                    "lv3_en": lv3_areas["lv3_en"].values[area_ind],
                    "lv3_sim": sim_parts_by_comma_vs_lv3_en[filt_good],
                    "_": ["_"] * len(lv3_good_match_ind)
                })
            elif np.any(pd.isna(df_lv3_good_match_ind["lv3_en"]) == False):
                native_en_mixed = True
        else:
            sim_parts_by_comma_vs_lv3_en = cosine_similarity(parts_by_comma_by_lv3_en, mtx_lv3_en)
            filt_good = sim_parts_by_comma_vs_lv3_en > 0.85
            lv3_good_match_ind = np.argwhere(filt_good)
            if len(lv3_good_match_ind) > 0:
                df_lv3_good_match_ind = pd.DataFrame({
                    "lv3_part_ind": lv3_good_match_ind[:, 0],
                    "lv3_area_ind": lv3_good_match_ind[:, 1],
                    "lv3_en": lv3_areas["lv3_en"].values[lv3_good_match_ind[:, 1]],
                    "lv3_sim": sim_parts_by_comma_vs_lv3_en[filt_good],
                    "_": ["_"] * len(lv3_good_match_ind)
                })
            elif np.any(pd.isna(df_lv3_good_match_ind["lv3_en"]) == False):
                native_en_mixed = True

        lv3_en, lv2_en, lv1_en, sim_en = select_best(df_lv3_good_match_ind, df_lv2_good_match_ind, df_lv1_good_match_ind, skip_part_index_validation=native_en_mixed)

        if sim_en > sim_native:
            return lv3_en, lv2_en, lv1_en, sim_en
        else:
            return lv3_native, lv2_native, lv1_native, sim_native


def to_thai_address_object(addr_text, load_admin_area_path=None):
    if load_admin_area_path is not None:
        load_thai_admin_areas(load_admin_area_path)

    for_extract = addr_text

    postal, part = extract_postal(for_extract)
    if postal is not None:
        for_extract = for_extract.replace(part, ",")

    plus_code, part = extract_plus_code(for_extract)
    if plus_code is not None:
        for_extract = for_extract.replace(part, "")

    street, part = extract_street_name(for_extract)
    if street is not None:
        for_extract = for_extract.replace(part, ",")

    house_no, part = extract_house_no(for_extract)
    if house_no is not None:
        for_extract = for_extract.replace(part, ",")

    moo_no, part = extract_village_no(for_extract)
    if moo_no is not None:
        for_extract = for_extract.replace(part, ",")

    lv3, lv2, lv1, sim = extract_admin_areas(for_extract)

    return {
        "house_no": house_no,
        "moo_no": moo_no,
        "street": street,
        "admin_lv3": lv3,
        "admin_lv2": lv2,
        "admin_lv1": lv1,
        "admin_sim": sim,
        "postal_code": postal,
        "plus_code": plus_code
    }


def match_thai_vendor_addresses(customer_address, vendor_addresses, text_dist_thresh=0.85, validate_pinpoint_customer_address=False):
    result = {}

    if customer_address is not None:
        if type(customer_address) == str:
            if validate_pinpoint_customer_address and (customer_address == ""):
                raise ValidationException("Customer Address is empty.")
            cust_addr_text_upper = customer_address.upper()
        elif type(customer_address) == dict:
            if validate_pinpoint_customer_address and ((not customer_address.__contains__("addr_text")) or (customer_address["addr_text"] == "")):
                raise ValidationException("Customer Address is empty.")
            cust_addr_text_upper = customer_address["addr_text"].upper()
        else:
            raise ValidationException("Invalid Customer Address")

        if validate_pinpoint_customer_address:
            cust_comp = to_thai_address_object(cust_addr_text_upper)
            is_cust_pinpoint = (cust_comp["admin_lv2"] is not None) and (cust_comp["house_no"] is not None)

            if not is_cust_pinpoint:
                raise ValidationException("Customer Address must contain district and house number information.")

            pinpoint_sim = np.zeros(len(vendor_addresses))
            for i, vendor_addr in enumerate(vendor_addresses):
                if type(vendor_addr) == str:
                    vendor_addr_text_upper = "" if vendor_addr is None else vendor_addr.upper()
                elif type(vendor_addr) == dict:
                    vendor_addr_text_upper = "" if vendor_addr["addr_text"] is None else vendor_addr["addr_text"].upper()
                else:
                    raise ValidationException("Invalid Vendor Address")
                if cust_addr_text_upper == vendor_addr_text_upper:
                    pinpoint_sim[i] = 1
            if np.any(pinpoint_sim) == 1:
                for ind in np.argwhere(pinpoint_sim == 1).flatten():
                    result[ind] = 1
                return result
        else:
            pinpoint_sim = np.zeros(len(vendor_addresses))
            for i, vendor_addr in enumerate(vendor_addresses):
                if type(vendor_addr) == str:
                    vendor_addr_text_upper = "" if vendor_addr is None else vendor_addr.upper()
                elif type(vendor_addr) == dict:
                    vendor_addr_text_upper = "" if vendor_addr["addr_text"] is None else vendor_addr["addr_text"].upper()
                else:
                    raise ValidationException("Invalid Vendor Address")
                if cust_addr_text_upper == vendor_addr_text_upper:
                    pinpoint_sim[i] = 1
            if np.any(pinpoint_sim) == 1:
                for ind in np.argwhere(pinpoint_sim == 1).flatten():
                    result[ind] = 1
                return result

            cust_comp = to_thai_address_object(cust_addr_text_upper)
            is_cust_pinpoint = (cust_comp["admin_lv2"] is not None) and (cust_comp["house_no"] is not None)

        admin_area_matched = np.zeros(len(vendor_addresses), dtype=bool)
        for i, vendor_addr in enumerate(vendor_addresses):
            if type(vendor_addr) == str:
                vendor_addr_text_upper = "" if vendor_addr is None else vendor_addr.upper()
            elif type(vendor_addr) == dict:
                vendor_addr_text_upper = "" if vendor_addr["addr_text"] is None else vendor_addr["addr_text"].upper()
            else:
                raise ValidationException("Invalid Vendor Address")
            vendor_comp = to_thai_address_object(vendor_addr_text_upper)
            is_vendor_pinpoint = (vendor_comp["admin_lv2"] is not None) and (vendor_comp["house_no"] is not None)
            if is_cust_pinpoint and is_vendor_pinpoint:
                if (vendor_comp["admin_lv2"] == cust_comp["admin_lv2"]) and (vendor_comp["house_no"] == cust_comp["house_no"]):
                    if (cust_comp["street"] is not None) and (cust_comp["street"] == vendor_comp["street"]):
                        pinpoint_sim[i] = 0.99
                    else:
                        pinpoint_sim[i] = textdistance.jaro_winkler(cust_addr_text_upper, vendor_addr_text_upper)
                else:
                    pinpoint_sim[i] = 0
            elif (cust_comp["admin_lv3"] is not None) and (vendor_comp["admin_lv3"] == cust_comp["admin_lv3"]):
                admin_area_matched[i] = True
            elif (cust_comp["admin_lv2"] is not None) and (vendor_comp["admin_lv2"] == cust_comp["admin_lv2"]):
                admin_area_matched[i] = True
            elif (cust_comp["admin_lv1"] is not None) and (vendor_comp["admin_lv1"] == cust_comp["admin_lv1"]):
                admin_area_matched[i] = True

        if np.any(pinpoint_sim > text_dist_thresh):
            for ind in np.argwhere(pinpoint_sim > text_dist_thresh).flatten():
                result[ind] = pinpoint_sim[ind]
        else:
            for ind in np.argwhere(admin_area_matched).flatten():
                result[ind] = 0.95
    elif validate_pinpoint_customer_address:
        raise ValidationException("Customer Address is empty.")

    return result


def test():
    test_addresses = pd.DataFrame(
        [
            ("65 หมู่11 ซอย วิลาลัย ตำบลบางโฉลง อำเภอบางพลี สมุทรปราการ 10540", "Bang Chalong", "Bang Phli", "Samut Prakan"),
            (
            "355 หมู่ 4 นิคมอุตสาหกรรมบางปูถ.สุขุมวิท, ต.แพรกษา อ.เมือง จ.สมุทรปราการ, 10280 Tambon Phraeksa, Amphoe Mueang Samut Prakan, Chang Wat Samut Prakan 10280, Thailand",
            "Phraeksa", "Mueang Samut Prakan", "Samut Prakan"),
            ("25 20 ทางคู่ขนาน ถนน บางนาตราด - สุวรรณภูมิ ตำบลบางโฉลง อำเภอบางพลี สมุทรปราการ 10540", "Bang Chalong", "Bang Phli",
             "Samut Prakan"),
            (
            "55/2 หมู่ 2ถนนพระราม 2 ตำบลบางกระเจ้า, อำเภอเมือง สมุทรสาคร, 74000 Tambon Tha Chin, Amphoe Mueang Samut Sakhon, Chang Wat Samut Sakhon 74000, Thailand",
            "Bang Krachao", "Mueang Samut Sakhon", "Samut Sakhon"),
            ("ซอย กิ่งแก้ว 44/1 ตำบลราชาเทวะ อำเภอบางพลี สมุทรปราการ 10540", "Racha Thewa", "Bang Phli", "Samut Prakan"),
            ("หนองปรือ อำเภอบางพลี สมุทรปราการ 10540", "Nong Prue", "Bang Phli", "Samut Prakan"),
            ("ตำบล สำโรงกลาง อำเภอพระประแดง สมุทรปราการ 10130", "Samrong Klang", "Phra Pradaeng", "Samut Prakan"),
            ("33/4 ซอย ไอซีดี แขวง คลองสามประเวศ เขตลาดกระบัง กรุงเทพมหานคร 10520", "Khlong Sam Prawet", "Lat Krabang", "Bangkok"),
            ("ตำบลบางโฉลง อำเภอบางพลี สมุทรปราการ 10540", "Bang Chalong", "Bang Phli", "Samut Prakan"),
            ("ตำบล บางหญ้าแพรก อำเภอพระประแดง สมุทรปราการ 10130", "Bang Ya Phraek", "Phra Pradaeng", "Samut Prakan"),
            ("ตำบลทุ่งสุขลา อำเภอศรีราชา ชลบุรี 20230", "Thung Sukhla", "Si Racha", "Chon Buri"),
            ("42/59-42/60 ตำบลราชาเทวะ อำเภอบางพลี สมุทรปราการ 10540", "Racha Thewa", "Bang Phli", "Samut Prakan"),
            ("198/29 ม.12 ม.มัณฑนา(บางนา Bang Phli Yai, Amphoe Bang Phli, Chang Wat Samut Prakan 10540, Thailand", "Bang Phli Yai",
             "Bang Phli", "Samut Prakan"),
            ("7/485 ม .6 ต มา บ ยาง พร, Pluak Daeng District, Rayong", None, "Pluak Daeng", "Rayong"),
            ("5/1-3 ม.6, ถ.มิตรภาพ, ต.ท่าพระ อ.เมืองขอนแก่น Tha Phra, เมือง Khon Kaen 40260", "Tha Phra", "Mueang Khon Kaen", "Khon Kaen"),
            (
            "120 mu 2 Soi Wat Kae, Suksawad Rd.,, Pak Khlong Bang Plakod, อำเภอพระสมุทรเจดีย์ สมุทรปราการ 10290", "Pak Khlong Bang Pla Kot",
            "Phra Samut Chedi", "Samut Prakan"),
            ("88/1 Moo 4 Suksawat Road, Prapradang, สมุทรปราการ 10130", None, "Phra Pradaeng", "Samut Prakan"),
            ("196 20230, ชลบุรี Nong Kham, Si Racha District, Chonburi 20110", "Nong Kham", "Si Racha", "Chon Buri"),
            ("120 Moo 2 C.R.C Warehouse WatKhae Alley, Suksawat Road, Phra Samut Chedi District, Samut Prakan 10290", None,
             "Phra Samut Chedi", "Samut Prakan"),
            ("2 King Kaeo Rd, Tambon Rachathewa, Amphoe Bang Phli, Chang Wat Samut Prakan 10540, Thailand", "Racha Thewa", "Bang Phli",
             "Samut Prakan"),
            ("Huai Yank, Klaeng District, Rayong 21110", "Huai Yang", "Klaeng", "Rayong"),
            ("Huai Yang Kh, Klaeng District, Rayong 21110", "Huai Yang", "Klaeng", "Rayong"),
            ("Huai Yang, Klaeng District, Rayong 21110", "Huai Yang", "Klaeng", "Rayong"),
            ("DSG 2 s.8, Bua Loi, Nong Khae District, Saraburi", "Bua Loi", "Nong Khae", "Saraburi"),
            ("Aranyaprathet, Aranyaprathet District, Sa Kaeo 27120", "Aranyaprathet", "Aranyaprathet", "Sa Kaeo"),
            ("10/13-16 นน Arun Amarin Rd, Khwaeng Arun Amarin, Khet Bangkok Noi, Krung Thep Maha Nakhon 10700, Thailand", "Arun Ammarin",
             "Bangkok Noi", "Bangkok"),
            ("11/7 Bangna-Trad Road, Km.18 Tambon Bang Chalong, Amphoe Bang Phli, Chang Wat Samut Prakan 10540, Thailand", "Bang Chalong",
             "Bang Phli", "Samut Prakan"),
            ("11/7 Bangna-Trad Road, Km.18 Bang Chalong, Bang Phli, Samut Prakan 10540, Thailand", "Bang Chalong", "Bang Phli",
             "Samut Prakan"),
            ("11/7 Bangna-Trad Road, Km.18 Tambon Bang Chalong, Samut Prakan 10540, Thailand", "Bang Chalong", "Bang Phli", "Samut Prakan"),
            ("11/7 Bangna-Trad Road, Amphoe Bang Phli, Samut Prakan 10540, Thailand", None, "Bang Phli", "Samut Prakan"),
            ("V4J8+QV Yotaka, Bang Nam Priao District, Chachoengsao, Thailand", "Yothaka", "Bang Nam Priao", "Chachoengsao"),
            ("171 Chantharu Beksa Road  Khlong Thanon Subdistrict, Sai Mai District  Bangkok, Thailand 10220", "Khlong Thanon", "Sai Mai",
             "Bangkok"),
            ("15 , Rama 2 Raod, Bangnumjued, Mueang Samut Sakhon District, Samut Sakhon", None, "Mueang Samut Sakhon", "Samut Sakhon"),
            ("7WWW+QHG, Samet, Chon Buri District, Chon Buri 20000, Thailand", "Samet", "Mueang Chon Buri", "Chon Buri"),
            ("Aranyaprated", "Aranyaprathet", "Aranyaprathet", "Sa Kaeo"),
            ("1/19 I.C.D Road  Klong 3 Pravet, Ladkrabang, Bangkok 10520, Thailand", "Lat Krabang", "Lat Krabang", "Bangkok"),
            ("No. 57 Moo 4 Tarsatorn District, Punpin Suratthani Province 84130", None, None, "Surat Thani"),
            ("YCH (THAILAND) Co., Ltd. 128 Ladkrabang Industrial Estate Soi Chalongkrung 31, Lamplatiew Ladkrabang Bangkok 10520 Thailand",
             None, None, None),
            ("C2GH+5R Don Hua Lo, Chon Buri District, Chon Buri, Thailand,", "Don Hua Lo", "Mueang Chon Buri", "Chon Buri"),
            ("48 Khum Klao Rd, Khwaeng Lam Prathew, Khet Lat Krabang, Krung Thep Maha Nakhon 10520, Thailand,", "Lam Pla Thio",
             "Lat Krabang", "Bangkok"),
            (
            "8/8 Moo 8, Poochaosamingprai Road., Bangyapreak, Phapradeang, Samutprakarn,10130,Thailand,", "Bang Ya Phraek", "Phra Pradaeng",
            "Samut Prakan"),
            ("M4HX+249 มา บ ตา พุ ต, Map Ta Phut, Amphoe Nikhom Phatthana, Rayong 21150", None, "Nikhom Phatthana", "Rayong")
        ], columns=["addr", "actual_lv3", "actual_lv2", "actual_lv1"]
    )

    for r, row in test_addresses.iterrows():
        addr = row["addr"]
        act_lv3 = None if pd.isna(row["actual_lv3"]) else row["actual_lv3"].upper()
        act_lv2 = None if pd.isna(row["actual_lv2"]) else row["actual_lv2"].upper()
        act_lv1 = None if pd.isna(row["actual_lv1"]) else row["actual_lv1"].upper()
        print(addr)
        comps = to_thai_address_object(addr)
        lv3, lv2, lv1, sim = comps["admin_lv3"], comps["admin_lv2"], comps["admin_lv1"], comps["admin_sim"]
        if (act_lv3 == lv3) and (act_lv2 == lv2) and (act_lv1 == lv1):
            print("OK at {}".format(sim))
        else:
            print("{} != {} or {} != {} or {} != {}".format(act_lv3, lv3, act_lv2, lv2, act_lv1, lv1))
        print(comps, "\n")

    ind = match_thai_vendor_addresses("2 King Kaeo road, Rachathewa, Thailand,", test_addresses["addr"])
    print(ind)

    ind = match_thai_vendor_addresses("2 King Kaeo Raod, Rachathewa, Bang Phli, Samut Prakan 10540", test_addresses["addr"])
    print(ind)

