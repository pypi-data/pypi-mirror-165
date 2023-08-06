import os
import math
import json
import shutil

from . import merge_data_img_files
from pypers.core.interfaces import db, msgbus
from pypers.core.interfaces.storage.backup import Backup
from pypers.steps.base.step_generic import EmptyStep
from pypers.utils.utils import clean_folder, delete_files, rename_file


class Split(EmptyStep):
    """
    Merge extraction directories chronologically
    """
    spec = {
        "version": "2.0",
        "descr": [
            "Merges by order and returns the merged directory"
        ],
        "args":
        {
            "inputs": [
                {
                    "name": "data_files",
                    "descr": "input structured data"
                },
                {
                    "name": "img_files",
                    "descr": "input structured data"
                },
                {
                    "name": "extraction_dir",
                    "descr": "the extraction dir"
                },
                {
                    "name": "gbd_extraction_date",
                    "descr": "the extraction date"
                }
            ],
            "outputs": [
                {
                    "name": "consolidated_items",
                    "descr": "the extracted data organized by appnum"
                },
                {
                    "name": "padding",
                    "descr": "the padding value for subfolders"
                }

            ],
            "params": [
                {
                    "name": "nb_records_per_subdir",
                    "type": "int",
                    "descr": "number of records in stage subdir",
                    "value": 10000
                }
            ]
        }
    }

    # self.data_files [ { appnum : { "gbd": _, "ori": _, "qc" : [], "st13": _}, appnum ... } ]
    # self.img_files  [ { appnum : [{ "crc": _, "high": _, "icon" : _, "ori": _, "thum": _ }, ...], appnum ... } ]
    # self.extraction_dir [ ORIFILES_DIR/type/collection/office_extraction_date/archive_name ]
    # self.gbd_extraction_date [ yyyy-mm-dd, ... ]
    def process(self):
        self.collection_name = self.collection.replace('harmonize_', '')
        self.padding = []
        self.consolidated_items = []
        if not len(self.data_files):
            return

        # ---------------------
        # consolidate
        # ---------------------
        # consolidate info from different extractions
        consolidated = {}

        # total number of extracted records
        nb_records_total = 0

        for index, extraction_dir in enumerate(self.extraction_dir):
            # header info
            office_extraction_date, archive_name = extraction_dir.split(os.sep)[-2:]
            gbd_extraction_date = self.gbd_extraction_date[index]

            # header information corresponding to single archive extraction
            record_header = { 'office_extraction_date': office_extraction_date,
                              'archive_name': archive_name,
                              'extraction_dir': extraction_dir,
                              'gbd_extraction_date': gbd_extraction_date }

            # data files
            data_files = self.data_files[index]
            # image_files
            img_files = self.img_files[index]

            nb_records_total += len(data_files.keys())

            # merge data and images under appnum
            archive_files = merge_data_img_files(data_files, img_files)

            # add the header information related to the record
            for appnum, item in archive_files.items():
                item['header'] = record_header

            # consolidate : the newer replaces the older ;)
            consolidated.update(archive_files)

        nb_subdir_total = math.ceil(nb_records_total / self.nb_records_per_subdir)
        pd_subdir = max(len(str(nb_subdir_total)), 3)
        tmp = {}
        counter = 0
        for el in consolidated.keys():
            if counter == self.nb_records_per_subdir:
                self.consolidated_items.append(tmp)
                self.padding.append(pd_subdir)
                counter = 0
                tmp = {}
            counter += 1
            tmp[el] = consolidated[el]

        self.consolidated_items.append(tmp)
        self.padding.append(pd_subdir)



