import logging
from yaml import load, FullLoader
from time import sleep
from random import randint

from bcutils.bc_utils import (
    create_bc_session,
    get_barchart_downloads,
    update_barchart_downloads,
)

from bcutils.config import CONTRACT_MAP, EXCHANGES, CONTRACT_MAP2

logging.basicConfig(level=logging.INFO)

def find_instruments_with_days_count():
    return_instrs = {}
    for instr in CONTRACT_MAP.keys():
        instr_config = CONTRACT_MAP[instr]
        if "days_count" in instr_config:
            #return_instrs += {instr: instr_config["days_count"]}
            return_instrs[instr]=instr_config["days_count"]

    return(return_instrs)        


def download_with_config(configfile):
    # run a download session, with config picked up from the passed file
    # See private_config_sample.yaml
    config = load_config(configfile)
    instruments = list(CONTRACT_MAP.keys()).sort()
    #instruments = ["SP500", "US30Y", "GOLD", "SOYBEAN","CRUDE_W","JPY"]

    get_barchart_downloads(
        create_bc_session(config),
        instr_list=instruments, #config["barchart_download_list"],
        start_year=config["barchart_start_year"],
        end_year=config["barchart_end_year"],
        save_dir=config["barchart_path"],
        do_daily=config["barchart_do_daily"],
        dry_run=config["barchart_dry_run"],
    )


def update_with_config():
    # run an update session, with config picked up from the passed file
    # See private_config_sample.yaml
    config = load_config("./private_config.yaml")
    instr_list = config["barchart_update_list"]
    save_dir = config["barchart_path"]
    dry_run = config["barchart_dry_run"]
    for code in instr_list:
        update_barchart_downloads(instr_code=code, save_dir=save_dir, dry_run=dry_run)


def load_config(config_path):
    config_stream = open(config_path, "r")
    return load(config_stream, Loader=FullLoader)


if __name__ == "__main__":
    
    download_with_config("./private_config.yaml")
    sleep(randint(0,20))
    
    #download_with_config("./private_config2.yaml") cancelled
    sleep(randint(0,20))

    #download_with_config("./private_config3.yaml") cancelled 
    sleep(randint(0,20))

    #download_with_config("./private_config4.yaml") # cancelled 
    sleep(randint(0,20))

    #download_with_config("./private_config5.yaml") # cancelled 
    sleep(randint(0,20))

    #download_with_config("./private_config6.yaml") # cancelled
    sleep(randint(0,20))

    #download_with_config("./private_config7.yaml") # cancelled 
    sleep(randint(0,20))

    #download_with_config("./private_config8.yaml") # cancelled 
    sleep(randint(0,20))

    #download_with_config("./private_config9.yaml") #cancelled 
    sleep(randint(0,20))

    #download_with_config("./private_config10.yaml") #cancelled 
    # update_with_config()