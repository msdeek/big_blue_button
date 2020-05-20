from odoo import fields, models, api, _
import xml.etree.ElementTree as ETS
import urllib.request, urllib.parse, urllib.response, urllib.error
from urllib.request import urlopen
from urllib.parse import urlencode
from hashlib import sha1
from urllib.parse import quote
from .bbbclass import (BBBException, ApiMethod, BBBModule)
from jxmlease import parse


class BbbMeeting(models.Model):

    _inherit = 'slide.slide'

    nbr_online = fields.Integer("Number of Online Sessions", compute="_compute_slides_statistics", store=True)
    slide_type = fields.Selection(selection_add=[('online', 'Online Session')])
    is_online = fields.Boolean(string="Online Session")
    bbb_server = fields.Many2one(comodel_name="bbb_servers.server", string="BigBlueButton Server")
    bbb_server_url = fields.Char(string="", related='bbb_server.bbb_server_url', store=True)
    bbb_server_secret = fields.Char(string="", related='bbb_server.bbb_server_secret', store=True)
    bbb_meeting_id = fields.Char(string="", readonly=True, required=True, copy=False, default='New', store=True)
    bbb_welcome	= fields.Text(string='A welcome message')
    bbb_meeting_create = fields.Char(compute='create_meeting')
    current_user = fields.Many2one('res.users', 'Current User', default=lambda self: self.env.uid)
    current_user_name = fields.Char(related='current_user.name', store=True)
    bbb_meeting_info = fields.Char()
    bbb_moderatorPW = fields.Char(store=True)
    join_m = fields.Char(compute='join_meeting_m')
    join_a = fields.Char(compute='join_meeting_a')
    autoStartRecording = fields.Boolean()
    allowStartStopRecording = fields.Boolean()
    record =fields.Boolean()
    start = fields.Date()
    end = fields.Date()


    @api.model
    def create(self, vals):
        if vals.get('bbb_meeting_id', 'New') == 'New':
            vals['bbb_meeting_id'] = self.env['ir.sequence'].next_by_code(
                'meeting.id.seq') or 'New'
        result = super(BbbMeeting, self).create(vals)
        return result

    @api.model
    def _send_api_request(self, api_call, params={}, data=None):
        url = self._build_call_url(api_call, params)

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
    def _build_call_url(self, api_call, params={}):
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

    #@api.model
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
                attendeePW = 'Att334375@'
                params = {'name':name,
                          'meetingID':meetingID,
                          'record': record,
                          'autoStartRecording':autoStartRecording,
                          'allowStartStopRecording':allowStartStopRecording,
                          'moderatorPW':moderatorPW,
                          'attendeePW':attendeePW
                          }
                rawXml = meeting._send_api_request(ApiMethod.CREATE, params=params)
            else:
                rawXml = ""
        meeting.bbb_meeting_create = rawXml
        return rawXml


    #@api.model
    def join_meeting_m(self):
        for meeting in self:
            if meeting.is_online == True:
                call = 'join'
                fullName = quote(self.env.uid.name)
                meetingID = meeting.bbb_meeting_id
                password = 'Ms3343785@'
                params = {'fullName':fullName,
                          'meetingID':meetingID,
                          'password':password,
                          }
                response = meeting._build_call_url(api_call=call, params=params)
            else:
                response = ""
        meeting.join_m = response


    def join_meeting_a(self):
        for meeting in self:
            if meeting.is_online == True:
                call = 'join'
                fullName = meeting.current_user_name
                meetingID = meeting.bbb_meeting_id
                password = 'Att334375@'
                params = {'fullName':fullName,
                          'meetingID':meetingID,
                          'password':password,
                          }
                response = meeting._build_call_url(api_call=call, params=params)
            else:
                response = ""
        meeting.join_a = response

    def _create_meeting(self, call):
        if self.is_online == True:
            for rec in self:
                call = 'create'
                api_call = 'api/'
                api_call += call + '?'
                url = rec.bbb_server_url
                url += api_call
                params = 'name='
                qname = quote(rec.name)
                params += str(qname) + '&'
                params += 'meetingID='
                params += str(rec.bbb_meeting_id) + '&'
                params += 'autoStartRecording='
                params += str(self.autoStartRecording) + '&'
                params += 'allowStartStopRecording='
                params += str(self.allowStartStopRecording)
                url += params
                checksum = call + params
                checksum += str(rec.bbb_server_secret)
                url += '&checksum='
                url += sha1(checksum.encode()).hexdigest()
                uh = urllib.request.urlopen(url)
                data = uh.read().decode()
                res = ETS.fromstring(data)
                ffres = res.find('moderatorPW').text
                rec.bbb_meeting_create = url
                rec.moderatorPW = ffres
                jcall = 'join'
                japi_call = "api/"
                japi_call += call + "?"

        else:
            self.bbb_meeting_create = ""


    def _get_meeting_info(self):
        if self.is_online == True:
            call = 'getMeetingInfo'
            api_call = "api/"
            api_call += call + "?"
            url = self.bbb_server_url
            url += api_call
            params = 'meetingID='
            params += str(self.bbb_meeting_id)
            url += params + "&"
            checksum = call + params
            checksum += str(self.bbb_server_secret)
            url += "checksum=" + sha1(checksum.encode()).hexdigest()
            uh = urllib.request.urlopen(url)
            data = uh.read().decode()
            res = ETS.fromstring(data)
            #fres = res.find('meetingID').text
            self.bbb_meeting_info = url
            #self.moderatorPW = fres
        else:
            self.bbb_meeting_info = ""

    def xjoin_meeting(self):
        if self.is_online == True:
            call = 'join'
            api_call = "api/"
            api_call += call + "?"
            url = self.bbb_server_url
            url += api_call
            params = 'fullName=' + str(self.current_user_name) + '&'
            params += 'meetingID='
            params += str(self.bbb_meeting_id) + '&'
            params += 'password='
            params += str(self.moderatorPW) + '&'
            params += 'allowStartStopRecording=true'
            #params += str(self.allowStartStopRecording)
            url += params
            checksum = call + params
            checksum += str(self.bbb_server_secret)
            url += "&checksum=" + sha1(checksum.encode()).hexdigest()
            uh = urllib.request.urlopen(url)
            data = uh.read().decode()
            #res = ETS.fromstring(data)
            self.join = url
        else:
            self.join = ""

class BbbMeetingChannel(models.Model):
    _inherit = 'slide.channel'

    nbr_online = fields.Integer('Online Sessions', compute='_compute_slides_statistics', store=True)



