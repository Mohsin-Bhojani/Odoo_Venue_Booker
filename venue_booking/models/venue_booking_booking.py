from odoo import api, models, fields
from odoo.exceptions import UserError, ValidationError

class VenueBookingBooking(models.Model):
    _name = "venue.booking.booking"
    _description = "Venue Booking"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_start desc"

    name = fields.Char(required=True, copy=False, readonly=True, default="New")
    venue_id = fields.Many2one("venue.booking.venue", required=True, tracking=True)
    partner_id = fields.Many2one("res.partner", string="Customer", required=True, tracking=True)
    date_start = fields.Datetime(string="Start Date & Time", required=True)
    date_end = fields.Datetime(string="End Date & Time", required=True)
    duration = fields.Float(string="Duration (hrs)", compute="_compute_duration", store=True)
    hourly_rate = fields.Float(related="venue_id.hourly_rate", readonly=True)
    currency_id = fields.Many2one("res.currency", related="venue_id.currency_id", readonly=True)
    total_amount = fields.Float(compute="_compute_total_amount", store=True)
    state = fields.Selection(
        selection=[("draft", "Draft"), ("confirmed", "Confirmed"), ("cancelled", "Cancelled")],
        default="draft",
        tracking=True
    )
    invoice_id = fields.Many2one("account.move", readonly=True, copy=False)
    notes = fields.Text()

    _check_dates = models.Constraint("CHECK(date_end > date_start)", "End time must be after start time!")

    @api.depends("date_start", "date_end")
    def _compute_duration(self):
        for record in self:
            if record.date_start and record.date_end:
                delta = record.date_end - record.date_start
                record.duration = delta.total_seconds() / 3600
            else:
                record.duration = 0.0

    @api.depends("duration", "hourly_rate")
    def _compute_total_amount(self):
        for record in self:
            record.total_amount = record.duration * record.hourly_rate

    @api.constrains("date_start", "date_end", "venue_id")
    def _check_venue_availability(self):
        for record in self:
            overlapping = self.search([
                ("venue_id", "=", record.venue_id.id),
                ("state", "!=", "cancelled"),
                ("id", "!=", record.id),
                ("date_start", "<", record.date_end),
                ("date_end", ">", record.date_start),
            ])
            if overlapping:
                raise ValidationError(f"The venue '{record.venue_id.name}' is already booked during this time slot!")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("venue.booking.booking") or "New"
        return super().create(vals_list)
        
    def action_confirm(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("A cancelled booking cannot be confirmed!")
            else:
                record.state = "confirmed"

    def action_cancel(self):
        for record in self:
            if record.state == "confirmed" and record.invoice_id:
                raise UserError("Cannot cancel a booking that already has an invoice!")
            else:
                record.state = "cancelled"

    def action_reset_draft(self):
        for record in self:
            record.state = "draft"

    def action_create_invoice(self):
        self.ensure_one()
        if self.state != "confirmed":
            raise UserError("Only confirmed bookings can be invoiced!")
        invoice = self.env["account.move"].create({
            "move_type": "out_invoice",
            "partner_id": self.partner_id.id,
            "invoice_line_ids": [(0, 0, {
                "name": f"Venue Booking: {self.venue_id.name} ({self.name})",
                "quantity": self.duration,
                "price_unit": self.hourly_rate,
            })],
        })
        self.invoice_id = invoice
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.move",
            "view_mode": "form",
            "res_id": invoice.id,
        }
