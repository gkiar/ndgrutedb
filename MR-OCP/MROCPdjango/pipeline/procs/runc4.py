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

# runc4.py
# Created by Disa Mhembere, Greg Kiar on 2015-05-28.
# Email: disa@jhu.edu, gkiar07@gmail.com

import argparse
from django.core.mail import send_mail
from django.conf import settings
import ndmg.scripts.ndmg_pipeline as mgp
import os

def runc4(dti_path, mprage_path, bvalue_path, bvector_path,
          atlas_path, mask_path, labels_path, outdir):
    """
    Job launched by webservice to execute ndmg pipeline and graph generation.
    """
    msg = "Dear Greg,\n\nSomeone has made more work for you. \n\n"
    msg += "Here's some info you care about:\n"
    msg += "- dti path: {0}\n".format(dti_path)
    msg += "- mprage path: {0}\n".format(mprage_path)
    msg += "- bvalue path: {0}\n".format(bvalue_path)
    msg += "- bvector path: {0}\n".format(bvector_path)
    msg += "- atlas path: {0}\n".format(atlas_path)
    msg += "- mask_path path: {0}\n".format(mask_path)
    msg += "- labels_path path: {0}\n".format(labels_path)
    #msg += "- Requester's email: {0}\n".format(email)
    send_mail("C4 job request", msg, settings.SERVER_EMAIL,
              ["asidom2002@yahoo.com"], fail_silently=False)
              #["gkiar07@gmail.com"], fail_silently=False)

    pipeline = mgp.ndmg_pipeline
    pipeline(dti_path, bvalue_path, bvector_path, mprage_path,
        atlas_path, mask_path, labels_path, outdir, clean=True)

    print "Output written to {} ...".format(outdir)
