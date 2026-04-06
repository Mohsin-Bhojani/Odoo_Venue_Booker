#Venue Booking — Odoo Module

A clean Odoo module for managing venue reservations, bookings, and calendar scheduling.

---

## Features

- **Venue Management** — Define venues with capacity, hourly rates, currency, and amenities
- **Booking Workflow** — Draft → Confirmed → Checked In state machine with contextual action buttons
- ** Calendar View** — Monthly calendar with per-venue colour coding
- ** Amenities** — Reusable amenity tags attached to venues

---

## Models

 Model                     Description 

 `venue.booking.venue`     Physical venues with pricing configuration 
 `venue.booking.booking`   Individual bookings linked to a venue and customer 
 `venue.booking.amenity`   Reusable amenity tags with Font Awesome icons 

---

## Booking States

```
Draft ──► Confirmed ──► Checked In
  ▲            │
  │            ▼
  └──── Cancelled
```

 State        Colour     Available Actions 

 Draft        Yellow     Confirm, Cancel 
 Confirmed    Green      Check In, Cancel 
 Checked In   Blue       -
 Cancelled    Grey       Reset to Draft 

---

# Installation

1. Clone into your Odoo addons directory:

```bash
git clone https://github.com/your-org/venue_booking.git /path/to/odoo/addons/venue_booking
```

2. Restart Odoo and upgrade the module:

```bash
./odoo-bin -c odoo.conf -u venue_booking -d your_database
```

3. In Odoo go to **Apps**, search for **Venue Booking**, and click **Install**.

---

# Module Structure

```
venue_booking/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── venue.py
│   ├── booking.py
│   └── amenity.py
├── views/
│   ├── venue_views.xml
│   ├── booking_views.xml
│   ├── amenity_views.xml
│   └── menu.xml
└── security/
    └── ir.model.access.csv
```

---

# Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push and open a Pull Request

Please follow [Odoo's coding guidelines](https://www.odoo.com/documentation/17.0/contributing/development/coding_guidelines.html).

---

## License

This module is licensed under the [LGPL-3.0 License](LICENSE).

---

## Author

Built with love using [Odoo](https://www.odoo.com).
