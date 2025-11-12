*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Todos

*** Test Cases ***
At start there are no todos
    Go To  ${HOME_URL}
    Title Should Be  reference app
    Page Should Contain  things still unfinished: 0

After adding a citation, there is one
    Go To  ${HOME_URL}
    Click Link  Create new reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  BA441
    Click Button  Create
    Page Should Contain  BA441