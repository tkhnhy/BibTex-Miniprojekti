*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Filtering shows only the selected tag type
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
    Input Text  year  2150
    Input Text  tag-input  reviewed
    Click Button  Add tag
    Click Button  Create

    Page Should Contain  ROB01
    Page Should Contain  ROB02

    Execute Javascript    document.querySelectorAll('.tooltiptext').forEach(e => e.style.display = 'none');

    Wait Until Element Is Visible  xpath=//input[@value='reviewed']  timeout=5s
    Select Checkbox  reviewed
    Wait Until Element Is Visible  id=btn-apply-filters  timeout=5s
    Scroll Element Into View  id=btn-apply-filters
    Click Element  id=btn-apply-filters

    Page Should Contain  ROB02
    Page Should Not Contain  ROB01

Clearing filters restores all references 
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
    Input Text  year  2150
    Input Text  tag-input  reviewed
    Click Button  Add tag
    Click Button  Create

    Page Should Contain  ROB01
    Page Should Contain  ROB02

    Execute Javascript    document.querySelectorAll('.tooltiptext').forEach(e => e.style.display = 'none');

    Wait Until Element Is Visible  xpath=//input[@value='reviewed']  timeout=5s
    Select Checkbox  reviewed
    Wait Until Element Is Visible  id=btn-apply-filters  timeout=5s
    Scroll Element Into View  id=btn-apply-filters
    Click Element  id=btn-apply-filters

    Page Should Contain  ROB02
    Page Should Not Contain  ROB01

    Wait Until Element Is Visible  id=btn-clear-filters  timeout=5s
    Scroll Element Into View  id=btn-clear-filters
    Click Element  id=btn-clear-filters

    Page Should Contain  ROB01
    Page Should Contain  ROB02


*** Comments ***
CI failed for no reason, trying again.