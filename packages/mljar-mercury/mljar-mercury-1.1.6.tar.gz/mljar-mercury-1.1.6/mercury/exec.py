import nbformat 
from jupyter_client import MultiKernelManager 
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import HTMLExporter
import codecs


mkm = MultiKernelManager()
#mkm.start_kernel(kernel_name="python3", kernel_id="some-kernel")
km = mkm.get_kernel("some-kernel")

notebook_path = "./demo.ipynb"

with open(notebook_path, encoding="utf-8", errors="ignore") as f:
    nb = nbformat.read(f, as_version=4)

#print(nb.cells)

ep = ExecutePreprocessor()
ep.preprocess(nb, km=km)

#print(nb.cells)


exporter = HTMLExporter()
output, resources = exporter.from_notebook_node(nb)
codecs.open("amazing.html", 'w', encoding='utf-8').write(output)