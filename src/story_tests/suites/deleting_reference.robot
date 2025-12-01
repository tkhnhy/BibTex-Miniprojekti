*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
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