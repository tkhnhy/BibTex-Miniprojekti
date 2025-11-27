*** Settings ***
Resource         ../resources/dl_resource.robot
Suite Setup      Open And Configure Download Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Pressing the download BibTeX-file downloads a bib file.
    Go To  ${HOME_URL}
    Quick Add Reference
    Click Element  id=download-btn

    Log To Console    Download dir: ${DOWNLOAD_DIR}
    Wait Until Keyword Succeeds    30x    1s
    ...    File Should Exist    ${DOWNLOAD_DIR}/*.bib
    ${files}=    List Files In Directory    ${DOWNLOAD_DIR}
    Log To Console    Files downloaded: ${files}