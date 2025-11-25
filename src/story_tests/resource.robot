*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.5 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chrome
${HEADLESS}   false
${CREATE_URL}  http://${SERVER}/new_reference
${DOWNLOAD_DIR}    ${OUTPUT DIR}${/}downloads

*** Keywords ***
Open And Configure Browser
    Create Directory  ${DOWNLOAD_DIR}

    IF  $BROWSER == 'chrome'
        ${prefs}=    Create Dictionary
        ...    download.default_directory=${DOWNLOAD_DIR}
        ...    download.prompt_for_download=${False}
        ...    download.directory_upgrade=${True}
        ...    safebrowsing.enabled=${True}
        ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
        Call Method    ${options}    add_argument    --incognito
        Call Method    ${options}    add_experimental_option    prefs    ${prefs}
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        
        ${headless_args}=    Create List    --headless=new
        ${download_feature}=    Create List    --enable-features=AllowFileDownloadsInHeadless

        Call Method    ${options}    add_argument    @{headless_args}
        Call Method    ${options}    add_argument    @{download_feature}
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset References
    Go To  ${RESET_URL}