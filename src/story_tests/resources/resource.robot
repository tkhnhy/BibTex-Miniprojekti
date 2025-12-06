*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}     localhost:5001
${DELAY}      0.1 seconds
${HOME_URL}   http://${SERVER}
${RESET_URL}  http://${SERVER}/reset_db
${BROWSER}    chrome
${HEADLESS}   false
${CREATE_URL}  http://${SERVER}/new_reference
${QUICK_ADD_URL}  http://${SERVER}/reference_for_storytest
${FILES_DIR}    ${EXECDIR}/src/story_tests/files

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

Reset References
    Go To  ${RESET_URL}

Quick Add Reference
    Go To  ${QUICK_ADD_URL}
    
Add Two References
    Go To  ${HOME_URL}

    Click Button  New reference
    Select From List By Label  reference_type  Book
    Input Text  reference_key  ROB01
    Input Text  author  Rob Bot
    Input Text  title  Robot Book
    Input Text  publisher  RobotPublishing
    Input Text  year  2150
    Click Button  Create

    Click Button  New reference
    Select From List By Label  reference_type  Article
    Input Text  reference_key  DR02
    Input Text  author  Anne Droid
    Input Text  title  Droid Article
    Input Text  journal  DroidJournal
    Input Text  year  2200
    Click Button  Create