import os
from datetime import datetime

from sample.pst import load_config
from bcutils.config import CONTRACT_MAP
from bcutils.bc_utils import Resolution
from bcutils.bc_utils import get_barchart_downloads, create_bc_session
from data_to_download.missingcontracts import missingcontracts, new_instruments , EU_Sector_Indices, new_instruments2



# This script downloads specific contract data, similar to samples.download_specific_contracts but generates the contract list from PST contract_dt string of the format YYYYMM00
def contract_dt_to_futures_month_year_code(contract_dt):
    """
    Convert a contract date string (YYYYMM00) to a futures code (e.g., XH20).

    Args:
        contract_dt (str): Contract date string in the format YYYYMM00.
        contract_map (dict): Mapping of instrument names to their details.

    Returns:
        str: Corresponding futures code.
    """
    year = contract_dt[:4]
    month = contract_dt[4:6]
    month_code_map = {
        "01": "F",
        "02": "G",
        "03": "H",
        "04": "J",
        "05": "K",
        "06": "M",
        "07": "N",
        "08": "Q",
        "09": "U",
        "10": "V",
        "11": "X",
        "12": "Z",
    }

    if month not in month_code_map:
        raise ValueError(f"Invalid month in contract date: {month}")

    month_code = month_code_map[month]
    year_code = year[2:]  # Last two digits of the year

    futures_code = f"{month_code}{year_code}"
    return futures_code

def instrument_and_contract_dt_to_futures_code(instr, contract_dt, contract_map):
    """
    Convert an instrument name and contract date string to a full futures code (e.g., XH20).

    Args:
        instr (str): Instrument name (e.g., "FTSE100").
        contract_dt (str): Contract date string in the format YYYYMM00.
        contract_map (dict): Mapping of instrument names to their details.

    Returns:
        str: Corresponding full futures code.
    """
    
    if instr not in contract_map:
        print( ValueError(f"Instrument {instr} not found in contract map."))
        return None
    
    
    month_year_code = contract_dt_to_futures_month_year_code(contract_dt)
    code_prefix = contract_map[instr]["code"]
    futures_code = f"{code_prefix}{month_year_code}"
    return futures_code

def check_downloaded_files(instrument, contract_dt, resolution, download_dir=None):
    """
    Check whether the file has already been downloaded
    Args:
        instrument (str): Instrument name (e.g., "FTSE100").
        contract_dt (str): Contract date string in the format YYYYMM00.
        frequency (str): Frequency of the data ("Hour" or "Day").
        download_dir (str, optional): Directory where files are stored. If not specificed, then looks up in the config file 
    """
    if download_dir is None:
        config = load_config("./sample/private_config.yaml")
        download_dir = config["barchart_path"]

    

    #futures_code = instrument_and_contract_dt_to_futures_code(instrument, contract_dt, contract_map=CONTRACT_MAP)
    if resolution == Resolution.Hour:
        frequency = "Hour"
    elif resolution == Resolution.Day:
        frequency = "Day"
    

    file_name = f"{frequency}_{instrument}_{contract_dt}.csv"
    file_path = os.path.join(download_dir, file_name)

    return os.path.isfile(file_path)
    

def from_contract_dt_list_to_futures_codes(instr, contract_dt_list, contract_map=CONTRACT_MAP, check_existing_files=True, resolution=Resolution.Day, download_dir=None):

    futures_codes_list = []

    for contract_dt in contract_dt_list:
        if check_existing_files:
            if check_downloaded_files(instr, contract_dt, resolution, download_dir):
                #print(f"File for {instr} {contract_dt} already exists. Skipping download.")
                continue
        
        
        futures_code = instrument_and_contract_dt_to_futures_code(instr, contract_dt, contract_map)
        if futures_code: 
            futures_codes_list.append(futures_code)

    return futures_codes_list

