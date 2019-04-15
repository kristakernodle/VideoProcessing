tic;
%% VideosWorkFlowTesting_V1.m

% Version 1, 20180920
% Author: Krista Kernodle (kkrista@umich.edu)

% The purpose of this file is to provide a workflow for behavioral videos
% collected by the Dauer & Leventhal labs mouse single-pellet skilled
% reaching set up (automated, arduino based, two mirror views, slow motion
% videos - 100 fps - captured).

% This workflow will take videos ready for processing, resize them (saved), cut
% them into trials (saved), and create deidentified trials (saved). Videos
% will then be ready for DeepLabCut and human analysis. 

%% Step One: Check if there are any video files ready for processing

% Define the folder that videos ready for processing can be found
readyDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ReDoLED/';

% Find files that are ready for processing. Only videos with names and
% filetypes matching the following format will be identified:
% ET#_YYYYMMDD_T#_V#.mp4
readyFiles = dir(strcat(readyDir, '*_*_*_*.MP4'));

% Count the number of files that need to be processed
% value 'a' gives # of files
[a,b] = size(readyFiles);

%% Step Two: Resize videos
% tic;
% % Define the output directory
% outDir = '/Users/kkrista/Desktop/Test_WorkFlowEnd/';
% 
% for vidNum = 1:a
%     
%     outVid = [outDir readyFiles(vidNum).name];
%     
%     input = VideoReader([readyDir readyFiles(vidNum).name]);
%     output = VideoWriter(outVid, 'MPEG-4'); 
%     
%     output.Quality = 50;
%     output.FrameRate = input.FrameRate;
%     open(output);
%     
%     while hasFrame(input)
%        
%         vidFrame = readFrame(input);
%        
%        imageData = imresize(vidFrame, 0.5);
%     
%         % write image
%         resized_frame = im2frame(imageData);
%         writeVideo(output, resized_frame);
%         
%     end
%     
%     close(output);
%     
% end
% toc

%% Step Three: Cut resized video into trials

% Define the output directory
outDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/ToBeCut/';
base = 0;

for vidNum = 1:a

    if contains(readyFiles(vidNum).name, {'._'})
        continue;
    else
        [base,reaches] = LEDDetection2([readyDir readyFiles(vidNum).name],outDir,base);
    end
end

%% Step Four: Duplicate trial videos as de-identified, ready to be scored, videos

% Save to HD_Krista
toc;