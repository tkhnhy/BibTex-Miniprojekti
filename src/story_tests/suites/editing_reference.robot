*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
After adding a reference, editing it, the data is changed
    Go To  ${HOME_URL}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB04
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create
    Page Should Contain  ROB04
    Click Button  Edit
    Select From List By Label  reference_type  Article
    Input Text  author  Robert Botman
    Input Text  journal  Goodjournal
    Click Button  Save changes
    Page Should Contain  Robert Botman
    Page Should Not Contain  Rob Bot
    Page Should Contain  Article