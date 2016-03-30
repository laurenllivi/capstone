from homepage import models as hmod

# FEATURE_CHOICES = [(feature.name, feature.name) for feature in hmod.Feature.objects.all()]

POLICY_CHOICES = [(policy.id, policy.name) for policy in hmod.Cancellation_Policy.objects.all()]

QUESTION_TOPICS = (
    ('', 'Subject'),
    ('Booking a Venue', 'Booking a Venue'),
    ('Managing my Venue', 'Managing my Venue'),
    ('Account and Profile', 'Account and Profile'),
    ('Payments', 'Payments'),
    ('Rules and Regulations', 'Rules and Regulations'),
    ('General', 'General'),
)

VENUE_TYPE_CHOICES = (
    ('backyard', 'Backyard'),
    ('barn', 'Barn'),
    ('porch', 'Deck/Porch/Patio'),
    ('theater', 'Home Theater'),
    ('pool', 'Pool'),
    ('rooftop', 'Rooftop'),
    ('sports', 'Sports')
)

WITHIN_MILES_CHOICES = (
    ('5', '5 miles'),
    ('10', '10 miles'),
    ('15', '15 miles'),
    ('20', '20 miles'),
    ('30', '30 miles'),
    ('50', '50 miles'),
    ('100', '100 miles'),
)

STATE_CHOICES = (
    ('AL', "Alabama"),
    ('AK', "Alaska"),
    ('AZ', "Arizona"),
    ('AR', "Arkansas"),
    ('CA', "California"),
    ('CO', "Colorado"),
    ('CT', "Connecticut"),
    ('DE', "Delaware"),
    ('FL', "Florida"),
    ('GA', "Georgia"),
    ('HI', "Hawaii"),
    ('ID', "Idaho"),
    ('IL', "Illinois"),
    ('IN', "Indiana"),
    ('IA', "Iowa"),
    ('KS', "Kansas"),
    ('KY', "Kentucky"),
    ('LA', "Louisiana"),
    ('ME', "Maine"),
    ('MD', "Maryland"),
    ('MA', "Massachusetts"),
    ('MI', "Michigan"),
    ('MN', "Minnesota"),
    ('MS', "Mississippi"),
    ('MO', "Missouri"),
    ('MT', "Montana"),
    ('NE', "Nebraska"),
    ('NV', "Nevada"),
    ('NH', "New Hampshire"),
    ('NJ', "New Jersey"),
    ('NM', "New Mexico"),
    ('NY', "New York"),
    ('NC', "North Carolina"),
    ('ND', "North Dakota"),
    ('OH', "Ohio"),
    ('OK', "Oklahoma"),
    ('OR', "Oregon"),
    ('PA', "Pennsylvania"),
    ('RI', "Rhode Island"),
    ('SC', "South Carolina"),
    ('SD', "South Dakota"),
    ('TN', "Tennessee"),
    ('TX', "Texas"),
    ('UT', "Utah"),
    ('VT', "Vermont"),
    ('VA', "Virginia"),
    ('WA', "Washington"),
    ('WV', "West Virginia"),
    ('WI', "Wisconsin"),
    ('WY', "Wyoming"),
)

PRICE_CHOICES = (
    ('5', '5'),
    ('10', '10'),
    ('15', '15'),
    ('20', '20'),
    ('30', '30'),
    ('50', '50'),
    ('100', '100'),
)

TIME_CHOICES = (
    ('---', ''),
    ('00:00', '12:00 AM'),
    ('01:00', '1:00 AM'),
    ('12:00', '12:00 PM'),
    ('13:00', '1:00 PM'),
    ('13:30', '1:30 PM'),
    ('14:00', '2:00 PM'),
    ('14:30', '2:30 PM'),
    ('15:00', '3:00 PM'),
    ('15:30', '3:30 PM'),
    ('16:00', '4:00 PM'),
    ('16:30', '4:30 PM'),
    ('17:00', '5:00 PM'),
    ('17:30', '5:30 PM'),
    ('18:00', '6:00 PM'),
    ('18:30', '6:30 PM'),
    ('19:00', '7:00 PM'),
    ('19:30', '7:30 PM'),
    ('20:00', '8:00 PM'),
    ('20:30', '8:30 PM'),
    ('21:00', '9:00 PM'),
    ('21:30', '9:30 PM'),
    ('22:00', '10:00 PM'),
    ('22:30', '10:30 PM'),
)