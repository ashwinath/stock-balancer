import argparse
import yfinance as yf
import yaml

from tabulate import tabulate
from google.protobuf import json_format
from generated.proto.config_pb2 import Config
from termcolor import colored

exchange_rate_cache = {}

def download_stock_data(config):
    stocks_info = []
    nav = 0
    for stock in config.stock_info:
        name = stock.name
        stock_ticker = yf.Ticker(name)
        ask = stock_ticker.info["ask"]
        market_value = ask * stock.count
        currency = stock_ticker.info["currency"]
        if currency != "USD":
            if currency in exchange_rate_cache:
                exchange_rate = exchange_rate_cache[currency]
            exchange_rate_ticker = yf.Ticker(f"{currency}USD=x")
            exchange_rate = exchange_rate_ticker.info["ask"]
            exchange_rate_cache[currency] = exchange_rate

            market_value *= exchange_rate
            ask *= exchange_rate

        stocks_info.append({
            "ask": ask,
            "market_value": market_value,
            "name": stock.name,
            "count": stock.count,
            "desired_weight": stock.desired_weight,
        })
        nav += market_value

    return stocks_info, nav


def balance(stocks_info, nav, dca_fund):
    new_nav = nav + dca_fund
    for stock in stocks_info:
        stock["desired_amount"] = stock["desired_weight"] / 100 * new_nav
        stock["diff_value"] = stock["desired_amount"] - stock["market_value"]
        stock["desired_quantity"] = stock["desired_amount"] / stock["ask"]
        stock["diff_quantity"] = stock["diff_value"] / stock["ask"]


def print_table(stocks_info):
    headers = [
        "Name",
        "Weight",
        "Current Value",
        "Desired Value",
        "Diff Value",
        "Current Quantity",
        "Desired Quantity",
        "Diff Quantity",
    ]
    headers = [ colored(header, 'red') for header in headers ]
    table = []
    for stock in stocks_info:
        row = [
            stock["name"],
            stock["desired_weight"],
            stock["market_value"],
            stock["desired_amount"],
            stock["diff_value"],
            stock["count"],
            stock["desired_quantity"],
            stock["diff_quantity"],
        ]
        new_row = []
        for index, item in enumerate(row):
            new_item = item
            if index == 4 or index == 7:
                if new_item >= 0:
                    new_item = format_decimal_place(new_item)
                    new_item = colored(new_item, "green")
                else:
                    new_item = format_decimal_place(new_item)
                    new_item = colored(new_item, "red")
            new_row.append(new_item)

        table.append(new_row)
    print(tabulate(table, headers=headers))

def format_decimal_place(number):
    if isinstance(number, float):
        number = f"{number:.2f}"
    return number


def parse_args():
    parser = argparse.ArgumentParser(description="Balance your portfolio.")
    parser.add_argument(
        '--config',
        dest='config',
        type=str,
        required=True,
        help='Path to the config YAML file specification',
    )
    args = parser.parse_args()
    with open(args.config, "r") as file:
        return json_format.ParseDict(yaml.safe_load(file), Config())


def main():
    config = parse_args()
    stocks_info, nav = download_stock_data(config)
    balance(stocks_info, nav, config.amount_to_dca)
    print(
        colored(
            f"NAV: USD {nav:.2f}, SGD {nav/exchange_rate_cache['SGD']:.2f}",
            "green",
        )
    )
    print_table(stocks_info)


if __name__ == "__main__":
    main()
