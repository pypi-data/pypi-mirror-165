import requests

def info(currency):
        response = requests.get("https://cbu.uz/common/json").json()
        response.append({
            "Ccy": "UZS",
            "Rate": 1
        })
        for cur in response:
            curr = cur["Ccy"]
            rate = cur["Rate"]
            if curr == currency:
                return rate

def convert(from_currency: str, to_currency: str, value: int):
    curr1_rate = info(from_currency)
    curr2_rate = info(to_currency)
    result = float(curr1_rate) / float(curr2_rate) * float(value)
    return {
        "from": from_currency,
        "to": to_currency,
        "rate": result,
    }