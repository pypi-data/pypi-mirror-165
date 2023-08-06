*** Settings ***
Variables    myVars.py
Library    Remote    http://127.0.0.1:8270       WITH NAME    SuperRemoteLibrary
Library    SeleniumLibrary    timeout=10    implicit_wait=1    run_on_failure=Capture Page Screenshot
Resource    ..${/}..${/}..${/}Resources${/}technical_keywords.resource.resource
# UNKNOWN    SeleniumLibrary
Metadata    UniqueID    itba-TC-800
Metadata    Name    Login mit korrekten Benutzerdaten
Metadata    Numbering    1.1.1
Force Tags    Smoke    TextfeldTfs:l    WerteListetTfs:Wert_2    AnkreufeldTfs


*** Test Cases ***
itba-TC-800-PC-2621
    [Tags]    Smoke    RfTag:
    SeleniumLibrary.Close Browser



