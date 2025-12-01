*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Uploading a valid BibTeX file adds references
    Go To  ${HOME_URL}

    Choose File  id:fileInput  ${FILES_DIR}/test_references.bib

    Page Should Contain  Number of references: 2
    Page Should Contain  Artificial intelligence (AI) applications for marketing: A literature-based study
    Page Should Contain  A New Era in Alzheimer' s Research