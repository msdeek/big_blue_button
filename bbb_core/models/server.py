from odoo import fields, models, api, _
import xml.etree.ElementTree as ET
import urllib.request, urllib.parse, urllib.response, urllib.error

class ModelName (models.Model):
    _name = 'bbb_servers.server'
    _description = 'BigBlueButton Servers'

    name = fields.Char()
    bbb_server_url = fields.Char(string="Server URL", required=True, )
    bbb_server_secret = fields.Char(string="Server Secret", required=True, )
    bbb_api_ver = fields.Char(compute='api_ver')

    def api_ver(self):
        url = self.bbb_server_url + 'api/'
        uh = urllib.request.urlopen(url)
        data = uh.read().decode()
        res = ET.fromstring(data)
        fres = res.find('version').text
        self.bbb_api_ver = fres



