function [timeOn timeOff] = LEDDetect(vidName,color_LED,thresh)
%LEDDetect Determine if an LED is on in video frame.

%   [TIMEON TIMEOFF] = LEDDETECT(FILENAME, COLOR_LED, THRESH) returns vectors
%   TIMEON and TIMEOFF for the specified LED color in each frame.
%
% This function uses RGB values. See line 31 to change this to a different
% color space.
%
% INPUTS: 
%   filename - full file path for video that will be processed.
% OUTPUTS:
%   No variable outputs. 
%   .csv file is created with same filepath and name as 'filename'
%

%
% By Krista Kernodle, 2019
% kristakernodle@gmail.com
% https://github.com/kristakernodle
%

%%

% Define Output Variables
timeOn = [];
timeOff = [];

% Import video
obj = VideoReader(vidName);

reachNum = 0;
lightOn = 0;

% Begin processing frames
while hasFrame(obj)
    
    vidFrame = readFrame(obj);
    time=obj.CurrentTime;

    % Detect if LED is on or off
    bluePix=sum(sum(vidFrame(:,:,3)>250));
    
    % If the light is on && was previously off
    if bluePix >= thresh && lightOn == 0
        
        reachNum = reachNum + 1; % Define the reach number
        reaches(reachNum,1) = reachNum; % Save reach number
        reaches(reachNum,2) = time; % Save "time on" of LED
        
        % Make sure that we don't jump beyong video duration (if LED is on
        % at end of video)
        if obj.CurrentTime+10 <= obj.Duration
            obj.CurrentTime=time+10;
        else
            obj.CurrentTime=obj.Duration;
        end
        
        lightOn = 1; % Declare that the light is on
        
    % If the light is off but was previously on
    elseif bluePix < thresh && lightOn ==1
        reaches(reachNum,3) = time; % Save "time off" of LED
        lightOn = 0; % Declare that the light is NOT on
    end
        
end

end
