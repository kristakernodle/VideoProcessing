%% script_detectLED

% This script walks through the necessary steps for locating files that
% need to have the LED detected. 

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% USER DEFINED VARIABLES
animalDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/Animals/';

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
        
        if isempty(csvFiles)
            for nn = 1:length(mp4Files)
                if contains(mp4Files(nn), '._')
                    continue;
                else
                    LEDDetect([trainingDir trainFolders{jj} '/' mp4Files{nn}]);
                end
            end
        else
            for kk = 1:length(csvFiles)

                if contains(csvFiles(kk),'._')
                    continue;
                end

                csvNameParts=strsplit(csvFiles{kk},'.csv');

                for nn = 1:length(mp4Files)
                    if contains(mp4Files(nn),csvNameParts{1})
                        continue;
                    else
                        if contains(mp4Files(nn),'._')
                            disp('this file has a ._ in it');
                            continue;
                        else
                            LEDDetect([trainingDir trainFolders{jj} '/' mp4Files{nn}]);
                        end
                    end
                end
            end
        end
         
    end % end processing one training day at a time
    
end % end processing one folder at a time