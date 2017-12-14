%% Rename Video Files
% This purpose of this code is to search through the provided directory for
% all folders, then search those folders for video files that need to be
% copied to a new location and renamed. 

directory = '/Volumes/HD_Krista/MouseReaching/AutoReaching_TestGroup/ReachingVideos_Date/20171207/063_PT1_01/Reaches_02/';

reachVideos = dir([directory '*.mp4']);

for id = 1:length(reachVideos)
    
    if reachVideos(id).isdir == 0 && reachVideos(id).bytes ~= 4096
    
        oldname = [directory reachVideos(id).name];
        
        ID = num2str(id);
        newname = [directory 'NewVideo' ID '.mp4'];
    
        copyfile(oldname, newname);
    
    end

end

