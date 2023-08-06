#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   core.py
@Time    :   2022/07/19 15:37:18
"""
import os

import pytest


def pytest_load_initial_conftests(early_config, args, parser):
    COIN_SYMBOL = {
        "USDT": "BTCUSDT",
        "USDC": "BTCPERP",
        "BTC": "BTCUSD",
        "ETH": "ETHUSD",
        "BIT": "BITUSD",
        "SOL": "SOLUSD",
        "DOT": "DOTUSD",
        "ADA": "ADAUSD",
        "LTC": "LTCUSD",
        "XRP": "XRPUSD",
        "EOS": "EOSUSD",
        "MANA": "MANAUSD"
    }

    instance_params = None
    symbol_params = None
    tail_num_params = None

    for index, value in enumerate(args):  # --store
        if value.find('--instance') != -1:
            instance_params = (index, value)
        if value.find('--symbol') != -1:
            symbol_params = (index, value)
        if value.find('--tailnum') != -1:
            tail_num_params = (index, value)
            tail_num = value.strip().split("=")[-1]
            os.environ["_PYTEST_TAILNUM"] = tail_num
        if value.find('--env') != -1:
            env = value.strip().split("=")[-1]
            os.environ["_PYTEST_ENV"] = env

    # overwrite
    if instance_params:
        _, value = instance_params
        if "trading" in value:
            *_, ins = value.split(".")
            coin, tail_num, *_ = ins.split("_")

            if len(tail_num) < 2:  # TODO
                if symbol_params:
                    args[symbol_params[0]] = f"--symbol={COIN_SYMBOL[coin]}"
                else:
                    args.append(f"--symbol={COIN_SYMBOL[coin]}")

                if tail_num_params:
                    args[tail_num_params[0]] = f"--tailnum={tail_num}"
                else:
                    args.append(f"--tailnum={tail_num}")

                os.environ["_PYTEST_TAILNUM"] = tail_num
            print(f"pytest_load_initial_conftests >> {args}")


@pytest.fixture(scope="session", autouse=True)
def clear_env():
    yield
    if "_PYTEST_TAILNUM" in os.environ:
        del os.environ["_PYTEST_TAILNUM"]
