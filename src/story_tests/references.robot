*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
At start there are no references
    Go To  ${HOME_URL}
    Title Should Be  My references
    Page Should Contain  Number of references: 0

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
    
After adding a reference, then removing it, there are no references
    Go To  ${HOME_URL}
    Quick Add Reference
    Page Should Contain  Number of references: 1
    Click Button  Delete
    Click Button  Delete
    Page Should Contain  Number of references: 0
    
After adding a reference, pressing delete, but canceling, the reference stays
    Go To  ${HOME_URL}
    Quick Add Reference
    Page Should Contain  Number of references: 1
    Click Button  Delete
    Click Button  Cancel
    Page Should Contain  Number of references: 1

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

A comment can be added to a reference
    Go To  ${HOME_URL}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB05
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Input Text  comment  Test comment here
    Click Button  Create
    Page Should Contain  ROB05
    Click Button  Details
    Page Should Contain  Test comment here

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
