%% Random Filename Generator
% The purpose of this file is to create random and unique filenames that
% contain lowercase letters and numbers. 
% 
% Inputs: 
%       saveDir - The directory where the finale '.csv' file will be saved
%       n - Total number of random 10 digit filenames to generate
%
% Outputs:
%       filenames.csv - a .csv file containing 1 column with all file names



saveDir = '/Users/Krista/Desktop/'; % Where the '.csv' output will be saved
n = 100000; % Number of filenames to generate

filenames = repmat({''},n,1); % Cell array to hold filenames

% Array containing all possible elements in the filenames
el = {'a','b','c','d','e','f','g','h','i','j','k','l','m',...
            'n','o','p','q','r','s','t','u','v','w','x','y','z',...
            '0','1','2','3','4','5','6','7','8','9'};
        
for num = 1:n
    
    unique = 0;
    
    % While the filename is not unique, run this loop
    while unique == 0
        
        % Generate 10 random integers in [1,36]
        randElNum = randi(36,10,1);
        
        % Create a random name based on random numbers (used as indicies
        % for el array)
        randName = [el{randElNum(1)} el{randElNum(2)} el{randElNum(3)} el{randElNum(4)}...
                    el{randElNum(5)} el{randElNum(6)} el{randElNum(7)}...
                    el{randElNum(8)} el{randElNum(9)} el{randElNum(10)}];
        

        if ~any(strcmp(filenames,randName))
            
            % If the newly generated randName is not the same as any strings
            % already in filenames cell array save the name
            filenames{num} = randName;
            
            % Identify name as unique
            unique = 1;
            
        end
        
    end
    
    
end

% Write the output file
fid = fopen([saveDir 'filenames.csv'],'w');
fprintf(fid, '%s\n', filenames{:,1});
fclose(fid);
        