%% Complete Processing

searchDir = '/Volumes/HD_Krista/MouseReaching/SkilledReaching_Winter2018/ReachingVideos/';

% Use this if you want to only search through folders after a specific date
% (dates are the names of the folders in YYYYMMDD format)

startDate = '20180108'; % IF YOU DON'T WANT TO USE THIS, SET TO 'NONE'

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
            
            disp([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/' filenameExt, ' start']);
            
            inVideo = VideoReader([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/' filenameExt]);
            outVideo = VideoWriter([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/' filename '_s.mp4'],'MPEG-4');
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
            
             while i < totalFrames
                 
                 image = read(inVideo, i);
                 
                 % resize
                 imageResized = imresize(image, 0.5);
                 
                 bwVidFrame = rgb2gray(imageResized);
                 binaryFrame = bwVidFrame >= 200;
                 whitePix = sum(sum(binaryFrame(295:295+245,1:1+200)));
                 
                 if whitePix >= thresh && lightOn == 0
                     
                     lightOn = 1; % Declare that the light is on
                     reachNum = reachNum + 1; % Define the reach number
                     reaches(reachNum,1) = reachNum; % Save reach number
                     reaches(reachNum,2) = i*(1/frameRate); % Save "time on" of LED
                     i = i + floor(trialTime * frameRate);
                     
                     reachNumChar = num2str(reachNum);
                     reachVideo = VideoWriter([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/Reaches_' videoNum '/' filename '_s_' reachNum '.mp4'],'MPEG-4');
                     
                     reachVideo.Quality = 50;
                     reachVideo.FrameRate = frameRate;
                     reachFrame = im2frame(imageResized);
                     open(reachVideo);
                     writeVideo(reachVideo, reachFrame);
                     
                     % If the light is off
                 elseif whitePix < thresh
                     
                     % If the light was previously on
                     if lightOn == 1
                         reaches(reachNum,3) = i*(1/frameRate); % Save "time off" of LED
                         lightOn = 0; % Declare that the light is NOT on
                         close(reachVideo); % Close the previous reaching video file
                     end
                     
                     i = i + 1;
                     
                 else
                     reachFrame = im2frame(imageResized);
                     writeVideo(reachVideo, reachFrame);
                     i = i + 1;
                 end
                 
                 
                 % write image
                 resized_frame = im2frame(imageResized);
                 writeVideo(outVideo, resized_frame);
                 
             end
             
             close(reachVideo);
             close(outVideo);
             
             % Add line to save reach timestamps
             fid= [searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/Reaches_' videoNum '/' filename '_reaches.csv'];
             csvwrite(fid,reaches)
             
             disp([searchDir mainDirSubfolders{subfolderInd,1} '/' folderDirSubfolders{subsubfolderInd,1} '/' filenameExt, ' end']);
             
        end
    end
   
end
toc;