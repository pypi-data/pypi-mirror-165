import random
import hashlib
import os
import json

from flask import Blueprint, request, send_file

import utils
import dav


class Share:
    def __init__(self, fs, auth=None,secret=None):
        self.fs = fs
        self.auth = auth
        self.secret=secret
        self.shares = {}
        self.api = Blueprint("share", __name__, url_prefix="/")
        self.dav = dav.Dav(self.fs, blueprint=False)
        self.api.add_url_rule('/api/shares/new',
                              view_func=self.make_share_view,
                              methods=["POST"]
                              )
        self.api.add_url_rule('/api/shares/del',
                              view_func=self.del_share_view,
                              methods=["POST"]
                              )
        self.api.add_url_rule(
                            "/api/shares/dav/<path:path>",
                            methods=["GET", "PUT", "PROPFIND", "DELETE", "MKCOL"],
                            view_func=self.share_dav,
        )
        self.api.add_url_rule(
                            "/api/shares/info/<idt>",
                            view_func=self.share_info,
        )
        self.api.add_url_rule(
                            "/api/shares/",
                            view_func=self.all_shares,
        )
        self.api.add_url_rule(
                            "/shares/<path:path>",
                            view_func=self.view_share,
        )
    def do_make_share(self, path, username=None,mode='r'):
        data={'path':path,'username':username,'mode':mode}
        idt = hashlib.sha512((json.dumps(data) + str(random.random())).encode()).hexdigest()[:10]
        self.shares[idt] = data
        return idt
    def do_del_share(self,idt):
        del self.shares[idt]
    def del_share_view(self):
        if not utils.chk_auth(auth,self.secret):
            return {"error": 403}, 403
        id = request.json['id']
        try:
            self.do_del_share(id)
            return {"res":"ok"},200
        except KeyError:
            return {"res":"err","error":404},404
    def make_share_view(self):
        if not utils.chk_auth(auth,self.secret):
            return {"error": 403}, 403
        req = request.json
        path = req['path']
        args={'path':path,'username':username}

        if 'mode'  in req:
             args['mode']=req['mode']
        res = {"res":"ok",'id': self.do_make_share(**args)}
        return res

    def share_dav(self, path):
        p = list(filter(''.__ne__, path.split("/")))
        info=self.shares[p[0]]
        path=os.path.join(info['path'], "/".join(p[1:]))
        utils.fs_context.username=info['username']

        print(info)
        #return self.dav(os.path.join(self.shares[str(p[0])], "/".join(p[1:])))
        if info['mode']=='r' and request.method in ['PUT','DELETE','MKCOL']:
            return "",403
        return self.dav(path)
    def share_info(self,idt):
        return self.shares[idt]
    def view_share(self,path):
        if path.split('/')[0] in self.shares:
            return send_file("static/share.html")
        return 'Not such share',404
    def all_shares(self):
        return self.shares
