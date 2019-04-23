function LEDDetect(filename)
% LEDDetect detects the presence of a blue LED in a video object. 

% The purpose of this script is to detect when a blue LED is turned on in a
% video frame. Time stamp associated with first frame and last frame of LED
% being on are saved into a .csv file. 
%
% This function uses RGB values. See line 31 to change this to a different
% color space. Note: You will likely have to change the thresh value also.
%
% INPUTS: 
%   filename - full file path for video that will be processed.
% OUTPUTS:
%   No variable outputs. 
%   .csv file is created with same filepath and name as 'filename'
%
% 

% Define the pixel threshold for the blue LED being on/off. Note: This
% value may change depending on frame size, size of LED, etc.
thresh = 5000;

% Define Output Variables
reaches = zeros(100,3);

% Import video
obj = VideoReader(filename);

reachNum = 0;
lightOn = 0;

tic;
while hasFrame(obj)
    
    vidFrame = readFrame(obj);
    time=obj.CurrentTime;

    % Detect if LED is on or off
    bluePix=sum(sum(vidFrame(:,:,3)>250));
    
    % If the light is on, was previously off, & time is past the ID card
    if bluePix >= thresh && lightOn == 0
        
        lightOn = 1; % Declare that the light is on
        reachNum = reachNum + 1; % Define the reach number
        reaches(reachNum,1) = reachNum; % Save reach number
        reaches(reachNum,2) = time;
        
        if time+10 < obj.Duration
            obj.CurrentTime=time+10;
        else 
            obj.CurrentTime=obj.Duration;
        end
        
    % If the light is off
    elseif bluePix < thresh && lightOn ==1
        reaches(reachNum,3) = time; % Save "time off" of LED
        lightOn = 0; % Declare that the light is NOT on
    end
        
end

vidName=strsplit(filename,'.');
csvwrite([vidName{1} '.csv'],reaches);

toc;

end
