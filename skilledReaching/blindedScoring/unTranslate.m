% unTranslate.m
% Used to convert videos scored by blinded reviewers back into useful data

load('/home/kkrista/Desktop/translate.mat');

acDir = '/home/kkrista/Desktop/Scored_AC/';
abDir = '/home/kkrista/Desktop/Scored_AB/';

acFiles = dir(acDir);
abFiles = dir(abDir);

for ii=1:length(acFiles)
    
    if acFiles(ii).isdir
        continue;
    end
    
    currFile = acFiles(ii).name;
    currFileSplit = split(currFile,{'_'});
    newName = currFileSplit(end-1);
    newName = newName{1};
    
    idx = find(strcmp(newName,allNewName));
    
    if ~isempty(idx)
        oldName = allOrigName(idx);
    
        oldName = split(oldName,'.MP4');
        oldName = char(oldName(1));
    
        copyfile(['/home/kkrista/Desktop/Scored_AC/' currFile],['/home/kkrista/Desktop/unTranslated/' oldName '_AC.csv'])
    else
        continue;
    end
        
end

for ii=1:length(abFiles)
    
    if abFiles(ii).isdir
        continue;
    end
    
    currFile = abFiles(ii).name;
    currFileSplit = split(currFile,{'_'});
    newName = currFileSplit(end-1);
    newName = newName{1};
    
    idx = find(strcmp(newName,allNewName));
    
    if ~isempty(idx)
        oldName = allOrigName(idx);
    
        oldName = split(oldName,'.MP4');
        oldName = char(oldName(1));
    
        copyfile(['/home/kkrista/Desktop/Scored_AB/' currFile],['/home/kkrista/Desktop/unTranslated/' oldName '_AB.csv'])
    else
        continue;
    end
        
end