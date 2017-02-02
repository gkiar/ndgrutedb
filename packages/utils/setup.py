#!/usr/bin/env python
# Copyright 2014 Open Connectome Project (http://openconnecto.me)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# setup.py
# Created by Disa Mhembere on 2015-04-15.
# Email: disa@jhu.edu

"""
Initial script for setting up m2g

**Inputs**
    (Indirect) $M2G_HOME: [string]
        - System variable needs to be set to the base directory
          of the cloned m2g repo.

**Outputs**
    data/: [directory]
        - Directory containing atlas labels and template images.
    zindex.c: [c]
        - Compiled cython script used in the framework.
"""

import argparse
import os
from subprocess import call
from webget import wget


__data_dir__ = os.path.abspath(os.path.join(os.environ['M2G_HOME'], "data/"))
weburl = "http://openconnecto.me/data/public/MR-data/"
__files__ = {
    "Atlas": [
        "desikan_in_mni_space/MNI152_T1_1mm_brain_incremented.nii",
        "desikan_in_mni_space/MNI152_T1_1mm_desikan_adjusted.nii",
        "desikan_in_mni_space/MNI152_T1_1mm_desikan_adjusted.txt",
        "desikan_in_mni_space/MNI152_T1_1mm_brain_mask.nii",
        "desikan_in_mni_space/MNI152_T1_1mm_brain_labels.nii",
        "desikan_in_mni_space/MNI152_T1_1mm_brain.nii",
        "desikan_in_mni_space/MNI152_T1_1mm.nii.gz",
        "downsampled/mni152ds00071.nii",
        "downsampled/mni152ds00071.nii",
        "downsampled/mni152ds00108.nii",
        "downsampled/mni152ds00195.nii",
        "downsampled/mni152ds00350.nii",
        "downsampled/mni152ds00583.nii",
        "downsampled/mni152ds01216.nii",
        "downsampled/mni152ds03231.nii",
        "downsampled/mni152ds16784.nii",
        "downsampled/mni152ds00096.nii",
        "downsampled/mni152ds00140.nii",
        "downsampled/mni152ds00278.nii",
        "downsampled/mni152ds00446.nii",
        "downsampled/mni152ds00833.nii",
        "downsampled/mni152ds01876.nii",
        "downsampled/mni152ds06481.nii",
        "downsampled/mni152ds72784.nii",
        "m2g/slab_atlas.nii",
    ],
    "Centroids": ["centroids.mat"]
}


def get_local_fn(fn, _type):
    return os.path.join(
        os.path.join(__data_dir__, _type, os.path.basename(fn))
    )


def get_files(force):
    """
    Get static files from the web

    @param force: Even if the file exists -- fetch a new copy
    """
    atlas_dir = os.path.join(__data_dir__, "Atlas")
    centroid_dir = os.path.join(__data_dir__, "Centroids")

    if not os.path.exists(atlas_dir):
        os.makedirs(atlas_dir)
    if not os.path.exists(centroid_dir):
        os.makedirs(centroid_dir)

        for k in __files__.keys():
            for v in __files__[k]:
                if not os.path.exists(get_local_fn(v, k)) or force:
                    wget(get_local_fn(v, k), weburl+k+"/"+v)


def compile_cython():
  os.chdir(os.path.join(os.environ['M2G_HOME'],"MR-OCP/mrcap/"))
  ret = call(["python", "setup.py", "install"])
  assert not ret, "Failed to run setup.py in 'mrcap' directory. Perhaps running this script with 'sudo' will help"

  # Compile utils cython modules
  os.chdir(os.path.join(os.environ['M2G_HOME'],"MR-OCP/mrcap/utils/"))
  ret = call(["python", "setup.py", "install"])
  assert not ret, "Failed to run setup.py in 'mrca/utilsp' directory. Perhaps running this script with 'sudo' will help"

def main():
    """
    Fetch static data from the web and / compile zindex cython module
    """
    parser = argparse.ArgumentParser(description="Gets data files that " +
                                     "graph gen and verification code needs." +
                                     " Also can build zindex.")
    parser.add_argument("-c", "--compile",
                        action="store_true",
                        help="Compile the zindex cython module")
    parser.add_argument("-f", "--force",
                        action="store_true",
                        help="Force the download of data even if we have it")
    result = parser.parse_args()

    get_files(result.force)
    if result.compile:
        compile_cython()


if __name__ == "__main__":
    main()
