
network_filters = {
    "filters": {
        "Profession": {
            "unconditional": ["Actor", "Singer", "Dancer", "Voice Actor", "Puppeteer", "Crew"],
            "conditional": {
                "Director": { "locked": True },
                "Producer": { "locked": True }
            },
            "locked": False
        },
        "Connection": {
            "unconditional": ["1st", "2nd", "3rd", "4+"],
            "locked": False
        },
        "Location": {
            "unconditional": ["Toronto, ON", "Montreal, QC", "Sudbury, ON"],
            "locked": False
        },
        "Gender": {
            "unconditional": ["Female", "Male", "Non-binary", "Other"],
            "locked": False
        },
        "Age": {
            "unconditional": ["10-15", "15-20", "20-30", "30-40", "40-60", "60+"],
            "locked": True
        },
        "Skills": {
            "unconditional": sorted(["Martial arts", "Aerobics", "Pilot", "Rock climbing", "Shooting", "Swimming", "Fencing", "Skateboarding", "Boxing", "Golf", "Tennis", "Cheerleading", "Surfing", "Trampoline"]),
            "locked": True
        },
        "Languages": {
            "unconditional": ["English", "Spanish", "French", "Mandarin", "Cantonese", "Japanese", "Arabic", "Russian", "German", "Thai", "Indigenous (N. America)", "Vietnamese", "Norwegian"],
            "locked": True
        },
        "Union status": {
            "unconditional": ["Union", "Non-union", "Other"],
            "locked": True
        }
    }
}