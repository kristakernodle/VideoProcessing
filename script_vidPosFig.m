v=VideoReader('/Users/Krista/Desktop/710_20181126_01_R24.MP4');
[bodyparts,parts_loc,p]=read_DLC_csv('/Users/Krista/Desktop/710_20181126_01_R24DeepCut_resnet50_rightPP_CenterFeb9shuffle1_1030000.csv');

dlcCropParams=[732 1316 44 1062];

% 1:1019
% 1:1080
% 44:1062

startTime = 7; % seconds
endTime = 9.75; % seconds

parts_loc(1,:,2)=abs(parts_loc(1,:,2)-v.Height);
parts_loc(2,:,2)=abs(parts_loc(1,:,2)-v.Height);

lowPLeftPaw=find(p(1,:)<0.75);
lowPRightPaw=find(p(2,:)<0.75);
parts_loc(1,lowPLeftPaw,2)=NaN;
parts_loc(1,lowPLeftPaw,1)=NaN;
parts_loc(2,lowPRightPaw,1)=NaN;
parts_loc(2,lowPRightPaw,2)=NaN;

startFrameNum=floor(startTime*v.FrameRate);
endFrameNum=ceil(endTime*v.FrameRate);

% yminLeftPaw=min(parts_loc(1,startFrameNum:endFrameNum,2));
% yminRightPaw=min(parts_loc(2,startFrameNum:endFrameNum,2));
% ymin=min(yminLeftPaw,yminRightPaw);
% 
% ymaxLeftPaw=max(parts_loc(1,:,2));
% ymaxRightPaw=max(parts_loc(2,:,2));
% ymax=max(ymaxLeftPaw,ymaxRightPaw);

v.CurrentTime=startTime;

time=NaN(length(parts_loc));
% startTime=v.CurrentTime;
% v.CurrentTime=0;
xTime=[];
frameCnt=1;
while hasFrame(v)
    % Get information for plot
    frame = readFrame(v);
    time=v.CurrentTime;
    
    if time >= startTime && time <= endTime
        
        yLeftPaw=parts_loc(1,frameCnt,2);
        yRightPaw=parts_loc(2,frameCnt,2);
        xTime(frameCnt)=time;
        
        % Make figure
        f=figure('Visible','off');
        frame = frame(dlcCropParams(3):dlcCropParams(4),dlcCropParams(1):dlcCropParams(2),:);
        
        % The figure consists of a column of two subplots
        % The first subplot contains the video frame
        subplot(2,2,[1 3]);
        hold on
        imshow(frame)
        scatter(abs(parts_loc(1,frameCnt,1)-dlcCropParams(1)),parts_loc(1,frameCnt,2)+410,'filled','r');
        scatter(parts_loc(2,frameCnt,1)+19,parts_loc(2,frameCnt,2)+210,'filled','b');

        % The second subplot contains the plot with a line indicating location
        subplot(2,2,2);
        hold on;
        plot(xTime,parts_loc(1,1:frameCnt,1))
        plot(xTime,parts_loc(2,1:frameCnt,1))
        line([time time],[0,ymax])
        axis([startTime endTime 250 350]);
        title('Side to Side');
        
        subplot(2,2,4);
        hold on;
        plot(xTime,parts_loc(1,1:frameCnt,2))
        plot(xTime,parts_loc(2,1:frameCnt,2))
        line([time time],[0,ymax])
        axis([startTime endTime 580 660]);
        title('Up and Down');

        M(frameCnt)=getframe(gcf);
        close all;
    end
    frameCnt=frameCnt+1;
end

figure('Visible','on');
axes('Position',[0 0 1 1])
movie(M,2)
