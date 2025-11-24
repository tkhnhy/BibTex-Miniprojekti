*** Settings ***
Resource  resource.robot
Library  OperatingSystem
Suite Setup  Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Pressing the download BibTex-file downloads a bib file.
    Go To  ${HOME_URL}
    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create
    Click Button  Download as BibTex-file

    Log To Console    Download dir: ${DOWNLOAD_DIR}
    Wait Until Keyword Succeeds    20x    2s

    ...    File Should Exist    ${DOWNLOAD_DIR}/*.bib
    ${files}=    List Files In Directory    ${DOWNLOAD_DIR}
    Log To Console    Files downloaded: ${files}
