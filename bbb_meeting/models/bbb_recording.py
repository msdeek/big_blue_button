from odoo import fields, models, api


class BBBRecording (models.Model):
    _name = 'bbb.recording'
    _description = 'Description'

    recordID = fields.Char(string='Record ID')
    calendarID = fields.Many2one('calendar.event')
    bbb_meeting_id = fields.Char(string="Meeting ID", related='calendarID.bbb_meeting_id', store=True)
    url = fields.Char(string='Record')
    rname = fields.Char(string="Meeting Name", related='calendarID.name', store=True)
    


