import nbformat 
from jupyter_client import MultiKernelManager 
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import codecs

import json
from jupyter_client import BlockingKernelClient

info = json.load(open("kernel-some-kernel.json"))

kc = BlockingKernelClient()
kc.load_connection_info(info)

print(kc)
print(kc.kernel_info(), "|", kc.kernel_name)