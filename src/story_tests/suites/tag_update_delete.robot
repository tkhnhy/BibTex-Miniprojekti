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

*** Test Cases ***
Manage tags button opens the managing panel
    Go To  ${HOME_URL}
    Page Should Contain  Manage tags

    Click Button  New reference
    Input Book With Fields  ROB05  Rob Bot  Robot Book  RobotPublishing  2150
    Input Tag  abc
    Input Tag  def
    Click Button  Create

    Click Button  Manage tags
    Textfield Value Should Be  new_tag_name_abc  abc
    Textfield Value Should Be  new_tag_name_def  def

Renaming tags works correctly
    Go To  ${HOME_URL}
    Page Should Contain  Manage tags

    Click Button  New reference
    Input Book With Fields  ROB05  Rob Bot  Robot Book  RobotPublishing  2150
    Input Tag  abc
    Input Tag  def
    Click Button  Create

    Click Button  Manage tags
    Input Text  new_tag_name_abc  xyz
    Click Button  Apply edit
    Click Button  To main page
    
    Click Button  Details
    Page Should Contain  xyz
    Page Should Not Contain  abc

Deleting tags works correctly
    Go To  ${HOME_URL}
    Page Should Contain  Manage tags

    Click Button  New reference
    Input Book With Fields  ROB05  Rob Bot  Robot Book  RobotPublishing  2150
    Input Tag  abc
    Input Tag  def
    Click Button  Create

    Click Button  Manage tags

    # intercept confirm: save message and RETURN FALSE so navigation is blocked
    Execute JavaScript    window.__last_confirm = null; window._orig_confirm = window.confirm; window.confirm = function(msg){ window.__last_confirm = msg; return false; };

    Click Button  delete_tag_def

    # read the captured confirm text
    ${confirm_msg}=    Execute JavaScript    return window.__last_confirm;
    Should Contain    ${confirm_msg}    Delete tag

    # restore original confirm and submit the form
    Execute JavaScript    if(window._orig_confirm){ window.confirm = window._orig_confirm; delete window._orig_confirm; }
    Execute JavaScript    document.querySelector('.delete-tag-form[data-tag="def"]').submit();

    Click Button  To main page
    Click Button  Details
    Page Should Contain  abc
    Page Should Not Contain  def

*** Comments ***
# Additional manual tag add/remove tests commented out...



