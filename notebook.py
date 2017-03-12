#### Modify ipython_notebook_config.py configuration file
# Configuration file for ipython-notebook.
c = get_config()
c.IPKernelApp.pylab = 'inline'
c.IPKernelApp.matplotlib = 'inline'
c.NotebookApp.certfile = u'/home/ubuntu/test1/mycert.pem'
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.password = u'sha1:bf7ec004c369:1aaab829a1e113ef52b8b7bef3d49ff806e63cda'
c.NotebookApp.port = 8888
