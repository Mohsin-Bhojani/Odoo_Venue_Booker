from odoo import models, fields

class VenueBookingAmenity(models.Model):
    _name = "venue.booking.amenity"
    _description = "Venue Amenity"

    name = fields.Char(required=True)
    icon = fields.Char(string="Icon (FA class)")

    _unique_amenity_name = models.Constraint("UNIQUE(name)", "An amenity must have a unique name!")
