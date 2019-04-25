%% script_detectLED

% This script walks through the necessary steps for locating files that
% need to have the LED detected. 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% USER DEFINED VARIABLES
animalDir = '/Volumes/HD_Krista/Experiments/skilledReaching/SR_DlxCKO_BehOnly/Animals/';

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Identify animal folders
allFolders=getNames_contain(animalDir,1,'et');

% start processing one animal at a time
for ii = 1:length(allFolders)
    
    % Define directory that training videos should exist in
    trainingDir=[animalDir allFolders{ii} '/Training/'];
    
    if ~exist(trainingDir,'dir')
        % If training video directory doesn't exist, move to next animal
        continue
    end
    
    trainFolders=getNames_contain(trainingDir,1,'et');
        
    % start processing one training day at a time
    for jj = 1:length(trainFolders)
        mp4Files=getNames_contain([trainingDir trainFolders{jj}],0,'.MP4');
        csvFiles=getNames_contain([trainingDir trainFolders{jj}],0,'.csv');
        
        % If there are no csv files:
        if isempty(csvFiles)
            
            for nn = 1:length(mp4Files)
                
                % Sort out videos that have '._', LEDDetect the rest
                if contains(mp4Files(nn), '._')
                    continue;
                else
                    disp(['Working on: ' mp4Files{nn}]);
                    fileName=[trainingDir trainFolders{jj} '/' mp4Files{nn}];
                    reaches=LEDDetect(fileName);
                    disp('pause here');
                end
                
            end
            
        % If there are csv files:
        else
            
            for nn=1:length(mp4Files)
                
                split=strsplit(mp4Files{nn},'.');
                
                % Sort out videos that have already been analyzed
                if any(contains(csvFiles,split{1}))
                    continue;
                else
                    
                    % Sort out videos that have '._', LEDDetect the rest
                    if contains(mp4Files(nn),'._')
                        disp('this file has a ._ in it');
                        continue;
                    else
                        disp(['Working on: ' mp4Files{nn}]);
                        fileName=[trainingDir trainFolders{jj} '/' mp4Files{nn}];
                        reaches=LEDDetect(fileName);
                        disp('pause here');
                    end
                    
                end
                
            end

        end
         
    end % end processing one training day at a time
    
end % end processing one folder at a time