class Reference:
    def __init__(self, id_, key_, type_, content_):
        self.id = id_
        self.reference_key = key_
        self.reference_type = type_
        #citation_content holds all relevant info in JSON format, later can make-
        #a function that checks based on reference_type required entry is included.
        self.reference_content = content_

    def __str__(self):
        return f"{self.reference_key}"
