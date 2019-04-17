function [base,reaches] = LEDDetection2(file,outDir,base)

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
reaches = zeros(100,2);

% Import video
obj = VideoReader(file);

frameRate = obj.FrameRate; % Get frame rate
videoDuration = obj.Duration; % Get video duration
totFrames = frameRate*videoDuration; % Calculate the total number of frames

time = 0;
reachNum = 0;
lightOn = 0;
trialTime = 3;
intTrialInt = 1;

% thresh = 5000;
tic;
while time < videoDuration
    
    obj.CurrentTime = time;
    
    if obj.CurrentTime >= videoDuration-8
        time = videoDuration;
        break
    end
        vidFrame = readFrame(obj);

    % At the beginning of the video, define where the LED is
        xmin = 1;
        ymin = 560;
        width = 260;
        height = 500;

    % Detect if LED is on or off
    
    bwVidFrame = rgb2gray(vidFrame);
    binaryFrame = bwVidFrame >= 200;

    whitePix = sum(sum(binaryFrame(ymin:ymin+height,xmin:xmin+width)));
%     disp(whitePix);
%     disp(time);
%     time = time+20/frameRate;
    
   
    % If the light was previous off but is now on
    if whitePix >= 24000 && lightOn == 0
            
            lightOn = 1; % Declare that the light is on
            reachNum = reachNum + 1; % Define the reach number
            reaches(reachNum,1) = reachNum; % Save reach number
            reaches(reachNum,2) = time; % Save "time on" of LED
            if time == 0
                time = time + (20/frameRate);
            else
                time = time + 20;
            end
    
    % If the light is off
    elseif whitePix < 24000
        
        if lightOn == 1 && time
             time = time + 8; % Skip forward 1 frame
             lightOn = 0;
        else
             time = time + 1;
        end

    else
%         disp(time);
        time = time + (20/frameRate);
    end
        
end
toc;

movefile(file, outDir)

reaches(:,2) = floor(reaches(:,2));

csvname = filename(1:end-4);
csvwrite([outDir csvname '.csv'],reaches);

end
