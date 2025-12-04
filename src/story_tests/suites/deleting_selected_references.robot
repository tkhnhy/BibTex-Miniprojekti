*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Keywords ***
Add Book Reference
    [Arguments]    ${key}    ${author}    ${title}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ${key}
    Input Text  author  ${author}
    Input Text  title  ${title}
    Input Text  publisher  Publisher
    Input Text  year  2024
    Click Button  Create

*** Test Cases ***
Delete selected button is disabled when no references are selected
    Go To  ${HOME_URL}
    Add Book Reference  REF01  Author One  Title One
    Element Should Be Disabled  id=delete-selected-btn

Delete selected button is enabled when a reference is selected
    Go To  ${HOME_URL}
    Add Book Reference  REF01  Author One  Title One
    Select Checkbox  xpath=//input[@data-key="REF01"]
    Element Should Be Enabled  id=delete-selected-btn

Selecting multiple references and deleting them removes all selected
    Go To  ${HOME_URL}
    Add Book Reference  REF01  Author One  Title One
    Add Book Reference  REF02  Author Two  Title Two
    Add Book Reference  REF03  Author Three  Title Three
    
    Page Should Contain  Number of references: 3
    
    Select Checkbox  xpath=//input[@data-key="REF01"]
    Select Checkbox  xpath=//input[@data-key="REF03"]
    Click Button  id=delete-selected-btn
    
    Page Should Contain  Are you sure you want to delete the following 2 reference(s)?
    Page Should Contain  REF01
    Page Should Contain  REF03
    Page Should Not Contain  REF02
    
    Click Button  Delete
    
    Page Should Contain  Number of references: 1
    Page Should Contain  REF02
    Page Should Not Contain  REF01
    Page Should Not Contain  REF03

Canceling delete selected keeps all references
    Go To  ${HOME_URL}
    Add Book Reference  REF01  Author One  Title One
    Add Book Reference  REF02  Author Two  Title Two
    
    Page Should Contain  Number of references: 2
    
    Select Checkbox  xpath=//input[@data-key="REF01"]
    Select Checkbox  xpath=//input[@data-key="REF02"]
    Click Button  id=delete-selected-btn
    
    Page Should Contain  Are you sure you want to delete the following 2 reference(s)?
    
    Click Button  Cancel
    
    Page Should Contain  Number of references: 2
    Page Should Contain  REF01
    Page Should Contain  REF02

Select all checkbox selects all references for deletion
    Go To  ${HOME_URL}
    Add Book Reference  REF01  Author One  Title One
    Add Book Reference  REF02  Author Two  Title Two
    Add Book Reference  REF03  Author Three  Title Three
    
    Page Should Contain  Number of references: 3
    
    Select Checkbox  id=select-all
    Click Button  id=delete-selected-btn
    
    Page Should Contain  Are you sure you want to delete the following 3 reference(s)?
    
    Click Button  Delete
    
    Page Should Contain  Number of references: 0
