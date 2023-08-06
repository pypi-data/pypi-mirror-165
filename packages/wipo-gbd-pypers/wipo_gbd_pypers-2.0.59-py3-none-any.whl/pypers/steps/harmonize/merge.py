import os
import math
import json
import shutil

from . import merge_data_img_files
from pypers.core.interfaces import db, msgbus
from pypers.core.interfaces.storage.backup import Backup
from pypers.steps.base.step_generic import EmptyStep
from pypers.utils.utils import clean_folder, delete_files, rename_file


class Merge(EmptyStep):
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
                    "name": "consolidated_items",
                    "descr": "the extracted data organized by appnum",
                    "iterable": True
                },
                {
                    "name": "padding",
                    "descr": "the padding value for subfolders",
                    "iterable": True
                }
            ],
            "params": [
                {
                    "name": "chain",
                    "type": "int",
                    "descr": "an int flag (0|1) whether to "
                             "chain to the next pipeline",
                    "value": 0
                }
            ]
        }
    }

    def _create_new_entry(self, run_id, appnum, *args, **kwargs):
        return {
            'st13': appnum,
            'gbd_collection': None,
            'latest_run_id': run_id,
        }

    def _update_latest(self, old, run_id, appnum, collection, copy_data, qc):
        if not old:
            old = self._create_new_entry(run_id, appnum)

        old['gbd_collection'] = collection
        old['latest_run_id'] = run_id
        old['gbd_extraction_date']  = copy_data.get('gbd_extraction_date', '')
        old['office_extraction_date'] = copy_data.get('office_extraction_date', '')
        old['gbd_type'] = copy_data.get('gbd_type', '')
        old['archive'] = copy_data.get('archive', '')

        if qc:
            old['qc'] = qc

        old['logo'] = [os.path.splitext(x)[0] for x in copy_data.get('logo', [])]

        return old

    # self.data_files [ { appnum : { "gbd": _, "ori": _, "qc" : [], "st13": _}, appnum ... } ]
    # self.img_files  [ { appnum : [{ "crc": _, "high": _, "icon" : _, "ori": _, "thum": _ }, ...], appnum ... } ]
    # self.extraction_dir [ ORIFILES_DIR/type/collection/office_extraction_date/archive_name ]
    # self.gbd_extraction_date [ yyyy-mm-dd, ... ]
    def process(self):
        self.collection_name = self.collection.replace('harmonize_', '')
        if not len(self.consolidated_items):
            return
        
        self.backup = Backup(self.pipeline_type, self.collection_name)

        # ---------------------------
        # backup & stage & get latest
        # --------------------------
        stage_root = os.path.join(os.environ.get('GBDFILES_DIR'),
                                  self.run_id,
                                  self.pipeline_type,
                                  self.collection_name)
        # left pad subdirs
        pd_subdir = self.padding

        # keep count to generate sub-directories
        records_count = 0
        for appnum, item in self.consolidated_items.items():
            extraction_dir = item['header']['extraction_dir']
            st13 = item['data']['st13']

            # create subdirs to contain max nb_records_per_subdir doc directories
            stage_subdir = str(self.sub_step).zfill(pd_subdir)
            stage_path = os.path.join(stage_root, stage_subdir, st13)
            os.makedirs(stage_path, exist_ok=True)
            records_count += 1

            # -- image files
            # backup img files
            crcs = []
            for img in item.get('img', []):
                img_hi = os.path.join(extraction_dir, img['high'])
                if not os.path.exists(img_hi):
                    continue
                img_th = os.path.join(extraction_dir, img['thum'])
                img_ic = os.path.join(extraction_dir, img['icon'])

                self.backup.store_img_gbd(img_hi, st13, hard=False)
                self.backup.store_img_gbd(img_th, st13, hard=True)
                self.backup.store_img_gbd(img_ic, st13, hard=True)

                crcs.append(img['crc'])
                # stage hi image
                dest = os.path.join(stage_path, os.path.basename(img_hi))
                if os.path.exists(dest):
                    os.remove(dest)
                shutil.move(img_hi, stage_path)
            # -- data file
            # backup gbd file
            gbd_file = os.path.join(extraction_dir, item['data']['gbd'])
            gbd_file = rename_file(gbd_file, self.run_id)

            self.backup.store_doc_gbd(gbd_file, st13, hard=False)

            # stage gbd file
            dest = os.path.join(stage_path, os.path.basename(gbd_file))
            if os.path.exists(dest):
                os.remove(dest)
            if not os.path.exists(gbd_file):
                continue
            shutil.move(gbd_file, stage_path)


            # -- latest dynamodb doc
            # try first to load from gbd_docs_live table
            dydb_doc = db.get_pre_prod_db().get_document(st13)
            # if not, create a new one
            if not dydb_doc:
                dydb_doc = {'st13': st13,
                            'gbd_collection': self.collection_name,
                            'gbd_type': self.pipeline_type }

            # set the header information
            dydb_header = {'latest_run_id': self.run_id,
                           'archive':  item['header']['archive_name'],
                           'gbd_extraction_date': item['header']['gbd_extraction_date'],
                           'office_extraction_date': item['header']['office_extraction_date'] }

            dydb_doc.update(dydb_header)

            # set the logo names
            if len(crcs):
                dydb_doc.update({'logo': crcs})

            # stage latest.json
            latest_file = os.path.join(stage_path, 'latest.json')
            with open(latest_file, 'w') as f:
                json.dump(dydb_doc, f, indent=2)

        # -----------------------------------
        # clean ori stage from empty folders
        # -----------------------------------
        ori_path = os.path.join(os.environ.get('ORIFILES_DIR'),
                                self.run_id,
                                self.pipeline_type,
                                self.collection_name)

        clean_folder(ori_path)

    def postprocess(self):
        output_dir = os.path.join(os.environ['WORK_DIR'],
                                  self.run_id,
                                  self.pipeline_type,
                                  self.collection_name)

        if int(self.chain):
            force_restart = self.meta['pipeline'].get('force_restart', 'False')
            msgbus.get_msg_bus().send_message(self.run_id,
                                              collection="analyze_%s" % self.collection_name,
                                              type=self.pipeline_type,
                                              custom_config=['pipeline.output_dir=%s' % output_dir,
                                                             'pipeline.forced_restarted=%s' % force_restart,
                                                             'pipeline.is_operation=%s' % self.is_operation,
                                                             'steps.merge.chain=1'])

        pipeline_dir = self.meta['pipeline']['output_dir']
        delete_files(pipeline_dir, patterns=['.*json'])
        clean_folder(pipeline_dir)


