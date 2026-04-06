from odoo import api, models, fields
from odoo.exceptions import UserError

class VenueBookingVenue(models.Model):
    _name = "venue.booking.venue"
    _description = "Venue"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(required=True, tracking=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    city = fields.Char()
    capacity = fields.Integer(default=50)
    hourly_rate = fields.Float()
    currency_id = fields.Many2one("res.currency", default=lambda self: self.env.company.currency_id)
    amenity_ids = fields.Many2many("venue.booking.amenity", string="Amenities")
    booking_ids = fields.One2many("venue.booking.booking", "venue_id", string="Bookings")
    booking_count = fields.Integer(compute="_compute_booking_count")

    _check_capacity = models.Constraint("CHECK(capacity > 0)", "Capacity must be greater than zero!")
    _check_hourly_rate = models.Constraint("CHECK(hourly_rate >= 0)", "Hourly rate cannot be negative!")

    @api.depends("booking_ids")
    def _compute_booking_count(self):
        for record in self:
            record.booking_count = len(record.booking_ids)
