on run argv
    set sourcePath to item 1 of argv
    set targetPath to item 2 of argv
    with timeout of 40 seconds
        tell application "Microsoft PowerPoint"
            open POSIX file sourcePath
            set probePresentation to active presentation
            if name of probePresentation is not item 3 of argv then error "Unexpected active presentation; refusing export"
            save probePresentation in POSIX file targetPath as save as PDF
        end tell
    end timeout
end run
