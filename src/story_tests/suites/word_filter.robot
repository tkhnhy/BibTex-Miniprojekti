*** Settings ***
Resource         ../resources/resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset References

*** Test Cases ***
Filtering by word and any field shows only the references containing the word
    Add Two References

    Page Should Contain  ROB01
    Page Should Contain  DR02

    Input Text  keyword_value  Rob
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  ROB01
    Page Should Not Contain  DR02

Filtering by author gives only the reference containing the searchword in author field 
    Add Two References

    Click Button  New reference
    Select From List By Label  reference_type  Article
    Input Text  reference_key  ROB03
    Input Text  author  Rob Bot
    Input Text  title  Anne
    Input Text  journal  RobotJournal
    Input Text  year  2150
    Click Button  Create

    Wait Until Element Is Visible  name=keyword_field  timeout=5s
    Select From List By Label  keyword_field  Author
    Input Text  keyword_value  Anne
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  DR02
    Page Should Not Contain  ROB03
    Page Should Not Contain  ROB01

Filtering by year only returns only the approriate references
    Add Two References
    Wait Until Element Is Visible  name=keyword_field  timeout=5s
    Select From List By Label  keyword_field  Year
    Input Text  keyword_value  2150
    
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  ROB01
    Page Should Not Contain  DR02
    
Filtering by year, different modifiers work
    Add Two References
    
    Wait Until Element Is Visible  name=keyword_field  timeout=5s
    Select From List By Label  keyword_field  Year
    Input Text  keyword_value  <2200
    
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  ROB01
    Page Should Not Contain  DR02
    
    Scroll Element Into View  btn-clear-filters
    Click Button  Clear Filters
    
    
    Wait Until Element Is Visible  name=keyword_field  timeout=5s
    Select From List By Label  keyword_field  Year
    Input Text  keyword_value  >2150
    
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters
    
    Page Should Not Contain  ROB01
    Page Should Contain  DR02
    
    Scroll Element Into View  btn-clear-filters
    Click Button  Clear Filters
    
    
    Wait Until Element Is Visible  name=keyword_field  timeout=5s
    Select From List By Label  keyword_field  Year
    Input Text  keyword_value  2000-2199
    
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters
    
    Page Should Contain  ROB01
    Page Should Not Contain  DR02

Searching a specific title works
    Add Two References

    Wait Until Element Is Visible  name=keyword_field  timeout=5s
    Select From List By Label  keyword_field  Title
    Input Text  keyword_value  Robot
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  ROB01
    Page Should Not Contain  DR02
    
Searching a specific a partial key works
    Add Two References

    Wait Until Element Is Visible  name=keyword_field  timeout=5s
    Select From List By Label  keyword_field  Key
    Input Text  keyword_value  ROB
    Scroll Element Into View  btn-apply-filters
    Click Button  Apply Filters

    Page Should Contain  ROB01
    Page Should Not Contain  DR02