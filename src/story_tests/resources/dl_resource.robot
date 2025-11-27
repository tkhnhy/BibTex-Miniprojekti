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
${QUICK_ADD_URL}  http://${SERVER}/reference_for_storytest
${DOWNLOAD_DIR}    ${OUTPUT DIR}${/}downloads

*** Keywords ***
Open And Configure Download Browser
    Create Directory  ${DOWNLOAD_DIR}
       
    IF  $BROWSER == 'chrome'
        ${prefs}    Create Dictionary
        ...    download.default_directory=${DOWNLOAD_DIR}
        ...    download.prompt_for_download=${false}
        ...    download.directory_upgrade=${true}
        ...    safebrowsing.enabled=${true}
        ${options}    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
        Call Method    ${options}    add_experimental_option    prefs    ${prefs}
    ELSE IF  $BROWSER == 'firefox'
        ${options}    Evaluate    sys.modules['selenium.webdriver'].FirefoxOptions()    sys, selenium.webdriver

        Call Method    ${options}    set_preference    browser.download.folderList    2
        Call Method    ${options}    set_preference    browser.download.dir    ${DOWNLOAD_DIR}
        Call Method    ${options}    set_preference    browser.download.useDownloadDir    True
        Call Method    ${options}    set_preference    browser.helperApps.neverAsk.saveToDisk    application/pdf,application/octet-stream,application/vnd.ms-excel,application/zip,application/x-bibtex
        Call Method    ${options}    set_preference    browser.download.manager.showWhenStarting    false

    END
    IF  $HEADLESS == 'true'
        Set Selenium Speed  0.01 seconds
        IF  $BROWSER == 'chrome'
            ${headless_args}    Create List    --headless=new
            ${download_feature}    Create List    --enable-features=AllowFileDownloadsInHeadless
            Call Method    ${options}    add_argument    @{headless_args}
            Call Method    ${options}    add_argument    @{download_feature}
        ELSE IF    $BROWSER == 'firefox'
            Call Method    ${options}    add_argument    -headless
            Call Method    ${options}    set_preference    browser.helperApps.neverAsk.saveToDisk    text/csv,application/octet-stream,application/json,application/x-bibtex
            Call Method    ${options}    set_preference    browser.download.forbid_open_with    true
        END
    ELSE
        Set Selenium Speed  ${DELAY}
    END
    Open Browser  browser=${BROWSER}  options=${options}

Reset References
    Go To  ${RESET_URL}

Quick Add Reference
    Go To  ${QUICK_ADD_URL}