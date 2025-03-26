function moveImagesToSharedFolder() {
    var folderId = "1qof1gtNh5DuAs0X_5beR3r7QCrpdr1FS";  // הכנס כאן את מזהה התיקייה השיתופית
    var sharedFolder = DriveApp.getFolderById(folderId);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    var data = sheet.getDataRange().getValues();
    
    // עבר על כל השורות (נניח שהכותרת בשורה הראשונה)
    for (var i = 1; i < data.length; i++) {
        // עמודה 4 או 5 או כל עמודה ששם יש קישורים לתמונות
        var imageUrls = data[i][22];  // עמודה שבה יש את הקישורים לתמונות (תוכל לשנות את המיקום כאן)
        
        // אם יש קישורים לתמונות
        if (imageUrls && imageUrls.trim() !== "") {
            // נניח שהקישורים נמצאים כ-URLים מופרדים בפסיק
            var urls = imageUrls.split(",");  // במקרה שיש כמה תמונות בקישור
            
            for (var j = 0; j < urls.length; j++) {
                var imageUrl = urls[j].trim();
                
                // הדפסת ה-URL שנמצא בתא
                Logger.log("Processing URL: " + imageUrl);
                
                // אם הקישור הוא קישור תקני מ-Drive
                if (imageUrl.includes("drive.google.com")) {
                    try {
                        var fileId;
                        
                        // בדיקה אם הקישור בצורת "open?id=<fileId>"
                        if (imageUrl.includes("open?id=")) {
                            fileId = imageUrl.split("open?id=")[1];
                        } 
                        // או אם הקישור בצורת "file/d/<fileId>/view"
                        else if (imageUrl.includes("file/d/")) {
                            fileId = imageUrl.split("/d/")[1].split("/")[0];
                        }
                        
                        // הדפסת ה-`fileId` שנמצא
                        Logger.log("Extracted fileId: " + fileId);
                        
                        // לוודא שה- fileId תקין לפני שנבצע את הפעולה
                        if (fileId) {
                            var file = DriveApp.getFileById(fileId);
                            
                            // בדיקה אם הקובץ כבר נמצא בתיקייה
                            var filesInFolder = sharedFolder.getFilesByName(file.getName());
                            if (!filesInFolder.hasNext()) {  // אם אין קובץ עם אותו שם בתיקייה
                                file.moveTo(sharedFolder);
                                Logger.log("Moved file: " + fileId);
                            } else {
                                Logger.log("File already exists in the shared folder: " + fileId);
                            }
                        } else {
                            Logger.log("Invalid fileId in URL: " + imageUrl);
                        }
                    } catch (e) {
                        Logger.log("Error moving file: " + imageUrl + " - " + e.toString());
                    }
                } else {
                    Logger.log("Invalid URL (not a Google Drive URL): " + imageUrl);
                }
            }
        } else {
            Logger.log("No valid image URL found in row " + (i + 1));
        }
    }
}