def from_year_range_to_contract_dt_list(instrument, start_year, end_year, contract_map=CONTRACT_MAP):
    """
    Generate a list of contract date strings (YYYYMM00) for a given instrument and year range. 
    The actual months available depend on the instrument's trading cycle as defined in the contract_map.

    Args:
        instrument (str): PST instrument name (e.g., "FTSE100").
        start_year (int): Starting year (inclusive).
        end_year (int): Ending year (not inclusive, following bc-utils convention).

    Returns:
        list: List of contract date strings.
    """
    month_code_map = {
        "01": "F",
        "02": "G",
        "03": "H",
        "04": "J",
        "05": "K",
        "06": "M",
        "07": "N",
        "08": "Q",
        "09": "U",
        "10": "V",
        "11": "X",
        "12": "Z",
    }

    inverse_month_code_map = {v: k for k, v in month_code_map.items()}

    contract_dt_list = []
    if instrument not in contract_map:
        print(ValueError(f"Instrument {instrument} not found in contract map."))
        return []
    
    for year in range(start_year, end_year):
        for month in contract_map[instrument]["cycle"]:
            month_number = inverse_month_code_map.get(month)
            contract_dt = f"{year}{month_number}00"
            contract_dt_list.append(contract_dt)
    return contract_dt_list

def build_download_code_list(resolution=Resolution.Day):
    #1. List for all new instruments from missingcontracts.py : for simplicity: from 1985 to 2022 
    #2. List for all contracts from missingcontracts.py missingcontracts dictionary: based on data 
    #3. List for all the EU equity sector indices from missingcontracts.py: from 2000 to 2023, minus 20230900 and 20231200 
    download_list = []


    start_year = 1985
    end_year = 2023
    for instr in new_instruments:
        contract_dt_list = from_year_range_to_contract_dt_list(instr, start_year=start_year, end_year=end_year)
        if contract_dt_list:
            instr_download_list = from_contract_dt_list_to_futures_codes(instr, contract_dt_list=contract_dt_list, resolution= resolution)
            if instr_download_list: 
                download_list += instr_download_list
    

    for instr in missingcontracts.keys():
        if instr not in CONTRACT_MAP:
            print(f"Instrument {instr} not found in CONTRACT_MAP, skipping")
            continue
        contract_dt_list = missingcontracts[instr]
        futures_codes = from_contract_dt_list_to_futures_codes(instr, contract_dt_list, CONTRACT_MAP, check_existing_files=True, resolution=resolution, download_dir=download_dir)
        #print(f"Futures codes to download for {instr}: {futures_codes}")
        if futures_codes: 
            download_list += futures_codes

    download_list = [] # previous ones have already been downloaded, saving time 
    start_year = 2009
    end_year = 2024
    print(new_instruments2)
    for instr in new_instruments2:
        contract_dt_list = from_year_range_to_contract_dt_list(instr, start_year=start_year, end_year=end_year)
        if contract_dt_list:
            instr_download_list = from_contract_dt_list_to_futures_codes(instr, contract_dt_list=contract_dt_list, resolution= resolution)
            if instr_download_list: 
                download_list += instr_download_list
    

    start_year = 2000
    end_year = 2024
    for instr in EU_Sector_Indices:
        contract_dt_list = from_year_range_to_contract_dt_list(instr, start_year=start_year, end_year=end_year)
        if contract_dt_list:
            instr_download_list = from_contract_dt_list_to_futures_codes(instr, contract_dt_list=contract_dt_list, resolution=resolution)
            if instr_download_list: 
                download_list += instr_download_list

    print(len(download_list))
    return(download_list)




    







if __name__ == "__main__":
    
    config = load_config("./sample/private_config.yaml")
    download_dir = config["barchart_path"]
    resolution = Resolution.Day

    
    #print(from_year_range_to_contract_dt_list("NICKEL_LME", 2025, 2026, CONTRACT_MAP))
    #print(from_year_range_to_contract_dt_list("EU-INSURE", 2025, 2026, CONTRACT_MAP))
    day_codes_list = build_download_code_list(resolution=Resolution.Day)
    hourly_codes_list = build_download_code_list(resolution=Resolution.Hour)

    login_obj=dict(
        barchart_username="tang.eric.ht@gmail.com",
        barchart_password="cdefgh12",
    )
    print(login_obj)  
    get_barchart_downloads(
        create_bc_session(config_obj=login_obj),
        #instr_list=["HEATOIL-ICE", "JGB", "TECDAX"],
        #instr_list=["SOLANA", "SOLANA_micro", "XRP", "XRP_micro"],
        contract_list = day_codes_list,
        #start_year=2025,
        #end_year=2026,
        save_dir="/mnt/sda1/data/barchart2025",
        do_daily=True,
        dry_run=False,
    )