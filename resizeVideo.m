%% Resize Video
% This script contains the required codes for resizing videos in the .mp4
% format.
%
% Inputs:
%       inFileDir - Where the video that needs to be resized is located
%       outFileDir - Where the newly resized video should be saved
%       filename - What the name(s) of the files to be resized are
%
% Outputs:
%       output - Resized video written to outFileDir with name:
%                filename_s.mp4


inFileDir = '/Volumes/HD_Krista/MouseReaching/Pilot_Spring2017/ReachingVideos_Date/20170628/Train_6989_12/';
outFileDir = '/Volumes/HD_Krista/MouseReaching/Pilot_Spring2017/ReachingVideos_Date/20170628/Train_6989_12/';

filename = '6989_20170628_01';

input = VideoReader([inFileDir filename '.mp4']);
output = VideoWriter([outFileDir filename '_s.mp4'], 'MPEG-4');

output.Quality = 50;
output.FrameRate = input.FrameRate;
open(output);

for i = 1:input.NumberOfFrames
    image = read(input, i); 
    % resize
    imageData = imresize(image, 0.5);
    
    % write image
    resized_frame = im2frame(imageData);
    writeVideo(output, resized_frame);
end

close(output);
