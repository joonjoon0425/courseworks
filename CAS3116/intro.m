A = [1 2; 3 4];
B = [1, 2; 3, 4];

N = 5;
v = [1 0 0];
t = v';

% start:stepsize:end
% both start and end are inclusive
v2 = 1:.5:3.5;
% I guess the stepsize is 1 in default
v3 = -4:4;

% create a empty row * col matrix
% n * n if only one is given
m1 = zeros(2, 3);
square = zeros(3);

% very similar to PyTorch
m2 = ones(2, 3);
m3 = eye(3);
m4 = rand(3, 1);
m5 = randn(3, 4);

% matlab's index starts from 1
v4 = [1 2 3 1];
func(v4);


function y = func(x)
    a = [-2 -1 0 1];
    y = a + x;
end