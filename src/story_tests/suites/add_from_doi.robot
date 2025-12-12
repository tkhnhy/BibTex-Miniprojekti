*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Add from doi
    Go To  ${HOME_URL}
    Click Button  New reference
    Input Text  doi-input  https://dl.acm.org/doi/10.1145/3746175.3746187
    Click Button  Fetch
    Sleep    5s
    Click Button  Create
    Page Should Contain  Mets, Juri and Hooshyar, Danial and Bauters, Merja
