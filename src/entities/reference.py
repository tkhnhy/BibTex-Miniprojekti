class Reference:
    def __init__(self, id, reference_key, reference_type, reference_content):
        self.id = id
        self.reference_key = reference_key
        self.reference_type = reference_type
        #citation_content holds all relevant info in JSON format, later can make-
        #a function that checks based on reference_type required entry is included.
        self.reference_content = reference_content

    def __str__(self):
        return f"{self.reference_key}"
