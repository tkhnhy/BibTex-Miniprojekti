class Citation:
    def __init__(self, id,citation_key, citation_type, citation_content):
        self.id = id
        self.citation_key = citation_key
        self.citation_type = citation_type
        #citation_content holds all relevant info in JSON format, later can make-
        #a function that checks based on citation_type required entry is included.
        self.citation_content = citation_content

    def __str__(self):
        #is_done = "done" if self.done else "not done"
        return f"{self.citation_key}"
