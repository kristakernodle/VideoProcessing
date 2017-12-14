%% LED Detection Script
% The purpose of this script is to detect when an LED is turned on in a
% video frame, save the timestamp associated with the first frame it is on
% and the last frame it is on, and then cut the original video into the
% parts only when the LED is on.

% Define Directory
% directory = '/Users/kristakernodle/Documents/GitHub/VideoProcessingMatlab';
filename = 'LEDDetectTestTime.MP4';

% Define Output Variables
reaches = zeros(100,3);

% Import video
obj = VideoReader(filename);

frameRate = obj.FrameRate; % Get frame rate
videoDuration = obj.Duration; % Get video duration
totFrames = frameRate*videoDuration; % Calculate the total number of frames

time = 0;
reachNum = 0;
lightOn = 0;
trialTime = 4;
intTrialInt = 2;

thresh = 1000;
tic;
while time <= videoDuration
    
    obj.CurrentTime = time;
    
    vidFrame = readFrame(obj);

    % At the beginning of the video, define where the LED is
    if time == 0
        
        fig = figure;
        imshow(vidFrame);
        h = imrect;
        position = wait(h);
        
        close(fig)
        
        position = floor(position);
        xmin = position(1);
        ymin = position(2);
        width = position(3);
        height = position(4);

    end

    % Detect if LED is on or off
    bwVidFrame = rgb2gray(vidFrame);
    binaryFrame = bwVidFrame >= 200;

    whitePix = sum(sum(binaryFrame(ymin:ymin+height,xmin:xmin+width)));
    
    % If the light was previous off but is now on
    if whitePix >= thresh && lightOn == 0
            
            lightOn = 1; % Declare that the light is on
            reachNum = reachNum + 1; % Define the reach number
            reaches(reachNum,1) = reachNum; % Save reach number
            reaches(reachNum,2) = obj.CurrentTime; % Save "time on" of LED
            time = time + trialTime - (2/frameRate);
    
    % If the light is off
    elseif whitePix < thresh
        
        % If the light was previously on
        if lightOn == 1
             reaches(reachNum,3) = obj.CurrentTime; % Save "time off" of LED
        end
        
        lightOn = 0; % Declare that the light is NOT on
        time = time + (5/frameRate);
    else
        time = time + (1/frameRate);
    end
        
end
toc;
for row = 1:100
    if reaches(row,1) ~= 0
        rnum = num2str(reaches(row,1));
        startTime = reaches(row,2);
        endTime = reaches(row,3);
        vidObj = VideoWriter(['TimeTest_' rnum '.mp4'],'MPEG-4'); % 'Motion JPEG AVI'
        vidObj.Quality = 85;
        % vidObj.FrameRate = frameRate;
        open(vidObj);
        disp('Write new video');
        for times = startTime:1/frameRate:endTime
            obj.CurrentTime = times;
            saveMe = readFrame(obj);
            writeVideo(vidObj,saveMe);
        end
        close(vidObj);
    end
end
toc;