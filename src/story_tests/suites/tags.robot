*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Keywords ***
Input Book With Fields
    [Arguments]    ${key}    ${author}    ${title}    ${publisher}    ${year}
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ${key}
    Input Text  author  ${author}
    Input Text  title  ${title}
    Input Text  publisher  ${publisher}
    Input Text  year  ${year}

Input Tag
    [Arguments]    ${tag}
    Input Text  tag-input  ${tag}
    Click Button  Add tag

Remove Tag
    Click Element  css:.remove-tag-btn

*** Test Cases ***
Add Tags On New Reference Form
    Go To  ${HOME_URL}
    Click Button  New reference
    Input Book With Fields  ROB05  Rob Bot  Robot Book  RobotPublishing  2150
    Input Tag  abc
    Page Should Contain  abc
    Remove Tag
    Page Should Not Contain  abc
    Input Tag  abc
    Click Button  Create

    Page Should Contain  ROB05
    Click Button  Details
    Page Should Contain  abc

Add And Remove Tags On Edit Form
    Go To  ${HOME_URL}
    Click Button  New reference

    Input Book With Fields  ROB06  Rob Bot  Robot Book  RobotPublishing  2150
    Input Tag  InitialTag
    Click Button  Create
    Page Should Contain  ROB06

    # Add a new tag
    Click Button  Edit
    Input Tag  NewTag
    Click Button  Save changes

    Page Should Contain  ROB06
    Click Button  Details
    Page Should Contain  InitialTag
    Page Should Contain  NewTag

    # Remove the tags
    Click Button  Edit
    Remove Tag
    Remove Tag
    Click Button  Save changes

    Page Should Contain  ROB06
    Click Button  Details
    Page Should Not Contain  NewTag
    Page Should Not Contain  InitialTag
    


