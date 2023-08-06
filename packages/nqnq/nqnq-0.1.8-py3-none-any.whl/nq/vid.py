import hashlib
from typing import Union
import re
from datetime import date


def formatFloatString(float_str: str) -> str:
    if float_str:
        dot_split = float_str.split(".")
        if len(dot_split) == 1:
            return float_str

        elif len(dot_split) == 2:
            part_int, part_float = dot_split

            float_numbers = list(part_float)

            for i in range(len(part_float) - 1, -1, -1):
                number = float_numbers[i]
                if number != "0":
                    break
                else:
                    float_numbers.pop()

            no_trailing_zero_float_part = "".join(float_numbers)

            if no_trailing_zero_float_part:
                return ".".join([part_int, no_trailing_zero_float_part])
            else:
                return part_int

        else:
            return float_str

    else:
        return ""


removeComma = lambda s: s.replace(",", "")

formatFloat = lambda float_num: formatFloatString(removeComma(str(float_num)))

isPnuValid = lambda pnu: re.compile("^\d{19}$").match(pnu)


def isContractDateValid(contract_ymd):
    if type(contract_ymd) != str:
        contract_ymd = str(contract_ymd)
    if len(contract_ymd) == 8 and re.compile("^\d{8}$").match(contract_ymd):
        try:
            d = date.fromisoformat(
                f"{contract_ymd[:4]}-{contract_ymd[4:6]}-{contract_ymd[6:]}"
            )
            return True
        except:
            return False
    return False


def isNumberValid(number):
    try:
        ff = formatFloat(number)
        if (
            not ff
            or len(ff.split(".")) > 2
            or not re.compile("^\d*$").match(ff.replace(".", ""))
        ):
            return False
        else:
            return True
    except:
        return False


def validate(validator, value, value_nm):
    if value and not validator(value):
        raise Exception(f"invalid {value_nm}: {value}")


def genHashRaw(data_str: str) -> str:
    return hashlib.sha256(data_str.encode("utf-8")).hexdigest()


def generateRegistrationVid(
    pnu: str,
    contract_ymd: str,
    price: Union[float, int, None] = None,
    unit_ar: Union[float, int, str, None] = None,
    lot_ar: Union[float, int, str, None] = None,
    seller: Union[str, None] = None,
    buyer: Union[str, None] = None,
) -> str:
    try:
        validate(isPnuValid, pnu, "pnu")
        validate(isContractDateValid, contract_ymd, "contract_ymd")
        validate(isNumberValid, price, "price")
        if not unit_ar == "-":
            validate(isNumberValid, unit_ar, "unit_ar")
        if not lot_ar == "-":
            validate(isNumberValid, lot_ar, "lot_ar")
        validate(lambda seller: type(seller) == str, seller, "seller")
        validate(lambda buyer: type(buyer) == str, buyer, "buyer")

        data_str = "_".join(
            [
                pnu,
                contract_ymd,
                formatFloat(price) if price else "",
                formatFloat(unit_ar) if price else "",
                formatFloat(lot_ar) if price else "",
                seller or "",
                buyer or "",
            ]
        )

        h = genHashRaw(data_str)

        return [f"R_{pnu[:10]}_{h[:10]}_0000", h, data_str]
    except Exception as e:
        print(pnu, e)
        return [
            f"R_{pnu[:10] if isPnuValid(pnu) else 'pnu10dhead'}_{'hashstring'}_0000",
            None,
            None,
        ]
