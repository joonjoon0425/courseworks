% uint8 is given
I = imread('../DOGGO.png');
% change it to [0,1] double
I = im2double(I);

if size(I, 3) == 3, I = rgb2gray(I); end
% box filter
box = ones(3) / 9;
% gaussian filter
gaussian = [1 2 1; 2 4 2; 1 2 1] / 16;
% shifting to left one pixel
shift = [0 0 0; 0 0 1; 0 0 0;];
% sharpening
sharp = [0 0 0; 0 2 0; 0 0 0;] - box;
% gradients
grad = [1 0 -1; 2 0 -2; 1 0 -1;];

h = gaussian;
J = imfilter(I, h, "same");

figure;
subplot(1, 2, 1); imshow(I); title('original');
subplot(1, 2, 2); imshow(J); title('filtered');