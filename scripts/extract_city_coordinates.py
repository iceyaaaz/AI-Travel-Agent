import json
from datetime import datetime, timezone, timedelta


def main(weather_text: str) -> dict:
    data = json.loads(weather_text)

    # 按天气接口返回的城市时区计算当前当地日期
    offset = int(data.get("timezone", 28800))
    city_timezone = timezone(timedelta(seconds=offset))
    local_now = datetime.now(timezone.utc).astimezone(city_timezone)

    return {
        "lat": str(data["coord"]["lat"]),
        "lon": str(data["coord"]["lon"]),
        "current_local_date": local_now.strftime("%Y-%m-%d")
    }
