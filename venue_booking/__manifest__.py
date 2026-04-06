{
    "name": "Venue Booking",
    "depends": ["base", "mail", "account"],
    "application": True,
    "data": [
        "security/ir.model.access.csv",
        "views/venue_booking_venue_views.xml",
        "views/venue_booking_booking_views.xml",
        "views/venue_booking_amenity_views.xml",
        "views/venue_booking_menus.xml",
        "data/venue_data.xml",
    ]
}
