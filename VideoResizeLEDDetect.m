%% Video Editing: Resizing and LED Detection

inputDir = '/Volumes/HD_Krista/MouseReaching/SkilledReaching_Winter2018/ReachingVideos/';
outputDir = '/Volumes/HD_Krista/MouseReaching/AutoReaching_TestGroup/TestVideosOutput/';

videoNames = {};

files = dir(fullfile(inputDir));
for j = 1:length(files)
    if files(j).isdir == 0 && files(j).bytes ~= 4096
        videoNames{end+1} = files(j).name;
    end
end

for vidInd = 1:length(videoNames)
    
    inVideoFile = videoNames{vidInd};
    inVideoName = inVideoFile(1:end-4);
    outVideoName = [inVideoName '_s'];
    filetype = inVideoFile(end-4:end);

    inVideo = VideoReader([inputDir inVideoName filetype]);
    outVideo = VideoWriter([outputDir outVideoName filetype], 'MPEG-4');
    
    disp([inVideoFile, ' start']);

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
                reachVideo = VideoWriter([outputDir outVideoName '_0' reachNumChar '.mp4'],'MPEG-4');
                
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
        
        disp([inVideoFile, ' end']);

    end

close(reachVideo);
close(outVideo);

end
