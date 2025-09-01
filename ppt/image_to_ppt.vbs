' PowerPoint Image Presentation Generator
' Creates a 17-slide presentation with images [1-17].jpg

Option Explicit

Dim pptApp, pptPres, slide
Dim i, imgPath, fso
Dim slideWidth, slideHeight
Dim imgWidth, imgHeight, imgLeft, imgTop

' Create file system object for file checking
Set fso = CreateObject("Scripting.FileSystemObject")

On Error Resume Next

' Create PowerPoint application object
Set pptApp = CreateObject("PowerPoint.Application")
If Err.Number <> 0 Then
    WScript.Echo "Error: Could not create PowerPoint application. Make sure PowerPoint is installed."
    WScript.Quit
End If

' Make PowerPoint visible
pptApp.Visible = True

' Add new presentation
Set pptPres = pptApp.Presentations.Add
If Err.Number <> 0 Then
    WScript.Echo "Error: Could not create new presentation."
    WScript.Quit
End If

' Get slide dimensions (standard 16:9 ratio)
slideWidth = pptPres.PageSetup.SlideWidth
slideHeight = pptPres.PageSetup.SlideHeight

WScript.Echo "Creating PowerPoint presentation with 17 slides..."

' Loop to create 17 slides with images
For i = 1 To 17
    ' Create new slide with blank layout
    Set slide = pptPres.Slides.Add(i, 12) ' 12 = ppLayoutBlank
    
    ' Build image file path
    imgPath = "C:\Users\NaRPaVi Enterprises\Downloads\" & i & ".jpg"
    
    ' Check if image file exists
    If fso.FileExists(imgPath) Then
        ' Clear any previous errors
        Err.Clear
        
        ' Set image as slide background
        slide.FollowMasterBackground = False
        slide.Background.Fill.UserPicture imgPath
        
        WScript.Echo "Added slide " & i & " with background image: " & i & ".jpg"
    Else
        WScript.Echo "Warning: Image file not found: " & imgPath
        ' Still create the slide but add a text placeholder indicating missing background
        slide.Shapes.AddTextbox 1, 100, 100, 400, 100
        slide.Shapes(slide.Shapes.Count).TextFrame.TextRange.Text = "Background image " & i & ".jpg not found"
    End If
Next

' Optional: Save the presentation
' Uncomment the lines below to automatically save
' Dim savePath
' savePath = "C:\Users\NaRPaVi Enterprises\Downloads\ImagePresentation.pptx"
' pptPres.SaveAs savePath

WScript.Echo "Presentation created successfully with " & pptPres.Slides.Count & " slides!"
WScript.Echo "You can now save the presentation manually or uncomment the save lines in the script."

' Clean up objects
Set slide = Nothing
Set pptPres = Nothing
Set pptApp = Nothing
Set fso = Nothing

On Error GoTo 0