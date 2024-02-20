# submit-tool
Tool used to copy files from local host to another host / server within a local network, with same folder structure.

## Procedure
Set the project root folder in the destination side (Server) and the local root folder. This folders should contain the same folder structure to work properly.
![](./doc_imgs/mainUI_setLocations.png)

This step is only required once, the settings are stored under your user folder in your system.
You can always use the Settings menu to reset the root folders.

When you click either "Server project root folder" or "Local project root folder" a browse window is displayed to select your directory.
![](/doc_imgs/browser.png)

Once you select both locations the "OK" enables.
![](/doc_imgs/set_locations.png)


A pop up message will show up when "OK" button is pressed.
![](/doc_imgs/settings_confirmation.png)

This action creates a config json file under your user.


As all is set you can now drag and drop some files from your explorer to the tool/interface.
![](/doc_imgs/drag_and_drop.png)


And this is how it looks once you draged some files.
![](/doc_imgs/submit_files.png)


If files or folder comes from a diferent path than the one defined in first step, then your file or folder will be highlighted red to visually warn you about this issue.
![](/doc_imgs/red_warning1.png)


If you continue adding files and there is at least one coming from your local root path then the submit button will be enabled but only this valid file will be processed.
![](/doc_imgs/red_warning2.png)


When clicking submit the files will be copied to the destination root folder (server).
Depending of the file size it will take some time, once finished you should see a confirmation message.
![](/doc_imgs/submit_confirmation1.png)


There is also a terminal window where it will log some info confirming it is working.
![](/doc_imgs/submit_files_log.png)

## TODO
- Add functionality to submit files from diferent location but target an specific step/task.

## IMPORTANT
There is also an executable for this tool under "executable" folder, you can download and use it under windows.

