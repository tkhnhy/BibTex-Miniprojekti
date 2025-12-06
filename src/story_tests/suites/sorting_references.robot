*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Sorting by year sorts the references in right order
    Go To  ${HOME_URL}

    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Input Text  tag-input  flagged
    Click Button  Add tag
    Click Button  Create

    Click Button  New reference
    Select From List By Label  reference_type  Article
    Input Text  reference_key  ROB02
    Input Text  author  Rob Bot
    Input Text  title  Robot Article
    Input Text  journal  RobotJournal
    Input Text  year  500
    Input Text  tag-input  reviewed
    Click Button  Add tag
    Click Button  Create

    Page Should Contain  ROB01
    Page Should Contain  ROB02

    Select From List By Label  sort_by  Year
    Scroll Element Into View    btn-apply-filters
    Click Button  Apply Filters

    ${first}=    Get Text    xpath=(//div[@class="reference-item"]/div[3])[1]
    ${second}=   Get Text    xpath=(//div[@class="reference-item"]/div[3])[2]

    Should Contain    ${first}    ROB02
    Should Contain    ${second}   ROB01