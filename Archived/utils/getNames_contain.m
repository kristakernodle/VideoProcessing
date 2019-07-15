function [names]=getNames_contain(directory,dirFlag,str)
% getNames_contain function gets all folders (dirFlag=1), files
% (dirFlag=0), or both (isempty(dirFlag)) in the directory with str in the name. 

%% Check Valid Use of Function
% Make sure input directory exists
if ~exist(directory,'dir')
    error('Error: The directory (%s) does not exist.')
end

% Get all files from input directory
allFiles=dir(directory);

strExists=false;
% Make sure at least one file/folder with desired string exists
for ii = 1:length(allFiles)
    if contains(allFiles(ii).name,str)
        strExists=true;
        break;
    end
end
if strExists==false
%     warning('Warning: No files or folders in this directory contain string (%s) \n Directory: %s',str,directory)
    names=[];
end

%% Run Functions
foldNum=1;
% Start structure for dirFlag
if isempty(dirFlag)

    % All files AND folders with str in the name
    for ii = 1:length(allFiles)
       if contains(allFiles(ii).name,str)
           names{foldNum}=allFiles(ii).name;
           foldNum=foldNum+1;
       end
    end

elseif dirFlag ~= 1 && dirFlag ~=0

    % Error, improper input value
    error('Error: dirFlag should be 1 (folders), 0 (files) or [] (all).')
else
    % If dirFlag is either 1 or 0
    for ii = 1:length(allFiles)
       if allFiles(ii).isdir == dirFlag && contains(allFiles(ii).name,str)
           names{foldNum}=allFiles(ii).name;
           foldNum=foldNum+1;
       end
    end

end % End structure for dirFlag

end