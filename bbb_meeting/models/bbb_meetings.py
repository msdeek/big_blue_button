from odoo import fields, models, api, _
import xml.etree.ElementTree as ETS
import urllib.request, urllib.parse, urllib.response, urllib.error
from urllib.request import urlopen
from urllib.parse import urlencode
from hashlib import sha1
from urllib.parse import quote
from .bbb_classes import (BBBException, ApiMethod, BBBModule)
from jxmlease import parse
from datetime import datetime
from dateutil.relativedelta import relativedelta
from bs4 import BeautifulSoup


class BBBMeeting(models.Model):
    _inherit = 'calendar.event'

    is_online = fields.Boolean(string="Online Meeting")
    bbb_server = fields.Many2one(comodel_name="bbb.servers", string="Host Server")
    bbb_server_url = fields.Char(string="", related='bbb_server.bbb_server_url', store=True)
    bbb_server_secret = fields.Char(string="", related='bbb_server.bbb_server_secret', store=True)
    bbb_server_logoutURL = fields.Char(string='', related='bbb_server.bbb_logoutURL', store=True)
    bbb_meeting_id = fields.Char(string="BigBlueButton Meeting ID", readonly=True, required=True, copy=False,
                                 default='New', store=True)
    bbb_meeting_create = fields.Char(compute='create_meeting')
    bbb_current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.uid)
    bbb_current_user_name = fields.Char(related='bbb_current_user.name')
    bbb_host = fields.Many2one('res.users', string='Meeting Hosts', default=lambda self: self.env.uid)
    allowStartStopRecording = fields.Boolean(string="Allow Start and Stop Recording")
    record = fields.Boolean(string="Allow to Record Meeting")
    autoStartRecording = fields.Boolean(string="Auto Start Record")
    duration = fields.Integer()
    run = fields.Char(compute='isMeetingRunning', string='Meeting Status')
    muteOnStart = fields.Boolean(string="Mute on Start")
    datas = fields.Binary('Content', attachment=True)
    calendarID = fields.One2many('bbb.recording', 'calendarID', string='Recordes')
    brecord = fields.Char(compute='getRecordings')

    @api.model
    def create(self, vals):
        if vals.get('bbb_meeting_id', 'New') == 'New':
            vals['bbb_meeting_id'] = self.env['ir.sequence'].next_by_code(
                'bbb.meeting.id.seq') or 'New'
        result = super(BBBMeeting, self).create(vals)
        return result

    @api.model
    def send_api_request(self, api_call, params={}, data=None):
        url = self.build_call_url(api_call, params)

        # if data is none, then we send a GET request, if not, then we send a POST request
        if data is None:
            response = urlopen(url).read()
        else:
            response = urlopen(url, data=urlencode(data).encode()).read()

        try:
            rawXml = parse(response)["response"]
        except Exception as e:
            raise BBBException("XMLSyntaxError")

        # get default config xml request will simply return the xml file without
        # returncode, so it will cause an error when try to check the return code
        if api_call != ApiMethod.GET_DEFAULT_CONFIG_XML:
            if rawXml["returncode"] == "FAILED":
                raise BBBException(rawXml["messageKey"],
                                   rawXml["message"])

        return rawXml

    @api.model
    def build_call_url(self, api_call, params={}):
        url = self.bbb_server_url
        api_path = 'api/'
        url += api_path + api_call + '?'
        for key, value in params.items():
            if isinstance(value, bool):
                value = 'true' if value else "false"
            else:
                value = str(value)
            url += key + "=" + value + "&"

        url += "checksum=" + self._get_checksum(api_call, params)
        return url

    @api.model
    def _get_checksum(self, api_call, params):
        secret_str = api_call
        for key, value in params.items():
            if isinstance(value, bool):
                value = "true" if value else "false"
            else:
                value = str(value)
            secret_str += key + "=" + value + "&"
        if secret_str.endswith("&"):
            secret_str = secret_str[:-1]
        secret_str += self.bbb_server_secret
        return sha1(secret_str.encode('utf-8')).hexdigest()

    @api.model
    def create_meeting(self):
        for meeting in self:
            if meeting.is_online == True:
                call = 'create'
                name = quote(meeting.name)
                meetingID = meeting.bbb_meeting_id
                record = meeting.record
                autoStartRecording = meeting.autoStartRecording
                allowStartStopRecording = meeting.allowStartStopRecording
                moderatorPW = 'Ms3343785@'
                attendeePW = 'Att3343785@'
                copyright = 'codefish'
                # logo = 'https://www.tadreb.live/pluginfile.php/1/theme_klass/logo/1588118507/tadreb.png'
                if meeting.description:
                    msg = meeting.description
                else:
                    msg = "www.codefish.com.eg"
                welcome = quote(msg)
                duration = (meeting.duration) * 60
                muteOnStart = meeting.muteOnStart
                params = {'name': name,
                          'meetingID': meetingID,
                          'record': record,
                          'autoStartRecording': autoStartRecording,
                          'allowStartStopRecording': allowStartStopRecording,
                          'moderatorPW': moderatorPW,
                          'attendeePW': attendeePW,
                          'duration': duration,
                          'welcome': welcome,
                          'copyright': copyright,
                          'muteOnStart': muteOnStart
                          }

                rawXml = meeting.send_api_request(ApiMethod.CREATE, params=params)
            else:
                rawXml = ""

        meeting.bbb_meeting_create = rawXml
        return rawXml

    @api.model
    def join_meeting(self):
        for meeting in self:
            if meeting.is_online == True:
                call = 'join'
                userid = self.env.uid
                Name = self.env['res.users'].browse([userid]).name
                fullName = quote(Name)
                meetingID = meeting.bbb_meeting_id

                if meeting.bbb_host.id == userid:
                    password = 'Ms3343785@'
                else:
                    password = 'Att3343785@'

                params = {'fullName': fullName,
                          'meetingID': meetingID,
                          'password': password,
                          }

                response = meeting.build_call_url(api_call=call, params=params)
            else:
                response = ""
        return response

    # @api.model
    def openURL_m(self):
        z = self.join_meeting()
        return {
            'type': 'ir.actions.act_url',
            'url': z,
            'target': 'new',  # open in a new tab
        }

    @api.model
    def isMeetingRunning(self):
        for meeting in self:
            if meeting.is_online == True:
                call = 'isMeetingRunning'
                meetingID = meeting.bbb_meeting_id
                params = {
                    'meetingID': meetingID
                }
                url = meeting.build_call_url(api_call=call, params=params)
                uh = urllib.request.urlopen(url)
                data = uh.read().decode()
                res = ETS.fromstring(data)
                fres = res.find('running').text
                if fres == "true":
                    text = "Running"
                else:
                    text = "Not Running"

                meeting.run = text
            else:
                url = ""
                meeting.run = url
            return url

    @api.model
    def getRecordings(self):
        for meeting in self:
            if meeting.is_online == True and meeting.bbb_meeting_id != 'New':
                call = 'getRecordings'
                meetingID = meeting.bbb_meeting_id
                params = {
                    'meetingID': meetingID
                }
                url = meeting.build_call_url(api_call=call, params=params)
                uh = urllib.request.urlopen(url)
                data = uh.read().decode()
                res = ETS.fromstring(data)
                self.brecord = res
                recdata = res.findall('recordings/recording')
                for recid in recdata:
                    recordID = recid.find('recordID').text
                    rname = recid.find('name').text
                    fdata = res.findall('recordings/recording/playback/format')
                    for rec in fdata:
                        url = rec.find('url').text
                        bbb_meeting_id = meetingID
                        if not self.calendarID.filtered(lambda f: f.recordID == recordID):
                            self.env['bbb.recording'].create({
                                'recordID': recordID,
                                'url': url,
                                'bbb_meeting_id': bbb_meeting_id,
                                'calendarID': self.id,
                                'rname': rname
                            })

            else:
                self.brecord = ""
