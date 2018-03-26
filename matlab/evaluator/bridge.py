from pymatbridge import Matlab
import numpy as np
import tornado.ioloop
import tornado.web
import json

mlab = Matlab(matlab='/Applications/MATLAB_R2012b.app/bin/matlab')

class RegressionHandler(tornado.web.RequestHandler):
  def get(self):
    d = self.get_argument("data", None)
    if not d:
      self.finish('err')
    else:
      data = json.loads(d)
      res = mlab.run_func('~/Downloads/lasso/api_full.m', {'feature': data})
      self.finish(str(res["result"]))
      
class SVMHandler(tornado.web.RequestHandler):
  def get(self):
    d = self.get_argument("data", None)
    if not d:
      self.finish('err')
    else:
      data = json.loads(d)
      res = mlab.run_func('~/Downloads/lasso/api_svm.m', {'feature': data})
      self.finish(str(res["result"]))

class Application(tornado.web.Application):
    def __exit__(self):
      print "trying kill matlab"
      mlab.stop()
      print "matlab killed"
      super(Application, self).__del__()    
      
application = Application([
    (r"^/lr$", RegressionHandler),
    (r"^/svm$", SVMHandler),
])

if __name__ == "__main__":
    application.listen(8001)
    mlab.start()
    tornado.ioloop.IOLoop.instance().start()
