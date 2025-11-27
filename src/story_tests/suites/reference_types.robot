*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Adding multiple different reference types with their required fields succeeds
    Go To  ${HOME_URL}

    # Article
    Click Button  New reference
    Select From List By Label  reference_type  Article
    Input Text  reference_key  ART01
    Input Text  author  Alice Author
    Input Text  title  An Article
    Input Text  journal  ...
    Input Text  year  2025
    Click Button  Create
    Page Should Contain  ART01
    
    # Book (author OR editor allowed)
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  BK01
    Input Text  author  bob
    Input Text  title  The Book
    Input Text  publisher  PubHouse
    Input Text  year  2019
    Click Button  Create
    Page Should Contain  BK01

    # In Book (chapter OR pages allowed)
    Click Button  New reference
    Select From List By Label  reference_type  In Book
    Input Text  reference_key  IB01
    Input Text  author  Irene Inbook
    Input Text  title  In Book Title
    Input Text  booktitle  works
    Input Text  pages  13-42
    Input Text  publisher  art
    Input Text  year  2018
    Click Button  Create
    Page Should Contain  IB01

    # Techreport
    Click Button  New reference
    Select From List By Label  reference_type  Tech Report
    Input Text  reference_key  TR01
    Input Text  author  Tech
    Input Text  title  Tech Report Title
    Input Text  institution  hy
    Input Text  year  2020
    Click Button  Create
    Page Should Contain  TR01

    Page Should Contain  Number of references: 4