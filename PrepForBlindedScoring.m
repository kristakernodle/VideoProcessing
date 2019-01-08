%% Prep for Blinded Scoring
% Version 1, 20190107
% Author: Krista Kernodle (kkrista@umich.edu)
%
% Purpose: This code translates filenames into a new, randomly generated 10
%   digit filename. Uniqueness is checked both for the original file name
%   (so a file will not be translated twice) and for the randomly generated
%   filename (to eliminate difficulties in unblinding for analysis). 
%
% Inputs: 
%
%   transDir - Directory of the .mat file containing translated names and
%       original names
%   inDir - Directory of all files that need renaming
%   inDirWant - Common aspect of all folder names in the inDir
%   subDir - Commonly named folder for all folders in the inDir
%   subDitWant - Common aspect of all folder names in the subDir
%   finFoldWant - Common aspect of all folder names that contain files to
%       be renamed
%   filenameStruct - Commonly formatted names of all files to be renamed
%
%   NOTE: This code assumes that a .mat file already exists.  
%
% Outputs:

%% Inputs
transDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/VideoPipeline/';
transName = 'translate.mat';
inDir = '/Volumes/HD_Krista/Experiments/SkilledReachingExperiments/SR_DlxCKO_BehOnly/Animals/';
inDirWant = 'Score';
subDir = '/Training/';
subDirWant = 'CC';
finFoldWant = 'Reach';
filenameStruct = '/*_*_*_*.MP4';

%% Initiate Variables
wantFolders = [];
allNewNames = [];
uniqOrigNames = [];

%% Import .mat
transFile = load([transDir,transName]);
long = transFile.OriginalNames;
short = transFile.NewNames;

%% First Level of Folders
% wantFolders

files = dir(inDir);
dirFlags1 = [files.isdir];
subFolders = files(dirFlags1);

% Get only the folders of the inDir that containe inDirWant
for ii = 1:length(subFolders)
    
    currFold = subFolders(ii).name;
    
    if contains(currFold,inDirWant)
        wantFolders = [wantFolders; string(currFold)];
    end
    
end

%% Second Level of Folders
% wantTrainFolders

for jj = 1:length(wantFolders)
   
    animal = char(wantFolders(jj));
    trainDir = strcat(inDir, animal, subDir);
    trainFiles = dir(trainDir);
    dirFlags2 = [trainFiles.isdir];
    subTrainFolders = trainFiles(dirFlags2);
    
    wantTrainFolders = [];
    
    for jk = 1:length(subTrainFolders)
        
       currTrainFold = subTrainFolders(jk).name;
        
       if contains(currTrainFold,subDirWant)
           wantTrainFolders = [wantTrainFolders; string(currTrainFold)];
       end
        
    end
    
    %% Third Level of Folders
    % wantReachFolders
    
    for jl = 1:length(wantTrainFolders)
        
        trainDay = char(wantTrainFolders(jl));
        reachDir = strcat(trainDir,trainDay);
        reachFiles = dir(reachDir);
        dirFlags3 = [reachFiles.isdir];
        subReachFolders = reachFiles(dirFlags3);
        
        wantReachFolders = [];
        
        for jlm = 1:length(subReachFolders)
            
            currReach = subReachFolders(jlm).name;
            
            if contains(currReach,finFoldWant)
                wantReachFolders = [wantReachFolders; string(currReach)];
            end
        end
        
        %% Get all files in reachDir that can be translated
        % origName
        
        for jln = 1:length(wantReachFolders)
            allFiles = dir(strcat(reachDir,'/',char(wantReachFolders(jln)),filenameStruct));
       
            firstName = allFiles(1).name;
            split = strsplit(firstName,'_');
            
            % Dunno why, but some files will have a ._ in front, this is my
            % solution to get the original name without the ._
            if length(split) == 4
                origName = strcat(split{1},'_',split{2},'_',split{3},'.MP4');
            elseif length(split) == 5
                origName = strcat(split{2},'_',split{3},'_',split{4},'.MP4');
            else
                disp(length(split));
            end
            
            %% Generate New Names
            
            % Check for uniqueness of origName (not previously translated)
            if ~any(strcmp(origName,long))
                
                % For unique origName, generate newName
                newName = randFilenameGen();
                
                % Check uniqueness of newName
                while (any(strcmp(newName,short))) || (strcmp(newName,allNewNames))
                    disp('in loop');
                    newName = randFilenameGen();
                end
                
                %% Begin Translation
                
                % Save all newly generated names in character array allNewNames 
                allNewNames = [allNewNames;newName];
                
                % Save all unique origName in character array uniqOrigNames
                uniqOrigNames = [uniqOrigNames;origName];
                
            else
                % If not unique, continue to next file
                continue
            end % Check Uniqueness (Generate New Names)
  
        end % Get all files in reachDir that can be translated
        
    end % Third level of folders

end % Second level of folders

%% Save All

% Convert character arrays uniqOrigNames & allNewNames to strings
uniqOrigNames = string(uniqOrigNames);
allNewNames = string(allNewNames);

% Concatenate into one variable (transFile)
startRowCt = length(long)+1;
endRowCt = length(long)+length(uniqOrigNames);
OriginalNames(startRowCt:endRowCt,1) = uniqOrigNames;
NewNames(startRowCt:endRowCt,2) = allNewNames;

% Save new transFile as .mat, overwritting old variables

save([transDir,transName],OriginalNames,NewNames);





















