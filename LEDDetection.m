function LEDDetection(file,outDir)

%% LED Detection Script
% The purpose of this script is to detect when an LED is turned on in a
% video frame, save the timestamp associated with the first frame it is on
% and the last frame it is on, and then cut the original video into the
% parts only when the LED is on.

% Define Directory
% directory = '/Users/kristakernodle/Documents/GitHub/VideoProcessingMatlab';
% filename = '760_20180918_T4_01.mp4';

[directory,filename,ext] = fileparts(file);

filename = [filename ext];

% Define Output Variables
reaches = zeros(100,3);

% Import video
obj = VideoReader(file);

frameRate = obj.FrameRate; % Get frame rate
videoDuration = obj.Duration; % Get video duration
totFrames = frameRate*videoDuration; % Calculate the total number of frames

time = 0;
reachNum = 0;
lightOn = 0;
trialTime = 10;
intTrialInt = 2;

% thresh = 5000;
tic;
while time <= videoDuration
    
    obj.CurrentTime = time;
    
    vidFrame = readFrame(obj);

    % At the beginning of the video, define where the LED is
    if time == 0

        xmin = 1;
        ymin = 560;
        width = 260;
        height = 500;

    end

    % Detect if LED is on or off
    blueFrame = vidFrame(:,:,3);

    bluePix = sum(sum(blueFrame(ymin:ymin+height,xmin:xmin+width)));
    
    if time < 1 && strcmp(filename(end-5:end-4),'01')
        base = bluePix;
    end
    
    % If the light was previous off but is now on
    if bluePix >= base+1000 && lightOn == 0
            
            lightOn = 1; % Declare that the light is on
            reachNum = reachNum + 1; % Define the reach number
            reaches(reachNum,1) = reachNum; % Save reach number
            reaches(reachNum,2) = obj.CurrentTime; % Save "time on" of LED
            time = time + trialTime - (2/frameRate);
    
    % If the light is off
    elseif bluePix < base+1000
        
        % If the light was previously on
        if lightOn == 1
             reaches(reachNum,3) = time + 5; % Save "time off" of LED
             time = time + (800/frameRate); % Skip forward ~15 seconds
        end
        
        lightOn = 0; % Declare that the light is NOT on
        time = time + (50/frameRate);
    else
        time = time + (100/frameRate);
    end
        
end
toc;

movefile(file, outDir)

if reaches(reachNum,3) == 0
    reaches(reachNum,3) = videoDuration;
end

reaches(:,2) = floor(reaches(:,2));
reaches(:,3) = ceil(reaches(:,3)) + 5;

csvname = filename(1:end-4);
csvwrite([outDir csvname '.csv'],reaches);

end
