import re
import pandas as pd
from collections import defaultdict
from .data import getData, getFiles

bjd_defs = {}
bjd_def_dates = sorted(
    [
        re.compile("\d{8}").search(f).group()
        for f in getFiles()
        if f.startswith("bjd") and re.compile("\d{8}").search(f)
    ]
)

latest_def_date = bjd_def_dates[-1]


def getBjdDef(def_date=latest_def_date):
    if def_date in bjd_defs:
        # print("using cached bjd data")
        return bjd_defs[def_date]

    # print("reading bjd data file")
    bjd = getData(f"bjd_{def_date}.pkl")
    bjd_defs[def_date] = bjd
    return bjd


region_names_store = {}


def getRegionNamesData(def_date=latest_def_date):
    if def_date in region_names_store:
        return region_names_store[def_date]

    bjd = getBjdDef(def_date)

    region_names = defaultdict(list)
    for i, row in bjd.iterrows():
        region_name = []
        for region in ["sido_nm", "sgg_nm", "emd_nm", "dl_nm"]:
            if not pd.isna(row[region]):
                region_name.append(row[region])
        region_name = " ".join(region_name)
        region_names[region_name].append(
            {"region_cd": str(row["bjd_cd"]), "erased": not pd.isna(row["erased_dt"])}
        )

    region_names_store[def_date] = region_names

    return region_names


bjd_dict_store = {}


def getBjdDict(def_date=latest_def_date):
    if def_date in bjd_dict_store:
        return bjd_dict_store[def_date]

    bjd = getBjdDef(def_date)

    bjd_dict = {}
    for idx, row in bjd.iterrows():
        bjd_cd = str(row["bjd_cd"])
        bjd_datum = {}
        bjd_full_nm = []
        for col in ["sido_nm", "sgg_nm", "emd_nm", "dl_nm"]:
            if not pd.isna(row[col]):
                bjd_datum[col] = row[col]
                bjd_full_nm.append(row[col])
            else:
                bjd_datum[col] = None
        bjd_datum["bjd_full_nm"] = " ".join(bjd_full_nm)
        bjd_datum["created_dt"] = row["created_dt"]
        bjd_datum["erased_dt"] = None if pd.isna(row["erased_dt"]) else row["erased_dt"]

        bjd_dict[bjd_cd] = bjd_datum

    bjd_dict_store[def_date] = bjd_dict

    return bjd_dict


sgg_split_list = {
    "고양덕양구",
    "고양일산동구",
    "고양일산서구",
    "성남분당구",
    "성남수정구",
    "성남중원구",
    "수원권선구",
    "수원영통구",
    "수원장안구",
    "수원팔달구",
    "안산단원구",
    "안산상록구",
    "안양동안구",
    "안양만안구",
    "용인기흥구",
    "용인수지구",
    "용인처인구",
    "전주덕진구",
    "전주완산구",
    "창원마산합포구",
    "창원마산회원구",
    "창원성산구",
    "창원의창구",
    "창원진해구",
    "천안동남구",
    "천안서북구",
    "청주상당구",
    "청주서원구",
    "청주청원구",
    "청주흥덕구",
    "포항남구",
    "포항북구",
}

last_nm_refine_map = {
    "북문로1가동": "북문로1가",
    "북문로2가동": "북문로2가",
    "북문로3가동": "북문로3가",
    "남문로1가동": "남문로1가",
    "남문로2가동": "남문로2가",
    "대율리": "대률리",
    "어용리": "어룡리",
    "청룡리": "청용리",
}


def getRegionCode(region_nm: str, def_date=latest_def_date):
    region_nm = " ".join(region_nm.split())

    region_names = getRegionNamesData(def_date)
    if region_nm in region_names:
        region_cd_list = region_names[region_nm]
        if len(region_cd_list) > 1:
            region_cd = list(
                filter(
                    lambda region_cd_data: not region_cd_data["erased"], region_cd_list
                )
            )[0]
        else:
            region_cd = region_cd_list[0]

        return {**region_cd, "def_date": def_date}

    else:
        sgg = region_nm.split()[1]
        if sgg in sgg_split_list:
            sgg_split_nm = f"{sgg[:2]}시 {sgg[2:]}"
            region_nm = region_nm.replace(sgg, sgg_split_nm)
            return getRegionCode(region_nm, def_date)

        last_nm = region_nm.split()[-1]
        if last_nm in last_nm_refine_map:
            region_nm = region_nm.replace(last_nm, last_nm_refine_map[last_nm])
            return getRegionCode(region_nm, def_date)

    return None


def getBjd(bjd_cd: str, def_date=latest_def_date):
    bjd_dict = getBjdDict(def_date)

    try:
        bjd_cd = str(bjd_cd)
        if len(bjd_cd) != 10:
            raise Exception("bjd_cd length should be 10:", bjd_cd)
        return {"error": False, **bjd_dict[bjd_cd], "def_date": def_date}
    except Exception as e:
        return {"error": True, "msg": str(e)}


def generatePnu(region_cd: str, jibun: str):
    msg = ""
    try:
        if pd.isna(jibun) or jibun[0] in ["B", "가", "지"] or "*" in jibun:
            mt_part = "1"
            jb_part = "00000000"
            bun, ji = 0, 0
            if "*" in jibun:
                msg = "매칭필요"
            else:
                msg = "블록지번"

        else:
            if jibun[0] in ["산", "산"]:
                mt_part = "2"
                jibun = jibun.replace("산", "")
            else:
                mt_part = "1"

            jb_split = jibun.split("-")
            if len(jb_split) == 2:
                bun, ji = [int(num) for num in jb_split]
                jb_part = "%04d%04d" % (bun, ji)
            elif len(jb_split) == 1:
                bun = int(jibun)
                jb_part = "%04d0000" % (bun)
                ji = 0
            else:
                jb_part = "00000000"
                bun, ji = 0, 0
                msg = "블록지번"
    except Exception as e:
        mt_part = "1"
        jb_part = "00000000"
        bun, ji = 0, 0
        msg = str(e)

    return {
        "pnu": f"{region_cd}{mt_part}{jb_part}",
        "region_cd": region_cd,
        "sgg_cd": region_cd[:5],
        "bjd_cd": region_cd[5:],
        "mt_part": mt_part,
        "jb_part": jb_part,
        "bun": bun,
        "ji": ji,
        "msg": msg,
    }
