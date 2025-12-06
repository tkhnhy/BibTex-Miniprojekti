*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Filtering shows only the selected reference type
    Go To  ${HOME_URL}

    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create

    Click Button  New reference
    Select From List By Label  reference_type  Article
    Input Text  reference_key  ROB02
    Input Text  author  Rob Bot
    Input Text  title  Robot Article
    Input Text  journal  RobotJournal
    Input Text  year  2150
    Click Button  Create

    Page Should Contain  ROB01
    Page Should Contain  ROB02

    Select Checkbox  book
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  ROB01
    Page Should Not Contain  ROB02

Clearing filters restores all references 
    Go To  ${HOME_URL}

    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create

    Select Checkbox  booklet
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  Number of references: 0
    
    Scroll Element Into View  btn-clear-filters
    Click Button  Clear Filters

    Page Should Contain  ROB01

*** Comments ***
Clearing filters failed once on CI. Runs well locally, so marking as comment for now. Committing and pushing to rerun CI.