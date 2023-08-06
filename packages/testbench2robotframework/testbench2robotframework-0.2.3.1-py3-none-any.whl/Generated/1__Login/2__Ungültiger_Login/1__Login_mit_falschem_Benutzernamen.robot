*** Settings ***
Variables    myVars.py
Library    Remote    http://127.0.0.1:8270       WITH NAME    SuperRemoteLibrary
Library    SeleniumLibrary    timeout=10    implicit_wait=1    run_on_failure=Capture Page Screenshot
Resource    ..${/}..${/}..${/}Resources${/}technical_keywords.resource.resource
# UNKNOWN    SeleniumLibrary
Metadata    UniqueID    itba-TC-804
Metadata    Name    Login mit falschem Benutzernamen
Metadata    Numbering    1.2.1
Force Tags    Smoke    TextfeldTfs:lö    WerteListetTfs:Wert_1    AnkreufeldTfs


*** Test Cases ***
itba-TC-804-PC-2627
    [Tags]    Smoke    RfTag:
    SeleniumLibrary.Close Browser



