class Post():

    def __init__(self, _apibase):
        self.apibase = _apibase

    def registerfile(self, _path, _dns, _created_by, _filenames, _projects):
        _data = dict(path=_path, dns=_dns, created_by=_created_by, filenames=_filenames, projects=_projects)
        print(_data)
        # requests.post(conf.ALYX_PLUGIN_ADDRESS + '/register-file',headers = self.apibase.headers, data = _data)
