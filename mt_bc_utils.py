import logging
from yaml import load, FullLoader

from bcutils.bc_utils import (
    create_bc_session,
    get_barchart_downloads,
    update_barchart_downloads,
)
from bcutils.config import CONTRACT_MAP
from sample.pst import load_config

logging.basicConfig(level=logging.INFO)


def download_with_config():
    # run a download session, with config picked up from the passed file
    # See /sample/private_config_sample.yaml
    config = load_config("./private_config.yaml")
    get_barchart_downloads(
        create_bc_session(config),
        instr_list=config["barchart_download_list"],
        start_year=config["barchart_start_year"],
        end_year=config["barchart_end_year"],
        save_dir=config["barchart_path"],
        do_daily=config["barchart_do_daily"],
        dry_run=config["barchart_dry_run"],
    )

def find_instruments_with_days_count():
    return_instrs = []
    for instr in CONTRACT_MAP.keys():
        instr_config = CONTRACT_MAP[instr]
        if "days_count" in instr_config:
            return_instrs += [instr]

    return(return_instrs)        



if __name__ == "__main__":
    config = load_config("./private_config.yaml")
    #bc_session = create_bc_session(config)
    special_instrs = find_instruments_with_days_count()
    print(special_instrs)
    """ get_barchart_downloads(
        bc_session,
        instr_list=special_instrs,
        start_year=2024,
        end_year=2029,
        save_dir=config["barchart_path"],
        do_daily=config["barchart_do_daily"],
        dry_run=True,
    ) """
    """ get_barchart_downloads(
        bc_session,
        instr_list=None,
        start_year=1975,
        end_year=2026,
        save_dir=config["barchart_path"],
        do_daily=config["barchart_do_daily"],
        dry_run=False,
    ) """