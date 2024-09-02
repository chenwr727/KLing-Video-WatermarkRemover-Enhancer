import datetime


def update_status(message: str) -> None:
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now_str}: {message}")
