
import nbformat
from pathlib import PosixPath
from nbconvert.preprocessors import ExecutePreprocessor
import os

class notebook:
    def __init__(self, path, file):
        self.file = file
        self.path = path

    @property
    def notebook(self):
        try:
            return self._notebook
        except:
            with open(self.fullpath) as fin:
                self._notebook = nbformat.read(fin, as_version=4)
            return self._notebook
    
    @property
    def fullpath(self):
        return self.path / self.file
    
    @property
    def runpath(self):
        return self.path.runfolder / self.file

    @property
    def errorpath(self):
        return self.path.errorfolder / self.file
    
    def exists(self):
        return self.fullpath.exists()
    
    def mtime(self):
        return os.path.getmtime(self.fullpath)
    
    def newer(self, other):
        return self.mtime() > other.mtime()
    
    def write_run(self):
        with open(self.runpath, 'w', encoding='utf-8') as fout:
            nbformat.write(self.notebook, fout)
        
    def write_error(self):
        with open(self.errorpath, 'w', encoding='utf-8') as fout:
            nbformat.write(self.notebook, fout)

    def execute(self):
        kernel = self.path.kernel or self.notebook.metadata.kernelspec.name
        ep = ExecutePreprocessor(timeout=self.path.timeout, 
                                 kernel_name=kernel)
        try:
            ep.preprocess(self.notebook, 
                          {'metadata': {'path': str(self.path)}})
            self.write_run()
            print('success')
        except:
            self.write_error()
            print('error')
         
        
class notebookpath(PosixPath):
    """
    A path containing notebooks, use execute_all to execute all notebooks in the folder and 
    store the finished notebooks in a subfolder
    """
    def __new__(cls, *path, **kwargs):
        return PosixPath.__new__(cls, *path)
        
    def __init__(self, *path, kernel=None,
                 runfolder='run', 
                 errorfolder='error',
                 timeout=600):
        super().__init__()
        self.kernel = kernel
        self._runfolder = runfolder
        self._errorfolder = errorfolder
        self.timeout = timeout
 
    def _subfolder(self, folder):
        r = self / folder
        r.mkdir(exist_ok=True)
        return r

    @property
    def runfolder(self):
        return self._subfolder(self._runfolder)

    @property
    def errorfolder(self):
        return self._subfolder(self._errorfolder)
        
    def notebook(self, file, path=None):
        path = path or self
        return notebook(path, file)
        
    def execute_all(self):
        for f in sorted(self.glob('*.ipynb')):
            print(f)
            nb = self.notebook(f.name)
            run = self.notebook(f.name, self.runfolder)
            error = self.notebook(f.name, self.errorfolder)
            
            if error.exists() and nb.newer(error):
                error.fullpath.unlink() 
            if run.exists() and nb.newer(run):
                run.fullpath.unlink()

            if not (run.exists() or error.exists()):
                nb.execute()
