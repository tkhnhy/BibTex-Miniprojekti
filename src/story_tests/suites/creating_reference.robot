*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
After adding a reference, there is one
    Go To  ${HOME_URL}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create
    Page Should Contain  ROB01
    Page Should Contain  Number of references: 1

Creating a reference does not proceed, when a required field is empty
    Go To  ${HOME_URL}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Click Button  Create
    Location Should Be  ${CREATE_URL}

After adding a reference, then adding another with same key, adding fails
    Go To  ${HOME_URL}
    Quick Add Reference
    Page Should Contain  Number of references: 1
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROBSTORY01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create
    Location Should Be  ${CREATE_URL}
    Go To  ${HOME_URL}
    Page Should Contain  Number of references: 1

After filling reference fields, but canceling, none are created.
    Go To  ${HOME_URL}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Cancel
    Page Should Contain  Number of references: 0

Adding reference with unfilled alternative required fields fails
    Go To  ${HOME_URL}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  BK02
    Input Text  title  Missing Author and Editor
    Input Text  publisher  pub
    Input Text  year  1001
    Click Button  Create
    Location Should Be  ${CREATE_URL}