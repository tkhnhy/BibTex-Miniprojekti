*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
At start there are no references
    Go To  ${HOME_URL}
    Title Should Be  reference app
    Page Should Contain  Number of references: 0

After adding a reference, there is one
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  book_title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create
    Page Should Contain  ROB01
    Page Should Contain  Number of references: 1
    
After adding a reference, then removing it, there are no references
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB02
    Input Text  author  Rob Bot
    Input Text  book_title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create
    Page Should Contain  ROB02
    Page Should Contain  Number of references: 1
    Click Button  Delete
    Click Button  Delete
    Page Should Contain  Number of references: 0
    
After adding a reference, pressing delete, but canceling, the reference stays
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB03
    Input Text  author  Rob Bot
    Input Text  book_title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create
    Page Should Contain  ROB03
    Page Should Contain  Number of references: 1
    Click Button  Delete
    Click Button  Cancel
    Page Should Contain  Number of references: 1