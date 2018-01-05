%% Resizing Videos - For Habituation Days
tic;

searchDir = '/Volumes/HD_Krista/MouseReaching/SkilledReaching_Winter2018/ReachingVideos/';

% Use this if you want to only search through folders after a specific date
% (dates are the names of the folders in YYYYMMDD format)

startDate = 'NONE'; % IF YOU DON'T WANT TO USE THIS, SET TO 'NONE'. Othewise the formate is YYYYMMDD

mainDir = dir(searchDir);
mainDirSubfolders = repmat({''},1);
mainFolderInd = 1;

for mainInd = 1:length(mainDir)
    
   if mainDir(mainInd).isdir == 1 && length(mainDir(mainInd).name) > 2
       mainDirSubfolders{mainFolderInd,1} = mainDir(mainInd).name;
       mainFolderInd = mainFolderInd + 1;
   end
   
end

if strcmp(startDate,'NONE') == 0
    startInd = find(contains(mainDirSubfolders,startDate));
else
    startInd = 1;
end

for subfolderInd = startInd:length(mainDirSubfolders)
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
                
        for fileInd = 1:length(files)
            
            filenameExt = files(fileInd).name;
            filename = filenameExt(1:end-4);
            videoNum = filename(end-2:end);
            
            inVideo = VideoReader([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/' filenameExt]);
            outVideo = VideoWriter([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/' filename '_s.mp4']);
            mkdir([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/Reaches_' videoNum])
            
            reachNum = 0;
            lightOn = 0;
            trialTime = 40;
            i = 1;
            thresh = 500;

            frameRate = inVideo.FrameRate;
            totalFrames = inVideo.Duration*frameRate;

            reaches = zeros(100,3);

            outVideo.Quality = 50;
            outVideo.FrameRate = frameRate;
            open(outVideo);
            
             while i <= totalFrames
                 
                 image = read(inVideo, i);
                 
                 % resize
                 imageResized = imresize(image, 0.5);
                 
                 % write image
                 resized_frame = im2frame(imageResized);
                 writeVideo(outVideo, resized_frame);
                 
             end
             
             close(outVideo);
             
        end
    end
   
end
toc;