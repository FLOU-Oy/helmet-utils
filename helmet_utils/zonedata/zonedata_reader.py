import pandas as pd
import geopandas as gpd
from pathlib import Path
from typing import Tuple
from .zonedata import ZoneData

class ZoneDataReader:
    def __init__(self, zonedata_directory: str, zones_filepath: str|None=None, landcover_filepath: str|None=None):
        if not Path(zonedata_directory).exists():
            raise FileNotFoundError(f"Directory {zonedata_directory} does not exist.")
        if zones_filepath and not Path(zones_filepath).exists():
            raise FileNotFoundError(f"File {zones_filepath} does not exist.")
        elif not zones_filepath:
            default_zones = Path(__file__).resolve().parent.parent / 'data' / 'SIJ2023_aluejako.gpkg'
            self.zones = gpd.read_file(default_zones)
        else:
            self.zones = gpd.read_file(zones_filepath)

        if landcover_filepath and not Path(landcover_filepath).exists():
            raise FileNotFoundError(f"File {landcover_filepath} does not exist.")
        elif not landcover_filepath:
            self.landcover_file = Path(__file__).resolve().parent.parent / 'data' / 'landcover.tif'
        else:
            self.landcover_file = landcover_filepath
        
        self.bks, self.bks_file = self._extract_df_from_zonedata(zonedata_directory, '*.bks')
        self.car, self.car_file = self._extract_df_from_zonedata(zonedata_directory, '*.car')
        self.cco, self.cco_file = self._extract_df_from_zonedata(zonedata_directory, '*.cco')
        self.edu, self.edu_file = self._extract_df_from_zonedata(zonedata_directory, '*.edu')
        self.ext, self.ext_file = self._extract_df_from_zonedata(zonedata_directory, '*.ext')
        self.lnd, self.lnd_file = self._extract_df_from_zonedata(zonedata_directory, '*.lnd')
        self.pop, self.pop_file = self._extract_df_from_zonedata(zonedata_directory, '*.pop')
        self.pnr, self.pnr_file = self._extract_df_from_zonedata(zonedata_directory, '*.pnr')
        self.prk, self.prk_file = self._extract_df_from_zonedata(zonedata_directory, '*.prk')
        self.tco, self.tco_file = self._extract_df_from_zonedata(zonedata_directory, '*.tco')
        self.trk, self.trk_file = self._extract_df_from_zonedata(zonedata_directory, '*.trk')
        self.wrk, self.wrk_file = self._extract_df_from_zonedata(zonedata_directory, '*.wrk')


    def zonedata(self) -> ZoneData:
        file_dict = {
            'bks': Path(self.bks_file).name if self.bks_file else None,
            'car': Path(self.car_file).name if self.car_file else None,
            'cco': Path(self.cco_file).name if self.cco_file else None,
            'edu': Path(self.edu_file).name if self.edu_file else None,
            'ext': Path(self.ext_file).name if self.ext_file else None,
            'lnd': Path(self.lnd_file).name if self.lnd_file else None,
            'pop': Path(self.pop_file).name if self.pop_file else None,
            'pnr': Path(self.pnr_file).name if self.pnr_file else None,
            'prk': Path(self.prk_file).name if self.prk_file else None,
            'tco': Path(self.tco_file).name if self.tco_file else None,
            'trk': Path(self.trk_file).name if self.trk_file else None,
            'wrk': Path(self.wrk_file).name if self.wrk_file else None,
        }

        return ZoneData(self.lnd, self.pop, self.wrk, self.edu, self.bks, self.prk, self.car, self.cco, self.ext, self.pnr, self.tco, self.trk, self.zones, self.landcover_file, file_dict)
    
    def _extract_df_from_zonedata(self, directory: str, pattern: str) -> Tuple[pd.DataFrame|dict|None, str|None]:
        file = next(Path(directory).glob(pattern), None)
        if file:
            if pattern == '*.cco':
                 return pd.read_csv(file, sep="\s+", comment="#"), str(file)
            if pattern == '*.trk':
                trk_data = {}
                with open(file, 'r') as f:
                    lines = f.readlines()
                    current_key = None
                    for line in lines:
                        line = line.strip()
                        if line.startswith('#'):
                            if 'Zones where trailer trucks are prohibited' in line:
                                current_key = 'prohibited_zones'
                                trk_data[current_key] = []
                            elif 'Zones were garbage is taken' in line:
                                current_key = 'garbage_zones'
                                trk_data[current_key] = []
                        elif current_key:
                            trk_data[current_key].extend(map(int, line.split()))

                return trk_data, str(file)
            if pattern == '*.tco':
                return pd.read_csv(file, sep="\s+", comment="#", index_col=0, keep_default_na=False, na_values=[]), str(file)
            else:
                return pd.read_csv(file, sep="\s+", comment="#", index_col=0), str(file)
        elif pattern == "*.car" or pattern == "*.bks":
            print(f"No {pattern} file found, skipping {pattern} data")
            return None, None
        else:
            raise FileNotFoundError(f"No file matching pattern {pattern} found in {directory}")    

def get_helmet_zonedata(zonedata_directory: str, zones_filepath: str|None=None, landcover_filepath: str|None=None) -> ZoneData:
    zondedata_reader = ZoneDataReader(zonedata_directory, zones_filepath=zones_filepath, landcover_filepath=landcover_filepath)
    return zondedata_reader.zonedata()