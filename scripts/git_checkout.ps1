# Copyright 2019 Google LLC

# Licensed under the the Apache License v2.0 with LLVM Exceptions (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     https://llvm.org/LICENSE.txt

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

. ${PSScriptRoot}\common.ps1

#Set-PSDebug -Trace 1

# Wrap git commant in error handling function
function Invoke-Git($cmd) {
    Invoke-Call -ScriptBlock { git @cmd } -ErrorAction Stop
}

if (Test-Path -PathType Container "llvm-project"){
    Set-Location llvm-project
    Write-Output "performing git pull..."
    $branch = (git branch) | Out-String
    $branch = ($branch -split '\r')[0]
    if ($branch -ne "* master"){
        Invoke-Call -ScriptBlock { git checkout master} -ErrorAction Stop
    }
    Invoke-Call -ScriptBlock { git reset --hard } -ErrorAction Stop
    Invoke-Call -ScriptBlock { git clean -fdx } -ErrorAction Stop
    Invoke-Call -ScriptBlock { git pull } -ErrorAction Stop
    # TODO: in case of errors: delete folder and clone
} else {
    Write-Output "performing git clone..."
    Invoke-Call -ScriptBlock { git clone -q --depth 1 https://github.com/llvm/llvm-project } -ErrorAction Stop
}