%% File Search
% The purpose of this code is to search through all of the folders in a
% directory, identify all subfolders, then identify all files. 

searchDir = '/Volumes/HD_Krista/MouseReaching/AutoReaching_TestGroup/ReachingVideos_Date/';

% Use this if you want to only search through folders after a specific date
% (dates are the names of the folders in YYYYMMDD format)
startDate = '';

mainDir = dir(searchDir);
mainDirSubfolders = repmat({''},1);
mainFolderInd = 1;

for mainInd = 1:length(mainDir)
    
   if mainDir(mainInd).isdir == 1 && length(mainDir(mainInd).name) > 2
       mainDirSubfolders{mainFolderInd,1} = mainDir(mainInd).name;
       mainFolderInd = mainFolderInd + 1;
   end
   
end


for subfolderInd = 1:length(mainDirSubfolders)
    folderDir = dir([searchDir mainDirSubfolders{subfolderInd,1}]);
    folderDirSubfolders = repmat({''},1);
    folderSubfolderInd = 1;

    for folderInd = 1:length(folderDir)

        if folderDir(folderInd).isdir == 1 && length(folderDir(folderInd).name) > 2
            folderDirSubfolders{folderSubfolderInd,1} = folderDir(folderInd).name;
            folderSubfolderInd = folderSubfolderInd + 1;
        end
    end
    
    for subsubfolderInd = 1:length(folderDirSubfolders)
        files = dir([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/*mp4']);
        
        %% Put what you want to do for each file here
        % Individual files cann be found using files.name
    end
        

end
