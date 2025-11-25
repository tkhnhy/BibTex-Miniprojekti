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
    IF  $BROWSER == 'chrome'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].ChromeOptions()  sys
        Call Method  ${options}  add_argument  --incognito
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        Call Method  ${options}  add_argument  --headless
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Open And Configure Download Browser
    Create Directory  ${DOWNLOAD_DIR}
    
    ${running_in_ci}=    Get Environment Variable    GITHUB_ACTIONS    default=False
    
    IF  $BROWSER == 'chrome'
        ${prefs}=    Create Dictionary
        ...    download.default_directory=${DOWNLOAD_DIR}
        ...    download.prompt_for_download=${False}
        ...    download.directory_upgrade=${True}
        ...    safebrowsing.enabled=${True}
        ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
        Call Method    ${options}    add_experimental_option    prefs    ${prefs}
        IF    '${running_in_ci}' != 'true'
            Call Method    ${options}    add_argument    --incognito
        END
    ELSE IF  $BROWSER == 'firefox'
        ${options}  Evaluate  sys.modules['selenium.webdriver'].FirefoxOptions()  sys
        Call Method  ${options}  add_argument  --private-window
    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        IF  $BROWSER == 'chrome'
            ${headless_args}=    Create List    --headless=new
            ${download_feature}=    Create List    --enable-features=AllowFileDownloadsInHeadless
            Call Method    ${options}    add_argument    @{headless_args}
            Call Method    ${options}    add_argument    @{download_feature}
        ELSE IF    $BROWSER == 'firefox'
            Call Method    ${options}    add_argument    -headless
        END
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset References
    Go To  ${RESET_URL}

