class Business:
    def __init__(
        self,
        name,
        website,
        phone,
        maps_url,
        rate,
        reviews,
        status="raw",
        lead_score=None,
        emails = None,
        contact_page = None,
        facebook = None,
        instagram = None,
        linkedin = None,
        youtube = None
    ):
        self.name = name
        self.website = website
        self.phone = phone
        self.maps_url = maps_url
        self.rate = rate
        self.reviews = reviews
        self.status = status
        self.lead_score = lead_score
        self.emails = emails or []
        self.contact_page = contact_page
        self.facebook = facebook
        self.instagram = instagram
        self.linkedin = linkedin
        self.youtube = youtube

    def __repr__(self):
        return (
            f"Business("
            f"name={self.name}, "
            f"website={self.website}, "
            f"phone={self.phone}, "
            f"emails={len(self.emails)}, "
            f"facebook={'Yes' if self.facebook else 'No'}, "
            f"instagram={'Yes' if self.instagram else 'No'}, "
            f"linkedin={'Yes' if self.linkedin else 'No'}, "
            f"status={self.status})"
        )
    def to_dict(self):
        return {
            "name": self.name,
            "website": self.website,
            "phone": self.phone,
            "maps_url": self.maps_url,
            "rate": self.rate,
            "status": self.status,
            "lead_score": self.lead_score,
            "emails": self.emails,
            "contact_page": self.contact_page,
            "facebook": self.facebook,
            "instagram": self.instagram,
            "linkedin": self.linkedin,
        }